"""仅整理既有研究的展示拓扑，不读取小说正文或改写正式资料库。"""
import json
from collections import Counter
from pathlib import Path

BASE=Path('writing-vault/library/reports/two-books-full-20261025/zeidan')
OUT=Path('.planning/tree-maps-20261025')
graph=json.loads((BASE/'plot/graph.json').read_text(encoding='utf-8'))
questions=json.loads((BASE/'terminal-question-map.json').read_text(encoding='utf-8'))['items']
qmap={q['key']:q for q in questions}
scenes=[n for n in graph['nodes'] if n.get('kind')=='scene']
by_num={i:n for i,n in enumerate(scenes,1)}
by_id={n['id']:n for n in scenes}

def ev_clean(e):
    return {k:e[k] for k in ('chapter_id','start_line','end_line')}

def dedup_evidence(evs):
    found=set(); result=[]
    for e in evs:
        e=ev_clean(e); key=tuple(e.values())
        if key not in found:
            found.add(key); result.append(e)
    return result

def ids(nums):
    return [n['id'] for n in sorted((by_num[x] for x in set(nums)),key=lambda n:(n['narrative_order'],n['id']))]

core=[1,2,3,7,9,12,16,17,21,23,25,28,33,35,38,40,42,43,46,49,50,51,54,59,63,66,69,73,74,78,79,80,81,82,91,92,94,95,97,99,101,103,104,105,106,107,109,110,111,112]

