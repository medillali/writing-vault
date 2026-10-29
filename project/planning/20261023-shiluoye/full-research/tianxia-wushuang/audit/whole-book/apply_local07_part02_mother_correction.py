import hashlib,json
from audit_evidence import H
proposal=json.loads((H/'local07-part02-mother-correction-proposal.json').read_text(encoding='utf-8'))
p=H/'adjudications-local-v07-part02.json';raw=p.read_bytes();assert hashlib.sha256(raw).hexdigest()==proposal['signed_batch_sha256']
d=json.loads(raw);i=next(i for i,x in enumerate(d) if x['candidate_id']==proposal['candidate_id']);assert d[i]==proposal['before'];d[i]=proposal['after']
(H/'reviewed-batches'/'adjudications-local-v07-part02-before-mother-scope-correction.json').write_bytes(raw)
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');sha=hashlib.sha256(p.read_bytes()).hexdigest()
(H/'local07-part02-mother-correction-delta.json').write_text(json.dumps(dict(status='primary_approved_targeted_correction_applied_pending_new_signature',candidate_id=proposal['candidate_id'],before_sha256=proposal['signed_batch_sha256'],after_sha256=sha,before=proposal['before'],after=proposal['after'],unchanged_other_items=59),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
md=H/'local-v07-reviewed-part02.md';text=md.read_text(encoding='utf-8').replace(proposal['before']['rationale'],proposal['after']['rationale']).replace('后证raw：'+', '.join(map(str,proposal['before']['later_chapters'])),'后证raw：'+', '.join(map(str,proposal['after']['later_chapters'])))
md.write_text(text,encoding='utf-8');print(sha)
