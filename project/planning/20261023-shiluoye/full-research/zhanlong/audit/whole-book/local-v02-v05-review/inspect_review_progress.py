import sys,json
sys.stdout.reconfigure(encoding='utf-8')
from save_focus_manual import A,B,read
for p in [B/'primary-audit-review-progress.json',B/'primary-research-group-review-progress.json']:
 if not p.exists():continue
 x=read(p);print(p.name,list(x));
 for k,v in x.items():
  if isinstance(v,list):print(k,'len',len(v),'sample',json.dumps(v[-1:] if v else [],ensure_ascii=False))
  elif isinstance(v,dict):print(k,'keys',list(v)[:8])
  else:print(k,v)
