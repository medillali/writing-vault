import pathlib,json,hashlib,collections,sys
sys.stdout.reconfigure(encoding='utf-8');P=pathlib.Path(__file__).parent;A=P.parent
for name in ['local-question-pool.json','historical-question-pool.json']:
 x=json.loads((A/name).read_text(encoding='utf-8'))
 print(name,'keys',list(x) if isinstance(x,dict) else 'array')
 if isinstance(x,dict):
  for k,v in x.items():
   if isinstance(v,list):print('list',k,len(v));
   elif isinstance(v,dict):print('object',k,list(v)[:12])
   else:print(k,str(v)[:180])
  rows=x.get('candidates',x.get('questions',[]))
 else:rows=x
 print('volumes',dict(collections.Counter(r.get('volume') for r in rows)))
 print('first',json.dumps(next((r for r in rows if r.get('volume')==2),{}),ensure_ascii=False))
