import json,hashlib
from pathlib import Path
D=Path(__file__).resolve().parent;A=D.parent;ROOT=D.parents[6]
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def wr(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
dest=A/'reader4-character-arcs-part02.json';md=dest.with_suffix('.md');access=D/'part02-access-receipt.json';archive=D/'unsubmitted-part02-before-ref-completion';archive.mkdir(exist_ok=True)
for p in [dest,md,access]:(archive/p.name).write_bytes(p.read_bytes())
d=rd(dest);acc=rd(access)
for aid,ch,a,b in [('character-arc-r4-007',1265,91548,91554),('character-arc-r4-012',1282,92786,92794)]:
 row=next(x for x in d['characters'] if x['audit_id']==aid);n=next(json.loads(s) for s in (ROOT/'writing-vault/library/reports/zhanlong/vol06-chapter-notes.jsonl').read_text(encoding='utf-8-sig').splitlines() if json.loads(s)['chapter_id']==f'ch-{ch:04}')
 row['evidence'].append({'source_id':d['source_id'],'revision':d['revision'],'chapter_id':f'ch-{ch:04}','start_line':a,'end_line':b,'claim_kind':'fact','access_level':'targeted-limited-source-excerpt-not-full-chapter','research_path':access.relative_to(ROOT).as_posix(),'original_reader':n['reader']})
 acc['limited_source_ranges'].append({'chapter_id':f'ch-{ch:04}','start_line':a,'end_line':b,'actual_reader':'/root/zongheng_vol04_full','access_scope':'targeted-limited-source-excerpt-not-full-chapter','additional_unique_chapters':0})
wr(access,acc)
for row in d['characters']:
 for ref in row['evidence']:
  if ref.get('research_path')==access.relative_to(ROOT).as_posix():ref['research_sha256']=sha(access)
d['formal_input_sha256'][access.relative_to(ROOT).as_posix()]=sha(access);wr(dest,d)
md.write_text(md.read_text(encoding='utf-8')+'\n提交前补定位：r4-007 ch-1265 L91548—91554；r4-012 ch-1282 L92786—92794。五项文学字段未改。\n',encoding='utf-8')
print(json.dumps({'sha256':sha(dest),'md_sha256':sha(md),'literary_fields_unchanged':True}))
