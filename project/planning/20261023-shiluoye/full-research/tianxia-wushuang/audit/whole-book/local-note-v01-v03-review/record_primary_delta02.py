import json,hashlib,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');P=Path(__file__).parent
load=lambda p:json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
f=P/'adjudications-local-note-v01-part02.json';old=load(f);oldsha=sha(f)
new=[r for r in load(P/'adjudications-local-note-v01.json') if 24<=r['original_index']<44]
d=[{'candidate_id':a['candidate_id'],'before':a,'after':b} for a,b in zip(old,new) if a!=b]
assert [x['candidate_id'] for x in d]==['v01-local-notes-unresolved-041-04','v01-local-notes-unresolved-042-01']
save(f,new);save(P/'primary-delta-part02.json',{'old_part_sha256':oldsha,'new_part_sha256':sha(f),'delta':d,
 'reason':'042-01按root删净流入断言；041-04继续读54后确认旧黑腿换书，补专属后用但不宣十银现金。'})
print(json.dumps({'part02':sha(f),'delta':sha(P/'primary-delta-part02.json')},ensure_ascii=False))
