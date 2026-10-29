"""保存阶段审计问题结构；这些是待核点而非已判定错误。"""
import json,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
P=Path(__file__).parent;B=P.parent
R=lambda p:json.loads(p.read_text(encoding='utf-8'))
rows=R(P/'audit-seed.json')
for row in rows:
 refs=[]
 for v,d,i in row.pop('sources'):
  a=R(B/f'vol{v:02d}'/'analysis.json');s=R(B/f'vol{v:02d}'/'reader-state.json');obs=a['dimensions'][d][i]
  refs.append(dict(volume=v,reader=s['reader'],material=(B/f'vol{v:02d}'/'analysis.json').resolve().as_posix(),field=f'/dimensions/{d}/{i}',evidence=obs['evidence'],original_read_by_synthesizer=(v==3)))
 row.update(status='stage_checkpoint_waiting_late_materials',claim_kind='plan',basis=refs,verdict=None,opposing_evidence=[],late_resolution_evidence=[],suggested_final_fields=['具体包/字段路径','该字段原文','源事实/推断分层','互斥或后证定位','误配类型或核验通过理由','建议改法','原读者与复核者归属'])
out=dict(status='partial_audit_structure_only',complete_book=False,scope='卷一至五阶段材料；尚未作全书最终审计',cases=rows)
(P/'audit-readiness.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
lines=['# 无双全书审计准备：阶段检查点','','当前仅准备结构与前五卷已知边界，不是全书审计结论；16项均未预判为错误。后段材料齐备后逐项写具体字段、原证据、后证/反证、建议和真实读者归属。','','| 检查点 | 已知阶段边界 | 后段核验问题 |','|---|---|---|']
for r in rows:lines.append('|'+r['topic']+'|'+r['known']+'|'+r['late_question']+'|')
lines+=['','判定应区分：真实事实错配、时点倒灌、同名边界、承诺误作完成、来源疑点、后证已关闭、仍无明确回执。没有发现问题的项也写核验范围与依据，不用笼统通过代替。','']
(P/'audit-readiness.md').write_text('\n'.join(lines),encoding='utf-8')
print(json.dumps(dict(checkpoints=len(rows),status=out['status']),ensure_ascii=False))
