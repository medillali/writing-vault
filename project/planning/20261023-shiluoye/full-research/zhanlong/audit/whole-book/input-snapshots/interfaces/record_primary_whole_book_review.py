"""全部人工逐项复核完成后，独立核对签收集合与发布包再生成整书主审凭据。"""
from __future__ import annotations

import argparse
import datetime
import sys
from collections import Counter

from book_audit_common import (BASE, DEFAULT_ROOT, MAIN, STATUS, contained,
                              encode_json, load_package, read, require, sha, verify_map)


def check_batches(stage, audit, package):
    progress = read(stage / 'primary-audit-review-progress.json')
    signed = {}
    for group in progress['batches']:
        path = contained(audit, group['path'])
        require(sha(path) == group['sha256'], f'已签批次变化: {path}')
        rows = read(path)
        ids = [r['candidate_id'] for r in rows]
        require(ids == group['candidate_ids'] and len(ids) == group['count'], '批次ID或数量变化')
        for row in rows:
            cid = row['candidate_id']
            require(cid not in signed, f'候选重复签收: {cid}')
            require(row['status'] in STATUS and row['rationale'], f'候选判断不完整: {cid}')
            signed[cid] = row
    require(sorted(signed) == progress['distinct_reviewed_candidate_ids'], '进度ID集合不符')
    require(len(signed) == progress['distinct_reviewed_candidates'], '进度数量不符')
    final_rows = [r for kind in ('historical', 'local') for r in package[kind]['candidates']]
    require(Counter(r['candidate_id'] for r in final_rows) == Counter(signed.keys()),
            '整书候选与实际已签集合不相等')
    for final in final_rows:
        cid = final['candidate_id']
        expected, actual = signed[cid], final['terminal_assessment']
        for key in ('status', 'rationale', 'audit_domain'):
            require(actual[key] == expected[key], f'终评语义变化: {cid}/{key}')
        require(not actual.get('depends_on_volumes'), f'终评仍待输入: {cid}')
        expected_chapters = expected['later_chapters']
        require(all(isinstance(n, int) for n in expected_chapters), '签收后证章节非整数')
        if 'later_chapters' in actual:
            require(actual['later_chapters'] == expected_chapters, f'原后证数组变化: {cid}')
        actual_chapters = sorted({int(e['chapter_id'][3:]) for e in actual['later_evidence']})
        require(actual_chapters == sorted(set(expected_chapters)), f'后证集合变化: {cid}')
    return len(progress['batches']), signed


def check_groups(stage, audit, package):
    progress = read(stage / 'primary-research-group-review-progress.json')
    expected = {'characters': {}, 'findings': {}}
    for group in progress['groups']:
        section = group['section']
        require(section in expected, f'未知研究组类型: {section}')
        path = contained(audit, group['path'])
        require(sha(path) == group['sha256'], f'已签研究组变化: {path}')
        data = read(path)
        if data.get('formal_input_sha256'):
            verify_map(DEFAULT_ROOT, data['formal_input_sha256'])
        rows = data[section]
        ids = [r[group['id_field']] for r in rows]
        require(ids == group['reviewed_ids'] and len(ids) == group['count'], '研究组ID变化')
        for row, item_id in zip(rows, ids):
            require(item_id not in expected[section], f'研究项重复: {item_id}')
            expected[section][item_id] = row
    for section, signed in expected.items():
        require(signed, f'没有已签研究组: {section}')
        key = MAIN[section][2]
        rows = package[section][section]
        require({r[key] for r in rows} == set(signed), f'研究组未全部签收: {section}')
        for row in rows:
            require(row == signed[row[key]], f'最终研究项与已签对象不相等: {row[key]}')
    return len(progress['groups'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('book')
    parser.add_argument('--reviewed', action='store_true', required=True)
    args = parser.parse_args()
    stage = contained(BASE, args.book)
    audit = stage / 'audit/whole-book'
    freeze_path = audit / 'audit-freeze-manifest.json'
    freeze = read(freeze_path)
    for name, root in [('audit_sha256', audit), ('formal_input_sha256', DEFAULT_ROOT),
                       ('frozen_volume08_hashes', audit)]:
        verify_map(root, freeze[name])
    source = read(stage / 'source.json')
    require(source['source_id'] == freeze['source_id'], '来源ID变化')
    package, counts, references = load_package(audit, source)
    validation = read(audit / 'audit-validation.json')
    require(validation.get('frozen_volume08_unchanged'), '末卷冻结校验未通过')
    batches, signed = check_batches(stage, audit, package)
    groups = check_groups(stage, audit, package)
    reviewed_ids = {kind: [r[MAIN[kind][2]] for r in data[MAIN[kind][1]]]
                    for kind, data in package.items()}
    review = {
        'status': 'reviewed_for_library_import', 'reviewer': 'primary', 'user_approval': False,
        'reviewed_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'source_id': source['source_id'], 'freeze_manifest_sha256': sha(freeze_path),
        'reviewed_counts': {'character_arcs': counts['characters'], 'focused_findings': counts['findings'],
                            'historical_questions': counts['historical'], 'local_atomic_items': counts['local']},
        'reviewed_ids': reviewed_ids,
        'review_method': '各分卷读者实际全文阅读；主代理逐项阅读全部派生终评、人物弧、重点研究及定向修订。签收核验不生成阅读，也不冒称主代理个人重读全书。',
        'integrity_checks': {'signed_candidate_batches': batches, 'signed_research_groups': groups,
                             'candidate_semantic_objects_compared': len(signed),
                             'evidence_references_checked': references,
                             'final_research_objects_equal_signed_groups': True},
        'limits': ['研究解释不等用户审美批准', '定位有效不证明唯一解释',
                   'unknown不等作者忘记；answered可包含研究边界澄清',
                   '来源事实、角色猜测、机制抽象与原创正典保持分开']}
    target = stage / 'primary-whole-book-review.json'
    require(not target.exists(), '整书凭据已存在，不静默覆盖')
    target.write_bytes(encode_json(review))
    print(encode_json({'status': review['status'], 'reviewed_counts': review['reviewed_counts'],
                       'integrity_checks': review['integrity_checks'], 'review_path': str(target)}).decode('utf-8'))


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
