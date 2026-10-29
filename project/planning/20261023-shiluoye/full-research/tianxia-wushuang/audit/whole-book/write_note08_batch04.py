"""卷八追加notes原子180—239逐项终判。"""
import json,pathlib,hashlib
H=pathlib.Path(__file__).resolve().parent
rows=[x for x in json.loads((H/'local-question-pool.json').read_text(encoding='utf-8'))['candidates'] if x['volume']==8 and x['original_field']=='notes-unresolved']
J=[
('partial','conditional-agreement','1584明确先败古剑/守灼热为旧约条件，1585天荒败、1589灼热征服；陆断无须赴印仍是其结论，未见泪实际赴印/性履约或正式解除约文。',[1584,1585,1589]),
('answered','context-and-motive-boundary','泪的复杂神情、野王追约与陆所谓保护爱情需连条件失败/利益互用并读；神情不独证性行为、主动献身或同意后续安排。',[1583,1584,1585]),
('answered','elapsed-time','1584余约二十小时到1585余12小时40分之间叙明七小时苦战，可容战役时长；不把跨章文字短等同现实即时推进。',[1584,1585]),
('answered','narrative-time-boundary','同一章可概述七小时战斗/半小时行军，章节长短不提供秒级时钟；本项是时间读法约束，不冒作一个剧情伏笔。',[1585]),
('unknown','source-timeline','1586“连续27小时”与1574实下线睡约四个半小时不全相容；保明确休息动作，不删睡眠也不强改口号成精确在线记录。',[1574,1575,1586]),
('answered','knowledge-access','兵量来自李鬼情报、泪可能下线是主推；1587援军真正到/1588维真现不把主之前预测升级成始终全知。',[1586,1587,1588]),
('answered','prognosis-layer','1586怕活不过月是陆自估，1589才有杜父当面月余预估；1609仍治疗中/匿名活动暗示，不能将早自估写医学确定死期或已死。',[1586,1589,1609]),
('partial','research-progress','血样持续取送与1599抑制剂制/实注都有进展，1608最新明确解析87.2%；终点未给100%解析/机器疗程报告，不能用希望氛围补完研究。',[1586,1595,1599,1608,1609]),
('unknown','command-handover','许1586留青土且持杖、1587又迎援，场景允许换岗但未叙具体交接人/时点；不把旧命令作永不可动的禁令，也不造交接镜头。',[1586,1587]),
('answered','organization-title-layer','口语称陆盟主/副盟与何正式盟主可分指军中领袖/系统职位，未有系统换盟主回执；暗月城主1606转何是驻地产权另层。',[1587,1606]),
('answered','planned-vs-actual-force','各城四万是原部署基数，1588有实际传入/临时留陆帮泰坦等调整；计划不能作为后来兵数固定上限，精确逐部人数仍不另补。',[1587,1588]),
('answered','coordinate-containment','暗月属天空地图内，两点提示天空坐标不直接否定原暗月初点；按每次设点/取消回执，不造同时无限门。',[1546,1567,1587]),
('unknown','source-corruption','1588乱码片段无法恢复完整伤害动作/受害200名含义，只用周围清楚伤值与战损；没有原更正，不能以读者猜词填缺句。',[1588]),
('answered','reading-vs-source-quality','该段原读者明确BEGIN—END全文读取、乱码属于当前源文本，不是工具输出截断；其余证据照录，不能拿乱码宣该章未读或自行补正文。',[1588]),
('answered','conquest-failure','1589乱月明确四征服且英雄城被守住，纠正“杀英雄王取杖=征服”推断；1588宣不辱使命不替系统模式/终战结算。',[1588,1589]),
('answered','delayed-order-and-result','1587延三小时再征服灼热是命令，1589战后报告灼热确入四征服；本章不提前填杀君时点/击杀者，结果回执与过程省略分开。',[1587,1588,1589]),
('answered','equipment-evidence-boundary','1588明确维持新绝风且伤害实出；1577只证当时所展示战法，不能把后来装备倒填其当时已用此刀或倒算所有伤值。',[1577,1588]),
('answered','control-resistance-boundary','1588冰爆双MISS由本场神级抗性/状态体现，不推泪永久免所有控；同章主狂撞晕她、林主合杀提供反例。',[1588]),
('answered','fictional-medical-setting','冰毒、抗原与模拟次数只按小说研究者解释及后续药效证据分层；不作现实毒理/疗法正确性的断言。',[1589,1595,1599]),
('partial','reward-and-title','盘古斧1590实际交斗可证奖物存在；1589未重播最终系统MVP/经验，1609李情感MVP归陆亦非系统榜。物件已闭、完整奖励名次仍未示。',[1589,1590,1609]),
('unknown','individual-knowledge','厅众哭只证悲伤，何在场亲听杜父诊断、心1593才明确得知可能死亡；林北等何时听完整一月数字未逐人说明。',[1589,1593]),
('answered','dream-status','1589开场臣服/血海为醒前梦，醒后在南京病房且无新册封回执；不得把梦话写现实政治图节点或已发生王国事件。',[1589]),
('unknown','source-location','1588英雄王前消散与1590在泰坦原地下线处上线有源地点差；未叙中途传送，不强改场所或补秘密动作。',[1588,1590]),
('answered','progression-rule-boundary','1590榜中多名积分高者已神是实际列表，但资格/随机触发与人人保证不同；斗仍被劝早飞是直接限制，不把高积分一律等成神。',[1590]),
('unknown','individual-progression','斗得鬼兽与盘古斧后仍被劝早成神，后比赛冠军杯不提供他的神位回执；终点不能由神器/队伍强自动判斗已神。',[1590,1608,1609]),
('answered','capital-and-role-boundary','25%合同1512实签、1526总部确认转名；1590徐再次提及不构新签约、现金分红或完整法人程序，不多记一次产权移转。',[1512,1526,1590]),
('answered','character-medical-belief','陆怕亲密传毒、林坚持靠近属小说人物风险判断；后林主动抗原另有专门证据，不由吻/同睡直接推真实传播机制或现实医学建议。',[1590,1595]),
('partial','territory-and-pronoun','巨象俄占有系统条件/陆雪夜交涉与1596后控报告相互支持；1591李“我们”具体代词所指仍不明，不能因此把主权改中国。',[1581,1586,1591,1596]),
('answered','territorial-evidence-priority','以寒剑系统占领及俄控后证记巨象，李口语“我们”不替主权回执；原代词歧义另保，不虚报中国占有。',[1581,1586,1591,1596]),
('partial','custody-vs-disbursement','五亿为陆称余额、卡实交鬼保管，后记没有花用/归还流水；不能记父已收五亿，亦无依据用此冲销早期独立五万账。',[1591,1609]),
('answered','literary-limit','旁人羞男人哭与朋友性玩笑只是文本立场，主鬼杜实际哭并互护是反面证据；不把羞哭/物化语言转用户处世或文风准则。',[1591,1593]),
('answered','reported-video-evidence','1592是乱月引用录像，不是本审计者直接看视频；可作为强于原猜测的角色后证，保持二手来源，不冒充逐帧核验。',[1592]),
('answered','kill-contribution','1579系统/林见尸、1580她述尾局，1592录像报助另三死；助杀不等尾刀，不把雷洛/战神王等系统击杀全改归林。',[1579,1580,1592]),
('unknown','information-origin','记者何以知月内死未明；1589杜父诊断存在不证记者亲获同资料，提问本身不是新医学检测或同意披露证明。',[1589,1592]),
('answered','corporate-role-continuity','1592以CEO/25%出场承既有身份，1512/1526已提供合同与转名；本章演讲不再当新任命/新受股。',[1512,1526,1592]),
('answered','corporate-allocation-boundary','保既有25%与代理CEO、总部议事层级；登台发言/长辈估价不追加其他股权、更换公司分权或实收分红。',[1526,1592,1596]),
('answered','event-vs-registration','1592真实动员/开幕发言；1594才NPC报名，1598才预选五场实打，三阶段已可明确分开。',[1592,1594,1598]),
('answered','event-calendar','群体说次日开赛按当场活动口语记录；以后1594实报名/1598定时首夜可实证，不仅凭一句口号倒置竞技开局。',[1592,1594,1598]),
('answered','identity-vs-analogy','战天以书生/七星作下一代竞争类比，不是揭陆或战为旧作实体；本书有明确陆尘身份，跨书称谓不自动合人。',[1593,1600]),
('answered','affection-boundary','行云实吻脸、称现实朋友并助资料；陆接物不等答应排他恋爱或性关系，后续不新增两人关系协议。',[1593,1594]),
('unknown','other-person-intent','北等替解释行云心意仍为她们观点；行云亲述线上报复/现实愿主活可证，未直接给完整恋爱意图，不由旁人代定。',[1593]),
('unknown','complete-attendance','现场多人跪为概述且有部分点名，未给全书顶尖逐人名单；不能把没点名角色全补在场/跪下。',[1593]),
('answered','contextual-typo','MPV处承国战奖励话语可按MVP语境理解，保原字不另造MPV赛事称号；这不等正式系统MVP榜已展示。',[1589,1594]),
('answered','measurement-layer','近三秒由主自述/实际对练体验，未仪器检测；1599—1600药后实战反应改善是后效验证，不能倒造早测量报告。',[1590,1594,1599,1600]),
('answered','fictional-research-boundary','姓名和行云资料来源分别据书内言说/文件，博士“领先十年”为故事内评价；不据此作现实国家技术水平判断。',[1593,1594]),
('answered','consent-and-literary-limit','林明确拒入、主急砸门而见危情，两行动与救危动机同时记录；后她承认抗原不把此前拒绝消除，不泛化未经同意为浪漫规范。',[1594,1595]),
('partial','antigen-treatment-and-commitment','1595林自证自愿/采样及阶段浓度下降、1599制首剂并实注，故不再只有1594主推；终点未示林彻底排毒与婚礼/多方协议，30%等仍预测。',[1594,1595,1599,1609]),
('partial','prognosis-and-clearance','林阶段毒浓下降与首批抑制剂有实证，但七日全排毒/主余25天未获精确检测回执；1608倒计时仍主自计，后记不补百分百根治。',[1595,1599,1608,1609]),
('answered','fictional-medical-setting','一般人24小时死是徐宁小说科研转述，不能当现实输血/毒理依据；本审计仅核林采样/药成/主药效的故事链。',[1595,1599]),
('answered','wealth-action-boundary','财富/新车/海滨住处话语不是当场购置回执；1604现车报废、1605公司调别克为另外明确行动，不添加没发生的新车/别墅购买。',[1595,1604,1605]),
('unknown','source-rule-continuity','1586青土征服90日禁攻中方任何城，1596数日后清攻暗月，未解释驻地豁免或取消条款；保源规则疑点，不能自行发明例外。',[1586,1596]),
('unknown','source-rule-continuity','此禁攻/暗月被袭并列保留，后记未更正/给豁免，不能以附属PK弱20%另规则代解禁攻。',[1586,1596,1602]),
('answered','valuation-not-cash','2500亿美元是林扬电话转述估价，非陆现金或100%企业持有；25%转名的文件层证据仍优先，不能把估值写银行余额。',[1526,1596]),
('answered','office-vs-ownership','陆两次称代理、长辈称老板属于角色俗称；实际职衔/股份另保，不据夸赞话语把25%改全部公司所有权。',[1596]),
('answered','troop-scope','青土500万总来与50万围驻地口径不同，李只是报告千骨龙击退；不能算500万人同格同轮全被龙杀。',[1596]),
('answered','battle-result-boundary','1596明说清认输回城，结果是退敌，非全军被清/永久灭会；保护伞红唇等守城贡献也不能抹。',[1596]),
('answered','comfort-vs-health','林说很好与此前出血/1597痛七小时冲突为安慰层，1599仍第5日取样；不能用一句乐观话记医学痊愈。',[1595,1596,1597,1599]),
('unknown','item-tier-speculation','神域魂器奖励等级只有主推测，终点李杯/象征MVP未给该魂器面板；不把估最多上古写为已证新装备等级。',[1597,1609]),
('partial','competition-rule-version','1598第二季实放幻影狼/天河飞行，当前允许行为有实证；与前季限制差异未见完整新规则声明，不能据旧规删去已发生比赛。',[1597,1598]),
('unknown','competition-exception','第二季现场可用不等已给特批或旧禁令取消理由；源未解释规则变更程序，保赛季表现差，不造主专享豁免。',[1597,1598]),
]
assert len(J)==60
out=[dict(candidate_id=rows[i+180]['candidate_id'],status=s,audit_domain=d,rationale=r,later_chapters=c) for i,(s,d,r,c) in enumerate(J)]
p=H/'adjudications-local-note-v08-004.json';p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
md=['# 卷八追加notes原子004组（180—239，可主审）','','所有医学说法按本书虚构研究/人物体验分层；物件、角色知情与规则疑点分别保。','']
for x in out:
 row=next(r for r in rows if r['candidate_id']==x['candidate_id']);md += [f"## {x['candidate_id']} {row['title']}",'',f"{x['status']} / {x['audit_domain']}：{x['rationale']}",'','后证raw：'+', '.join(map(str,x['later_chapters'])),'']
(H/'local-notes-v08-reviewed-004.md').write_text('\n'.join(md),encoding='utf-8')
print(len(out),hashlib.sha256(p.read_bytes()).hexdigest())
