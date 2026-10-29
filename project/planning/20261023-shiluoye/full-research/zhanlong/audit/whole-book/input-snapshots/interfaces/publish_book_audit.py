"""默认只读预检；实际主审完成后用 --reviewed 发布独立全书审计叠加包。"""
from __future__ import annotations
import argparse
import datetime
import os
import shutil
import sys
import uuid
from pathlib import Path
from book_audit_common import (
    BASE, DEFAULT_ROOT, MAIN, AuditError, contained, encode_json, pool_stats,
    preflight, read, remove_nav, replace_nav, require, sha, snapshot_files,
)


def arguments():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, default=DEFAULT_ROOT, help='Novel工作区根目录')
    p.add_argument('--book', default='zongheng-tianxia')
    p.add_argument('--staging', type=Path, help='本书暂存根；内含真实primary-whole-book-review.json')
    p.add_argument('--audit-subdir', default='vol08', help='相对staging的冻结审计目录')
    p.add_argument('--source-index', type=Path, help='来源章节索引，默认staging/source.json')
    p.add_argument('--identity-profile', type=Path, help='人物姓名层级及不合并规则')
    p.add_argument('--reviewed', action='store_true', help='核验真实主审凭据后执行正式复制')
    p.add_argument('--dry-run', action='store_true', help='与--reviewed合用时只读核验发布条件')
    return p.parse_args()


def cell(value):
    return str(value).replace('|', '｜').replace('\r', '').replace('\n', '<br>')


def identities(ctx, profile):
    require(profile.get('book', ctx['book']) == ctx['book'], '身份配置不属于本书')
    require(profile.get('source_id', ctx['source']['source_id']) == ctx['source']['source_id'], '身份配置来源不符')
    rows = []
    overrides = profile.get('subjects', {})
    arcs = ctx['data']['characters']['characters']
    require(set(overrides).issubset({x['audit_id'] for x in arcs}), '身份配置指向不存在的人物弧')
    for arc in arcs:
        rule = dict(overrides.get(arc['audit_id'], {}))
        if 'expected_name' in rule:
            require(rule.pop('expected_name') == arc['name'], '身份配置的人物标签已漂移')
        rows.append(dict(
            audit_id=arc['audit_id'], audited_label=arc['name'],
            display_label=arc.get('display_name', arc['name']),
            entity_scope=rule.pop('entity_scope', arc.get('entity_type', 'audited-subject-no-automatic-alias-merge')),
            names=rule.pop('names', [{'name': arc.get('display_name', arc['name']), 'level': 'audited-label'}]),
            component_entities=arc.get('component_entities'),
            structured_identity_from_audit=arc.get('identity_names'),
            identity_rule=rule, evidence=arc.get('evidence', []),
            evidence_boundaries=arc.get('evidence_boundaries', ''), review_status='draft'))
    return dict(schema_version=1, artifact_type='audited-character-identity-index',
                source_id=ctx['source']['source_id'], review_status='draft',
                primary_review_status='reviewed_for_library_import', auto_merge=False,
                policy=profile.get('policy', '仅索引已审人物条目；姓名相似不构成合并依据。'),
                collision_guards=profile.get('collision_guards', []), subjects=rows)


