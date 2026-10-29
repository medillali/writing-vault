import json,hashlib
from audit_evidence import H
p=H/'assemble_signed_batches.py';code=p.read_text(encoding='utf-8')
prefix='先读[核源纠正叠加](priority-corrections-delta.json)：旧notes与旧正式派生的受影响文字以此叠加为解释优先，原件作为历史输入保留；不回写冻结分卷、不改变已签候选/研究结论。\\n\\n'
changes=[]
for filename in ['whole-book-audit-handoff.md','whole-book-audit-report.md']:
 before=f" output_text('{filename}','\\n'.join(lines))"
 after=f" output_text('{filename}','{prefix}'+'\\n'.join(lines))"
 assert code.count(before)==1
 changes.append(dict(target=filename,before=before,after=after))
out=dict(status='proposal_pending_primary_review_no_assembler_change',input_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),changes=changes,freeze_behavior='priority-corrections-delta.json沿用现有根*-delta.json通配加入audit_sha256，无需改核心组装/语义比对逻辑。仅在root核定overlay后原样复制该正式叠加。')
(H/'assembler-priority-entry-change-proposal.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(out['input_sha256'])
