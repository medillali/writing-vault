import json,hashlib,copy
from audit_evidence import H
src=H/'local-v06-review/note-1117-mother-attribution-overlay-proposal.json'
digest=hashlib.sha256(src.read_bytes()).hexdigest();assert digest=='8f7445ae63c1281d843c00f5729d159eb1d9354acb2a2e1c4a2871968f73a83b'
original=json.loads(src.read_text(encoding='utf-8'));out=copy.deepcopy(original)
out['primary_approval']=dict(reviewer='primary',user_approval=False,proposal_sha=digest,proposal_path=src.relative_to(H).as_posix(),status='approved-for-library-reading-overlay',approval_scope='只批准单一逻辑facts[0]的读者纠正叠加，四历史副本原样保留；不改现签4130候选/115人物/30重点。',full_text_verification=dict(reader='primary',chapter_id='ch-1117',start_line=90388,end_line=90480,complete_full_raw_read=True,attribution='root明确报告已BEGIN-END实际全文核对；本组装代理只阅读完整提案，不冒认该次原章回读。'))
out['approval_precedence']='原status保留提案历史状态；当前读者解释以primary_approval.status及proposed_corrected_fact为优先，未就地应用或覆盖任何原notes。'
assert all(out[k]==v for k,v in original.items())
p=H/'priority-corrections-delta.json';assert not p.exists();p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
proposal=json.loads((H/'assembler-priority-entry-change-proposal.json').read_text(encoding='utf-8'));script=H/'assemble_signed_batches.py';before=script.read_text(encoding='utf-8');assert hashlib.sha256(script.read_bytes()).hexdigest()==proposal['input_sha256'];after=before
for c in proposal['changes']:
 assert after.count(c['before'])==1;after=after.replace(c['before'],c['after'])
script.write_text(after,encoding='utf-8')
delta=dict(status='applied_after_primary_explicit_pure_link_authorization',before_sha256=proposal['input_sha256'],after_sha256=hashlib.sha256(script.read_bytes()).hexdigest(),changes=proposal['changes'],core_assembly_and_signed_semantics_unchanged=True,priority_overlay_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),approval='root明确允许仅handoff/report纯链接直接修改并总装；现有*-delta.json通配冻结该overlay。')
(H/'assembler-priority-entry-change-delta.json').write_text(json.dumps(delta,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
log=H/'research-interface-read-log.json';x=json.loads(log.read_text(encoding='utf-8'));x.setdefault('targeted_interfaces',[]).append(dict(path=src.relative_to(H).as_posix(),interface='complete-correction-proposal-before-after-and-source-attribution-read',scope='本代理完整读取1117纠正提案、四指针和before/after；原章本轮全文回读归agent5及primary，不计本代理亲读。'));log.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('overlay',delta['priority_overlay_sha256'],'assembler',delta['after_sha256'])
