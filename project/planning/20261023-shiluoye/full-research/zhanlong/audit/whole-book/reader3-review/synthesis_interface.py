from common import ROOT,P,B,dump,sha
import json,sys
F=ROOT/'writing-vault/library/reports/zhanlong'
if sys.argv[1]=='schema':
 w=json.loads((B.parent/'tianxia-wushuang/book-synthesis-draft.json').read_text(encoding='utf-8'))
 print('TOP',list(w));print(json.dumps({k:w[k] for k in w if k not in ['dimensions','upstream_documents']},ensure_ascii=False,indent=2)[:13000])
 print('UPSTREAM',json.dumps(w['upstream_documents'][:1],ensure_ascii=False,indent=2))
 print('DIMKEYS',list(w['dimensions']) if isinstance(w['dimensions'],dict) else [list(x) for x in w['dimensions'][:1]])
 print('FIRST',json.dumps(next(iter(w['dimensions'].values())) if isinstance(w['dimensions'],dict) else w['dimensions'][0],ensure_ascii=False,indent=2)[:18000])
elif sys.argv[1]=='meta':
 for n in range(1,7):
  a=json.loads((F/f'vol{n:02d}-analysis.json').read_text(encoding='utf-8'));d=a['dimensions'];print(n,[(k,len(v)) for k,v in d.items()],[(k,len(json.dumps(v,ensure_ascii=False))) for k,v in d.items()])
elif sys.argv[1]=='read':
 n=int(sys.argv[2]);keys=sys.argv[3:];a=json.loads((F/f'vol{n:02d}-analysis.json').read_text(encoding='utf-8'))
 for k in keys:
  print('BEGIN',n,k)
  for i,x in enumerate(a['dimensions'][k]):print(i+1,json.dumps(x,ensure_ascii=False))
  print('END',n,k)
elif sys.argv[1]=='compact':
 n=int(sys.argv[2]);keys=sys.argv[3:];a=json.loads((F/f'vol{n:02d}-analysis.json').read_text(encoding='utf-8'))
 def compact_nested(v):
  if isinstance(v,list):
   if v and isinstance(v[0],dict) and 'chapter_id' in v[0]:return [f"{e['chapter_id']} L{e['start_line']}-{e['end_line']} {e.get('claim_kind','')}" for e in v]
   return [compact_nested(x) for x in v]
  if isinstance(v,dict):return {k:compact_nested(x) for k,x in v.items()}
  return v
 for k in keys:
  print('BEGIN ALL SEMANTIC FIELDS',n,k)
  for i,x in enumerate(a['dimensions'][k]):
   out={}
   for field,value in x.items():
    if field=='interpretation_evidence' and [(e['chapter_id'],e['start_line'],e['end_line']) for e in value]==[(e['chapter_id'],e['start_line'],e['end_line']) for e in x.get('evidence',[])]:
     out[field]='同evidence定位，claim_kind=inference';continue
    if isinstance(value,list) and value and isinstance(value[0],dict) and 'chapter_id' in value[0]:
     out[field]=[f"{e['chapter_id']} L{e['start_line']}-{e['end_line']} {e.get('claim_kind','')}" for e in value]
    else:out[field]=compact_nested(value)
   print(i+1,json.dumps(out,ensure_ascii=False))
  print('END ALL SEMANTIC FIELDS',n,k)
elif sys.argv[1]=='mark':
 n=int(sys.argv[2]);keys=sys.argv[3:];f=F/f'vol{n:02d}-analysis.json';p=P/'synthesis-material-read-log.json'
 log=json.loads(p.read_text(encoding='utf-8')) if p.exists() else {'boundary':'研究材料全部语义栏读取，证据定位去重展示，不冒原文重读；来源只最终formal。','sections':[]}
 for k in keys:
  assert not any(x['volume']==n and x['dimension']==k for x in log['sections'])
  log['sections'].append({'volume':n,'dimension':k,'path':str(f.relative_to(ROOT)).replace('\\','/'),'sha256':sha(f),'all_semantic_fields_read':True,'locator_display':'同组解释证据同定位时只展示一次，非省略语义观察'})
 dump(p,log);print(len(log['sections']))
elif sys.argv[1]=='rowkeys':
 w=json.loads((B.parent/'tianxia-wushuang/book-synthesis-draft.json').read_text(encoding='utf-8'))
 r=w['dimensions']['worldbuilding'][0]
 print(list(r));print(json.dumps({k:v for k,v in r.items() if k not in ['evidence','supporting_observations']},ensure_ascii=False,indent=2))
