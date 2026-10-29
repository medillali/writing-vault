import json,hashlib,subprocess,sys
from pathlib import Path
P=Path(__file__).parent;load=lambda p:json.loads(p.read_text(encoding='utf-8'))
save=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
q=P/'unsubmitted-snapshots';q.mkdir(exist_ok=True)
p=P/'adjudications-local-v05-tail-part05.json';before=q/'part05-before-first-report-self-check.json';assert not before.exists();before.write_bytes(p.read_bytes())
subprocess.run([sys.executable,str(P/'build_checkpoint.py')],check=True)
rows=[r for r in load(P/'adjudications-local-v05-tail.json') if 418<=r['scope_onebased_offset']<=477];assert len(rows)==60;save(p,rows)
v=load(P/'part05-validation.json');v['sha256']=hashlib.sha256(p.read_bytes()).hexdigest();save(P/'part05-validation.json',v)
print(v['sha256'])