def generated(ctx, profile):
    """只由已冻结审计派生索引，结论原文留在独立冻结文件。"""
    sid = ctx['source']['source_id']
    counts, data = ctx['counts'], ctx['data']
    identity = identities(ctx, profile)
    hist, local = [data[k]['candidates'] for k in ['historical', 'local']]
    stats = {k: pool_stats(data[k]['candidates']) for k in ['historical', 'local']}
    overlay_rows = []
    for row in hist:
        is_thread = row['entry_type'] == 'graph.threads'
        overlay_rows.append(dict(
            candidate_id=row['candidate_id'], volume=row['volume'], title=row['title'],
            entry_type=row['entry_type'], original_stage_status=row['original_stage_status'],
            collected_thread_id=(f'v{row["volume"]}-' + row['original_record']['id']) if is_thread else None,
            original_record=row['original_record'], terminal_assessment=row['terminal_assessment']))
    overlay = dict(schema_version=1, artifact_type='terminal-assessment-overlay',
                   source_id=sid, review_status='draft', primary_review_status='reviewed_for_library_import',
                   original_graph_unchanged=True, graph_sha256=sha(ctx['graph_path']),
                   graph_revision=ctx['graph'].get('revision'),
                   boundary='全书终点判断叠加在历次卷末快照之上；不回写原线程status，不把历史问题全部当图线程。',
                   thread_count=sum(x['collected_thread_id'] is not None for x in overlay_rows),
                   question_count=sum(x['collected_thread_id'] is None for x in overlay_rows), entries=overlay_rows)
    ledger = dict(schema_version=1, artifact_type='question-pools-index', not_a_merged_pool=True,
                  source_id=sid, review_status='draft', primary_review_status='reviewed_for_library_import',
                  boundary='两池保留原schema与标识；分类未知不等于作者未回收，条目总数不等于伏笔总数。',
                  pools=[dict(pool=k, json_path=f'audit/whole-book/{MAIN[k][0]}',
                              markdown_path=f'audit/whole-book/{MAIN[k][0][:-5]}.md', **stats[k])
                         for k in ['historical', 'local']])
    files = {}
    def put(path, value):
        files[path] = encode_json(value) if isinstance(value, dict) else value.encode('utf-8')
    prefix = 'audit/whole-book/'
    put(prefix + 'character-identities.json', identity)
    put(prefix + 'terminal-thread-overlay.json', overlay)
    put('question-ledger.json', ledger)
    rows = ['# 人物身份索引', '', '主代理已审；用户评价仍为draft。每行对应独立审计条目，不自动合并正式人物卡。', '',
            '[人物全弧原稿](character-arc-audit-draft.md) · [结构化身份索引](character-identities.json)', '',
            '| 审计ID | 标签 | 姓名层级 | 实体范围 |', '|---|---|---|---|']
    for row in identity['subjects']:
        names = '；'.join(x['name'] + ' [' + x['level'] + ']' for x in row['names'])
        rows.append(f'| {row["audit_id"]} | {cell(row.get("display_label",row["audited_label"]))} | {cell(names)} | {row["entity_scope"]} |')
    rows += ['', identity['policy'], '']
    for row in identity['subjects']:
        if row['identity_rule'].get('boundary'):
            rows += [row['audited_label'] + '：' + row['identity_rule']['boundary'], '']
    for guard in identity['collision_guards']:
        rows += [guard['surface_name'] + '（' + guard.get('context', '') + '）：' + guard['boundary'], '']
    put(prefix + 'character-identities.md', '\n'.join(rows))
    rows = ['# 全书终点线程叠加', '', overlay['boundary'], '',
            f'图线程{overlay["thread_count"]}条；独立历史问题{overlay["question_count"]}条。未知、部分回答均保留理由与范围。', '',
            f'[原分卷结构总览](../../../../views/plots/{sid}/collected/index.html) · [完整叠加JSON](terminal-thread-overlay.json) · [历史审计池](historical-question-pool.md)', '',
            '| 候选ID | 标题 | 卷末状态 | 终点判定 | 判定理由 |', '|---|---|---|---|---|']
    for row in overlay_rows:
        d = row['terminal_assessment']
        rows.append(f'| {row["candidate_id"]} | {cell(row["title"])} | {cell(row["original_stage_status"])} | {d["status"]} | {cell(d["rationale"])} |')
    put(prefix + 'terminal-thread-overlay.md', '\n'.join(rows) + '\n')
    rows = ['# 全书问题审计入口', '', ledger['boundary'], '', '主代理已逐项审阅；用户评价仍为draft。JSON是两池索引，不合并其schema。', '',
            '| 池 | 条数 | 可读页 | 原始JSON |', '|---|---:|---|---|',
            f'| 历史问题与图线程 | {len(hist)} | [历史池](audit/whole-book/historical-question-pool.md) | [JSON](audit/whole-book/historical-question-pool.json) |',
            f'| 分卷原子问题 | {len(local)} | [原子池](audit/whole-book/local-question-pool.md) | [JSON](audit/whole-book/local-question-pool.json) |', '',
            f'[终点线程叠加](audit/whole-book/terminal-thread-overlay.md) · [{counts["findings"]}项聚焦终态审计](audit/whole-book/end-state-audit-draft.md) · [审计验收凭据](audit/whole-book/publication-receipt.json)', '']
    for k, label in [('historical', '历史池'), ('local', '原子池')]:
        rows += [f'## {label}分类', '', '| 分类轴 | 类别 | 数量 |', '|---|---|---:|']
        for axis in ['terminal_statuses', 'entry_types', 'audit_domains']:
            for name, count in stats[k][axis].items():
                rows.append(f'| {axis} | {cell(name)} | {count} |')
        rows.append('')
    put('question-ledger.md', '\n'.join(rows))
    rows = ['# 全书人物弧入口', '', f'{counts["characters"]}项人物弧已完成主代理审阅；用户评价仍为draft。保留原读者归属、事实与推断层级。', '',
            '[人物全弧审计](audit/whole-book/character-arc-audit-draft.md) · [人物身份索引](audit/whole-book/character-identities.md) · [结构化原稿](audit/whole-book/character-arc-audit-draft.json)', '',
            '| 审计ID | 人物 | 终点记录 |', '|---|---|---|']
    for row in data['characters']['characters']:
        rows.append(f'| {row["audit_id"]} | {cell(row.get("display_name",row["name"]))} | {cell(row["terminal_state"])} |')
    put('character-arcs.md', '\n'.join(rows) + '\n')
    put('reading/plot/terminal-audit.md', '# 全书终点审计叠加入口\n\n历次分卷图保留当时状态；以下为主代理审阅后的独立全书终点叠加，用户评价仍为draft。\n\n[终点线程对照](../../audit/whole-book/terminal-thread-overlay.md) · [问题两池](../../question-ledger.md) · [人物全弧](../../character-arcs.md) · [审计目录](../../audit/whole-book/README.md)\n')
    put(prefix + 'README.md', f'# 全书审计\n\n主代理已审：{counts["characters"]}人物弧、{counts["findings"]}聚焦项、{counts["historical"]}历史项、{counts["local"]}原子项。用户评价保持draft。\n\n[人物身份与姓名层级](character-identities.md) · [人物全弧](character-arc-audit-draft.md) · [聚焦终态](end-state-audit-draft.md)\n\n[历史问题池](historical-question-pool.md) · [原子问题池](local-question-pool.md) · [终点线程叠加](terminal-thread-overlay.md)\n\n[冻结清单](audit-freeze-manifest.json) · [真实主审凭据](primary-whole-book-review.json) · [发布回执](publication-receipt.json) · [原读者交接](whole-book-audit-handoff.md)\n\n[本书阅读页](../../reading/README.md) · [本书总览](../../README.md)\n\n冻结研究文件原样保存；provenance中的脚本只作来源存档，不在此目录执行。独立叠加不覆写卷末状态、正式卡片、人工笔记或用户审美。\n')
    root_readme = ctx['report'] / 'README.md'
    corrections = 'priority-corrections-delta.json' in ctx['manifest']['audit_sha256']
    if corrections:
        files[prefix + 'README.md'] += ('\n## 已核实的旧笔记纠正\n\n'
            '[优先纠错记录](priority-corrections-delta.json)。检索旧分卷笔记时须同时读取此层；旧错误保留来源历史，不作为当前事实。\n').encode('utf-8')
    nav = ('## 全书审计导航\n\n'
           f'主代理已逐项审阅{counts["characters"]}人物弧、{counts["findings"]}聚焦项、{counts["historical"]}历史项与{counts["local"]}原子项；用户评价仍为draft。\n\n'
           '[人物全弧](character-arcs.md) · [问题两池及分类](question-ledger.md) · [全书审计目录](audit/whole-book/README.md) · [终点线程叠加](reading/plot/terminal-audit.md)')
    if corrections:
        nav += '\n\n[已核实的旧笔记纠正](audit/whole-book/priority-corrections-delta.json)：检索旧分卷时同步读取纠正层。'
    put('README.md', replace_nav(root_readme.read_bytes().decode('utf-8'), nav))
    reading = ctx['report'] / 'reading/README.md'
    if reading.is_file():
        put('reading/README.md', replace_nav(reading.read_bytes().decode('utf-8'),
            '## 全书终点审计\n\n[人物全弧](../character-arcs.md) · [问题两池](../question-ledger.md) · [终点线程叠加](plot/terminal-audit.md)'))
    return files, stats, overlay


