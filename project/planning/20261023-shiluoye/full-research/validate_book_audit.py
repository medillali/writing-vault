"""独立验收已发布全书审计，不依赖暂存目录，不执行任何生成器。"""
from __future__ import annotations
import argparse
import hashlib
import sys
from pathlib import Path
from book_audit_common import (
    DEFAULT_ROOT, MAIN, AuditError, check_md_links, contained, encode_json,
    load_package, pool_stats, read, remove_nav, require, review_check, sha, verify_map,
)


def validate(root, book):
    root = Path(root).resolve()
    bookroot = contained(root / 'writing-vault/library/reports', book)
    audit = bookroot / 'audit/whole-book'
    receipt = read(audit / 'publication-receipt.json')
    manifest_path = audit / 'audit-freeze-manifest.json'
    manifest = read(manifest_path)
    source = read(audit / 'provenance/source-index.json')
    require(receipt['book'] == book and receipt['source_id'] == source['source_id'] == manifest['source_id'], '发布来源不一致')
    require(receipt['revision'] == source['revision'], '发布来源修订不一致')
    require(receipt['freeze_manifest_sha256'] == sha(manifest_path), '已发布冻结清单SHA不符')
    review = review_check(audit / 'primary-whole-book-review.json', sha(manifest_path), source['source_id'], True)
    require(sha(audit / 'primary-whole-book-review.json') == receipt['primary_review_sha256'], '主审凭据复制SHA不符')
    require(receipt['review_status'] == 'draft' and receipt['user_approval'] is False, '用户草稿边界被改写')
    require(receipt['primary_review_status'] == review['status'], '发布主审状态不一致')
    # 逐一验全部清单SHA，存档的6份卷末核心不依赖原暂存目录继续存在。
    require(set(receipt['copied_audit_paths']) == set(manifest['audit_sha256']), '冻结审计文件未全部复制')
    checked = 0
    for name, digest in manifest['audit_sha256'].items():
        target = contained(audit, receipt['copied_audit_paths'][name])
        require(target.is_file() and sha(target) == digest, f'发布副本与冻结SHA不符: {name}')
        checked += 1
    checked += verify_map(root, manifest['formal_input_sha256'])
    checked += verify_map(audit / 'provenance/frozen-volume', manifest['frozen_volume08_hashes'])
    copied = verify_map(bookroot, receipt['published_file_sha256'])
    unchanged = verify_map(root, receipt['unchanged_formal_sha256'])
    data, counts, refs = load_package(audit, source)
    require(counts == receipt['counts'] and refs == receipt['evidence_references_checked'], '实际条数/证据数与发布回执不符')
    for kind, (_, field, _) in MAIN.items():
        for row in data[kind][field]:
            if 'review_status' in row:
                require(row['review_status'] == 'draft', '冻结研究的用户审阅状态被改写')
    for name, original_digest in receipt['navigation_original_content_sha256'].items():
        content = contained(bookroot, name).read_bytes().decode('utf-8')
        digest = hashlib.sha256(remove_nav(content).encode('utf-8')).hexdigest()
        require(digest == original_digest, f'原阅读/综合导航内容被改写: {name}')
    index = read(bookroot / 'question-ledger.json')
    require(index['artifact_type'] == 'question-pools-index' and index['not_a_merged_pool'] is True,
            '问题标准入口须是两池索引')
    require('candidates' not in index, '问题索引不得伪装合并schema')
    require(len(index['pools']) == 2 and {x['pool'] for x in index['pools']} == {'historical', 'local'}, '两池入口缺失')
    for entry in index['pools']:
        kind = entry['pool']
        stats = pool_stats(data[kind]['candidates'])
        require(all(entry[k] == v for k, v in stats.items()), f'问题池分类计数错误: {kind}')
        require(contained(bookroot, entry['json_path']) == audit / MAIN[kind][0], '问题池入口指向错误')
        require(contained(bookroot, entry['markdown_path']).is_file(), '问题池可读页不可达')
    identities = read(audit / 'character-identities.json')
    require(identities['auto_merge'] is False and identities['review_status'] == 'draft', '身份边界被改写')
    require([x['audit_id'] for x in identities['subjects']] == [x['audit_id'] for x in data['characters']['characters']], '身份索引未对应全部人物弧')
    for subject, arc in zip(identities['subjects'], data['characters']['characters']):
        require(subject['audited_label'] == arc['name'] and subject['evidence'] == arc.get('evidence', []), '身份索引人物或证据被重配')
    if book == 'zongheng-tianxia':
        first = identities['subjects'][0]
        layers = {x['name']: x['level'] for x in first['names']}
        require(layers.get('丁舒升') == 'real-name' and layers.get('轻狂书生') == 'game-name'
                and layers.get('丁书生') == 'misnomer-or-address', '主人公姓名层级缺失')
        dragon = next(x for x in identities['subjects'] if x['audit_id'] == 'character-arc-29')
        require(dragon['entity_scope'] == 'unresolved-title-and-entity-group'
                and 'character-arc-28' in dragon['identity_rule']['do_not_merge_with'], '龙神实体不合并边界缺失')
        require(any(x['surface_name'] == '邱华' and x['auto_merge'] is False for x in identities['collision_guards']), 'CGL同名不合并边界缺失')
    graph_path = root / 'writing-vault/library/sources' / source['source_id'] / 'plot-graph.json'
    graph = read(graph_path)
    overlay = read(audit / 'terminal-thread-overlay.json')
    require(overlay['graph_sha256'] == sha(graph_path) and overlay['original_graph_unchanged'] is True,
            '全书图已被覆盖或叠加基准失效')
    require(overlay['graph_revision'] == graph.get('revision'), '图版本不符')
    originals = data['historical']['candidates']
    require(len(overlay['entries']) == len(originals), '叠加条数与历史池不符')
    threads = {x['id']: x for x in graph['threads']}
    thread_count = 0
    for entry, original in zip(overlay['entries'], originals):
        require(entry['candidate_id'] == original['candidate_id'], '终点叠加候选ID错位')
        require(entry['original_record'] == original['original_record']
                and entry['terminal_assessment'] == original['terminal_assessment']
                and entry['original_stage_status'] == original['original_stage_status'], '终点叠加改写源判定')
        if original['entry_type'] == 'graph.threads':
            tid = f'v{original["volume"]}-' + original['original_record']['id']
            require(entry['collected_thread_id'] == tid and threads[tid]['status'] == original['original_stage_status'], '阶段线程映射错误')
            thread_count += 1
        else:
            require(entry['collected_thread_id'] is None, '独立历史问题被伪造为图线程')
    require(overlay['thread_count'] == thread_count and overlay['question_count'] == len(originals) - thread_count, '线程与问题计数错误')
    # 检查所有正式新增可读页，以及接入它们的原总览/阅读导航。
    markdown_paths = [contained(bookroot, name) for name in receipt['published_file_sha256']
                      if name.endswith('.md') and '/provenance/' not in name]
    link_count = sum(check_md_links(path) for path in markdown_paths)
    for name, required_links in {
        'README.md': ['character-arcs.md', 'question-ledger.md', 'reading/plot/terminal-audit.md'],
        'reading/README.md': ['plot/terminal-audit.md'],
        'reading/plot/terminal-audit.md': ['../../audit/whole-book/terminal-thread-overlay.md'],
    }.items():
        path = contained(bookroot, name)
        if name == 'reading/README.md' and not path.exists():
            continue
        text = path.read_text(encoding='utf-8')
        require(all(f']({target})' in text for target in required_links), f'缺少审计可达入口: {name}')
    return dict(status='published-audit-validation-passed', book=book,
                freeze_manifest_sha256=sha(manifest_path), counts=counts,
                evidence_references_checked=refs, frozen_sha256_entries_checked=checked,
                published_file_hashes_checked=copied, unchanged_formal_hashes_checked=unchanged,
                reachable_markdown_links_checked=link_count, graph_threads=thread_count,
                independent_historical_questions=len(originals) - thread_count,
                primary_review_status=review['status'], user_review_status='draft',
                original_graph_unchanged=True, original_volume_and_card_files_unchanged=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=DEFAULT_ROOT)
    parser.add_argument('--book', default='zongheng-tianxia')
    parser.add_argument('--output', type=Path, help='可选验收回执路径；默认仅输出不写文件')
    args = parser.parse_args()
    result = validate(args.root, args.book)
    if args.output:
        # 不允许验收输出覆盖原审计、主审凭据、卡片或分卷。
        target = args.output.resolve()
        audit = args.root.resolve() / 'writing-vault/library/reports' / args.book / 'audit/whole-book'
        require(target.name == 'publication-validation.json' and target.parent == audit
                or not target.is_relative_to(args.root.resolve() / 'writing-vault'),
                '--output仅可写独立回执；正式库内仅允许audit/whole-book/publication-validation.json')
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(encode_json(result))
    print(encode_json(result).decode('utf-8'), end='')


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    try:
        main()
    except (AuditError, KeyError, OSError, ValueError, StopIteration) as error:
        print('审计验收失败: ' + str(error), file=sys.stderr)
        sys.exit(1)
