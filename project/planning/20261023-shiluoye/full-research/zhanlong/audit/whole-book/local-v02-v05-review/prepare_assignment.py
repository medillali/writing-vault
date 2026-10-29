"""只固定本代理终审输入和ID，不生成任何终点判断。"""
import pathlib,json,hashlib,collections,sys,datetime
sys.stdout.reconfigure(encoding='utf-8');P=pathlib.Path(__file__).resolve().parent;A=P.parent;B=A.parents[1];ROOT=B.parents[3]
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def save(n,x):(P/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert not (P/'input-receipt.json').exists()
F=ROOT/'writing-vault/library/reports/zhanlong';pool=read(A/'local-question-pool.json');hist=read(A/'historical-question-pool.json');assert not pool['pending_inputs'] and not hist['pending_inputs']
assigned=[x for x in pool['candidates'] if x['volume'] in [2,5]]
inputs={}
for v in range(1,7):
 for suffix in ['analysis.json','cards.json','graph.json','chapter-notes.jsonl','handoff.md','.md']:
  file=F/(f'vol{v:02d}'+suffix if suffix=='.md' else f'vol{v:02d}-'+suffix);assert file.exists();inputs[str(file.relative_to(ROOT)).replace('\\','/')]=h(file)
for name in ['vol02-primary-corrections.json','vol03-note-corrections.json','vol06-primary-review-applied-delta.json','vol05-primary-review-merged-delta.json']:
 file=F/name;inputs[str(file.relative_to(ROOT)).replace('\\','/')]=h(file)
source=B/'source.json';assert source.exists()
save('input-receipt.json',dict(status='inputs-fixed-before-manual-adjudication',source_id=pool['source_id'],reviewer='/root/zongheng_vol04_full',pool_sha256={'local-question-pool.json':h(A/'local-question-pool.json'),'historical-question-pool.json':h(A/'historical-question-pool.json')},workflow_sha256=h(A/'WORKFLOW.md'),source_sha256=h(source),formal_input_sha256=inputs,assigned_counts=dict(collections.Counter(x['volume'] for x in assigned)),total_assigned=len(assigned),reading_attribution='卷二raw252—404本人原文/405—504 primary原文且本人完整派生；卷五本人全卷原文。其他卷只读正式派生或另列定向原文，绝不冒个人全书全文。',meaning='文件哈希固定不代表语义已读或终点评定已完成。'))
save('assigned-candidate-id-freeze.json',dict(status='assignment-id-snapshot-not-pool-mutation',pool_sha256=h(A/'local-question-pool.json'),volumes={str(v):[x['candidate_id'] for x in assigned if x['volume']==v] for v in [2,5]},candidate_record_sha256={x['candidate_id']:hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True).encode('utf-8')).hexdigest() for x in assigned}))
save('reader-state.json',dict(status='terminal-audit-in-progress',assigned_counts=dict(collections.Counter(x['volume'] for x in assigned)),adjudicated_ids=[],submitted_batches=[],current_volume=2,next_offset=0,focused_cross_review='not-started',complete=False))
print(json.dumps(dict(formal_files=len(inputs),assigned=dict(collections.Counter(x['volume'] for x in assigned)),total=len(assigned),receipt_sha256=h(P/'input-receipt.json')),ensure_ascii=False))
