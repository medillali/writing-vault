from save_manual_batch import P,F,read,write,sha
import json,copy
f=P/'adjudications-local-v02-batch012.json';cid='v02-local-chapter_unresolved_index-0103-01';before=next(x for x in read(f) if x['candidate_id']==cid);after=copy.deepcopy(before)
after['rationale']=before['rationale'].replace('843唐实际救回东、1386送别仍在同伴关系中。','843唐实际救回东，1354唐再以毒镖/借钢盾/枪口内射杀A级，后续实际保护职责有证。').replace('不靠强迫恋爱解释适应。','不靠强迫恋爱解释适应，不由东终章拥别倒证唐到场或她与唐恋爱。')
after['later_chapters']=[1354 if k==1386 else k for k in before['later_chapters']]
n=next(json.loads(l) for l in (F/'vol06-chapter-notes.jsonl').read_text(encoding='utf-8').splitlines() if l.strip() and json.loads(l)['chapter_id']=='ch-1354')
e=copy.deepcopy(next(e for e in before['later_evidence'] if e['chapter_id']=='ch-1386'));e.update(chapter_id=n['chapter_id'],start_line=n['start_line'],end_line=n['end_line'],source_reader=n['reader'])
after['later_evidence']=[e if v['chapter_id']=='ch-1386' else v for v in before['later_evidence']]
q=P/'tang-duty-without-final-farewell-proposal.json';assert not q.exists();write(q,dict(status='proposal-pending-primary-review-not-applied',reason='根完整复读1386未点唐；本代理已完整读1354四栏，撤终章到场暗示，改用明确实际职责，非新原文全书阅读。',changes=[dict(path=f.name,candidate_id=cid,input_sha256=sha(f),before=before,after=after,scope='仅此条理由和1386证据替换1354，status/domain/其余19不变')]))
print(sha(q))
