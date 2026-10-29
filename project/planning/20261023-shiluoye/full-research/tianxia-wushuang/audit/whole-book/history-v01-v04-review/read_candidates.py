import json,sys,hashlib
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');P=Path(__file__).parent;A=P.parent
R=lambda n:json.loads((A/n).read_text(encoding='utf-8'))
pool=R('historical-question-pool.json');mode=sys.argv[1]
if mode=='closed':
 for name in ['adjudications-history-closed-early.json','adjudications-history-closed-middle.json']:
  rows=[x for x in R(name) if int(x['candidate_id'][1:3])<=4]
  print('BEGIN',name,len(rows))
  for x in rows:print(json.dumps(x,ensure_ascii=False))
  print('END',name)
elif mode in ['volume','compact']:
 v=int(sys.argv[2]);rows=[x for x in pool['candidates'] if x['volume']==v]
 print('BEGIN VOLUME',v,len(rows))
 for x in rows:
  y={k:x[k] for k in ['candidate_id','volume','entry_type','original_stage_status','title','original_record']}
  if mode=='compact':
   y['original_record']={k:z for k,z in x['original_record'].items() if k not in ['evidence','resolution_evidence','node_ids','edge_ids']}
   y['original_evidence_chapters']=list(dict.fromkeys(e['chapter_id'] for e in x['original_evidence']))
  print(json.dumps(y,ensure_ascii=False))
 print('END VOLUME',v)
elif mode=='ids':
 closed=[x['candidate_id'] for name in ['adjudications-history-closed-early.json','adjudications-history-closed-middle.json'] for x in R(name) if int(x['candidate_id'][1:3])<=4]
 rows=[x for x in pool['candidates'] if x['volume']<=4]
 for x in rows:print(x['candidate_id'],('EXISTING' if x['candidate_id'] in closed else 'NEW'),x['title'])
 print('TOTAL',len(rows),'EXISTING',len(closed),'NEW',len(rows)-len(closed))
