from pathlib import Path
import json,hashlib,sys
sys.stdout.reconfigure(encoding='utf-8')
A=Path(__file__).resolve().parent.parent;p=A/'character-arcs-part06.json';m=p.with_suffix('.md');d=json.loads(p.read_text(encoding='utf-8'));key='.planning/20261023-shiluoye/full-research/zhanlong/audit/whole-book/local-question-pool.json';val=d['formal_input_sha256'][key]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(p)=='1db6a17252d8e0fb164dd20c16ae3184077f7fc66ae6825c60dbcaa949e74714'
out=dict(status='proposal_pending_primary_not_applied',scope='仅wrapper依赖分类，不删依赖、不改人物/MD/其他wrapper',input_sha256={p.name:sha(p),m.name:sha(m)},changes=[dict(operation='move_key_same_path_same_sha256',from_path=['formal_input_sha256',key],to_path=['additional_support_sha256',key],before=val,proposed_after=val)],rationale='formal_input供可恢复正式文件验收，stage池为当时派生支持快照；同键同SHA迁到additional_support，保历史证据而不要求恢复时旧planning树存在。')
q=A/'character-arcs-part06-support-classification-proposal.json';q.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');q.with_suffix('.md').write_text('# 人物06依赖分类最小提案\n\n不改人物行或MD；仅将formal_input_sha256中的 '+key+' = '+val+' 移到additional_support_sha256，路径与SHA保持，依赖不删除。旧JSON SHA '+sha(p)+'。\n',encoding='utf-8');print(json.dumps(dict(proposal_sha256=sha(q),md_sha256=sha(q.with_suffix('.md')),changes=out['changes']),ensure_ascii=False,indent=2))
