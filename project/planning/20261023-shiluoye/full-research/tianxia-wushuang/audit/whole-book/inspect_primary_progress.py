import pathlib,json,sys
sys.stdout.reconfigure(encoding='utf-8');H=pathlib.Path(__file__).resolve().parent
p=H.parents[1]/'primary-audit-review-progress.json';d=json.loads(p.read_text(encoding='utf-8'))
print('TOP',list(d))
for k,v in d.items():
 if isinstance(v,list):
  print('LIST',k,len(v))
  for x in v:
   if isinstance(x,dict):print(json.dumps({kk:vv for kk,vv in x.items() if kk in ['path','sha256','count','candidate_count','ids','scope','file','status'] and kk!='ids'},ensure_ascii=False))
 elif not isinstance(v,dict):print(k,v)
