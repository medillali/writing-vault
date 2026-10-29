import json,hashlib,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
D=Path(__file__).resolve().parent;A=D.parent;ROOT=D.parents[6];B=A.parents[1];F=ROOT/'writing-vault/library/reports/zhanlong'
old='御林违令出击被降的具名将领，后守凡书实死。';new='狂雷军违令出击被降的具名将领，后守凡书实死。';aid='chr-36eaf0a80230530c92963612fcccc15f';out=[]
def walk(x,prefix=()):
 if isinstance(x,dict):
  for k,v in x.items():yield from walk(v,prefix+(k,))
 elif isinstance(x,list):
  for k,v in enumerate(x):yield from walk(v,prefix+(k,))
 elif isinstance(x,str) and old in x:yield list(prefix),x
files=[B/'vol05/cards.json',B/'vol05/analysis.json',B/'vol05/report.md',F/'vol05-cards.json',F/'vol05-analysis.json',F/'vol05.md',ROOT/f'writing-vault/library/characters/{aid}.json',ROOT/f'writing-vault/library/views/{aid}.md']
for p in files:
 raw=p.read_bytes();s=raw.decode('utf-8-sig');sha=hashlib.sha256(raw).hexdigest()
 matches=list(walk(json.loads(s))) if p.suffix=='.json' else [(['line',i+1],line) for i,line in enumerate(s.splitlines()) if old in line]
 for path,before in matches:out.append({'path':p.relative_to(ROOT).as_posix(),'sha256':sha,'field_path':path,'before':before,'after':before.replace(old,new),'issue_id':'xuyan-kuanglei-not-yulin-summary'})
proposal={'status':'proposal-not-applied','source_id':'src-20f2d16e3d1b472fa4b230ab0e1770c9','revision':'61ab0b114c76446fda554abfafdac8c432cd88afaba7c2541f4473a3902134e3','actual_reviewer':'/root/zongheng_vol04_full','scope':'只更正真实summary投影中的御林违令；其余起点、死亡、死灵再现、证据与正文笔记一律不改。','affected_fields':out,'evidence':[{'source_id':'src-20f2d16e3d1b472fa4b230ab0e1770c9','revision':'61ab0b114c76446fda554abfafdac8c432cd88afaba7c2541f4473a3902134e3','chapter_id':'ch-1001','start_line':74206,'end_line':74206,'claim_kind':'fact','actual_access':'本人本轮限定原文命中与完整正式四栏接读；非本轮整章重读，原卷五首读仍本人。'},{'source_id':'src-20f2d16e3d1b472fa4b230ab0e1770c9','revision':'61ab0b114c76446fda554abfafdac8c432cd88afaba7c2541f4473a3902134e3','chapter_id':'ch-1067','start_line':78313,'end_line':78377,'claim_kind':'fact','actual_access':'完整正式四栏派生；原卷五首读为本人，未冒本轮重读原章。'}],'original_files_unchanged':True}
p=D/'xuyan-summary-correction-proposal.json';p.write_text(json.dumps(proposal,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({'fields':len(out),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'fields_found':out},ensure_ascii=False))