thread_specs=[
('livelihood','试用头盔、银行到账与自主生活','subplot','resolved',
 [1,12,14,16,17,25,42,43,45,59,93,101],
 '萧御能否让技艺成为现实生计，并在获得财富后自主决定居住与报恩？',
 '首笔千元、配方与金币变现、黑赛收益相继落实；最初生计目标完成，留下同住与报恩成为主动选择。购盔只见委托，不补现场手续；博彩和组织资本与个人打宝收入分列。',
 ['free-helmet','paid-box-escape','helmet-money','bookscholar-match','shaman-win']),
('technique','完成度学习、控制窗口与条件胜负','subplot','resolved',
 [2,4,5,6,9,10,13,15,18,21,27,31,37,39,41,46,56,60,70,76,80,84,93,105,108],
 '可验证的动作练习能否发展为面对不同敌人仍会调整的技艺，而不是无条件碾压？',
 '成长由失败复盘、超过100%的连贯、短幅效率、敌技时序和多资源配合展开；平局、死亡、未能团灭与二对十失败持续标定边界。旁观刺刀的腕臂理论仍含角色推想，末段胜利也不抹除早期限制。',
 ['skill-combo','skill-ceiling','cidao-style','yunyi-duel','one-vs-fifty-boundary','potion-master-complete']),
('free-cooperation','自由合作者与公会互利的成本','subplot','partial',
 [7,8,12,14,20,22,26,34,36,53,54,65,67,68,69,71,72,73,75,74,77,81,87,95,98],
 '拒绝固定归属的独行者如何使用合作，又由谁支付其成长与生存的成本？',
 '有限合作、承认辅助、公开演示和公平付款形成互利；救尸、捕宠与生产线显出公会人员和资本成本。萧御保留自由身份却高度依靠组织，卫风最终分开；没有全员永久固定队或独力成功的结算。',
 ['weifeng-permanent-team','bone-dragon-raid','ska-zero-loss','z-c-q-guild-war']),
('zhao-future','赵岚馨的恋爱自主、父亲认可与新星婚约','subplot','partial',
 [17,19,35,36,38,59,77,78,79,86,94,96,103,104,105,106,107],
 '同住与互助能否变成双方自主确认的恋爱，并跨过现实家庭压力走向共同未来？',
 '初吻、叙述及公开女友称谓确认恋爱；父亲本人试探后认可，双方约定赴新星结婚，终章三人实际起飞。婚约已成；抵达、婚礼和法律婚姻均未描写。燕琳两次求复合被明确拒绝，礼貌止于朋友。',
 ['zhao-official','father-obstacle','father-blocks-love','marriage-planned','yan-reconcile','new-star-arrival']),
('scar','心口旧伤与飞刀师承的有限披露','hidden','unknown',
 [19,107],
 '被赵怀疑另有隐情的心口刀伤，是否得到独立可靠的真因揭晓？',
 '只保留萧御自述十五六岁与流氓争执被捅、赵的怀疑，以及燕琳二手转述的童年飞刀师承。公开飞刀表演证实技艺，不能证实师承细节或解释心口伤；后文断手骨自接也不是答案。',
 ['scar-origin','knife-training','scar-cause']),
('aode-child','导师债约、童灵身份与兄弟救援','hidden','partial',
 [3,28,29,30,32,33],
 '赊账委托背后的诅咒和童灵身份能否解开，奥德兄弟又能否获救？',
 '圣言匕入场、童灵友情及身份揭示共同使刺核心解咒任务完成。沃卡德自决毁肉身而暂存灵魂，复生无保证；童灵与黑幽灵的关系仍未明；最初失物字面身份未单独命名。任务完成与这些未明事项分开。',
 ['aode-lost-item','child-two-men','black-child-spirit','wokade-revival']),
('old-man','古墓老者、异星双任务与本命余谜','hidden','partial',
 [11,102,110,111],
 '早期传亡灵历史、送信与赠匕的老者，与后期克文图斯及异星任务怎样相接？',
 '390本人现身且叙述确认克文图斯就是古墓老者；427/428指定探索交奖，光暗双门通向最终神战，462本命任务系统完成。40任务面板另称哈蒙斯而无别名说明，仍保留称名冲突。旧方盒仅是主角猜测，460不见后没有独立毁盒或本命实体指认；任务完成不填平物件说明。军队后续和全部异星地图清尽无确证。身份确认场面未被112场景另收节点，在线索证据中说明，不借最近场景冒充揭晓画面。',
 ['hamons-letter-delivery','hamons-army','kevintus-identity','z-c-q-ufnos','light-dark-gate','soul-box-identity']),
('nightmare-space','梦魇回返、索德牺牲与空间神器双门','hidden','resolved',
 [23,24,85,86,88,89,90,91,92,110,111],
 '早期梦魇局部探索能否接续更深救援，所得封印空间器最终有什么必要用途？',
 '重返梦魇后救出巨人和画像主人，索德燃命与五敌同归、巨人永眠；空间转换交到萧御，后解封并充当光暗双门钥匙，接上万人与单人的神战。此线的救援、牺牲和神器用途已兑现；不等于梦魇全地图清尽，格里奥/索德称名差异仍保留。',
 ['nightmare-cleared','z-c-q-nightmare-gate','z-c-q-pradilok','z-c-q-space-unseal','sode-death','sode-name']),
('lost-city','费思与哈尔的遗失城承诺','subplot','resolved',
 [44,46,47,48,49,50],
 '不可靠的NPC合作与守乡誓言，最终能否真正终结女皇与遗失城任务？',
 '培养与保护费思、利用哈尔规则接近机械核心后，女皇诱惑分判占有与守护：哈尔化灰，费思自爆，零血女皇仍须任务神谕审判终结，系统确认通关。哈尔口述历史保留立场，人偶残核重启等不随通关自动解释。',
 ['nameless-rider','nad-half-undead','haer-motive','lost-city-success']),
('mine-necklace','矿洞爱情反述与首赠项链回收','hidden','resolved',
 [35,36,37,38,103,104],
 '任务中的爱情叙述如何被反证，所得旧饰物又为何能在很久以后推动行动？',
 '子爵痴情表述被迪娜等当事人证词改写为多方责任的悲剧。所得首赠饰物被赵长期珍戴，遇围杀掉落后实际追回归还；数值落后没有抹去人物记忆，报复过程也显出萧御的残酷。托人谢蓝月赠装不补成已交付。',
 ['dina-avoidance','zhao-level-misbelief']),
('national-ten','国家十环、队伍责任与接力完成','subplot','resolved',
 [51,52,55,56,57,58,61,62,63,64,82,83,95,97,98,99],
 '十盗队能否在不只依赖队长个人击杀的情况下完成国家十环，并公平结算？',
 '救援责任、控制交接、反追踪、刺城主与炮塔等任务逐步展开；九环安东尼克由自爆开窗和队友接力完成，十环再追十刺客，408实交全奖后解散。98%源于早放走五人；完成十环不等于当时战争全部结束。中段任务编号冲突不自动改正。',
 ['dy-first-ring','dy-second-ring','z-c-q-task-numbers','ritual-power','end-war']),
('snail-candy','蜗牛的标记计与糖果由争到合','hidden','resolved',
 [51,52,55,61,62,63,64,97,98],
 '蜗牛为何在表面无功时仍能威胁团队，好胜糖果又如何从竞争者成为合作者？',
 '第一场蜗牛对局无胜负结算；回城袭击后标记之尘逐人上身，清粉与移位反用才完成合击击杀。糖果取消不公平计数赌，接受石剪布分配并在九环代理指挥；最终真正约战另由451研究证据确认，112场景未单收该战，不拿苍冥场景代指。',
 ['snail-winner','snail-tracking','snail-rematch','candy-bet','candy-duel']),
('phoenix','凤凰救援、有限复活与保留末次','hidden','partial',
 [66,69,97,102],
 '一次以本人死亡完成的护凤，所得有限复活能否兑现，又剩多少？',
 '护蛋目标成功但本人被天龙狂龙合杀，凤凰回报复活与羽毛；后来九环自爆消耗复活，422另用起搏器且此前收羽保末次。三次/五次数值冲突及最终库存未获解释，末战起搏复活者是萧翎，不能补成萧御耗尽或确定弃线。',
 ['phoenix-help','phoenix-count','soul-limit','final-feather']),
('behemoth','童灵赠物与幽灵比蒙的捕获养成','subplot','resolved',
 [30,75,74,77,96,97,101,104,109,110,112],
 '安抚与招魂能否从友情赠物变成真正可用的长期伙伴？',
 '公会分散牺牲拖狂暴、控血到600以下后实际捕获，宠物重置一级再以魂珠和双人群练养成；后续竞技、围战和神路持续使用并多次付死亡代价。不能把捕获前30级强化BOSS属性原样带入PK。',
 ['ghost-behemoth','ghost-capture-done']),
('blood-freedom','列昂的自由与赵的关键终结','subplot','resolved',
 [78,79],
 '渴望自由却要求他人绝对忠诚的列昂，能否摆脱霍尔斯控制？',
 '萧御宁弃任务护赵后受束缚；赵的梦魇破精神控制并完成霍尔斯尾刀，列昂给予人类恢复药和出口，两人实际恢复。列昂留在塌洞且叙述判必死，自由得到兑现而生还没有。',
 ['blood-freedom','z-c-q-blood-victory']),
('soul-ring','噬魂戒第一封与双戒纸余谜','hidden','partial',
 [79,86,88],
 '埃莫、双戒纸与噬魂封印的承诺是否全部得到解释？',
 '吸霍尔斯魂只解第一封并成为传说，后续吸石魔、女王没有第二封结果。第一层进展确成，人物身份、双戒纸和其余封印仍未明；石魔与女王场景只承载该次击杀，紧随的吸魂状态以独立问题证据补足。',
 ['soul-ring-identity','z-c-q-soul-next']),
('shadowsand','影砂个人赌斗与雇佣组织追击','hidden','partial',
 [39,96],
 '早期影砂赌斗之后，其现实雇佣组织的再次围杀是否得到全面处置？',
 '影砂先败死；后五人围攻被破，二死三逃，逃者放弃纠缠。386补明六人现实雇佣兵、接有偿凶杀和游戏谋利背景；没有六人全灭、组织覆灭或现实受惩的确证。',
 ['shadowsand-resolution']),
('arena-gods','刺刀标杆、全服冠军与最终友战','subplot','resolved',
 [21,39,41,42,54,60,70,76,93,99,100,101,105,106,108,109,111,112],
 '从旁观刺刀到第一人目标，最高竞技承诺最终如何分层兑现？',
 '414最高黑赛实胜刺刀并结算；452全服1v1与萧赵2v2夺冠，九胜包含熟人及炎神认输，苍冥退游赌约由主脑实际执行。463末战萧翎先死，萧御跳台余11%生还，复活后败者认输共饮；胜负明确，同时保留下位神对凡体的属性优势，不能拿早期停手切磋替换。',
 ['cidiao','cangming-wager','tangtang-brother','final-duel-result','god-player'])
]

