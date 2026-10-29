import json,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
B=Path(__file__).parent.parent;v=int(sys.argv[1]);a=json.loads((B/f'vol{v:02d}'/'analysis.json').read_text(encoding='utf-8'))
def plain(x):
 return x.get('text',x) if isinstance(x,dict) else x
if len(sys.argv)==2:
 print(json.dumps({'keys':list(a),'dimension_keys':{k:list(x[0]) if isinstance(x,list) and x else list(x) for k,x in a['dimensions'].items()}},ensure_ascii=False));raise SystemExit
if sys.argv[2]=='compact':
 selected=sys.argv[3:] or list(a['dimensions'])
 for k in selected:
  vals=a['dimensions'][k]
  print('BEGIN',v,k)
  for i,x in enumerate(vals):
   print(json.dumps(dict(index=i,key=x.get('id',x.get('key',x.get('title'))),title=x.get('title'),fact=plain(x.get('fact')),inference=plain(x.get('inference')),mechanism=plain(x.get('mechanism')),limits=plain(x.get('limits_and_counterevidence')),evidence_chapters=list(dict.fromkeys(e['chapter_id'] for e in x['evidence']))),ensure_ascii=False))
  print('END',v,k)
 raise SystemExit
for k in sys.argv[2:]:
 print('BEGIN',v,k);print(json.dumps(a['dimensions'][k],ensure_ascii=False,indent=2));print('END',v,k)