def publish(ctx, files, stats, profile_path=None):
    dest = ctx['report'] / 'audit/whole-book'
    require(dest.resolve().is_relative_to(ctx['report'].resolve()), '发布目录越界')
    if dest.exists():
        old = read(dest / 'publication-receipt.json')
        if old.get('freeze_manifest_sha256') == ctx['manifest_sha']:
            from validate_book_audit import validate
            return validate(ctx['root'], ctx['book']) | {'publication': 'already-published-no-change'}
        raise AuditError('已有不同冻结版本；请保留旧发布后另行规划版本迁移，本脚本不覆盖既有人工作业。')
    # 所有验证和派生在第一次正式写入前完成。
    for name, digest in ctx['manifest']['audit_sha256'].items():
        rel = 'provenance/' + name if name.endswith('.py') else name
        files['audit/whole-book/' + rel] = contained(ctx['audit'], name).read_bytes()
    for name in ctx['manifest']['frozen_volume08_hashes']:
        files['audit/whole-book/provenance/frozen-volume/' + name] = contained(ctx['audit'], name).read_bytes()
    files['audit/whole-book/audit-freeze-manifest.json'] = ctx['manifest_path'].read_bytes()
    files['audit/whole-book/primary-whole-book-review.json'] = ctx['review_path'].read_bytes()
    files['audit/whole-book/provenance/source-index.json'] = encode_json(ctx['source'])
    if profile_path:
        files['audit/whole-book/provenance/identity-profile.json'] = Path(profile_path).read_bytes()
    unchanged = snapshot_files(ctx['root'], ctx['book'], ctx['source']['source_id'], ctx['manifest']['formal_input_sha256'])
    before = {name: contained(ctx['report'], name).read_bytes() if contained(ctx['report'], name).is_file() else None
              for name in files if not name.startswith('audit/whole-book/')}
    # 若标准入口已有内容，原字节作为历史输入保留，不混成新schema。
    for name, content in before.items():
        if content is not None:
            files['audit/whole-book/provenance/previous-navigation/' + name] = content
    import hashlib
    receipts = {name: hashlib.sha256(content).hexdigest() for name, content in files.items()}
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    receipt = dict(schema_version=1, artifact_type='whole-book-audit-publication-receipt',
                   status='published-primary-reviewed-user-draft', book=ctx['book'],
                   source_id=ctx['source']['source_id'], revision=ctx['source']['revision'],
                   published_at_utc=now, review_status='draft', user_approval=False,
                   primary_review_status=ctx['review']['status'], freeze_manifest_sha256=ctx['manifest_sha'],
                   primary_review_sha256=sha(ctx['review_path']), counts=ctx['counts'],
                   evidence_references_checked=ctx['refs'], pool_statistics=stats,
                   copied_audit_paths={name: ('provenance/' + name if name.endswith('.py') else name)
                                       for name in ctx['manifest']['audit_sha256']},
                   published_file_sha256=receipts, unchanged_formal_sha256=unchanged,
                   navigation_original_content_sha256={name: hashlib.sha256(remove_nav(content.decode('utf-8')).encode('utf-8')).hexdigest()
                                                       for name, content in before.items() if name in ['README.md', 'reading/README.md'] and content is not None},
                   boundary='主审签收研究可入库，不代表用户审美认可；不改分卷、全书图、卡片或人工字段。')
    files['audit/whole-book/publication-receipt.json'] = encode_json(receipt)
    # 独立子目录先完整落地；根导航用同目录临时文件替换，失败恢复导航原字节。
    # Windows普通路径有260字符上限；临时目录比最终whole-book目录仅略长。
    temp = dest.parent / ('.wb-' + uuid.uuid4().hex[:12])
    require(temp.resolve().is_relative_to(ctx['report'].resolve()), '临时目录越界')
    temp.mkdir(parents=True)
    committed = False
    try:
        for name, content in files.items():
            if name.startswith('audit/whole-book/'):
                path = contained(temp, name.removeprefix('audit/whole-book/'))
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(content)
        # 复制后再次确认源冻结包及签收清单没有发生并发变化。
        from book_audit_common import verify_map, review_check
        verify_map(ctx['audit'], ctx['manifest']['audit_sha256'])
        verify_map(ctx['audit'], ctx['manifest']['frozen_volume08_hashes'])
        verify_map(ctx['root'], unchanged)
        require(sha(ctx['manifest_path']) == ctx['manifest_sha'], '发布准备时冻结清单已变化')
        require(sha(ctx['review_path']) == receipt['primary_review_sha256'], '发布准备时主审凭据已变化')
        review_check(ctx['review_path'], ctx['manifest_sha'], ctx['source']['source_id'], True)
        temp.rename(dest)
        committed = True
        for name, content in files.items():
            if not name.startswith('audit/whole-book/'):
                path = contained(ctx['report'], name)
                path.parent.mkdir(parents=True, exist_ok=True)
                pending = path.with_name('.' + path.name + '.audit-' + uuid.uuid4().hex)
                pending.write_bytes(content)
                os.replace(pending, path)
        from validate_book_audit import validate
        return validate(ctx['root'], ctx['book']) | {'publication': 'published'}
    except BaseException:
        if committed:
            for name, content in before.items():
                path = contained(ctx['report'], name)
                if content is None:
                    path.unlink(missing_ok=True)
                else:
                    path.write_bytes(content)
            # 只移动本次创建的确切审计目录，保留失败现场便于检查。
            dest.rename(dest.parent / ('.whole-book-failed-' + uuid.uuid4().hex))
        raise
    finally:
        if temp.exists():
            # 不递归删除，保留尚未提交的准备目录。
            pass


