import pathlib,json,hashlib
H=pathlib.Path(__file__).resolve().parent;p=H/'adjudications-local-v07-part03.json'
before=json.loads(p.read_text(encoding='utf-8'));oldsha=hashlib.sha256(p.read_bytes()).hexdigest()
old=H/'reviewed-batches/adjudications-local-v07-part03-before-firekirin-name.json';assert not old.exists();old.write_bytes(p.read_bytes())
after=json.loads(json.dumps(before));cid='v07-local-local_historical_questions-075-03'
x=next(x for x in after if x['candidate_id']==cid);x['rationale']=x['rationale'].replace('1368幼龙蛋绑定','1368火麒麟蛋赠北并绑定')
assert [x['candidate_id'] for x,y in zip(before,after) if x!=y]==[cid]
p.write_text(json.dumps(after,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');newsha=hashlib.sha256(p.read_bytes()).hexdigest()
d=dict(candidate_id=cid,before_sha256=oldsha,after_sha256=newsha,unchanged_other_items=59,before=next(x for x in before if x['candidate_id']==cid),after=x)
(H/'local07-part03-firekirin-delta.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for name in ['write_local07_part03.py','local-v07-reviewed-part03.md']:
 q=H/name;s=q.read_text(encoding='utf-8').replace('1368幼龙蛋绑定','1368火麒麟蛋赠北并绑定');q.write_text(s,encoding='utf-8')
print(newsha)
