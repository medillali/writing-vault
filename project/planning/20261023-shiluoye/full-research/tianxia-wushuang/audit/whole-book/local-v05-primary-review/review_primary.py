"""主代理卷五终点裁定的暂存辅助；只保存手写判断，不生成判断。"""
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
HERE = Path(__file__).resolve().parent
BOOK = HERE.parents[2]
ROOT = HERE.parents[6]

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def notes():
    result = {}
    for path in sorted(BOOK.glob('vol??/chapter-notes.jsonl')):
        for line in path.read_text(encoding='utf-8-sig').splitlines():
            row = json.loads(line)
            result[row['chapter_id']] = (row, path, hashlib.sha256(line.encode()).hexdigest())
    return result

action, *args = sys.argv[1:]
if action == 'init':
    target = HERE/'assigned-candidates.json'
    assert not target.exists(), '已有快照，不能覆盖'
    pool = read(HERE.parent/'local-question-pool.json')
    rows = [r for r in pool['candidates'] if r['volume'] == 5]
    assert len(rows) == 556
    write(target, rows)
    write(HERE/'input-read-log.json', {
        'reviewer': '/root', 'assigned_candidates': 556,
        'original_volume_reader': '/root/zongheng_vol04_full',
        'boundary': '本专项重读完整候选及派生章节四栏笔记；不冒称主代理全文重读卷五原文。快照不是已读凭据。',
        'snapshot_sha256': digest(target), 'complete_derived_notes_read': {}})
    print('SNAPSHOT_ONLY 556')
elif action == 'marknotes':
    log = read(HERE/'input-read-log.json')
    index = notes()
    for chapter in args:
        cid = f'ch-{int(chapter):04d}'
        row, path, sha = index[cid]
        log['complete_derived_notes_read'][cid] = {
            'record_sha256': sha, 'path': path.relative_to(ROOT).as_posix(),
            'original_reader': row.get('reader'),
            'access': 'complete-derived-note-read-not-original-reread'}
    write(HERE/'input-read-log.json', log)
    print('COMPLETE_DERIVED_NOTES', len(log['complete_derived_notes_read']))
elif action == 'build':
    decision_file = HERE/args[0]
    out = HERE/args[0].replace('decisions-', 'adjudications-local-')
    assert not out.exists(), '稳定批不能覆盖；纠错须另留delta'
    assigned = {r['candidate_id']: r for r in read(HERE/'assigned-candidates.json')}
    logged = read(HERE/'input-read-log.json')['complete_derived_notes_read']
    index, result = notes(), []
    for decision in read(decision_file):
        cid, status, domain, rationale, chapters = decision
        assert status in ('answered', 'partial', 'unknown', 'unrecovered')
        assert cid in assigned and domain and rationale
        original = assigned[cid]
        row = {k: v for k, v in original.items() if k != 'terminal_assessment'}
        evidence = []
        for chapter in chapters:
            ch = f'ch-{chapter:04d}'
            assert ch in logged, f'后证未实际完整读notes：{ch}'
            note, path, sha = index[ch]
            assert sha == logged[ch]['record_sha256'], '已读笔记变化'
            evidence.append({k: note[k] for k in ('source_id', 'revision', 'chapter_id', 'start_line', 'end_line')} | {
                'claim_kind': 'fact', 'access_level': 'derived-volume-research',
                'research_path': path.relative_to(ROOT).as_posix(),
                'locator_basis': '主代理本专项完整读四栏派生笔记；不冒认亲读本章原文'})
        row.update(status=status, audit_domain=domain, rationale=rationale,
                   later_chapters=chapters, later_evidence=evidence,
                   reviewer='/root', review_status='primary-reviewed-user-draft')
        result.append(row)
    assert len({r['candidate_id'] for r in result}) == len(result)
    write(out, result)
    print(json.dumps({'count': len(result), 'statuses': dict(Counter(r['status'] for r in result)),
                      'file': out.name, 'sha256': digest(out)}, ensure_ascii=False))
else:
    raise ValueError(action)
