import sys,json,hashlib
from pathlib import Path
D=Path(__file__).resolve().parent;A=D.parent;ROOT=D.parents[6];F=ROOT/'writing-vault/library/reports/zhanlong'
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def wr(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
data=rd(D/sys.argv[1]);n=data['group'];p=A/f'reader4-character-arcs-part{n:02}.json';ac=D/f'part{n:02}-access-receipt.json';m=p.with_suffix('.md');b=D/f'unsubmitted-part{n:02}-before-evidence-completion';b.mkdir(exist_ok=False)
for f in [p,ac,m]:(b/f.name).write_bytes(f.read_bytes())
d=rd(p);acc=rd(ac);notes={};paths={}
for v in range(1,7):
 np=F/f'vol{v:02}-chapter-notes.jsonl'
 for s in np.read_text(encoding='utf-8-sig').splitlines():
  row=json.loads(s);notes[row['chapter_id']]=row;paths[row['chapter_id']]=np
for addition in data['additions']:
 row=next(x for x in d['characters'] if x['audit_id']==addition['audit_id'])
 for ch in addition.get('notes',[]):
  cid=f'ch-{ch:04}';nt=notes[cid];np=paths[cid];d['formal_input_sha256'][np.relative_to(ROOT).as_posix()]=sha(np);acc['formal_note_rows_complete'].append(ch)
  row['evidence'].append(dict(source_id=d['source_id'],revision=d['revision'],chapter_id=cid,start_line=nt['start_line'],end_line=nt['end_line'],claim_kind='fact',access_level='derived-formal-four-column-note',research_path=np.relative_to(ROOT).as_posix(),research_sha256=sha(np),original_reader=nt['reader']))
 for ch,a,z in addition.get('limited_ranges',[]):
  cid=f'ch-{ch:04}';acc['limited_source_ranges'].append(dict(chapter_id=cid,start_line=a,end_line=z,actual_reader='/root/zongheng_vol04_full',access_scope='targeted-limited-source-excerpt-not-full-chapter',additional_unique_chapters=0));row['evidence'].append(dict(source_id=d['source_id'],revision=d['revision'],chapter_id=cid,start_line=a,end_line=z,claim_kind='fact',access_level='targeted-limited-source-excerpt-not-full-chapter',research_path=ac.relative_to(ROOT).as_posix(),original_reader=notes[cid]['reader']))
wr(ac,acc)
for row in d['characters']:
 for e in row['evidence']:
  if e.get('research_path')==ac.relative_to(ROOT).as_posix():e['research_sha256']=sha(ac)
d['additional_support_sha256'][ac.relative_to(ROOT).as_posix()]=sha(ac);wr(p,d)
m.write_text(m.read_text(encoding='utf-8')+'\n提交前精定位补齐（文学字段不变）：'+json.dumps(data['additions'],ensure_ascii=False)+'\n',encoding='utf-8')
wr(D/f'part{n:02}-evidence-completion-delta.json',{'before_sha256':sha(b/p.name),'after_sha256':sha(p),'literary_fields_unchanged':True,'additions':data['additions']});print(sha(p))
