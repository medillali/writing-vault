"""机械保留各卷所有open_questions及graph.threads；终点判断需独立人工决策。"""
import json,sys,hashlib
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
R=Path(__file__).parent;ROOT=R.parents[4];FORMAL=ROOT/'writing-vault/library/reports/zongheng-tianxia'
pool=[];inputs=[];local=[]
def textof(x):
 if not isinstance(x,dict):return str(x)
 return next((str(x[k]) for k in ['question','claim','title','text','issue','summary'] if x.get(k)),str(x))
def evs(x):
 if isinstance(x,list):return [e for i in x for e in evs(i)]
 if isinstance(x,dict):
  if {'source_id','revision','chapter_id','start_line','end_line'}.issubset(x):return [x]
  return [e for v in x.values() for e in evs(v)]
 return []
for v in range(1,9):
 pa=FORMAL/f'vol{v:02}-analysis.json';pg=FORMAL/f'vol{v:02}-graph.json';accepted=True
 if not pa.exists():pa=R.parent/f'vol{v:02}'/'analysis.json';pg=R.parent/f'vol{v:02}'/'graph.json';accepted=False
 if not pa.exists() or not pg.exists():inputs.append(dict(volume=v,status='pending-delivery',analysis=None,graph=None));continue
 A=json.loads(pa.read_text(encoding='utf-8'));G=json.loads(pg.read_text(encoding='utf-8'))
 inp=dict(volume=v,status='formal-library' if accepted else 'research-draft',analysis=str(pa.relative_to(ROOT)).replace('\\','/'),graph=str(pg.relative_to(ROOT)).replace('\\','/'),analysis_sha256=hashlib.sha256(pa.read_bytes()).hexdigest(),graph_sha256=hashlib.sha256(pg.read_bytes()).hexdigest())
 q=A.get('open_questions',[])
 if isinstance(q,dict):q=[dict(id=k,**val) if isinstance(val,dict) else dict(id=k,question=val) for k,val in q.items()]
 inp.update(open_questions=len(q),graph_threads=len(G['threads']),open_questions_field_present='open_questions' in A);inputs.append(inp)
 for j,x in enumerate(q,1):
  k=x.get('id',f'{j:03}') if isinstance(x,dict) else f'{j:03}'
  pool.append(dict(candidate_id=f'v{v:02}-question-{k}',volume=v,entry_type='analysis.open_questions',original_path=inp['analysis'],original_index=j-1,original_stage_status=x.get('status') if isinstance(x,dict) else None,title=textof(x),original_record=x,original_evidence=evs(x)))
 nm={n['id']:n for n in G['nodes']};em={e['id']:e for e in G['edges']}
 for j,x in enumerate(G['threads'],1):
  evidence=evs(x) or evs([nm[n] for n in x.get('node_ids',[])]+[em[e] for e in x.get('edge_ids',[])])
  pool.append(dict(candidate_id=f"v{v:02}-thread-{x['id']}",volume=v,entry_type='graph.threads',original_path=inp['graph'],original_index=j-1,original_stage_status=x['status'],title=x['title'],original_record=x,original_evidence=evidence))
 # 地方悬念/异文另存，不混作本卷独立open_questions条数。
 for field in ['unresolved_and_anomalies','unresolved_and_source_issues','anomalies']:
  if field in A:local.append(dict(volume=v,field=field,path=inp['analysis'],original_records=A[field]))
decpath=R/'audit-terminal-decisions.json'
dec=json.loads(decpath.read_text(encoding='utf-8')) if decpath.exists() else {}
for x in pool:
 d=dec.get(x['candidate_id'])
 x['terminal_assessment']=d or dict(status='unknown',review_progress='pending-manual-adjudication',rationale='尚未逐项作终点判断；unknown不表示作者未回收。',later_evidence=[],depends_on_volumes=[])
result=dict(status='draft-ready-for-primary-review' if all(x['status']=='formal-library' for x in inputs) and all(x['candidate_id'] in dec for x in pool) else 'draft-incomplete-inputs-or-adjudication',method='机械全收并保留original_record和卷末状态；终点结论在terminal_assessment另写，不覆盖旧卷。',terminal_enums=dict(answered='问题得到后证回答或目标已有明确结算，失败也是回答',partial='已有结果但复合问题/后续仍未全明',unrecovered='全书证据核毕后确无回收，不能以缺卷或未查代填',unknown='具体证据、来源或认知边界未知，不等未读或作者遗忘；须读audit_domain/review_progress'),inputs=inputs,candidates=pool,local_issue_records=local)
(R/'historical-question-pool.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
lines=['# 全书历史问题与线程候选池（全收草稿）','','保留每个原条目，包括原resolved；终点判定另栏。`unknown/pending-manual-adjudication`不是判作者遗漏。输入区分正式库与待审研究稿，不把派生复核算重新全文阅读。','', '| 候选ID | 原卷末状态 | 历史题目 | 终点状态 | 审查进度 |','|---|---|---|---|---|']
for x in pool:
 d=x['terminal_assessment'];lines.append(f"| {x['candidate_id']} | {x['original_stage_status']} | {x['title'].replace('|','／')} | {d['status']} | {d.get('review_progress','reviewed-draft')} |")
(R/'historical-question-pool.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
for x in pool:print(x['candidate_id'],x['original_stage_status'],x['title'])
print('COUNTS',json.dumps(dict(candidates=len(pool),inputs=inputs),ensure_ascii=False))
