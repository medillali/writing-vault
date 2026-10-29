"""独立重放获批两条矿产后证；先留旧签账，重新签入由单独主审工具执行。"""
from pathlib import Path
import hashlib, json, copy
B = Path(__file__).resolve().parent
S = B / 'zhanlong'
A = S / 'audit/whole-book'
P = A / 'reader3-review'
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
d = read(P / 'halfmine-approved-combined-delta.json')
before = P / 'v04-batch016-before-approved-halfmine-e70.json'
current = A / 'adjudications-local-v04-batch016.json'
assert sha(before) == d['before_sha256'] == 'e70a117e4cbb0379b12dcda81212705148b671e473d834d833a3f7e4fa7eb0eb'
assert sha(current) == d['after_sha256'] == '73704c15d8d0e6f5b79829ce8d14a280e238ccdf8ec737b9e02314f0880c0bb5'
expected = read(before)
assert len(d['changes']) == 2
for change in d['changes']:
    i = next(i for i,r in enumerate(expected) if r['candidate_id'] == change['candidate_id'])
    assert expected[i] == change['before']
    assert {k for k in change['before'] if change['before'][k] != change['after'][k]} == {'status','rationale','later_chapters','later_evidence'}
    assert change['after']['status'] == 'answered' and set(change['before']['later_chapters']).issubset(change['after']['later_chapters'])
    assert set(change['after']['later_chapters']) - set(change['before']['later_chapters']) == {938}
    expected[i] = copy.deepcopy(change['after'])
assert expected == read(current) and len(expected) == 20
ledger = S / 'primary-audit-review-progress.json'
old_ledger = P / 'primary-progress-before-halfmine-resign.json'
if not old_ledger.exists():
    group = next(g for g in read(ledger)['batches'] if g['path'] == current.name)
    assert group['sha256'] == d['before_sha256']
    old_ledger.write_bytes(ledger.read_bytes())
else:
    assert next(g for g in read(old_ledger)['batches'] if g['path']==current.name)['sha256'] == d['before_sha256']
result = dict(status='exact-two-approved-changes-verified', unchanged_other_objects=18, current_batch_sha256=sha(current),
              original_signed_progress_sha256=sha(old_ledger), actual_primary_reread_items=20, source_chapter=938, semantic_reading_created=False)
(P / 'primary-halfmine-revision-verification.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps(result, ensure_ascii=False))
