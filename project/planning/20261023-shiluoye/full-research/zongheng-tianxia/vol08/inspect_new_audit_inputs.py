import json,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
R=Path(__file__).parent
for v in [int(x) for x in sys.argv[1:]] or [6,7]:
 p=R.parent/f'vol{v:02}'/'analysis.json'
 A=json.loads(p.read_text(encoding='utf-8'))
 print('VOLUME',v)
 for field in ['unresolved_and_anomalies','unresolved_and_source_issues']:
  if field in A:
   print('FIELD',field)
   for j,x in enumerate(A[field],1):
    y={k:val for k,val in x.items() if k not in ['evidence','review_action']}
    y['chapters']=[e['chapter_id'] for e in x.get('evidence',[])]
    print(j,json.dumps(y,ensure_ascii=False))
 G=json.loads((p.parent/'graph.json').read_text(encoding='utf-8'))
 for t in G['threads']:
  print('THREAD',json.dumps({k:t[k] for k in ['id','title','status','stage_note','resolution_note'] if k in t},ensure_ascii=False))
