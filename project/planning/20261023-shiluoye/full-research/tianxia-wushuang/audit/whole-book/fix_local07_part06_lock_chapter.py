import copy,hashlib,json,pathlib
H=pathlib.Path(__file__).resolve().parent;p=H/'adjudications-local-v07-part06.json'
raw=p.read_bytes();assert hashlib.sha256(raw).hexdigest()=='fcaf26253ab204afa1b6726e4d468b36fb93e486924b32e0613988ed6feb0c24'
a=json.loads(raw);b=copy.deepcopy(a);old=next(x for x in a if x['candidate_id']=='v07-local-local_historical_questions-150-01');new=next(x for x in b if x['candidate_id']==old['candidate_id']);new['rationale']=old['rationale'].replace('1433尚在锁中','1443尚在锁中')
assert old['rationale']!=new['rationale'] and sum(x!=y for x,y in zip(a,b))==1
(H/'reviewed-batches'/'adjudications-local-v07-part06-before-lock-chapter.json').write_bytes(raw)
p.write_text(json.dumps(b,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');sha=hashlib.sha256(p.read_bytes()).hexdigest()
(H/'local07-part06-lock-chapter-delta.json').write_text(json.dumps(dict(candidate_id=old['candidate_id'],before_sha256=hashlib.sha256(raw).hexdigest(),after_sha256=sha,unchanged_other_items=59,before=old,after=new),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for name in ['local-v07-reviewed-part06.md','write_local07_part06.py']:
 path=H/name;path.write_text(path.read_text(encoding='utf-8').replace(old['rationale'],new['rationale']),encoding='utf-8')
print(sha)
