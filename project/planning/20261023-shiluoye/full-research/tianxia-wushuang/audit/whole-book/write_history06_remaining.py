"""卷六历史余15条；11个resolved继续用既签组。"""
import json,pathlib,hashlib
H=pathlib.Path(__file__).resolve().parent
J=[
('v06-thread-003','partial','autonomous-alliance','1219已明确吻痕现为保护伞盟主；1571她带七十万自愿义援，1572意见改变陆部署。组织自治/义援有延续，非中国国籍或古剑正式并会，未来无限服从不证。',[1219,1235,1571,1572,1596]),
('v06-thread-004','unrecovered','specific-territory-timer','1143战胜后尚余17小时，后续行云仍活动/保霜风优势未给本次24小时终占系统回执。她抢剑或攻别城不能代偿该特定领地计时。',[1143,1270,1575]),
('v06-thread-006','partial','dungeon-and-bet-ledger','S3套装/斗气/守护刃的成长成果已成，后更强装备不抹这段；四份赌款未找到各笔实际到账，不能以主后富/其他拍卖净收冲销。',[1160,1161,1208,1511]),
('v06-thread-008','answered','judicial-update-by-report','卷六已捕/待公审属正确快照；1328乱月明确转述唐龙终身监禁，司法结果有后消息。保为角色报告，赃款是否全追/境外冻结未因此补成。',[1195,1196,1217,1328]),
('v06-thread-009','partial','relationship-and-consent','林自陈抗原/现实选陆、何持续照护/临别约、北明表爱/慕主动吻均有后续行动；终点仍无各方统一婚/多伴规则，林赴美不自动解决何北慕的全部关系。',[1230,1250,1595,1596,1605,1609]),
('v06-thread-011','unknown','spirit-awakening-and-hostile-remnant','玄女融剑沉睡已成，1461九州进轩辕可证武器阶段成长，却未明她醒来或蚩恶灵永灭；不能以终形称谓替灵魂苏醒回执。',[1215,1216,1461]),
('v06-thread-012','partial','exchange-and-future-vow','双方SS交换/赴会原已兑现；以后的守城/终身约束没有一份全程履行清单。有限终点不能验证终身永诺，也不因未叙认背约。',[1210,1219,1609]),
('v06-thread-014','partial','institution-and-payment','官网新CGL排名/工资制度确出，1525/1592等组织活动不能代首笔薪水到账；前千额外奖金也未有对应流水。制度已成、现金未独回执。',[1196,1220,1238,1525,1592]),
('v06-thread-017','partial','recovered-object-and-missing-route','1455卡琳令取并实际交斩龙剑、冰兰接认，可闭合旧失物最终再现；雪薇/索怀疑拾荒者受卡指使仍推断，1273到卡手的具体路程未全证。',[1273,1455]),
('v06-thread-019','unrecovered','specific-training-contract','十万补偿已付与100骑射需战天自备资源的约定分开；后有二百友训/别批龙骑不能证明原百名/资源已实际训练，未找到该笔对应回执。',[1263,1264,1341]),
('v06-thread-020','partial','borrowed-body-and-later-deaths','1452心然斩米头、1453明踩毁；1456大圣者取明宇心/破神格化尘，两者后死已明。林浅自身魂/意志仍未交代，不由借体者死自动补原主获救或也死。',[1268,1273,1280,1452,1453,1456]),
('v06-thread-021','partial','injury-recovery-and-affiliation','卡兰后1452请单挑战米且1457请冰活着重建、1467邀同行，明确仍活并参与；没有失肢重塑/完整伤愈过程。正式天空归属有1452当章后证，不能维持全书从未入军。',[1268,1273,1452,1457,1467]),
('v06-thread-022','unknown','early-employer-and-payment','血盟与暗佣/炼狱后期合作有1301/1350现场线索，不能反推1281逐人十万悬赏必同雇主。完整委托人/该笔赏金到账仍未明，不由谁获益定罪。',[1281,1282,1291,1301,1350,1351]),
('v06-thread-025','partial','boss-death-vs-quest-handin','1295实际杀斯特有九君王系统奖励，但公告不是龙心SS交付；本次复读整章未见取心交委托/该SS结算。主线怪已死，不能据战奖替具体交心任务回执。',[1287,1293,1295]),
('v06-thread-026','partial','injury-and-two-world-recovery','1298醒仍缺腿，1311腿长出/97%后新囚伤，1504活返人界；现实1508才睁眼并渐练走。互救已有行动，原断腿不是假、100%伤愈与新伤/现实肌力不可互代。',[1292,1293,1298,1311,1504,1508,1524]),
]
assert len(J)==15
out=[dict(candidate_id=c,status=s,audit_domain=d,rationale=r,later_chapters=e) for c,s,d,r,e in J]
p=H/'adjudications-history-v06-remaining.json';p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
lookup={x['candidate_id']:x for x in json.loads((H/'historical-question-pool.json').read_text(encoding='utf-8'))['candidates']}
md=['# 卷六历史余15条（可主审）','','原11条resolved沿用已签closed-middle。1295本次重新全文核公告与SS任务不是同一回执，其他卷六为派生研究。','']
for x in out:md += [f"## {x['candidate_id']} {lookup[x['candidate_id']]['title']}",'',f"{x['status']} / {x['audit_domain']}：{x['rationale']}",'','后证raw：'+', '.join(map(str,x['later_chapters'])),'']
(H/'historical-reviewed-vol06-remaining.md').write_text('\n'.join(md),encoding='utf-8')
print(len(out),hashlib.sha256(p.read_bytes()).hexdigest())
