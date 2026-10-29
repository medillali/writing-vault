"""重放已实际主审批准的方二百万指定援军复合项最小修订。"""
from pathlib import Path
import copy,hashlib,json
A=Path(__file__).parent/'zhanlong/audit/whole-book/local-v02-v05-review'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
p=A/'fang-two-million-specific-aid-proposal.json'
assert sha(p)=='bf9f34deab304acaf0d9e319b5a74f2da9040e2bc20d7affd27ecde4b1c7c19c'
change=read(p)['changes'][0]
d=read(A/'fang-two-million-specific-aid-merged-delta.json')['changes'][0]
old=A/d['before_snapshot'];cur=A/change['path']
assert sha(old)==change['input_sha256']==d['batch_before_sha256']
assert sha(cur)==d['batch_after_sha256']
rows=read(old);out=copy.deepcopy(rows)
idx=next(i for i,r in enumerate(rows) if r['candidate_id']==change['candidate_id'])
assert rows[idx]==change['before']
assert {k for k in change['before'] if change['before'][k]!=change['after'][k]}=={'status','rationale'}
out[idx]=change['after'];assert out==read(cur) and len(out)==20
result=dict(status='exact-approved-delta-verified',candidate_id=change['candidate_id'],
    other_19_exactly_equal=True,after_sha256=sha(cur),semantic_reading_created=False)
(A/'primary-fang-delta-verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
