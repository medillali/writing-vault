import json,hashlib
from pathlib import Path
D=Path(__file__).resolve().parent;A=D.parent;ROOT=D.parents[6]
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def wr(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
src=rd(A.parents[1]/'source.json');cs={c['chapter_id']:c for c in src['chapters']};p=A/'reader4-character-arcs-part02.json';ac=D/'part02-access-receipt.json';d=rd(p);a=rd(ac);changes=[]
for r in d['characters']:
 for e in r['evidence']:
  c=cs[e['chapter_id']];old=[e['start_line'],e['end_line']];new=[max(old[0],c['start_line']),min(old[1],c['end_line'])]
  if old!=new:
   changes.append({'audit_id':r['audit_id'],'chapter_id':e['chapter_id'],'before':old,'after':new});e['start_line'],e['end_line']=new
for e in a['limited_source_ranges']:
 c=cs[e['chapter_id']];e['start_line']=max(e['start_line'],c['start_line']);e['end_line']=min(e['end_line'],c['end_line'])
wr(ac,a)
for r in d['characters']:
 for e in r['evidence']:
  if e.get('research_path')==ac.relative_to(ROOT).as_posix():e['research_sha256']=sha(ac)
d['formal_input_sha256'][ac.relative_to(ROOT).as_posix()]=sha(ac);wr(p,d)
wr(D/'part02-unsubmitted-reference-boundary-completion.json',{'literary_fields_unchanged':True,'changes':changes,'final_sha256':sha(p)});print(sha(p))
