import json,sys
sys.stdout.reconfigure(encoding='utf-8')
from save_manual_batch import A,read,sha
p=A/'priority-corrections-delta.json';x=read(p);print('SHA',sha(p));print('TOP',x['status'],x['primary_approval'])
for i in x['issues']:
 print(json.dumps({k:v for k,v in i.items() if k in ['issue_id','finding','source_evidence','primary_approval','approval_precedence']},ensure_ascii=False))
changes=x.get('changes',[])
seen=set()
for z in changes:
 k=(z.get('issue_id'),z.get('after'))
 if k not in seen:
  seen.add(k);print('CORRECTION',json.dumps({k:v for k,v in z.items() if k in ['issue_id','before','after','evidence','composition_note']},ensure_ascii=False))
