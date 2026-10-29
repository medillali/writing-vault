import json,hashlib,subprocess,sys,collections
from pathlib import Path
P=Path(__file__).parent
load=lambda p:json.loads(p.read_text(encoding='utf-8'))
save=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
p=P/'adjudications-local-v05-tail-part03.json';old=load(p)
assert sha(p)=='0a866cf8175aef37bb00b2ac4c63a4d435475a6c00b4521643132ae0e2fbf6c1'
q=P/'primary-before';q.mkdir(exist_ok=True)
before=q/'part03-before-city935-cup941.json';assert not before.exists();before.write_bytes(p.read_bytes())
subprocess.run([sys.executable,str(P/'build_checkpoint.py')],check=True)
changed={321,357};agg={r['scope_onebased_offset']:r for r in load(P/'adjudications-local-v05-tail.json')}
new=[agg[r['scope_onebased_offset']] if r['scope_onebased_offset'] in changed else r for r in old]
assert all(a==b for a,b in zip(old,new) if a['scope_onebased_offset'] not in changed)
save(p,new)
v=load(P/'part03-validation.json');v['sha256']=sha(p);v['status_counts']=dict(collections.Counter(r['status'] for r in new));save(P/'part03-validation.json',v)
save(P/'primary-delta-part03.json',{'request':'root定向119-01补935直接升10；141-01补941同杯已存，其他58不变。','before_path':str(before.relative_to(P)),'before_sha256':sha(before),'after_sha256':sha(p),'changes':[{'before':a,'after':b} for a,b in zip(old,new) if a!=b],'other_58_unchanged':True})
print(json.dumps({'part03_sha256':sha(p),'delta_sha256':sha(P/'primary-delta-part03.json')},ensure_ascii=False))
