import json,copy,hashlib
from audit_evidence import H,render_characters
x=json.loads((H/'character-wenhen-leadership-proposal.json').read_text(encoding='utf-8'));p=H/x['path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==x['input_sha256']
before=json.loads(p.read_text(encoding='utf-8'));after=copy.deepcopy(before);i=next(i for i,r in enumerate(after['characters']) if r['audit_id']==x['audit_id']);assert after['characters'][i]==x['before'];after['characters'][i]=x['after'];assert all(a==b for n,(a,b) in enumerate(zip(before['characters'],after['characters'])) if n!=i)
(H/'reviewed-batches/character-arcs-part09-before-wenhen-leadership.json').write_bytes(p.read_bytes());p.write_text(json.dumps(after,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');render_characters(p.with_suffix('.md').name,after['characters'],after['title'])
x.update(status='applied_after_primary_semantic_approval',after_sha256=hashlib.sha256(p.read_bytes()).hexdigest());(H/'character-wenhen-leadership-delta.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(x['after_sha256'])
# 105提案内容不变，只有整组输入SHA因107已批准修改而跟随。
q=H/'character-yutong-admission-scene-proposal.json';proposal=json.loads(q.read_text(encoding='utf-8'));row=next(r for r in after['characters'] if r['audit_id']==proposal['audit_id']);assert row==proposal['before'];old=proposal['input_sha256'];proposal['input_sha256']=x['after_sha256'];q.write_text(json.dumps(proposal,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
log=dict(status='metadata_only_proposal_rebase',proposal=q.name,before_input_sha256=old,after_input_sha256=proposal['input_sha256'],before_after_semantic_objects_unchanged=True,reason='107独立获批合入，105当前原对象逐值未变；本105提案尚未实施。')
(H/'character-yutong-admission-proposal-rebase.json').write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('105 proposal SHA',hashlib.sha256(q.read_bytes()).hexdigest())
