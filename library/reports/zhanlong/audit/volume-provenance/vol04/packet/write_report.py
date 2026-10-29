"""将本卷手写研究导出阅读报告，不生成新文学结论。"""
import json
from pathlib import Path
P=Path(__file__).parent
A=json.loads((P/'analysis.json').read_text(encoding='utf-8'))
C=json.loads((P/'cards.json').read_text(encoding='utf-8'))
G=json.loads((P/'graph.json').read_text(encoding='utf-8'))
names={'worldbuilding':'世界观','characters':'人物','plot':'情节','style':'文风','narrative':'叙事','dialogue':'对话','pacing':'节奏','themes':'主题','continuity':'连续性'}
def refs(r):return '；'.join(e['chapter_id']+' L'+str(e['start_line'])+'—'+str(e['end_line']) for e in r['evidence'])
L=['# 《斩龙》卷四：逐鹿天下的九维蒸馏（待审阅草稿）','','raw ch-0754—ch-0968共215片、214正文已由 `/root/zongheng_vol03_full` 实际逐章全文阅读。ch-0754仅卷题，ch-0755印第749章，末ch-0968印第962章。55批四栏即时落盘，无未补截断；此前卷1分工归属不移入本卷，本卷也不包含任何969以后原文。','',
 '本卷的主要结构是：任务物把个人战斗引入军政权力，军政权力又依赖人口、供给和信任。主角越来越能调动组织，却不能让每个承诺兑现。救旧敌、拒卖俘、释放囚女是真的；接受尸桥、失五千降俘、选择不救盛临和矿民无改善也是真的。个人武力进步与伦理一致并非同一条成长线。','',
 '双城占领和北域MVP不消除徐翊、佩儿、罗特等死亡；主角的现实阳炎自修也不能救回阿雷。林婉儿有自己的侦情、夺关、杀王与火云治理权，唐琦实际救回东城月，多位NPC和成员提供不可替代的工程、治疗、控制及弱点知识。研究保这些独立贡献，不把系统最后一击等同全程独力。','',
 '九维36项；45人物、47场景、12机制，共104张卡；图54节点、39边、20线、27条知识。32来源异常与19卷末待核对象分别列出，逐章历史未明的208条原note/239原串完整保留。研究待primary逐项文学审查和正式导入，不能视为用户审美批准。','',
 '[九维主档](analysis.json) · [人物场景机制](cards.json) · [关系图](graph.json) · [真实阅读日志](read-log.json) · [逐章四栏](chapter-notes.jsonl) · [读取归属](reading-attribution.json) · [交接](handoff.md) · [自核](self-audit.json) · [校验冻结](validation.json)','',
 '## 九维观察','']
for d,rs in A['dimensions'].items():
 L+=['### '+names[d],'']
 for r in rs:
  L+=['**'+r['id']+' '+r['title']+'**','','文本事实：'+r['textual_fact'],'','研究解释：'+r['observation'],'','可迁移机制：'+r['mechanism'],'','限制与反证：'+r['limits_and_counterevidence'],'','证据：'+refs(r),'']
L+=['## 人物阶段取舍','','人物按独立行动与关系选择建卡，没有把NPC军、玩家组织或同姓亲属合为一个人。下列是本卷阶段变化，不能作为全书终点评价。','']
for c in C:
 if c['asset_type']=='character':L+=['- **'+c['title']+'**：'+c['content']['stage_change']+' 关系：'+c['content']['relationships']]
L+=['','## 场景的适用条件与失效边界','','场景以目标、阻碍、选择、后果与状态变化串联。每卡均有独立适用和失效条件，以下便于逐项查阅，完整行动链在cards。','']
for c in C:
 if c['asset_type']=='scene':
  L+=['**'+c['title']+'**','',c['content']['summary'],'','条件：'+c['content']['applicability'],'','失效/研究边界：'+c['content']['failure_mode'],'','证据：'+refs(c),'']
L+=['## 十二项中性机制','','只抽取可操作关系，不提供在世作者的逐句仿写指令。原创迁移须另选人物、地理、资源、语气和事件排列，不能复刻本书识别性组合。','']
for c in C:
 if c['asset_type']=='pattern':
  L+=['- **'+c['title']+'**：'+c['content']['summary']+' 适用：'+c['content']['applicability']+' 失效：'+c['content']['failure_mode']+' 原创变换：'+c['content']['originality_transform']]
L+=['','## 二十条阶段线索','']
for t in G['threads']:L+=['- **'+t['title']+'**（'+t['status']+'）：'+t['stage_note']]
L+=['','## 来源异常','','异常保原章与层次，不静默修订原文；有些是确定数值/连续性冲突，有些因报告口径或阶段变化尚不能强裁。','']
for x in A['source_anomalies']:L+=['- '+x['id']+'：'+x['description']+' 处理：'+x['handling']+'（'+refs(x)+'）']
L+=['','## 卷末需要后续证据的具体对象','','这些是当前未闭项。逐章当时未明的原串另在chapter_unresolved_index保留，其中兰馨、剿盗、降俘命运、粮运等已有后证的旧题没有被静默删除，也不代表它们到卷尾仍开。','']
for x in A['unresolved_volume_end']:L+=['- **'+x['question']+'** '+x['stage_boundary']+'（'+refs(x)+'）']
L+=['','## 卷末事实结算','','已成：主受碎鼎公/浅林实际登基；火象、火云已归中国，临海系统委托保中国NPC王权和半税/印度玩家主城；凡书已重建生产铸币、原池军有驻处；罗鼎真正死亡/955北域系统结束、957神晶用于游戏五星蝴蝶；933斩龙六级、后主盟5万/三万骑。','',
 '代价：西奥多、罗林、盖文、塞林、凯尔、洛克、徐翊、佩儿、丁凡、欧恩、罗特、莫文、罗鼎等在不同层与不同确认方式下已死；唐麟、旧秋收夏等也不可被补员偷复。阿雷现实真亡，主昏迷自修、唐琦救月两事不能互换。英雄冢主盟347:0真解散但分盟仍存在。','',
 '未结：968新矿战的三万人战果未分玩家/NPC，不能宣布四万NPC全灭；主乘风刺魔被无敌、盾击和多奶挡住，亲认刺杀失败，魔山活、火神矛仍敌手、矿权未定。主酿酒10已成但未制仙人醉；仙人果仍无。','',
 '装备：主最近明确等级170；游戏蝴蝶五星+7，霸王仅靴腕二件、弑神甲/冠军项链已用。955面板魅1433后首3/5/7/8/9/10奖合275只是算术，原文无末新完整面板，不直接称确证1708。现实蝴蝶926收到/试挥，956未实战杀用；它不是957以游戏材料造的同名兵器。','',
 '本地验证只检验覆盖、源定位、字段与图引用；语义通过须primary另审。卡中无用户人工笔记、收藏或审美判断，未写入正式库、Git、Space或记忆。','']
(P/'report.md').write_text('\n'.join(L),encoding='utf-8')
print('report written; observations=36 cards='+str(len(C)))
