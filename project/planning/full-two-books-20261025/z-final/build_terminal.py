from pathlib import Path
import json,sys
sys.stdout.reconfigure(encoding='utf-8')
P=Path(__file__).parent
inv=json.loads((P/'integration-inventory.json').read_text(encoding='utf-8'))
validation=json.loads((P/'integration-validation.json').read_text(encoding='utf-8'))
over={q['key']:q for q in json.loads((P/'terminal-overrides.json').read_text(encoding='utf-8'))['items']}
items=[]
for k,history in inv['questions'].items():
 q=max(history,key=lambda q:q['through'])
 if k in over:row=over[k]
 else:
  status=q['status']
  if status in ('open','anomaly'):
   status='unknown';answer='在本次全文分段研究中未见本问题更明确的后续结算；最新有据阶段记录：'+q['answer']
  else:answer=q['answer']
  ev=q.get('setup_evidence',[])+q.get('resolution_evidence',[])
  ev=list({(e['chapter_id'],e['start_line'],e['end_line']):e for e in ev}.values())
  row={'key':k,'final_status':status,'answer':answer,'evidence':ev}
 items.append(row)
name='terminal-question-map.json' if not validation['missing_units'] and not validation['evidence_errors'] and validation['unit_count']==463 else 'terminal-question-map.provisional.json'
(P/name).write_text(json.dumps({'source_key':'z','items':items},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(name,len(items),'unique keys')
