"""独立重放四条已审授权修订并保全前一版主审签表。"""
from pathlib import Path
import copy, hashlib, json
B = Path(__file__).resolve().parent
S = B / 'zhanlong'
A = S / 'audit/whole-book'
P = A / 'reader3-review'
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
delta = read(P / 'cap-order-approved-combined-delta.json')
assert len(delta['batches']) == 3
changed = 0
for group in delta['batches']:
    before = P / (group['file'].removesuffix('.json')+'-before-approved-cap.json')
    current = A / group['file']
    assert sha(before) == group['before_sha256'] and sha(current) == group['after_sha256']
    expected = read(before)
    for change in group['changes']:
        i = next(i for i,r in enumerate(expected) if r['candidate_id'] == change['candidate_id'])
        assert expected[i] == change['before']
        fields = {k for k in change['before'] if change['before'][k] != change['after'][k]}
        allowed = {'rationale','later_chapters','later_evidence'}
        if change['candidate_id'].endswith('0177-01'):
            allowed.add('audit_domain')
            assert change['after']['audit_domain'] == 'resting-army-and-later-authorized-expansion'
        assert fields == allowed
        assert change['after']['status'] == change['before']['status'] == 'partial'
        assert set(change['after']['later_chapters']) - set(change['before']['later_chapters']) == {975}
        assert set(change['before']['later_chapters']).issubset(change['after']['later_chapters'])
        expected[i] = copy.deepcopy(change['after'])
        changed += 1
    assert expected == read(current) and len(expected) == 20
assert changed == 4
ledger = S / 'primary-audit-review-progress.json'
snapshot = P / 'primary-progress-before-cap-resign.json'
if not snapshot.exists():
    entries = {g['path']:g for g in read(ledger)['batches']}
    assert all(entries[g['file']]['sha256'] == g['before_sha256'] for g in delta['batches'])
    snapshot.write_bytes(ledger.read_bytes())
else:
    entries = {g['path']:g for g in read(snapshot)['batches']}
    assert all(entries[g['file']]['sha256'] == g['before_sha256'] for g in delta['batches'])
result = dict(status='exact-four-approved-cap-changes-verified', changed_objects=4, other_objects_unchanged=56,
              old_primary_progress_sha256=sha(snapshot), all_statuses_unchanged=True,
              primary_changed_objects_actual_read=4, prior_unchanged_objects_already_read=True,
              semantic_reading_created=False)
(P / 'primary-cap-revision-verification.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps(result, ensure_ascii=False))
