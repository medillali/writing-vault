"""只读检查审计候选完整性、判定枚举与跨卷证据定位；写本目录校验记录。"""
import json,collections,hashlib,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
R=Path(__file__).parent
S=json.loads((R.parent/'source.json').read_text(encoding='utf-8'));cs={c['chapter_id']:c for c in S['chapters']}
files=['historical-question-pool.json','local-question-pool.json','end-state-audit-draft.json','character-arc-audit-draft.json']
all_e=0
def check(x):
 global all_e
 if isinstance(x,list):
  for a in x:check(a)
 elif isinstance(x,dict):
  if {'source_id','revision','chapter_id','start_line','end_line'}.issubset(x):
   assert x['source_id']==S['source_id'] and x['revision']==S['revision'];c=cs[x['chapter_id']]
   assert c['start_line']<=x['start_line']<=x['end_line']<=c['end_line'];assert x.get('claim_kind') in ['fact','inference','plan','synthesis'];all_e+=1
  for a in x.values():check(a)
loaded={f:json.loads((R/f).read_text(encoding='utf-8')) for f in files}
for a in loaded.values():check(a)
history=loaded[files[0]];local=loaded[files[1]]
for p in [history,local]:
 ids=[x['candidate_id'] for x in p['candidates']];assert len(ids)==len(set(ids))
 for x in p['candidates']:
  d=x['terminal_assessment'];assert d['status'] in ['answered','partial','unrecovered','unknown']
  assert d['rationale'] and 'later_evidence' in d
  assert d.get('review_progress') not in ['pending-manual-adjudication','original-issue-read-awaiting-formal-cross-volume-evidence']
  assert not d.get('depends_on_volumes')
assert len(history['candidates'])==sum(x.get('open_questions',0)+x.get('graph_threads',0) for x in history['inputs'])
root=R.parents[4]
for x in history['inputs']:
 assert x['status']=='formal-library',x
 for kind in ['analysis','graph']:
  p=root/x[kind];assert hashlib.sha256(p.read_bytes()).hexdigest()==x[kind+'_sha256'],str(p)
for g in history['local_issue_records']:
 for ri,rec in enumerate(g['original_records']):
  assert any(x['volume']==g['volume'] and x['original_field']==g['field'] and x['original_index']==ri for x in local['candidates']),(g['volume'],g['field'],ri)
counts=lambda p:dict(collections.Counter(x['terminal_assessment']['status'] for x in p['candidates']))
freeze={f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in ['analysis.json','cards.json','graph.json','read-log.json','chapter-notes.jsonl','reader-state.json']}
expected={'analysis.json':'4b625c33a3f9245978473f192751a18f0dc97915839c33fc9b5ae81dd2e33789','cards.json':'178a2c07f46e97186839eb8fff4acd74fae6508d33f13d966886dc3226a3d094','graph.json':'f425822371a1faedfb22ed4d52887d50f49c3763ae3a8918c5f1ca7b4998a94d','read-log.json':'b9aa0c2dc8e45805b8afd7beb77810900234d53c96237850bb2ef353c6379c62','chapter-notes.jsonl':'c634042b6947ef2998328dbbeb509527ab62b0e564f5966ed7bf9e586ad94dc6','reader-state.json':'fb7133662bfe05c86a66259a2adae4e7a8dcc635b0a7b1a5a0132101291eff0e'}
assert freeze==expected,(freeze,expected)
arcs=loaded[files[3]]['characters'];assert len({x['audit_id'] for x in arcs})==len(arcs)
assert arcs[0]['identity_names']['real_name']=='丁舒升'
result=dict(status='draft-audit-structure-passed-ready-for-primary-review',historical_candidates=len(history['candidates']),historical_statuses=counts(history),original_resolved_preserved=sum(x['original_stage_status']=='resolved' for x in history['candidates']),local_candidates=len(local['candidates']),local_statuses=counts(local),local_domains=dict(collections.Counter(x['terminal_assessment'].get('audit_domain','pending') for x in local['candidates'])),character_arcs=len(arcs),focused_findings=len(loaded[files[2]]['findings']),evidence_references_checked=all_e,all_eight_inputs_formal=True,all_original_local_records_represented=True,unadjudicated_candidates=0,pending_inputs=[],nonempty_depends_on_volumes=0,frozen_volume08_unchanged=True,frozen_volume08_hashes=freeze,boundary='结构有效不等所有文学解释通过；不修改冻结卷八核心；不把派生资料查询或定点原行复核算整卷亲读。')
(R/'audit-validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
