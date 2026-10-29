import json,hashlib,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');P=Path(__file__).parent
load=lambda p:json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
f=P/'adjudications-local-note-v03-part02.json';old=load(f);oldsha=sha(f)
new=[r for r in load(P/'adjudications-local-note-v03.json') if 48<=r['original_index']<84]
d=[{'candidate_id':a['candidate_id'],'before':a,'after':b} for a,b in zip(old,new) if a!=b]
assert [x['candidate_id'] for x in d]==['v03-local-notes-unresolved-055-01']
save(f,new);save(P/'primary-delta-v03-part02.json',{'reason':'root要求去掉理由误输入1375，改第275章换链防1325，此处旧1165；状态证据不变','old_sha256':oldsha,'new_sha256':sha(f),'delta':d})
print(json.dumps({'part02':sha(f),'delta':sha(P/'primary-delta-v03-part02.json')},ensure_ascii=False))
