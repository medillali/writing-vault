import json,hashlib,sys
from pathlib import Path
P=Path(__file__).parent;A=P.parent;B=P.parents[2]
load=lambda p:json.loads(p.read_text(encoding='utf-8'))
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
lo,hi=map(int,sys.argv[1:3]);raw=list(map(int,sys.argv[3:]));p=P/'material-read-log.json';log=load(p)
entry={'onebased_start':lo,'onebased_end':hi,'interface':f'read_interfaces.py 5 localcompact {lo-1} {hi}','full_original_record_shown_once_per_group':True}
assert not any(x['onebased_start']==lo and x['onebased_end']==hi for x in log['candidate_interfaces_read'])
log['candidate_interfaces_read'].append(entry)
log['complete_four_field_notes_read']=sorted(set(log['complete_four_field_notes_read'])|set(raw));save(p,log)
m=P/'input-manifest.json'
if not m.exists():
 scope=[c for c in load(A/'local-question-pool.json')['candidates'] if c['volume']==5]
 assert len(scope)==556 and scope[176]['candidate_id']=='v05-local-local_historical_questions-057-01'
 identity=[{k:c[k] for k in ['candidate_id','volume','original_path','original_field','original_index','atomic_index','title','original_record','original_evidence']} for c in scope[177:]]
 canonical=json.dumps(identity,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
 save(m,{'assigned_onebased':[178,556],'count':379,'first_id':identity[0]['candidate_id'],'last_id':identity[-1]['candidate_id'],
 'assigned_identity_sha256':hashlib.sha256(canonical).hexdigest(),
 'local_identity_at_start':load(A/'candidate-id-freeze.json')['local']['candidate_identity_sha256'],
 'notes':[{'volume':v,'path':f'vol{v:02d}/chapter-notes.jsonl','sha256':hashlib.sha256((B/f'vol{v:02d}'/'chapter-notes.jsonl').read_bytes()).hexdigest()} for v in range(1,9)],
 'access':'derivative complete four-field notes; no new source full-text coverage',
 'primary_prefix_excluded':{'onebased':[1,177],'last_id':scope[176]['candidate_id']}})
print(json.dumps({'candidate_interface_ranges':len(log['candidate_interfaces_read']),'complete_notes_logged':len(log['complete_four_field_notes_read'])},ensure_ascii=False))
