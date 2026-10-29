import json,hashlib
from pathlib import Path
D=Path(__file__).resolve().parent;A=D.parent;ROOT=D.parents[6]
def rd(p):return json.loads(p.read_text(encoding='utf-8'))
def wr(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
p=A/'reader4-character-arcs-part02.json';ac=D/'part02-access-receipt.json';d=rd(p);c=rd(ac)
for x in c['limited_source_ranges']:
 if x['chapter_id']=='ch-1282' and x['start_line']==92786:x['end_line']=92790
wr(ac,c)
for r in d['characters']:
 for e in r['evidence']:
  if e['chapter_id']=='ch-1282' and e['start_line']==92786:e['end_line']=92790
  if e.get('research_path')==ac.relative_to(ROOT).as_posix():e['research_sha256']=sha(ac)
d['formal_input_sha256'][ac.relative_to(ROOT).as_posix()]=sha(ac);wr(p,d)
m=p.with_suffix('.md');m.write_text(m.read_text(encoding='utf-8').replace('L92786—92794','L92786—92790'),encoding='utf-8')
print(sha(p));print(sha(m))