def main():
    args = arguments()
    require(bool(__import__('re').fullmatch('[a-z0-9]+(?:-[a-z0-9]+)*', args.book)), 'book必须是安全slug')
    staging = args.staging or BASE / args.book
    source = args.source_index or staging / 'source.json'
    ctx = preflight(args.root, args.book, staging, args.audit_subdir, source, args.reviewed)
    profile_path = args.identity_profile or (BASE / 'zongheng-audit-identity-profile.json' if args.book == 'zongheng-tianxia' else None)
    profile = read(profile_path) if profile_path else {}
    files, stats, overlay = generated(ctx, profile)
    result = dict(status='read-only-preflight-passed', book=args.book,
                  freeze_manifest_sha256=ctx['manifest_sha'], checked_sha256_entries=ctx['checked_hashes'],
                  counts=ctx['counts'], evidence_references_checked=ctx['refs'],
                  primary_review_present=ctx['review'] is not None, graph_threads=overlay['thread_count'],
                  independent_historical_questions=overlay['question_count'], formal_writes=False)
    if args.reviewed and not args.dry_run:
        result = publish(ctx, files, stats, profile_path)
    print(encode_json(result).decode('utf-8'), end='')


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    try:
        main()
    except (AuditError, KeyError, OSError, ValueError) as error:
        print('审计发布失败: ' + str(error), file=sys.stderr)
        sys.exit(1)
