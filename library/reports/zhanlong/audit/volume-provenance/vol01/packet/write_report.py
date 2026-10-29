"""仅把已写核心研究导出为阅读报告，不读取正文推断新结论。"""
import json
from pathlib import Path
P=Path(__file__).parent
A=json.loads((P/'analysis.json').read_text(encoding='utf-8'));C=json.loads((P/'cards.json').read_text(encoding='utf-8'));G=json.loads((P/'graph.json').read_text(encoding='utf-8'))
names={'worldbuilding':'世界观','characters':'人物','plot':'情节','style':'文风','narrative':'叙事','dialogue':'对话','pacing':'节奏','themes':'主题','continuity':'连续性'}
def refs(row):
 return '；'.join(e['chapter_id']+' L'+str(e['start_line'])+'—'+str(e['end_line']) for e in row['evidence'])
lines=['# 《斩龙》卷一：从零开始的九维蒸馏（待审阅草稿）','',
 '本卷 raw ch-0002—ch-0251 已按现有 reading-units 共同全文覆盖250片、248个正文单元：卷题1片，印第28章为两片合一。前150片由本代理实际全文阅读；尾100片由 primary 实际全文阅读，本代理已分六批完整阅读其100条事实/推断/状态/未明四栏与交接。合并保留尾行原字节及 `reader=primary`，没有冒称独自阅读全文。','',
 '核心判断是：个人武力、任务目标、组织存续和资源主权不能用一个“赢”替代。本卷的主角可拿17杀MVP而旧盟仍被解散，可在28精英中杀26而三会仍败，也可将秦王醒魂到100%而仍无装备资格。人物成长主要在接受分工、理解规则和把个人收益转成团队资源，研究同时保留其报复、凝视和控制他人的争议。','',
 '九维36条均含文本事实、解释、具体机制、适用限制与章内证据；43人物、47场景、12机制；图54节点、33边、16线。此前核心初稿的41人物/45场景基础上，自审补入徐月、问剑及早期骗援/比克尾杀两场，纠正熊王剑“魂绑”误读为死亡后ROLL仍结算，并去一条泛化救援echo。','',
 '研究是私有来源分析与中性方法抽象，不自动成为用户审美规则、原创设定或对在世作者的模仿指令。当前只覆盖第一卷，不能称《斩龙》全书研究完成；本代理后续还负责卷四。','',
 '[九维主档](analysis.json) · [全部卡片](cards.json) · [阶段图](graph.json) · [真实日志](read-log.json) · [逐章四栏](chapter-notes.jsonl) · [读者归属](reading-attribution.json) · [合并回执](merge-receipt.json) · [下一阶段交接](handoff.md) · [本地校验](validation.json)','',
 '## 九维研究','']
for d,rows in A['dimensions'].items():
 lines+=['### '+names[d],'']
 for r in rows:
  lines+=['**'+r['title']+'**','',r['textual_fact'],'',r['observation'],'','可迁移方法：'+r['mechanism'],'','限制与反证：'+r['limits_and_counterevidence'],'','证据：'+refs(r),'']
lines+=['## 精选场景与人物的取舍','','卡片按作用选择，没有逐章凑卡。早期药剂尾杀保留敌队已耗王97%、主反用治疗及红名代价；中段天策保原约、九奶和四将；后段寒岩保八人死、机关虎与环境解法。组织戏不只围主打转：囡须看证据自主改追随、碧未转会，花枪坚持原队，简劝停/离战却未退会，与子和南宫兄妹保外部归属。','',
 '林的帮助分别是战术图、挡击、资源货运、日常照料，留英雄冢与父控制没有因感情亲近自动消失。抹茶按理论与执行两轴记：战术成绩有狐转述及真实部署后果，瞄准失误也继续出现；本卷不偷后态解释为伪装。阿雷私人余额不入基金，主明确拒其给全队买装。','',
 '## 可迁移机制卡','']
for c in C:
 if c['asset_type']=='pattern':
  lines+=['- **'+c['title']+'**：'+c['content']['summary']+' 失效：'+c['content']['failure_mode']]
lines+=['','原创迁移须换掉本书专属人名、物件、场景排列与句法口头禅，只抽取信息、资源、选择和反馈之间的可操作关系。','',
 '## 阶段线索状态','']
for t in G['threads']:lines+=['- '+t['title']+'（'+t['status']+'）：'+t['stage_note']]
lines+=['','## 连续性与来源异常','','analysis 的 `chapter_unresolved_index` 从合并250条原笔记中完整保留所有非空未明串，并保reader，不因本卷后来回收删旧记录。它是历史候选，不代表每条到卷末仍开；`unresolved_volume_end` 另列15个当前具体待核对象。终点审计需同时读这两层，不能只从选中九维取样。','']
for a in A['source_anomalies']:lines+=['- '+a['id']+'：'+a['description']+' 处理：'+a['handling']+'（'+refs(a)+'）']
lines+=['','## 卷尾实际结算','','已成：斩龙正式建且报告三级972；双月实加入，李牧为长老/忠烈营；凫水加入游戏队而不住工作室；NPC冉闵实复生留城；流霜中途实际收徒三转；神虎已孵、五卷已学、兵解已有15符。','',
 '未成或未见全证：251矿权终局与简生死、秦王重铸/装备、双女离英雄冢、南宫兄妹达10与正式合作、林实习及汪/改造体幕后；部分旧佣、500饭借、次月工资、售扇分款与抹合同细则。不可用一项新还款泛闭所有旧账。','',
 '角色判断层：罗林忠誓、卡尔害子控诉/流霜军令说法、主能自行清烙印记忆、与子说血认虎/转蛋，均按发言主体保留，不写研究者全知认证。','',
 '本地结构校验只证明覆盖、来源定位和图引用可用。主代理尚须逐项文学审查后决定正式导入；用户审美批准另行记录。','']
(P/'report.md').write_text('\n'.join(lines),encoding='utf-8')
print('report.md written from reviewed-by-author draft cores')
