import json,hashlib,subprocess,sys,collections
from pathlib import Path
P=Path(__file__).parent
load=lambda p:json.loads(p.read_text(encoding='utf-8'))
save=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
p=P/'adjudications-local-v05-tail-part05.json';old=load(p)
assert sha(p)=='49b0a1998a3c49bedae461df8be4979ef89e67e4ac379ba2918fc50b2939be25'
q=P/'primary-before';q.mkdir(exist_ok=True)
before=q/'part05-before-qingkong1185-19801.json';assert not before.exists();before.write_bytes(p.read_bytes())
subprocess.run([sys.executable,str(P/'build_checkpoint.py')],check=True)
newrow=next(r for r in load(P/'adjudications-local-v05-tail.json') if r['scope_onebased_offset']==439)
new=[newrow if r['scope_onebased_offset']==439 else r for r in old]
assert all(a==b for a,b in zip(old,new) if a['scope_onebased_offset']!=439)
save(p,new)
v=load(P/'part05-validation.json');v['sha256']=sha(p);v['status_counts']=dict(collections.Counter(r['status'] for r in new));save(P/'part05-validation.json',v)
save(P/'primary-delta-part05.json',{'request':'root亲读1185确认晴空亲口喜欢陆，198-01补其本人后证；其他59不变。','before_path':str(before.relative_to(P)),'before_sha256':sha(before),'after_sha256':sha(p),'candidate_id':newrow['candidate_id'],'before':next(r for r in old if r['scope_onebased_offset']==439),'after':newrow,'other_59_unchanged':True})
print(json.dumps({'part05_sha256':sha(p),'delta_sha256':sha(P/'primary-delta-part05.json')},ensure_ascii=False))
