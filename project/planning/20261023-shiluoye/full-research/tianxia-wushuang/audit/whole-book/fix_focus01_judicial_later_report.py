import json,copy,hashlib
from audit_evidence import H,evidence
p=H/'focused-findings-part01.json';before=json.loads(p.read_text(encoding='utf-8'));after=copy.deepcopy(before);i=next(i for i,r in enumerate(after['findings']) if r['key']=='judicial-and-player-sanctions');old=copy.deepcopy(after['findings'][i]);r=after['findings'][i]
r['stage_chain'][0]='唐龙先被抓/取证、1217差公审；1328乱月明确转述已判终身监禁，不能将早阶段未判沿用为全书没有判刑说明。唐风是其堂兄而不同人。'
r['conclusion']='唐龙判终身监禁已有乱月后文转述，不冒称亲见判决书/执行或追赃已完；听风仍无特定拘押判刑后证，真实救出月不等该处罚已成。'
r['limits_and_counterevidence']='判刑报告、亲见庭审/执行、境外资金追缴分层；保护动机不自动使现实斗殴或动用关系查前科成为可移植正确做法。原文暴力事实与研究评价分开。'
assert all(a==b for n,(a,b) in enumerate(zip(before['findings'],after['findings'])) if n!=i)
(H/'reviewed-batches/focused-findings-part01-before-judicial-report.json').write_bytes(p.read_bytes());p.write_text(json.dumps(after,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
lines=['# 无双终点重点第一组12项（待主审）','','本组依据八卷正式研究与已读必要接口派生；本代理未个人重新全文阅读八卷。','']
for x in after['findings']:
 lines+=['## '+x['key']+' '+x['title'],'','终点类型：'+x['terminal_status'],'']+[f'- {s}' for s in x['stage_chain']]+['','结论：'+x['conclusion'],'','限制与反证：'+x['limits_and_counterevidence'],'','证据raw：'+', '.join(e['chapter_id'][3:] for e in x['evidence']),'']
(H/'focused-findings-part01.md').write_text('\n'.join(lines),encoding='utf-8')
x=dict(status='draft_group_targeted_correction_pending_primary_signature',key=r['key'],before=old,after=r,before_sha256=hashlib.sha256((H/'reviewed-batches/focused-findings-part01-before-judicial-report.json').read_bytes()).hexdigest(),after_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),other_11_objects_unchanged=True)
(H/'focus01-judicial-later-report-delta.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(x['after_sha256'])
# 第二组尚未交审，仅同步同一错误结论，保其余17对象。
p=H/'focused-findings-part02.json';obj=json.loads(p.read_text(encoding='utf-8'));r=obj['findings'][0]
r['limits_and_counterevidence']='唐龙判终身监禁已有1328乱月转述，仍未亲见庭审/执行或追赃；其他盟主驱逐命令未逐个执行，不因复籍一项已成就清所有政治司法账。'
r['evidence']=evidence([int(e['chapter_id'][3:]) for e in r['evidence']]+[1328]);p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
lines=['# 无双终点重点第二组18项（待主审）','','依据八卷正式研究与必要派生接口；本代理亲读仅卷五/七，未个人重新阅读全文。','']
for x in obj['findings']:
 lines+=['## '+x['key']+' '+x['title'],'','终点类型：'+x['terminal_status'],'']+[f'- {s}' for s in x['stage_chain']]+['','结论：'+x['conclusion'],'','限制与反证：'+x['limits_and_counterevidence'],'','证据raw：'+', '.join(e['chapter_id'][3:] for e in x['evidence']),'']
(H/'focused-findings-part02.md').write_text('\n'.join(lines),encoding='utf-8');print(hashlib.sha256(p.read_bytes()).hexdigest())
