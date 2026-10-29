import json,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
R=Path(__file__).parent;root=R.parents[4];formal=root/'writing-vault/library/reports/zongheng-tianxia'
for v in range(1,9):
 if len(sys.argv)>1 and v not in [int(x) for x in sys.argv[1:]]:continue
 a=formal/f'vol{v:02}-analysis.json';g=formal/f'vol{v:02}-graph.json'
 if not a.exists():a=R.parent/f'vol{v:02}'/'analysis.json';g=R.parent/f'vol{v:02}'/'graph.json'
 if not a.exists():print('V',v,'pending');continue
 A=json.loads(a.read_text(encoding='utf-8'));G=json.loads(g.read_text(encoding='utf-8'))
 print('V',v,'keys',list(A))
 for k in ['open_questions','unresolved_questions','unresolved','pending_questions','unresolved_and_anomalies']:
  if k in A:
   val=A[k]
   if isinstance(val,dict):val=[dict(key=kk,value=vv) for kk,vv in val.items()]
   for j,x in enumerate(val):
    if isinstance(x,dict):print(k,j+1,x.get('question',x.get('claim',x.get('issue',x.get('title',x.get('summary',str(x)))))),x.get('status'))
    else:print(k,j+1,str(x))
 for x in G['threads']:print('T',x['id'],x['title'],x['status'],x.get('resolution_note',x.get('stage_note','')))
