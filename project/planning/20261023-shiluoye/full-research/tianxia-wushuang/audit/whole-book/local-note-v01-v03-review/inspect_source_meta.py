import json,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');B=Path(__file__).parents[3]
d=json.loads((B/'source.json').read_text(encoding='utf-8'))
print(type(d).__name__,list(d) if isinstance(d,dict) else len(d))
for k,v in d.items():
 if isinstance(v,(str,int,bool)):print(k,str(v)[:500])
 elif isinstance(v,list):print(k,'list',len(v),'first',json.dumps(v[:1],ensure_ascii=False)[:1200])
 elif isinstance(v,dict):print(k,list(v)[:20])
