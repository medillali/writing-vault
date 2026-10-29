import json,hashlib
from pathlib import Path
P=Path(__file__).parent;p=P/'adjudications-local-note-v03-part07.json'
assert hashlib.sha256(p.read_bytes()).hexdigest()=='2bb2b64b55a65f5310cdf7cde82bf284d5fc6617ced9838c9bdb2538fbd6bf5c'
old=json.loads(p.read_text(encoding='utf-8'));rows=json.loads((P/'adjudications-local-note-v03.json').read_text(encoding='utf-8'))
new=[r for r in rows if 264<=r['original_index']<300]
assert [a['candidate_id'] for a,b in zip(old,new) if a!=b]==['v03-local-notes-unresolved-300-01']
s=P/'unsubmitted-snapshots';s.mkdir(exist_ok=True);(s/'part07-before-added-550-anchor.json').write_bytes(p.read_bytes())
p.write_text(json.dumps(new,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(hashlib.sha256(p.read_bytes()).hexdigest())
