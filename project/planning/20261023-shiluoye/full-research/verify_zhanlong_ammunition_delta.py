"""仅核对已实际主审批准的持续供弹补证差分，不产生阅读声明。"""
from pathlib import Path
import copy, hashlib, json
A = Path(__file__).parent / 'zhanlong/audit/whole-book/local-v02-v05-review'
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
p = A / 'continuous-ammunition-performance-proposal.json'
assert sha(p) == '5f1ff2b401fcbf6081c3b23b759728a6f1abd64a5067b30d1c1fa18e44314c32'
c = read(p)['changes'][0]
d = read(A / 'continuous-ammunition-performance-merged-delta.json')['changes'][0]
old, cur = A / d['before_snapshot'], A / c['path']
assert sha(old) == c['input_sha256'] == d['batch_before_sha256']
assert sha(cur) == d['batch_after_sha256']
rows = read(old)
i = next(i for i, r in enumerate(rows) if r['candidate_id'] == c['candidate_id'])
assert rows[i] == c['before']
assert {k for k in c['before'] if c['before'][k] != c['after'][k]} == {'rationale', 'later_chapters', 'later_evidence'}
assert c['after']['later_chapters'] == c['before']['later_chapters'] + [1145]
assert c['after']['later_evidence'][:-1] == c['before']['later_evidence']
assert c['after']['later_evidence'][-1]['chapter_id'] == 'ch-1145'
out = copy.deepcopy(rows)
out[i] = c['after']
assert len(out) == 20 and out == read(cur)
result = dict(status='exact-approved-delta-verified', candidate_id=c['candidate_id'], other_19_exactly_equal=True,
              after_sha256=sha(cur), semantic_reading_created=False)
(A / 'primary-ammunition-delta-verification.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(result, ensure_ascii=False))
