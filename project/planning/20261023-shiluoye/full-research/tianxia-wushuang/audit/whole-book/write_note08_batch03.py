"""卷八追加notes原子120—179逐项终判。"""
import json,pathlib,hashlib
H=pathlib.Path(__file__).resolve().parent
rows=[x for x in json.loads((H/'local-question-pool.json').read_text(encoding='utf-8'))['candidates'] if x['volume']==8 and x['original_field']=='notes-unresolved']
J=[
('partial','rescue-outcome','1570/1571明确古精16000返7606、亡8394，且谷里十余分盟未救出；友军部分逃生不是三百万全救。获救者非逐名清单，仍有范围限制。',[1567,1569,1570,1571]),
('partial','rescue-casualty','1570给古精8394损失精数，1571给友盟逃出近数与增补；总被围三百万的完整存亡表未给，不能将逃生与后增援合算全部救回。',[1568,1570,1571]),
('partial','casualty-and-object-fate','救援古精损失1570明确，友军救出仍近数；1569斗死未交耀阳是否再次爆，不能拿他1562先前持用反推此次必留或必爆。',[1562,1569,1570,1571]),
('unrecovered','compensation-distribution','战天1亿确到陆账，但每亡5万金币/留1万等分发为计划，未给逐人到账及币种换算；不把实收赔款写成全部发完。',[1570,1591]),
('answered','future-vow-boundary','战天当时认错与不背叛誓言可证，后探病亦可证友谊；有限故事终点不能验证终身/永不的全称誓，保承诺层而非已兑现终身。',[1570,1593,1609]),
('unknown','source-troop-scope','计划五百万与实际编组、逃兵、再上线及保护伞七十万属于多阶段范围，没有逐笔总表；不能强凑为同一时点全军精数。',[1571,1572,1576]),
('answered','battle-and-terminal-outcome','1573—1574此线实胜但有回城者，1579—1580燕耳由林弃城，1589终战仅四征服且英雄保住。后证已匹配，不能用1572战前口号预记最终五城。',[1573,1574,1580,1589]),
('answered','budget-vs-loss','晴空雪一万是可接受损失预算，1574另有龙曜约两万/不同兵种统计；不能把预算直接当该段最终实际损数。',[1573,1574]),
('answered','escape-and-victory','1574明确青土最多百万回城，其余被杀；小蛮退路伏击已实施但不是所有人无一逃。聚歼目标完成为重创，不改写绝对全灭。',[1573,1574]),
('unknown','organization-dissolution','林报告长生殿五十万归零、彻底消失是战损判断；没有系统解散回执，不能套1519挑战解散规则。全军覆没与公会制度注销分开。',[1519,1573,1589]),
('unknown','source-near-name','1573长生刀/长生殿邻近词按源保留，未独立作者更正；可由上下文区分刀和组织，不据误称造新实体或补转手。',[1573,1579]),
('answered','knowledge-access','1573巨象/天岭由何许报告，主并未到场；1575主才抵天岭、1581有巨象系统界面。后证不能倒写1573已亲见两线。',[1573,1575,1581]),
('partial','city-result-and-transport','1580林明确燕耳杀君主/废弃，城权结果已闭；1576十一蚩尤翎在天岭部署不是原拟燕耳运输已完成的镜头，毁燕耳炮/运输过程未逐述。',[1574,1576,1580]),
('answered','statistical-applicability','慕七成阵亡是其组织统计、不是全员实名表；后续新上线/外盟增兵不能推死者国战内复活。answered仅说明记录适用边界。',[1574,1576,1589]),
('answered','statistical-scope','五小时损近两万与二十四小时至少六万时间窗不同，不能据此计算同一总体差额或当硬冲突；两口径原数均保。',[1574]),
('answered','illness-and-knowledge-layer','1589陆醒仍活且获诊，1593心才明确听人说主可能死；1574落泪不证明她已知全部时限。终点赴美/匿名生还暗示也不倒改她早期所知。',[1574,1589,1593,1609]),
('partial','account-fate-and-penalty','贝多芬1575被锁杀，1591李报删大号后重练新号；账号处置有报告回收，但具体此次掉级/归零数仍未显示，不能由锁脸变补值。',[1575,1591]),
('answered','skill-text-boundary','本场轩辕诀原数70%照录，后续多场仍70%；别场75等异文另列，不能自行改本场面板为统一数。',[1575,1577,1582]),
('unknown','individual-effect-coverage','轩辕诀范围内战场概述不提供每名敌人余血/受效表；后续总战果不能补本场全员都中或精确剩血。',[1575,1577]),
('answered','contextual-reading-boundary','行云成功击CGL虽缺“杀”字，前后死亡系统与战天后续游戏阵亡状态足以读为本次击杀；保原缺字，不冒称作者亲自修订。',[1575,1576,1589]),
('unknown','source-troop-scope','1576辅助远程五十万统计包含范围不明，前后九十万/多盟援军不是同一张点名表；不强行合并或算出隐亡。',[1574,1576,1577]),
('unknown','artillery-provenance','北只侦见三龙炮及军团，陆判断从燕耳借来；1579毁炮能证当前炮存亡，不能证其完整运输来源。',[1576,1579]),
('answered','duel-and-maneuver-outcome','1577维回疗/无敌逃，故1576未杀；1579三炮毁且李鬼实夹击，维到1588才真实被杀。原章末杀意不再冒充提前击杀。',[1576,1577,1579,1588]),
('unknown','source-deployment-continuity','魂归原分给正面而后骨干/兵种出现后方，源已列回城与实际新部署，但具体改令/各部划分未交待；不另造第二支同数军或擅修指令。',[1576,1577,1579]),
('unknown','source-troop-accounting','近120万是此处集结近数，与前段辅助/外盟统计范围不完全对应；缺明细无法配平，不能据此添同量复活兵。',[1576,1577]),
('answered','counterfactual-boundary','否则天空必失是主对失败后果的战前判断；实际1579夹击推进、1589国战结算四城征服，没有发生该反事实以供验证。',[1577,1579,1589]),
('unknown','item-effect-estimate','维回血量实给7921773，但50%比例由陆估，无本章完整戒面板或复测；不把估算固化为精确装备规则。',[1577]),
('answered','death-trigger-boundary','1577维回疗后无敌逃，锁未触发击杀后果；1588他后来真死也未列归零数，不能倒写1577已归零。',[1577,1588]),
('answered','unit-skill-attribution','1578口令写铁骑而实际执行段为弓骑震荡箭，效果归明确执行者；不因口误给普通龙曜骑新增远程箭技。',[1578]),
('answered','identity-normalization','何以为何艺近名由场景持续同一指挥/角色可归一，不据单字误称另建人物；不宣作者已更正原词。',[1578,1579]),
('unknown','local-casualty-count','诱5000斩铁入袋的局部目标是尽量无损，未列该局己损精数；全场继续成片死也不能反算这个局部一定零亡或具体亡几人。',[1578]),
('answered','progression-rule-boundary','北1578依职业积分第一并随机隐藏条件成神；慕1562亦有同类途径，但不推出所有第一必成神或固定概率。',[1562,1578]),
('unknown','unspecified-person','本章主称两个人而未该处点名另一人；不能只凭熟悉名单替其补名，已明北成神与可能指代分开。',[1578]),
('unknown','source-near-name','青衣侯与前后紫衣侯称名不齐，守源异文并以连续上下文链接紫衣侯，不自动再造死者或把标题当作者纠错。',[1575,1579,1590]),
('answered','identity-normalization','王洛在此死亡消息按前后京城洛神语境关联，1590榜/同伴线不据简称造新NPC；简称本身不添加现实姓名信息。',[1579,1590]),
('answered','identity-and-disclosure','1580陆当面对林明确猪一样的对手就是小小猪并请保密；1579主隐语不提前写林已明知，后证补具体知情时点。',[1579,1580]),
('answered','identity-and-disclosure','下章1580确有向林揭名回执，本原子不是终点待查；林同意保密，不等所有同伴同时获正式告知。',[1580,1592]),
('partial','object-rights-and-city-result','1580林明确燕耳杀王/废弃；长生刀1587借李、1597主述给侯，未还战天。城权已闭，刀的交还战天不能由“追回”二字推成。',[1579,1580,1587,1597]),
('unknown','inferred-kill-and-transfer','神火完整转手/猪被何人杀在1580是陆按尸体物件推断；后1581实借连/1587林实赠可闭当前权益，但不能把旧递传净化为亲见全链。',[1580,1581,1587]),
('unknown','source-item-alias','1575火神杖与1580神火杖在同一追物语境近称，后林确认送连的是神火；未有两杖独立面板或改字声明，保异文不造两器。',[1575,1580,1587]),
('partial','enemy-movement','泪1581实回灼热、1584再传天荒，有后续位置；1580李对英雄去向仍猜测，不因1576侦到炮团便补其每次中间路线。',[1580,1581,1584]),
('answered','knowledge-access','1580陆现场只见泪行军，后来她实际回城并不让原现场变成全程追踪；主见、李推与后证按时点分开。',[1580,1581]),
('partial','server-territory','1596斗报燕耳/冰河废弃、紫葡萄由苏菲控，可支持日本主城受损后状；但不是全服每一政权/日后永久无城的普查，陆1580预判不能全称化。',[1580,1596]),
('unknown','unseen-player-identity','系统仅显示另十名中方，陆猜采参没有职业名单/相遇补证；不能据人数推他们全为生活玩家。',[1581]),
('answered','relative-comparison','城墙坚固可与“较英雄/青土弱”同时成立，相对强弱不等绝对脆弱；后七小时/多轮攻坚是具体阻力，不构必须二选一的硬矛盾。',[1581,1582,1585]),
('answered','transport-capacity-boundary','神石按络绎/多分钟传送，100×100是入口区域非两百万人瞬间同格容积；1577明确15分钟集结也支持过程性运输。',[1577,1581]),
('unknown','political-motive','泪没借红枫炮与暧昧程度的联系是陆解释，未见双方借炮谈判或唯一原因证词；后援军/协议不能单证此动机。',[1581,1584]),
('unknown','source-approximation','空军初见近万/清近两万是视野/近数口径而无补兵清单，不能据差额肯定一万复活或精确增援。',[1582]),
('unknown','source-force-scope','团长说维二百万可能指总服可拼而前英雄三十万是局部残军，未列同分母明细；不强算忽增170万或作精确同军矛盾。',[1580,1582]),
('answered','cross-book-comparison-boundary','冰火/乱月对七星等战力的评价是人物观点，没有本书同条件实战；不得把20%或世一称号当跨书客观排名。',[1582,1600]),
('unknown','source-ranking','连北第二第三/李第五与前榜3/4/6不同且无新榜时间，可能口径变但未解释；保阶段概述漂移，不能替作者重排实时榜。',[1582,1583]),
('unknown','past-order-attribution','野王原奉王令留守是鬼好像的判断，后野王确实援来/有旧约不独证此前命令；不把猜测升事实。',[1583,1584]),
('partial','conditional-agreement','1584野王追问旧约、泪明说先败古剑/守灼热才履，证确有条件协议；1585两目标失败，未见赴印或性行为发生，传闻内容不作已履事实。',[1583,1584,1585]),
('answered','sexual-claim-boundary','主等对泪性生活/爱烛的成人常识式评价不是独立证词；现实探病、旧约谈话都不能补她历史性行为或关系协议。',[1583,1584,1593]),
('answered','identity-normalization','尹沛萌为明确实名，佩萌是相邻近字误称；同一泪残痕不因误字拆两人，也不把读者归一称作者已改稿。',[1569,1584]),
('unknown','ownership-and-npc-office','天荒玩家领主泪与面板秋枫子爵可能分属产权/管理层，但源未明解释职责结构；不强报同名矛盾，也不自造法定从属规则。',[1584,1585]),
('answered','statistical-scope','三生近二十万是早约数，随后实报24万+且允许拼集；不应只据近数差认死人复活，answered是适用边界，不是精确人数已清。',[1583,1584]),
('unknown','source-troop-accounting','20万部署、野王称30万及再调20万是不同说话者/阶段，没有同一时点全表；不强配平或添暗军。',[1584,1585]),
('answered','counterfactual-and-location','北假设百龙半小时毁天荒未执行；天荒1585由地面苦战七小时后废，1596千骨龙实际在暗月防守。两种行动不能倒合。',[1584,1585,1596]),
('answered','statistical-applicability','古剑≤30万加红唇约10万与末近30万为近数/范围不同，源未说其间另亡十万；不能用两报数直接计算精确新增战损。',[1585]),
]
assert len(J)==60
out=[dict(candidate_id=rows[i+120]['candidate_id'],status=s,audit_domain=d,rationale=r,later_chapters=c) for i,(s,d,r,c) in enumerate(J)]
p=H/'adjudications-local-note-v08-003.json';p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
md=['# 卷八追加notes原子003组（120—179，可主审）','','实读派生notes后逐项匹配；人物猜测、消息、系统与现场分层。','']
for x in out:
 row=next(r for r in rows if r['candidate_id']==x['candidate_id']);md += [f"## {x['candidate_id']} {row['title']}",'',f"{x['status']} / {x['audit_domain']}：{x['rationale']}",'','后证raw：'+', '.join(map(str,x['later_chapters'])),'']
(H/'local-notes-v08-reviewed-003.md').write_text('\n'.join(md),encoding='utf-8')
print(len(out),hashlib.sha256(p.read_bytes()).hexdigest())
