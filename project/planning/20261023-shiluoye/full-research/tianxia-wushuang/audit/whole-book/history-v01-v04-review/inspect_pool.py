import json,sys,hashlib,collections
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');P=Path(__file__).parent;A=P.parent
def R(n):return json.loads((A/n).read_text(encoding='utf-8'))
for name in ['historical-question-pool.json','adjudications-history-closed-early.json','adjudications-history-closed-middle.json']:
 a=R(name)
 print(json.dumps(dict(file=name,sha256=hashlib.sha256((A/name).read_bytes()).hexdigest(),top_keys=list(a) if isinstance(a,dict) else 'list'),ensure_ascii=False))
 if isinstance(a,dict):
  for k,x in a.items():
   if isinstance(x,list):print(json.dumps(dict(field=k,count=len(x),sample=x[:1]),ensure_ascii=False))
