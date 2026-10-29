"""全书审计发布与独立验收共用的只读结构检查，不执行旧审计生成器。"""
from __future__ import annotations
import collections
import hashlib
import json
import re
from pathlib import Path, PurePosixPath

BASE = Path(__file__).resolve().parent
DEFAULT_ROOT = BASE.parents[2]
MAIN = {
    'characters': ('character-arc-audit-draft.json', 'characters', 'audit_id'),
    'findings': ('end-state-audit-draft.json', 'findings', 'key'),
    'historical': ('historical-question-pool.json', 'candidates', 'candidate_id'),
    'local': ('local-question-pool.json', 'candidates', 'candidate_id'),
}
STATUS = {'answered', 'partial', 'unrecovered', 'unknown'}
EVIDENCE = {'source_id', 'revision', 'chapter_id', 'start_line', 'end_line'}
BEGIN = '<!-- whole-book-audit:start -->'
END = '<!-- whole-book-audit:end -->'


class AuditError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise AuditError(message)


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def encode_json(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')


def contained(root, relative):
    """清单路径只允许相对路径，并核实解析后仍在指定根内。"""
    root = Path(root).resolve()
    raw = str(relative).replace('\\', '/')
    rel = PurePosixPath(raw)
    require(raw and not rel.is_absolute() and ':' not in raw and '..' not in rel.parts,
            f'非法清单相对路径: {relative}')
    target = (root / Path(*rel.parts)).resolve()
    require(target.is_relative_to(root), f'路径越界: {relative}')
    return target


def verify_map(root, entries):
    require(isinstance(entries, dict) and entries, 'SHA清单为空')
    for name, digest in entries.items():
        require(bool(re.fullmatch('[0-9a-f]{64}', digest)), f'SHA格式错误: {name}')
        path = contained(root, name)
        require(path.is_file(), f'缺少冻结文件: {path}')
        require(sha(path) == digest, f'SHA不符: {path}')
    return len(entries)


def review_check(path, manifest_sha, source_id, required=False):
    if not Path(path).exists():
        require(not required, f'发布须有真实主审凭据: {path}')
        return None
    data = read(path)
    require(data.get('status') == 'reviewed_for_library_import', '主审凭据status不符')
    require(data.get('reviewer') == 'primary', '主审凭据reviewer必须为primary')
    require(data.get('freeze_manifest_sha256') == manifest_sha, '主审签收的冻结清单已变化')
    if 'source_id' in data:
        require(data['source_id'] == source_id, '主审凭据source_id不符')
    return data


def load_package(audit, source):
    data = {kind: read(Path(audit) / filename) for kind, (filename, _, _) in MAIN.items()}
    counts = {}
    for kind, (_, field, id_key) in MAIN.items():
        rows = data[kind][field]
        require(isinstance(rows, list), f'{kind}不是数组')
        ids = [row[id_key] for row in rows]
        require(len(ids) == len(set(ids)), f'{kind}标识重复')
        counts[kind] = len(rows)
    chapters = {c['chapter_id']: c for c in source['chapters']}
    refs = 0

    def evidence_check(value):
        nonlocal refs
        if isinstance(value, dict):
            if EVIDENCE.issubset(value):
                require(value['source_id'] == source['source_id'] and value['revision'] == source['revision'],
                        f'证据来源或修订不符: {value}')
                require(value['chapter_id'] in chapters, f'证据章节不存在: {value}')
                chapter = chapters[value['chapter_id']]
                require(isinstance(value['start_line'], int) and isinstance(value['end_line'], int), '证据行号非整数')
                require(chapter['start_line'] <= value['start_line'] <= value['end_line'] <= chapter['end_line'],
                        f'证据行范围越界: {value}')
                require(value.get('claim_kind') in {'fact', 'inference', 'synthesis', 'plan'}, '证据claim_kind缺失或无效')
                refs += 1
            for child in value.values():
                evidence_check(child)
        elif isinstance(value, list):
            for child in value:
                evidence_check(child)

    for value in data.values():
        evidence_check(value)
    for kind in ['historical', 'local']:
        for row in data[kind]['candidates']:
            decision = row['terminal_assessment']
            require(decision.get('status') in STATUS, f'终点状态无效: {row["candidate_id"]}')
            require(decision.get('rationale') and isinstance(decision.get('later_evidence'), list), '判定理由或证据数组缺失')
            require(not decision.get('depends_on_volumes'), '仍有待输入卷')
            require(decision.get('review_progress') not in {
                'pending-manual-adjudication', 'original-issue-read-awaiting-formal-cross-volume-evidence'}, '仍有未完成判定')
    history = data['historical']
    require(counts['historical'] == sum(x.get('open_questions', 0) + x.get('graph_threads', 0)
                                      for x in history['inputs']), '历史池数量与逐卷输入不符')
    local_keys = {(x['volume'], x['original_field'], x['original_index']) for x in data['local']['candidates']}
    for group in history.get('local_issue_records', []):
        empty = set(group.get('empty_record_indices', []))
        require(all(isinstance(i, int) and 0 <= i < len(group['original_records']) for i in empty), '空索引位置无效')
        for index, original in enumerate(group['original_records']):
            if index in empty:
                require(group['field'] in {'chapter_unresolved_index', 'chapter_source_anomaly_index'}
                        and isinstance(original, dict)
                        and original.get('unresolved', original.get('original_unresolved', original.get('source_anomalies'))) == [],
                        '非空原始问题不能跳过候选表示')
                continue
            require((group['volume'], group['field'], index) in local_keys, '存在未表示的原始本地问题')
    validation = read(Path(audit) / 'audit-validation.json')
    for kind, key in [('characters', 'character_arcs'), ('findings', 'focused_findings'),
                      ('historical', 'historical_candidates'), ('local', 'local_candidates')]:
        require(counts[kind] == validation[key], f'{kind}数量与冻结验证不符')
    require(refs == validation['evidence_references_checked'], '证据计数与冻结验证不符')
    require(not validation.get('pending_inputs') and not validation.get('unadjudicated_candidates'), '审计输入或判定未齐')
    return data, counts, refs


def snapshot_files(root, book, source_id, formal_inputs):
    """记录必须保持不变的分卷、图、人物卡和人工评价文件。"""
    vault = Path(root) / 'writing-vault'
    paths = {contained(root, name) for name in formal_inputs}
    bookroot = vault / 'library' / 'reports' / book
    paths.update(p for p in bookroot.glob('vol*') if p.is_file())
    graph = vault / 'library' / 'sources' / source_id / 'plot-graph.json'
    require(graph.is_file(), f'缺少正式全书图: {graph}')
    paths.add(graph)
    for directory in ['characters', 'scenes', 'patterns', 'assets']:
        base = vault / 'library' / directory
        if base.exists():
            for p in base.rglob('*.json'):
                value = read(p)
                if source_id in json.dumps(value, ensure_ascii=False):
                    paths.add(p)
    return {p.relative_to(Path(root)).as_posix(): sha(p) for p in sorted(paths)}


def preflight(root, book, staging, audit_subdir, source_index, require_review=False):
    root, staging = Path(root).resolve(), Path(staging).resolve()
    audit = contained(staging, audit_subdir)
    manifest_path = audit / 'audit-freeze-manifest.json'
    manifest = read(manifest_path)
    source = read(source_index)
    require(manifest['source_id'] == source['source_id'], '冻结清单与来源索引不符')
    checked = verify_map(audit, manifest['audit_sha256'])
    checked += verify_map(root, manifest['formal_input_sha256'])
    checked += verify_map(audit, manifest['frozen_volume08_hashes'])
    data, counts, refs = load_package(audit, source)
    for entry in data['historical']['inputs']:
        require(entry.get('status') == 'formal-library', '历史池仍依赖非正式分卷')
        for kind in ['analysis', 'graph']:
            require(sha(contained(root, entry[kind])) == entry[kind + '_sha256'], '历史池上游输入已变化')
    digest = sha(manifest_path)
    review_path = staging / 'primary-whole-book-review.json'
    review = review_check(review_path, digest, source['source_id'], require_review)
    report = Path(root) / 'writing-vault' / 'library' / 'reports' / book
    require(report.is_dir(), f'正式分卷目录不存在: {report}')
    require((report / 'README.md').is_file(), '缺少本书README')
    graph_path = Path(root) / 'writing-vault/library/sources' / source['source_id'] / 'plot-graph.json'
    graph = read(graph_path)
    threads = {x['id']: x for x in graph['threads']}
    for row in data['historical']['candidates']:
        if row['entry_type'] == 'graph.threads':
            tid = f'v{row["volume"]}-' + row['original_record']['id']
            require(tid in threads, f'正式图缺少线程: {tid}')
            require(threads[tid]['status'] == row['original_stage_status'], f'阶段线程状态已被改写: {tid}')
    return dict(root=root, book=book, staging=staging, audit=audit, source=source,
                manifest=manifest, manifest_path=manifest_path, manifest_sha=digest,
                review=review, review_path=review_path, data=data, counts=counts, refs=refs,
                checked_hashes=checked, report=report, graph_path=graph_path, graph=graph)


def pool_stats(rows):
    return {
        'count': len(rows),
        'terminal_statuses': dict(sorted(collections.Counter(x['terminal_assessment']['status'] for x in rows).items())),
        'entry_types': dict(sorted(collections.Counter(x.get('entry_type', 'local-atomic-item') for x in rows).items())),
        'audit_domains': dict(sorted(collections.Counter(x['terminal_assessment'].get('audit_domain', 'not-classified-in-pool') for x in rows).items())),
    }


def replace_nav(original, body):
    block = BEGIN + '\n' + body.rstrip() + '\n' + END
    if BEGIN in original or END in original:
        require(original.count(BEGIN) == original.count(END) == 1, '已有导航标记不完整')
        start, end = original.index(BEGIN), original.index(END) + len(END)
        return original[:start] + block + original[end:]
    return original.rstrip() + '\n\n' + block + '\n'


def remove_nav(text):
    if BEGIN in text:
        start, end = text.index(BEGIN), text.index(END) + len(END)
        return (text[:start] + text[end:]).rstrip()
    return text.rstrip()


def check_md_links(path):
    """验导航、身份与叠加视图的文件可达性；不把章节锚点语义当文学证明。"""
    text = Path(path).read_text(encoding='utf-8')
    links = re.findall(r'(?<!!)\[[^\]]*\]\(([^)]+)\)', text)
    checked = 0
    for target in links:
        target = target.strip().strip('<>')
        if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', target) or target.startswith('#'):
            continue
        target = target.split('#', 1)[0]
        require((Path(path).parent / target).resolve().is_file(), f'失效链接: {path} -> {target}')
        checked += 1
    return checked
