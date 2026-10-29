import json,pathlib,sys
sys.stdout.reconfigure(encoding='utf-8')
b=pathlib.Path(__file__).resolve().parent
r=b.parents[3]/'writing-vault/library/reports/zongheng-tianxia'
# 不读取新作品正文；只查本书已完成分卷研究。
def get(v):
 p=r/f'vol{v:02d}-analysis.json'
 if not p.exists():p=b/f'vol{v:02d}/analysis.json'
 return p,json.loads(p.read_text(encoding='utf-8'))
if sys.argv[1]=='coverage':
 for v in range(1,9):
  p=r/f'vol{v:02d}-read-log.json' if v<=5 else b/f'vol{v:02d}/read-log.json'
  a=json.loads(p.read_text(encoding='utf-8'))
  print('VOLUME',v,'KEYS',list(a))
  for k,x in a.items():
   if k in ['reader','reading_method','method','reader_attribution','reader_ranges','reading_ownership','scope','coverage_note']:print(k,str(x)[:2500])
elif sys.argv[1]=='summary':
 for v in range(1,9):
  p,a=get(v);print(v,p, list(a))
  for d,xs in a['dimensions'].items():
   xs=xs if isinstance(xs,list) else xs.get('observations',[])
   print(d,len(xs),[x.get('id',x.get('title',x.get('name',''))) for x in xs])
elif sys.argv[1]=='compact':
 v=int(sys.argv[2]);p,a=get(v)
 def clean(x):
  if isinstance(x,list):return [clean(i) for i in x]
  if isinstance(x,dict):
   if {'source_id','revision','chapter_id'}.issubset(x):return x['chapter_id']
   return {k:clean(z) for k,z in x.items() if k not in ['transfer_question','review_status','limits']}
  return x
 for d,xs in a['dimensions'].items():
  print('DIMENSION',d)
  for i,x in enumerate(xs if isinstance(xs,list) else xs.get('observations',[])):
   print(i,json.dumps(clean(x),ensure_ascii=False))
else:
 v=int(sys.argv[1]); dim=sys.argv[2];p,a=get(v)
 ds=a['dimensions']
 for d in (ds if dim=='all' else [dim]):
  print('DIMENSION',d)
  for x in (ds[d] if isinstance(ds[d],list) else ds[d].get('observations',[])):
   print(json.dumps(x,ensure_ascii=False))
