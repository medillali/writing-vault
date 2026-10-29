"""机械保全全部历史/本地候选；不预判终点，不改正式研究。"""
import json,pathlib,hashlib,sys,re,copy,collections
sys.stdout.reconfigure(encoding='utf-8');H=pathlib.Path(__file__).resolve().parent;B=H.parents[1];R=H.parents[5]
read=lambda p:json.loads(p.read_text(encoding='utf-8'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
source=read(B/'source.json');S={c['chapter_id']:c for c in source['chapters']}
def write(n,v):(H/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def refs(record,v,path):
 es=copy.deepcopy(record.get('evidence',[])) if isinstance(record,dict) else []
 if not es and isinstance(record,dict) and record.get('chapter_id') in S:
  c=S[record['chapter_id']];es=[dict(source_id=source['source_id'],revision=source['revision'],chapter_id=c['chapter_id'],start_line=c['start_line'],end_line=c['end_line'],claim_kind='fact')]
 for e in es:
  e.setdefault('claim_kind','fact');e['access_level']='direct-reading-by-this-agent' if v in [5,7] else 'derived-volume-research';e['research_path']=path
 return es
def title(x):
 if isinstance(x,str):return x
 return next((x[k] for k in ['question','title','claim','issue','observation','description'] if isinstance(x.get(k),str)),str(x))
def strings(x):
 if isinstance(x,str):return [x]
 if isinstance(x,list):return [s for item in x for s in strings(item)]
 for k in ['items','issues','original_record','unresolved']:
  if k in x and isinstance(x[k],(list,str)):return strings(x[k])
 for k in ['observation','detail','description','issue','question','claim']:
  if isinstance(x.get(k),str):return [x[k]]
 return [title(x)]
inputs=[];history=[];local=[];local_groups=[];snapshots={}
local_fields=['anomalies','source_anomalies','issue_log','chapter_unresolved_index','unresolved_and_anomalies','local_historical_questions']
for v in range(1,9):
 ap=R/f'writing-vault/library/reports/tianxia-wushuang/vol{v:02d}-analysis.json';gp=ap.with_name(f'vol{v:02d}-graph.json')
 assert ap.is_file() and gp.is_file(),v
 a,g=read(ap),read(gp);assert a['source_id']==source['source_id'] and a['revision']==source['revision']
 ar,gr=ap.relative_to(R).as_posix(),gp.relative_to(R).as_posix();qs=a.get('open_questions',[])
 inputs.append(dict(volume=v,status='formal-library',analysis=ar,graph=gr,analysis_sha256=sha(ap),graph_sha256=sha(gp),open_questions=len(qs),graph_threads=len(g['threads']),reading_ownership=a.get('reading_ownership',a.get('reading_attribution',a.get('reader','见正式分卷/状态')))))
 snapshots[ar]=sha(ap);snapshots[gr]=sha(gp)
 for field,rows,path in [('analysis.open_questions',qs,ar),('graph.threads',g['threads'],gr)]:
  for i,x in enumerate(rows):
   cid=f'v{v:02d}-'+('question' if field.startswith('analysis') else 'thread')+f'-{i+1:03d}'
   history.append(dict(candidate_id=cid,volume=v,entry_type=field,original_path=path,original_index=i,original_stage_status=x.get('status','unknown'),title=title(x),original_record=copy.deepcopy(x),original_evidence=refs(x,v,path),terminal_assessment=dict(status='unknown',review_progress='pending-manual-adjudication',rationale='候选已机械保全，尚未逐项终点判读；此占位不可作为交付。',later_evidence=[])))
 for field in local_fields:
  rows=a.get(field,[])
  assert isinstance(rows,list),(v,field)
  if not rows:continue
  local_groups.append(dict(volume=v,field=field,original_path=ar,original_records=copy.deepcopy(rows)))
  for i,x in enumerate(rows):
   atoms=[]
   for s in strings(x):
    atoms.extend(t.strip(' \n；;') for t in re.split('[；;]',s) if t.strip(' \n；;'))
   if not atoms:atoms=['该原记录没有文本问题；保全空记录边界。']
   for j,atom in enumerate(atoms):
    local.append(dict(candidate_id=f'v{v:02d}-local-{field}-{i+1:03d}-{j+1:02d}',volume=v,original_path=ar,original_field=field,original_index=i,atomic_index=j,original_record=copy.deepcopy(x),title=atom,original_evidence=refs(x,v,ar),terminal_assessment=dict(status='unknown',review_progress='pending-manual-adjudication',rationale='原记录原子项已保全，尚未逐项匹配全书后证；此占位不可作为交付。',later_evidence=[])))
write('historical-question-pool.json',dict(status='candidate_pool_pending_adjudication',method='全收八卷正式open_questions与graph.threads，resolved历史也保；原记录不改，终点另层。',terminal_enums=['answered','partial','unrecovered','unknown'],inputs=inputs,candidates=history,local_issue_records=local_groups))
write('local-question-pool.json',dict(status='candidate_pool_pending_adjudication',scope='八卷正式本地问题/源异常/逐章未决全部保全；按原列表及分号原子化，不把原读者未亲读边界当全书缺卷。',candidates=local))
write('input-inventory.json',dict(source_id=source['source_id'],revision=source['revision'],status='all_eight_formal_inputs_located_pending_field_reading',formal_input_sha256=snapshots,inputs=inputs,counts=dict(historical=len(history),local=len(local),by_volume={v:dict(historical=sum(x['volume']==v for x in history),local=sum(x['volume']==v for x in local)) for v in range(1,9)}),direct_full_reading_by_this_agent=[5,7],not_personal_full_book_rereading=True))
print(json.dumps(dict(status='all_candidates_preserved_not_adjudicated',historical=len(history),local=len(local),local_fields=collections.Counter(x['original_field'] for x in local)),ensure_ascii=False))
