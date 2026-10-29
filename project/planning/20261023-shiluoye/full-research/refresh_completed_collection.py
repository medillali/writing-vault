"""三书真实accept后刷新当前入口；历史范围和比较正文不倒填。"""
from pathlib import Path
import datetime,hashlib,json,re
B=Path(__file__).resolve().parent;R=B.parents[2];V=R/'writing-vault';C=V/'library/reports/collection'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
books={slug:read(V/'library/reports'/slug/'ACCEPTANCE.json') for slug in ['zongheng-tianxia','tianxia-wushuang','zhanlong']}
assert all(x['status']=='full-source-nine-dimensions-and-terminal-audit-complete' for x in books.values())
assert read(C/'catalog-config.json')['active_source_id'] is None
assert sum(x['body_units'] for x in books.values())==4157
def replace_one(p,old,new):
    data=p.read_bytes().decode('utf-8');assert data.count(old)==1,(p,old[:50]);p.write_bytes(data.replace(old,new).encode('utf-8'))
replace_one(V/'START-HERE.md','《纵横天下》1180正文及《天下无双》1599正文的全书研究已在本地验收；《斩龙》1378正文、六卷九维、649张阶段卡及36条全书综合已正式保存，人物全弧和整书最终审计继续。','失落叶三书已按《纵横天下》→《天下无双》→《斩龙》完成全书蒸馏与独立验收，共4157个正文阅读单元、22卷九维及1832张来源卡。[本轮最终研究验收](library/reports/collection/三书最终验收.md)列出人物研究、主暗线、疑点和实际证据边界。')
p=V/'RESEARCH-QUEUE.md';text=p.read_text(encoding='utf-8');lines=text.splitlines()
for i,line in enumerate(lines):
    if line.startswith('| 斩龙 | 1378正文/1386片段已实际全文；'):
        lines[i]='| 斩龙 | 1378正文/1386片段、6卷九维、649卡、36全书综合、161项人物及关联主体研究、24重点、232历史与2462原子题均主审发布，[整书验收](library/reports/zhanlong/ACCEPTANCE.md)通过 | 用户审阅；旧卡与原阶段判断保历史，检索时读[全书审计](library/reports/zhanlong/audit/whole-book/README.md)及[人物卡映射](library/reports/zhanlong/audit/whole-book/character-stage-card-resolution.md) |'
