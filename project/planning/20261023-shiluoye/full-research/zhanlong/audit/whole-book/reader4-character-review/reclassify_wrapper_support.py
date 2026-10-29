import json,hashlib
from pathlib import Path
D=Path(__file__).resolve().parent;A=D.parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
changes=[]
for n in [1,2]:
 p=A/f'reader4-character-arcs-part{n:02}.json';before=p.read_bytes();d=json.loads(before);oldsha=sha(p);rows=d['characters'];rowbytes=json.dumps(rows,ensure_ascii=False,sort_keys=True)
 moved={k:v for k,v in d['formal_input_sha256'].items() if not k.startswith('writing-vault/')};assert len(moved)==2
 snap=D/f'part{n:02}-before-wrapper-classification.json';assert not snap.exists();snap.write_bytes(before)
 for k in moved:del d['formal_input_sha256'][k]
 d.setdefault('additional_support_sha256',{}).update(moved)
 p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');assert rowbytes==json.dumps(json.loads(p.read_bytes())['characters'],ensure_ascii=False,sort_keys=True)
 changes.append({'part':n,'before_sha256':oldsha,'after_sha256':sha(p),'moved_exact_path_sha':moved,'character_rows_unchanged':True,'md_unchanged_sha256':sha(p.with_suffix('.md'))})
(D/'wrapper-classification-delta.json').write_text(json.dumps({'authorization':'primary explicit metadata-only reclassification','changes':changes},ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(changes,ensure_ascii=False))
