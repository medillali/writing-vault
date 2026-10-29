"""重放主审已实际读并批准的罗林归功/末刀最小修订，不改冻结卷稿。"""
from pathlib import Path
import copy, hashlib, json
A = Path(__file__).parent / 'zhanlong/audit/whole-book'
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
proposal = A / 'batch011-rolin-kill-attribution-proposal.json'
assert sha(proposal) == 'f9b503e02abbaf3ca42fc46aa6d9410858c1aab17ef4815650311bbcbdcb7bc7'
delta = read(A / 'batch011-rolin-kill-attribution-applied-delta.json')
current = A / 'adjudications-local-v03-batch011.json'
assert sha(current) == delta['after_batch_sha256']
rows = read(current)
assert len(rows) == 20
indexes = [i for i, r in enumerate(rows) if r['candidate_id'] == delta['candidate_id']]
assert len(indexes) == 1 and rows[indexes[0]] == delta['after']
restored = copy.deepcopy(rows)
restored[indexes[0]] = delta['before']
old_candidates = [p for p in A.rglob('*.json') if p != current and sha(p) == delta['before_batch_sha256']]
assert old_candidates, '未找到字节匹配的修订前整批'
assert all(read(p) == restored for p in old_candidates)
changed = [k for k in delta['before'] if delta['before'][k] != delta['after'][k]]
assert set(changed) == {'rationale', 'later_chapters', 'later_evidence'}
result = dict(status='exact-approved-delta-verified', candidate_id=delta['candidate_id'],
              before_files=[p.relative_to(A).as_posix() for p in old_candidates],
              after_sha256=sha(current), changed_fields=changed,
              other_19_exactly_equal=True, semantic_reading_created=False)
(A / 'primary-rolin-delta-verification.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps(result, ensure_ascii=False))