p.write_text('\n'.join(lines)+'\n',encoding='utf-8')
p=C/'本批验收.md';text=p.read_text(encoding='utf-8');a=text.index('当前进展（');z=text.index('\n\n以下是',a)
text=text[:a]+'当前进展（2026-10-26）：失落叶三书已全文蒸馏、主审和独立验收，共4157正文/4176片段、22卷九维、108条全书综合及1832张来源卡。人物与关联主体、主暗线和疑点均有独立终态研究；[本轮最终研究验收](三书最终验收.md)与[五书机制比较](写作机制比较.md)已接入[统一目录](README.md)。新备份与真实隔离恢复以[本轮恢复回执](backup-verification.json)及对应归档sidecar为准，下方建库旧记录不充当新证明。'+text[z:];p.write_text(text,encoding='utf-8')
replace_one(C/'机制索引.md','《纵横天下》《天下无双》整书已验收；《斩龙》1378正文及六卷九维、649份阶段卡和36条全书综合已正式保存，人物全弧与整书最终审计仍在进行。','《纵横天下》《天下无双》《斩龙》整书研究均已独立验收，实际范围与研究条目见[三书最终验收](三书最终验收.md)。')
p=C/'写作机制比较.md';receipt=C/'cross-book-comparison-validation.json';old=p.read_bytes();old_receipt=read(receipt)
history=C/'qa/cross-book-comparison-before-final-acceptance.json';assert not history.exists();history.parent.mkdir(parents=True,exist_ok=True)
write(history,{'purpose':'保最终验收前的比较发布状态与原字节；不是当前状态。','markdown_sha256':sha(p),'markdown_utf8':old.decode('utf-8'),'receipt':old_receipt})
needle='《斩龙》人物全弧和整书最终验收仍在进行；比较只证明所列机制及其证据范围，不代替整书验收。'
replace_one(p,needle,'三书的全文、九维、人物及终态研究均已独立验收，见[三书验收](三书最终验收.md)；本比较仍只支持所列机制及其证据范围，不等用户审美批准。')
new_receipt=old_receipt|{'zhanlong_full_book_acceptance':True,'published_sha256':sha(p),'acceptance_sha256':{k:sha(V/'library/reports'/k/'ACCEPTANCE.json') for k in books},'limits':'各书研究验收已通过；比较是研究推断，不代替用户审美。蜗牛旧成果不追认为本轮重读，备份恢复另有真实回执。'};write(receipt,new_receipt)
p=V/'CONTENT-GUIDE.md';text=p.read_text(encoding='utf-8');text+='\n\n## 三书完成后的入口与恢复\n\n失落叶三书已全量研究和独立验收，从[统一目录](library/reports/collection/README.md)或[本轮最终研究验收](library/reports/collection/三书最终验收.md)进入。先查全书综合、人物研究和终点账本，再回看阶段卡；《斩龙》另有[271旧人物卡映射](library/reports/zhanlong/audit/whole-book/character-stage-card-resolution.md)，原误合卡只计一次。无源名称、技术原型与组织行动接口不冒充独立人物。\n\n本轮完整研究快照另附SHA支持恢复计划，覆盖标准CLI白名单外的根入口、指南、队列与模板；卡片和剧情视图可按归档计划重建。最新实际恢复结果见[本轮备份恢复回执](library/reports/collection/backup-verification.json)及归档目录README。原小说仍独立保存；本地验收与备份不等Git推送、Space或ChatGPT记忆同步。\n';p.write_text(text,encoding='utf-8')
lines=['# 失落叶三书最终研究验收','','按实际创作顺序完成《网游之纵横天下》→《网游之天下无双》→《斩龙》。沿《超级骷髅兵》标准完成全文阅读、逐卷九维、全书人物研究、主暗线、疑点终态及综合核验；保留实际阅读署名。','','| 来源 | 正文/原片段 | 卷 | 来源卡 | 全书综合 | 人物及关联主体研究 | 重点 | 历史/原子疑点 |','|---|---:|---:|---:|---:|---:|---:|---:|']
for slug,title in [('zongheng-tianxia','纵横天下'),('tianxia-wushuang','天下无双'),('zhanlong','斩龙')]:
    r=books[slug];n=r['whole_book_audit']['counts'];lines.append(f"| [{title}](../{slug}/ACCEPTANCE.md) | {r['body_units']}/{r['indexed_segments']} | {r['volumes']} | {r['source_total_cards']} | 36 | {n['characters']} | {n['findings']} | {n['historical']}/{n['local']} |")
lines+=['','三书共4157个正文阅读单元、4176个原片段、22卷、108条全书综合、1832张来源卡。卡数保来源阶段，不当独立人物数；《斩龙》161项含159项单一人物或具名NPC身份研究及2项关联接口，另将无源罗戟、误述火犁补核槽单列。271旧人物卡全部映射，旧王翦/王将合卡仅计一次、分别指向二人。','','原图和卷末状态保留；终点判断另行叠加。answered可包括失败、规则与证据边界澄清；unknown/partial不等作者遗忘，也不保证所有承诺最终实现。来源事实、角色猜测、研究解释、用户评价和原创设定继续分开。','','[五书写作机制比较](写作机制比较.md)已连接失落叶三书及蜗牛《贼胆》《练级专家》的具体观察与适用条件。旧蜗牛成果沿各自原完整检查点接入，未追认为本轮重读。《贼行天下》《骷髅魔导师》仍仅为原开篇研究，未冒称八源全部全文完成。','','| 验收方面 | 实际记录 |','|---|---|','| 三书研究与发布 | 各书ACCEPTANCE及独立publication-validation均通过 |','| 旧主档和人工字段 | [626份原主档保护](baseline-protection.json) |','| 统一管理与范围 | [八源目录](README.md)、[固定阅读单元](reading-units.json)、[配置](catalog-config.json) |','| 全库结构、来源、检查点与链接 | [最终全库核验](full-project-validation.json) |','| 本轮新备份与真实隔离恢复 | [独立恢复回执](backup-verification.json)，另有归档sidecar；不采用建库旧回执代替 |','','最终备份排除原小说、Git内部与机器配置。根指南/模板等由SHA支持恢复计划保存，派生阅读视图从主档/图快照重建。回执在快照后生成，因此归档sidecar和现库保存本次新回执；不声称快照包含它自己。','','用户审美和研究采用仍待用户决定。此次本地完成未提交或推送Git、未写Space或ChatGPT记忆，也未创立原创项目或安排后台任务。']
(C/'三书最终验收.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps({'status':'three-book-current-navigation-refreshed','active_source_id':None,'body_units':4157,'source_cards':1832,'books':8,'user_approval':False,'backup_not_claimed_before_actual_run':True},ensure_ascii=False))
