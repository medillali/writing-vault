"""独立重放已经实际完整读并批准的西溪三条/唐职责一条。"""
from pathlib import Path
import json,hashlib,copy,sys
sys.stdout.reconfigure(encoding='utf-8')
A=Path(__file__).parent/'zhanlong/audit/whole-book'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
W=A/'reader3-review';p=W/'wetland-three-items-proposal.json'
assert sha(p)=='12dec62541cbe18d1eb3952c6de202ca4c1e74926e0663521c6d82ae4722c4ff'
for item in read(p)['proposals']:
 name=item['batch_file'];n=name.split('batch')[1].split('.')[0]
 oldpath=W/f'batch{n}-before-wetland-approved.json';current=A/name
 assert sha(oldpath)==item['submitted_sha256']
 old=read(oldpath);new=copy.deepcopy(old);idx=[i for i,r in enumerate(old) if r['candidate_id']==item['candidate_id']]
 assert len(idx)==1 and new[idx[0]]==item['before']
 new[idx[0]]=item['after'];assert new==read(current) and len(new)==20
 checks.append(dict(path=name,candidate_id=item['candidate_id'],only_approved_object_changed=True,sha256=sha(current),rationale=item['after']['rationale']))
D=A/'local-v02-v05-review';p=D/'tang-duty-without-final-farewell-proposal.json'
assert sha(p)=='fbece78c214bb2d7fd3d4faaceaaeb394203d8f56627692982a02fc4bf4899a9'
item=read(p)['changes'][0];oldpath=D/'history/adjudications-local-v02-batch012-before-tang-duty-without-final-farewell.json';current=D/item['path']
assert sha(oldpath)==item['input_sha256'];old=read(oldpath);new=copy.deepcopy(old);idx=[i for i,r in enumerate(old) if r['candidate_id']==item['candidate_id']]
assert len(idx)==1 and new[idx[0]]==item['before'];new[idx[0]]=item['after'];assert new==read(current) and len(new)==20
checks.append(dict(path='local-v02-v05-review/'+item['path'],candidate_id=item['candidate_id'],only_approved_object_changed=True,sha256=sha(current),rationale=item['after']['rationale']))
(A/'primary-recent-delta-verification.json').write_text(json.dumps(dict(status='exact-approved-deltas-verified',checks=checks,semantic_reading_created=False),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(status='exact-approved-deltas-verified',checks=checks,semantic_reading_created=False),ensure_ascii=False))
