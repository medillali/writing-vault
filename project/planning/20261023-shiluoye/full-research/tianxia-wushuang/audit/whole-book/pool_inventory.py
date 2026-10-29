import pathlib,json,sys
sys.stdout.reconfigure(encoding='utf-8');H=pathlib.Path(__file__).resolve().parent;B=H.parents[1];R=H.parents[5]
def clean(x):
 if isinstance(x,dict):return {k:clean(v) for k,v in x.items() if k not in ['evidence','source_id','revision']}
 if isinstance(x,list):return [clean(v) for v in x]
 return x
for v in range(1,9):
 p=R/f'writing-vault/library/reports/tianxia-wushuang/vol{v:02d}-analysis.json'
 if not p.exists():p=B/f'vol{v:02d}/analysis.json'
 a=json.loads(p.read_text(encoding='utf-8'));print('VOLUME',v)
 for k in ['anomalies','source_anomalies','issue_log','chapter_unresolved_index','unresolved_and_anomalies','local_historical_questions','threads','thread_states','plotline_states']:
  if k in a:
   val=a[k];print(k,type(val).__name__,len(val))
   if isinstance(val,list):print(json.dumps(clean(val[0]) if val else [],ensure_ascii=False))
   elif isinstance(val,dict):print(json.dumps({kk:dict(type=type(vv).__name__,count=len(vv) if hasattr(vv,'__len__') else 0,sample=clean(vv[0]) if isinstance(vv,list) and vv else clean(vv) if not isinstance(vv,list) else []) for kk,vv in val.items()},ensure_ascii=False))