threads=[]
for key,title,kind,status,nums,question,conclusion,qkeys in thread_specs:
    evs=[]
    for k in qkeys: evs.extend(qmap[k]['evidence'])
    for num in nums: evs.extend(by_num[num]['evidence'][:1])
    threads.append(dict(id='book-'+key,title=title,kind=kind,status=status,node_ids=ids(nums),question=question,conclusion=conclusion,evidence=dedup_evidence(evs),question_keys=qkeys))

# 原20条人工语义关系原样保留；不复制将问题账最近场景当代理的自动连线。
manual=json.loads((BASE/'causal-relations.json').read_text(encoding='utf-8'))['items']
links=[]
for old in manual:
    matches=[e for e in graph['edges'] if e.get('label')==old['label'] and e['from'] in by_id and e['to'] in by_id]
    assert len(matches)==1,old['label']
    edge=matches[0]
    links.append(dict(from_=edge['from'],to=edge['to'],kind=old['kind'],label=old['label'],evidence=dedup_evidence(old['evidence'])))

# 以下是对已读研究卡片的具体机制整合；echo只表示结构呼应，不表示角色回忆或因果。
extra_specs=[
 (1,2,'cause','试用头盔提供入游入口，职业尝试转为具体动作练习'),
 (2,4,'payoff','基础背刺、剔骨及完成度验证，进入头领战的瘫痪与出血控制链'),
 (2,9,'payoff','从失败动作到百分百的学习链，后来以实战102%突破原有上限'),
 (4,18,'echo','早期用控制填冷却取得胜利，遇冰法则因敌方先醒与减速反遭逃脱'),
 (5,37,'echo','鱼群嗜血与水潭洗毒腐尸，两次把刚观察到的生物或环境反应改成取利解法'),
 (6,14,'echo','先记巡逻与环境时窗，后把弩向、回头和读条等多个时间窗叠在一次潜入内'),
 (7,8,'cause','有限合作完成击杀后必须分掉落，集火让利把一次交易转为关系债'),
 (8,36,'echo','集火让利承认未来合作价值，后来萧御也承认治疗贡献而平分头骨'),
 (9,21,'reversal','突破100%证明完整动作的收益，旁观刺刀又发现短幅低伤但更快，单一完成度不再是唯一最优'),
 (12,13,'cause','接受潜入分工后亲自藏入营地死角，任务执行暴露无退路的具体风险'),
 (12,14,'cause','雇主提供机弩与头领情报、入口牵制和出口接应，使多时窗开箱方案有外部配合'),
 (13,14,'echo','藏点不能只看眼前安全，后续开箱也将读条完成与逃离条件同时纳入计算'),
 (14,16,'payoff','营地卷轴取得并交付后，银行实到千元才确认技术劳动支持现实'),
 (15,27,'echo','反手背刺被破解促成复盘与还招，后来对精算土法防线也以假动作换一次真实近身'),
 (17,43,'payoff','最初为妹妹忍自尊接受低租同住，收入足够后却因感情不愿搬走，外部贫困转为内部选择'),
 (18,41,'echo','冰环曾令主角先被控制而退逃，再遇冰环近败时突进接凿击产生新连贯'),
 (20,65,'echo','蜘蛛战拒援等待渔利与龙鹰合击后争抢，都暴露共同攻击目标并未建立共同收益规则'),
 (21,101,'payoff','早期旁观刺刀作为短幅标杆，最终正式最高黑赛实际交手并胜出；胜因仍包含双方资源条件'),
 (23,24,'cause','局部灵纹符与共享视野系统先被发现，首轮傀儡败损后才能用储备符重建围攻'),
 (24,25,'payoff','靠重建傀儡群取得回魔配方，再选择中立大市场把副本掉落按组织续航需求定价'),
 (28,33,'payoff','暂借圣言匕的移动与神圣伤害解决入场条件，最后仍需刺核心完成解咒'),
 (29,30,'payoff','与童灵建立友情所得安抚，被纳入隔怪、延迟苏醒和满完成度绕背的实际战术'),
 (34,51,'echo','因陌生人相守而偏离收益标准救援，进入队伍后则以亲自救宿命兑现队友责任'),
 (35,94,'payoff','任务名义下不敢承认的爱慕，后来进入父亲本人施压的现实场景，并以询问赵意愿守住关系'),
 (36,77,'echo','平分头骨先承认治疗与逃生劳动，后来以主角引怪填赵回复空档形成高收益双人生产线'),
 (39,96,'echo','同一组织先以影砂个人规则赌斗压迫，后以治疗和多法围杀施压；两次反制分别依赖保留技能与未知隐步'),
 (43,94,'echo','财富已能搬家后仍须回答自己的感情选择，父亲试探又要求其在金钱压力下维护赵的自主选择'),
 (44,48,'cause','救下被精英围攻的费思保住关键盟友，后续才可将经验集中培养他并制衡哈尔'),
 (48,49,'reversal','主角先通过培养费思防不可靠哈尔，女皇的占有诱惑最终使哈尔停援并被献祭，费思则自爆守誓'),
 (49,50,'cause','费思自爆把女皇打至零血并剥伪装，却不能终结不死本体，迫使主角使用专用神谕审判'),
 (51,55,'echo','糖果拒救暴露责任边界，后来主动取消不公平计数赌又显出其竞争仍有底线'),
 (55,64,'echo','先拒收不公平赌局的利益，后接受主脑认可的小游戏分配并守约，竞争逐步取得共同规则'),
 (56,60,'payoff','龙翔等突进组合先练会打断，正式对萨满仍先攻失败，再按图腾和低资源条件调整取胜'),
 (57,58,'cause','以月牙匕和旧陷阱终结暴熊才触发任务完成；随后的98%评价追溯先前放走五人，成功不等于最优'),
 (61,62,'cause','回城时蜗牛偷袭打破安全撤离，持续交锋又被其用于逐人附上标记之尘'),
 (63,64,'cause','清粉与移粉合击杀死蜗牛并得到肩与书，才产生两强竞争战利品和补偿其他队员的分配问题'),
 (66,102,'echo','护凤时本人战死却完成外部目标，异星脱困又主动选择可起搏复活的死处；死亡与目标失败不再等号'),
 (67,68,'payoff','转嫁危险后返身协作并教卫风斩杀，卫风随后独战旧友取胜，授艺通过独立行动验证'),
 (69,81,'echo','骨龙救尸以大量公会成员成本保个人收益，转职生产线又展示个人发现必须配套药钱、拾物、回魔装与防御'),
 (71,72,'cause','主坦硬扛强项无法解决斯卡机动，团队改为拖延守卫、抢出不可打断的开锁时间'),
 (75,74,'cause','公会分散牺牲拖完五分钟狂暴，使控血恢复可行，再降输出到捕获阈值实施招魂'),
 (74,77,'cause','捕获后比蒙重置一级，双人引怪与水瀑接续生产线才把伙伴实际培养到可用等级'),
 (74,101,'payoff','捕获并重养的比蒙在最高黑赛成为真实助力，刺刀付血将其击杀后才逼回一对一'),
 (78,79,'reversal','列昂从声称自由却要求绝对忠诚的威胁者，转为梦魇解控后的被救者，并给人药与出口而自身留洞'),
 (79,106,'echo','血族战由赵解控并完成尾刀，后续双人训练仍把控制交赵、主角专注输出并遮掩施法，伙伴能力持续独立生效'),
 (80,81,'setup','个人完成高评价转职后，新地图刷点被纳入药钱与公会防御体系，扩成集体转职优势'),
 (81,87,'echo','转职生产线已显示公会优势依赖资源和防御，吞魔域计划又被隐藏六会袭击校正为谨慎推进'),
 (82,83,'cause','刺城主让大军破城，却不自动处理炮塔；旧城民证被再用作伪装入塔、杀治疗和堵楼梯的工具'),
 (85,86,'cause','石魔战从反伤和仇恨试错推进到低血狂暴，末尾三段尖刺再要求无敌与治疗错开接续'),
 (90,91,'cause','缩小潜救已带出索德并取得神器，追踪暴露却引来五超阶追兵，巨人断后迫使双方返救'),
 (91,92,'payoff','索德定住玩家并燃命交戒的未结战斗，后以五敌同灭和巨人永眠给出不可逆结局'),
 (95,97,'echo','狂龙战通过可替代指挥保持己队秩序，安东尼克战又明确糖果接指挥、小鬼终结，让主角牺牲后任务仍能继续'),
 (97,98,'cause','接力击杀安东尼克获得神级战利品，队员自愿退出后仍需主角实际付款而非默认无偿占有'),
 (97,99,'setup','九环神级目标被接力击杀后仍未完成整串任务，第十环追十盗并以月白影子战兼作刺刀预习'),
 (101,109,'echo','刺刀战借比蒙和双体条件争胜，全服苍冥战再以本体、影子与比蒙连续追击耗尽逃技，召唤资源持续影响竞技'),
 (103,104,'cause','赵遭围杀并掉落首赠项链，使主角采取逐拆功能与保留复活希望的全团报复，之后仍承认怒气过度'),
 (104,105,'reversal','丛林对特定配置灭五十人的胜利，被本人拒绝推广为竞技常态；二对十偏利训练仍只杀六人而双亡'),
 (108,109,'echo','刀剑留终招因狂化晚一拍未翻盘，苍冥则被先耗逃技再以空场不确定性消耗蓝与信心；胜负都取决于资源时序'),
 (110,111,'cause','切断执金治疗蓝池并分杀守门者使神路打开，后续空间双门才将万人肉身战与单人分身战联通'),
 (111,112,'cause','双战场任务系统完成留下永久下位神格，末次友战萧御因此有对凡体萧翎的属性优势；临时主神力量已退')
]
for a,b,kind,label in extra_specs:
    links.append(dict(from_=by_num[a]['id'],to=by_num[b]['id'],kind=kind,label=label,evidence=dedup_evidence(by_num[a]['evidence']+by_num[b]['evidence'])))

