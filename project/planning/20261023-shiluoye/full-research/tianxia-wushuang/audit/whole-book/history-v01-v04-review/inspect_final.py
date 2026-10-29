import json,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
P=Path(__file__).parent;A=P.parent;B=A.parents[1]
for f in ['candidate-id-freeze.json','historical-question-pool.json','adjudications-history-closed-early.json','adjudications-history-closed-middle.json']:
 d=json.loads((A/f).read_text(encoding='utf-8'))
 print(f, type(d).__name__,list(d) if isinstance(d,dict) else len(d))
 if f=='candidate-id-freeze.json':print(json.dumps({k:{a:b for a,b in v.items() if a!='ids'} if isinstance(v,dict) else v for k,v in d.items()},ensure_ascii=False,indent=2))
 elif isinstance(d,dict):
  for k,v in d.items():
   if isinstance(v,list) and v and k in ['candidates','inputs']: print('SAMPLE',k,json.dumps(v[0],ensure_ascii=False))
print('FILES', '\n'.join(x.name for x in A.iterdir()))
