"""仅核已落盘分配覆盖、引用及SHA；不等于primary语义主审。"""
from save_manual_batch import P,A,F,read,write,sha
import json,collections,datetime
state=read(P/'reader-state.json');ids=read(P/'assigned-candidate-id-freeze.json');pool=read(A/'local-question-pool.json');cs={x['candidate_id']:x for x in pool['candidates']};seen=[];stats=collections.Counter();domains=collections.Counter();refs=0
notes={}
for v in range(1,7):
 for line in (F/f'vol{v:02d}-chapter-notes.jsonl').read_text(encoding='utf-8').splitlines():
  if line.strip():
   n=json.loads(line);notes[n['chapter_id']]=n
for b in state['submitted_batches']:
 file=P/b['path'];assert sha(file)==b['sha256'];rows=read(file);assert 0<len(rows)<=20 and len(rows)==b['count']
 for x in rows:
  c=cs[x['candidate_id']];assert x['title']==c['title'] and x['volume']==c['volume'];assert x['original_record_sha256']==ids['candidate_record_sha256'][x['candidate_id']]
  assert x['status'] in ['answered','partial','unknown','unrecovered'] and x['rationale'];assert x['actual_reviewer']=='/root/zongheng_vol04_full'
  assert x['later_chapters']==[int(e['chapter_id'].split('-')[1]) for e in x['later_evidence']]
  for e in x['later_evidence']:
   n=notes[e['chapter_id']];assert all(e[k]==n[k] for k in ['source_id','revision','start_line','end_line']);assert e['claim_kind'] in ['fact','inference'];refs+=1
  seen.append(x['candidate_id']);stats[x['status']]+=1;domains[x['audit_domain']]+=1
assert len(set(seen))==len(seen);assert seen==state['adjudicated_ids'];assert seen==ids['volumes']['2'][:len(seen)] if state['current_volume']==2 else True
out=dict(status='passed-structural-progress-only-not-semantic-review',updated_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),adjudicated=len(seen),assigned=749,remaining=749-len(seen),batch_count=len(state['submitted_batches']),by_status=dict(stats),by_audit_domain=dict(domains),evidence_count=refs,checks=['ID唯一且按固定候选序','原题/原候选hash不改','每批≤20','所有当前批SHA与state一致','后证章号集合与具体引用一致且固定SID/revision/章界正确'],primary_semantic_review='由root实际逐项阅读和签收；本脚本不生成该结论',pool_unchanged=sha(A/'local-question-pool.json')==ids['pool_sha256'])
assert out['pool_unchanged'];write(P/'progress-validation.json',out);print(json.dumps(out,ensure_ascii=False))