for link in links: link['from']=link.pop('from_')
result=dict(source_id=graph['coverage'][0]['source_id'],core_title='为妹妹谋生 → 学会技艺与合作 → 自由选择 → 最高竞技与共同神战',core_event_ids=ids(core),threads=threads,links=links)
assert len(scenes)==112
assert 35<=len(result['core_event_ids'])<=55
assert all(k in by_id for t in threads for k in t['node_ids'])
assert all(e['from'] in by_id and e['to'] in by_id and e['from']!=e['to'] and e['evidence'] for e in links)
assert all(len(t['node_ids'])>=2 and t['evidence'] for t in threads)
assert len({(e['from'],e['to'],e['kind'],e['label']) for e in links})==len(links)
assert all(0<e['start_line']<=e['end_line'] and e['chapter_id'].startswith('ch-') for item in threads+links for e in item['evidence'])
members=set(result['core_event_ids'])|{k for t in threads for k in t['node_ids']}
assert members==set(by_id),set(by_id)-members
OUT.mkdir(parents=True,exist_ok=True)
(OUT/'zeidan-topology.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

incoming=Counter(e['to'] for e in links)
outgoing=Counter(e['from'] for e in links)
semantic_junctions=[n for n in scenes if incoming[n['id']]>=2]
semantic_branches=[n for n in scenes if outgoing[n['id']]>=2]
thread_count=Counter(k for t in threads for k in t['node_ids'])
thread_shared=[n for n in scenes if thread_count[n['id']]>=2]
isolated=[n for n in scenes if not incoming[n['id']] and not outgoing[n['id']]]
review=[
 '# 《贼胆》展示拓扑审阅',
 '',
 '本轮只对既有全书研究作展示整合，逐一审阅了112个场景的标题、摘要、目标/阻碍/选择/后果/状态变化和证据定位，并核对全书综合、结局审计、115项问题终态与原20条手写联系。本轮新增正文阅读量为0；未改写writing-vault、工具或Git。',
 '',
 f'- 原场景覆盖：{len(members)}/112；展示主干{len(core)}个；整书线{len(threads)}条（暗线{sum(t["kind"]=="hidden" for t in threads)}条）。',
 f'- 语义联系{len(links)}条：原20条手写关系全部保留，新增{len(extra_specs)}条。类型分布：'+ '、'.join(f'{k} {v}' for k,v in sorted(Counter(e['kind'] for e in links).items()))+'。',
 f'- 按语义边计：入边≥2的汇合节点{len(semantic_junctions)}个，出边≥2的分枝节点{len(semantic_branches)}个；跨至少两条整书线的共享场景{len(thread_shared)}个。阅读衔接边没有计入这些数量。',
 '- 原始场景数组并非严格阅读顺序：例如部分遗失城、捕宠场景先后交错。core_event_ids与各线node_ids均按原narrative_order重新排序。',
 '',
 '主干用于读取关键推进顺序，不自动声称相邻节点互为因果。只有links中的关系才是有说明和证据的语义连接。echo明确为研究者抽象出的结构呼应，不声称正文写过角色回忆；setup也不等于充分因果。',
 '',
 '## 重要边界',
 '',
 '- 哈蒙斯任务称名与390克文图斯古墓老者确认并存，无已证别名解释。身份揭晓并未独占一个原场景，故只在线索结论与证据定位中补足，不把邻近场景伪称为该画面。',
 '- 方盒仍只是主角猜测；460原盒消失，462系统本命任务实际完成，不能增写毁盒或实体指认。最终双战场任务完成、永久下位神格和暂时主神力量退去分开保存。',
 '- 赵父本人认可、婚约、恋人关系均有据；结尾只到起飞，没有抵达新星、婚礼或法律婚姻完成。',
 '- 最后两萧真战萧御获胜、余11%生还，败者起搏后认输；仍有下位神对凡体属性优势。不得用早期停手切磋替代终战结果。',
 '- 古德任务完成不等于沃卡德复生或黑幽灵关系已明；幽灵比蒙需捕获重置一级、培养和组织成本。凤凰三/五次数冲突与末次未补证不等于确定弃线。',
 '- 只有沃思被误杀造成赛娜支线明确中断可称abandoned；它在主干独立保留为判断失误的代价，但原112场景只收一个相关场面，未为满足“每线至少两节点”而造出第二节点或乱接相邻竞技。',
 '- 糖果451真正约战、国家十环交全奖、圣光城战争结算、老者390确认、新星起飞等在原研究均有证据，但112场景未逐个单收。允许thread结论据终态证据解释，不能借另一战斗节点伪称这些画面已被收录。',
 '- 现有graph.edges里从问题账生成的部分场景代理边不适合作语义联系（例如将“隐月之钥用途”接到卫风成长场景）。本展示层只保留20条手写边，再逐条添加具体机制，不改动原图。',
 '',
 '## 整书线',
 '',
 '|线索|种类|终态|场景数|',
 '|---|---|---|---|',
]
review += [f'|{t["title"]}|{t["kind"]}|{t["status"]}|{len(t["node_ids"])}|' for t in threads]
review += ['', '## 语义汇合节点', '']
review += [f'- {n["id"]}：{n["title"]}（入{incoming[n["id"]]} / 出{outgoing[n["id"]]}）' for n in semantic_junctions]
review += ['', '## 无语义边的独立节点', '', '以下节点已保留在主干或整书线中；现有研究不足以为其补充具体场景间联系，不以时间相邻代替因果。', '']
review += [f'- {n["id"]}：{n["title"]}' for n in isolated]
review += ['', '## 112场景逐一归置核对', '', '此表是既有研究场景的展示位置核对，不是新增正文阅读回执。', '', '|原场景序号|场景|主干|整书线|入/出语义边|', '|---|---|---|---|---|']
for i,n in enumerate(scenes,1):
    ts=[t['title'] for t in threads if n['id'] in t['node_ids']]
    review.append(f'|{i}|{n["title"]} · {n["id"]}|{"是" if n["id"] in result["core_event_ids"] else "否"}|'+ '；'.join(ts)+f'|{incoming[n["id"]]}/{outgoing[n["id"]]}|')
(OUT/'zeidan-拓扑审阅.md').write_text('\n'.join(review)+'\n',encoding='utf-8')
print(json.dumps(dict(scenes=len(scenes),core=len(core),threads=len(threads),hidden=sum(t['kind']=='hidden' for t in threads),links=len(links),manual_preserved=len(manual),extra=len(extra_specs),semantic_junctions=len(semantic_junctions),semantic_branches=len(semantic_branches),shared_thread_nodes=len(thread_shared),isolated=len(isolated)),ensure_ascii=False))
