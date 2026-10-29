import json,hashlib,subprocess,sys
from pathlib import Path
P=Path(__file__).parent
load=lambda p:json.loads(p.read_text(encoding='utf-8'))
save=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
p=P/'adjudications-local-v05-tail-part02.json';old=load(p)
assert sha(p)=='c00ae2af016fcb45f350e5663c7bc652a94931225181436c22f34404552c74bf'
q=P/'primary-before';q.mkdir(exist_ok=True)
before=q/'part02-before-direct-city-mvp-10301.json';assert not before.exists();before.write_bytes(p.read_bytes())
subprocess.run([sys.executable,str(P/'build_checkpoint.py')],check=True)
newrow=next(r for r in load(P/'adjudications-local-v05-tail.json') if r['scope_onebased_offset']==290)
new=[newrow if r['scope_onebased_offset']==290 else r for r in old]
assert all(a==b for a,b in zip(old,new) if a['scope_onebased_offset']!=290)
save(p,new)
v=load(P/'part02-validation.json');v['sha256']=sha(p);save(P/'part02-validation.json',v)
save(P/'primary-delta-part02.json',{'request':'root定向补935国内MVP系统城池规模+1直接后证，仅103-01。','before_path':str(before.relative_to(P)),'before_sha256':sha(before),'after_sha256':sha(p),'candidate_id':newrow['candidate_id'],'before':next(r for r in old if r['scope_onebased_offset']==290),'after':newrow,'other_59_unchanged':True})
print(json.dumps({'part02_sha256':sha(p),'delta_sha256':sha(P/'primary-delta-part02.json')},ensure_ascii=False))
