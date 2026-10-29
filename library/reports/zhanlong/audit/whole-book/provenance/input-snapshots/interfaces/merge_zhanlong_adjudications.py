"""默认只读；仅将完整、字节未变的实际主审终评合入保全原题的两池。"""
from pathlib import Path
from collections import Counter
import argparse, copy, hashlib, json, os

B = Path(__file__).resolve().parent
STATUSES = {'answered', 'partial', 'unknown', 'unrecovered'}

def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def require(condition, message):
    if not condition:
        raise ValueError(message)

def prepare_merge(audit, progress_path, source):
    audit = Path(audit).resolve()
    progress = read(progress_path)
    pools = {kind: read(audit / f'{kind}-question-pool.json') for kind in ('historical', 'local')}
    originals = [r for p in pools.values() for r in p['candidates']]
    lookup = {r['candidate_id']: r for r in originals}
    require(len(lookup) == len(originals), '原池候选重复')
    for pool in pools.values():
        require(pool['source_id'] == source['source_id'] and not pool.get('pending_inputs'), '原池来源不符或仍待输入')
    chapters = {r['chapter_id']: r for r in source['chapters']}
    signed, origin = {}, {}
    for group in progress['batches']:
        path = (audit / group['path']).resolve()
        require(path.is_relative_to(audit), '批次路径越界')
        require(path.is_file() and sha(path) == group['sha256'], '已签批次SHA变化: ' + group['path'])
        rows = read(path)
        require(isinstance(rows, list), '批次不是数组')
        require([r['candidate_id'] for r in rows] == group['candidate_ids'] and len(rows) == group['count'], '批次ID/数量变化')
        for row in rows:
            cid = row['candidate_id']
            require(cid not in signed, '已签候选重复: ' + cid)
            require(cid in lookup, '已签候选不在原池: ' + cid)
            if 'original_question' in row:
                require(row['original_question'] == lookup[cid]['title'], '原问题串变化: ' + cid)
            if 'original_record' in row:
                require(row['original_record'] == lookup[cid]['original_record'], '原记录变化: ' + cid)
            require(row.get('status') in STATUSES and row.get('rationale') and row.get('audit_domain') and row.get('actual_reviewer'), '终评尚不完整: ' + cid)
            require(isinstance(row.get('later_chapters'), list) and all(type(n) is int for n in row['later_chapters']), '后证章节不完整: ' + cid)
            evidence = row.get('later_evidence')
            require(isinstance(evidence, list) and evidence, '缺少后证: ' + cid)
            require({e['chapter_id'] for e in evidence} == {f'ch-{n:04d}' for n in row['later_chapters']}, '后证章节集合不相等: ' + cid)
            for e in evidence:
                c = chapters.get(e['chapter_id'])
                require(c and e['source_id'] == source['source_id'] and e['revision'] == source['revision']
                        and type(e['start_line']) is int and type(e['end_line']) is int
                        and c['start_line'] <= e['start_line'] <= e['end_line'] <= c['end_line']
                        and e.get('claim_kind') in {'fact', 'inference', 'synthesis', 'plan'}, '证据范围/来源不符: ' + cid)
            signed[cid], origin[cid] = row, group
    require(sorted(signed) == progress['distinct_reviewed_candidate_ids'] and len(signed) == progress['distinct_reviewed_candidates'], '签收进度集合不符')
    require(set(signed) == set(lookup), f'未全部签收: {len(signed)}/{len(lookup)}，不允许合池')
    outputs = copy.deepcopy(pools)
    for pool in outputs.values():
        pool['status'] = 'all_candidates_primary_reviewed_draft_pending_whole_book_acceptance'
        for row in pool['candidates']:
            original = lookup[row['candidate_id']]
            decision = signed[row['candidate_id']]
            assessment = {key: copy.deepcopy(decision[key]) for key in (
                'status', 'audit_domain', 'rationale', 'later_chapters', 'later_evidence', 'actual_reviewer')}
            for key in ('reading_attribution', 'source_attribution', 'source_scope', 'source_checks'):
                if key in decision:
                    assessment[key] = copy.deepcopy(decision[key])
            group = origin[row['candidate_id']]
            assessment.update(review_progress='primary-reviewed-draft', user_approval=False,
                              adjudication_provenance=dict(path=group['path'], sha256=group['sha256']))
            row['terminal_assessment'] = assessment
            require({k:v for k,v in row.items() if k!='terminal_assessment'} == {k:v for k,v in original.items() if k!='terminal_assessment'}, '合池改变原记录')
            require(row['terminal_assessment']['later_evidence'] == decision['later_evidence'], '合池改变证据署名或精确范围')
    report = dict(status='complete-signed-set-ready-for-merge', candidates=len(signed), batches=len(progress['batches']),
                  counts={kind: len(p['candidates']) for kind, p in outputs.items()},
                  statuses={kind: dict(Counter(r['terminal_assessment']['status'] for r in p['candidates'])) for kind, p in outputs.items()},
                  original_records_unchanged=True, exact_evidence_objects_preserved=True,
                  semantic_reading_created=False, whole_book_accepted=False)
    return outputs, report

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    stage = B / 'zhanlong'
    audit = stage / 'audit/whole-book'
    progress = stage / 'primary-audit-review-progress.json'
    try:
        outputs, report = prepare_merge(audit, progress, read(stage / 'source.json'))
    except ValueError as error:
        print(json.dumps(dict(status='not-ready-no-write', reason=str(error), apply_requested=args.apply), ensure_ascii=False))
        if args.apply:
            raise SystemExit(1)
        return
    if args.apply:
        history = audit / 'unmerged-pools-before-primary-merge'
        require(not history.exists(), '已存在合池历史，不静默重复应用')
        targets = {kind: audit / f'{kind}-question-pool.json' for kind in outputs}
        before = {kind: (sha(p), p.read_bytes()) for kind, p in targets.items()}
        signed_sha = sha(progress)
        history.mkdir()
        for kind, (_, data) in before.items():
            (history / targets[kind].name).write_bytes(data)
        prepared = {}
        for kind, data in outputs.items():
            temp = history / (kind + '-prepared.json')
            temp.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
            prepared[kind] = temp
        require(sha(progress) == signed_sha and all(sha(p) == before[kind][0] for kind, p in targets.items()), '准备期间输入发生变化')
        for kind, target in targets.items():
            os.replace(prepared[kind], target)
        report.update(status='merged-exact-primary-reviewed-decisions',
                      pool_before_sha256={kind: value[0] for kind, value in before.items()},
                      pool_after_sha256={kind: sha(p) for kind, p in targets.items()},
                      primary_progress_sha256=signed_sha)
        (audit / 'adjudication-progress.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False))

if __name__ == '__main__':
    main()
