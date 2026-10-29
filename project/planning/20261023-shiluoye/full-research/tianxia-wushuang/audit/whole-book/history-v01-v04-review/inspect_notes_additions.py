import json,sys,collections
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');A=Path(__file__).parent.parent
for name in ['notes-unresolved-additions.json','local-note-coverage-check.json']:
 d=json.loads((A/name).read_text(encoding='utf-8'))
 print(name,type(d).__name__, list(d) if isinstance(d,dict) else len(d))
 if isinstance(d,dict):
  for k,v in d.items():
   print(k, json.dumps(v,ensure_ascii=False)[:2500] if not isinstance(v,list) else f'list count={len(v)} sample={json.dumps(v[:1],ensure_ascii=False)}')
pool=json.loads((A/'local-question-pool.json').read_text(encoding='utf-8'))
print('POOLKEYS',list(pool))
arr=pool.get('candidates',[])
for v in [1,3]:
 a=[x for x in arr if x['volume']==v and 'notes-unresolved' in x['candidate_id']]
 print('SCOPE',v,len(a),'FIRSTLAST', [x['candidate_id'] for x in a[:1]+a[-1:]])
 print('SAMPLE',json.dumps(a[:1],ensure_ascii=False,indent=2))
