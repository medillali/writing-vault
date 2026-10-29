"""卷八追加notes原子240—295逐项终判；不以匿名圆满后景清账。"""
import json,pathlib,hashlib
H=pathlib.Path(__file__).resolve().parent
rows=[x for x in json.loads((H/'local-question-pool.json').read_text(encoding='utf-8'))['candidates'] if x['volume']==8 and x['original_field']=='notes-unresolved']
J=[
('answered','population-claim-boundary','林说雪银两百万是玩笑/组织代表范围，不是实时在线主盟人口；1580不足千在线与战后话语不能混为同刻精确总表。',[1580,1597]),
('unknown','input-timing-mechanism','1598读秒后1.5秒出招与延2.7秒并列，预判提早指令可解释但原未说明输入队列；保实战胜果，不造精确预输入机制。',[1598]),
('unknown','competition-countdown-rule','源未给倒计时能否预下令/禁放的完整规则；不凭普通游戏常识判违规，也不擅补专用倒计时豁免。',[1598]),
('partial','competition-rule-version','第二季实放狼/天河飞行/AOE可证当前允许，前季限制与新季完整规章差异未解释；分赛季保存，不否定本场已执行。',[1597,1598]),
('answered','actual-event-priority','1598实际竞技行为应保，即使与旧季记载不同也不能删场景来造一致；规则差异作为另一未知，不把本场改成没放狼。',[1598]),
('unknown','probability-combination','18%是陆将7%与11%相加的口算，没有统计实测/独立叠加规则；本次买戒不证明一般游戏概率可线性相加。',[1598]),
('answered','valuation-and-utility','主实扣40万且实交北，战术目的是晕控补自身不稳；低稀有度不等无功能价值，但尚无北戴后统计可证效果提升数。',[1598]),
('answered','item-comparison-boundary','装备等级/稀有度与控制特效分轴评估；全身神器不直接取消低阶戒战术用途，也不据购买热情断言低阶全面强于神器。',[1598]),
('answered','efficacy-vs-cure','首剂90%是研究者转述有效预期，1599—1600短期实效而1604再发/1608最终无效，明确不是每次保证或根治率。',[1599,1600,1604,1608]),
('answered','fictional-medical-setting','编号药物与概率只按小说虚构科研及身体反应记录，不提供现实药方/剂量；后效不以现实指导方式外推。',[1599,1604]),
('unknown','expert-roster','全球专家大量参与为徐宁概述，源未给完整人员名单/国别统计；药物出来不能回填每个参与者身份。',[1599,1607]),
('answered','pain-and-efficacy','首针后剧痛/镇痛仍痛与十分钟后实感恢复可共存；1600实战延时消验证当时有效，不把注射痛直接等于药毫无作用。',[1599,1600]),
('unknown','source-player-count','1600初20人与右27/3刺的口径未列清，不补无证增援也不固定总30；现场清敌结局与精确初数分开。',[1600]),
('answered','prediction-vs-encounter','至少320是主看红图预期，外围315熊为实际、下层335王再现；区域/预测与所遇不同，不构同一对象等级硬矛盾。',[1600,1601,1602]),
('answered','past-report-vs-current-event','林纳震冰是论坛回述旧事，用于找入口；本段现场只有冰窟/追兵/王，不写林纳本章再现或复活。',[1600,1601]),
('unknown','source-stat-calculation','280%/1100万+按主算式口径保，没有全套同刻面板与取整说明，不自行反算改血值或添隐藏Buff。',[1600]),
('answered','anticipation-vs-death','以后难陪是病情担忧，1602—1603仍双人战/采药，1609明确赴美治疗；不将此次伤感当主已经死或最后行程确证。',[1601,1602,1603,1609]),
('answered','boss-plan-validated','1602王真杀/林尾刀，硬杀计划兑现，但清楚依双防、控制、吸血、两宠分身与合击，非无条件主一人秒王。',[1601,1602]),
('answered','combat-risk','1602七连若无两防主自认会死，实战仍需控王和吸血；无牧成功不等没有风险或所有王皆可硬扛。',[1602]),
('unrecovered','unrealized-commodity-valuation','蓝幽100棵1000RMB只是林报价，本次飞过未采/未售；之后29组仙云是另种原料，不能以它结清蓝幽收入。',[1601,1603]),
('unknown','source-damage-multiplier','1602突9倍与前7倍及1601匹配+20%未给清楚7→9换算；不能自行当新进化或四舍五入设定，原倍率异文保留。',[1601,1602]),
('unknown','source-damage-multiplier','匹配武器提升与9倍口径并列但无独立进化回执，轩辕仍可再进并不证本章已进；不研究者造特殊升阶修补。',[1601,1602]),
('answered','historical-knowledge-boundary','密草让林判断无人采过，论坛仅证旧采药者发现外草；无全图历史调查，不将本次丰收写从未有人进入任何洞。',[1600,1602,1603]),
('partial','observed-mount-and-estimate','飞骑落地换火犀是实见动作，可记形态转换；属性更强是主想必，缺面板/全表，不把推测扩所有坐骑规律。',[1602,1603]),
('unknown','inferred-enemy-stats','罗杰1400万血/敌30%破防由伤值反推而非独立面板；最终罗杰死可证胜负，不能反证估值精确。',[1603]),
('unrecovered','craft-and-sale','29组仙云采得已成，15药制作/交主队尚未给后证；本次摆摊无实收数，不能与1598五千收入并成另一笔。',[1598,1603]),
('unrecovered','item-equipping','冰玄甲口头分林，后来没有独立交付/穿装镜头；不能由两人已回城自动补装备过程。',[1602,1603]),
('answered','fictional-medical-setting','G12、粉末与治法只据小说医生发言/后续眼况，不拿现实指南强证小说病名，也不转成现实诊疗建议。',[1604,1605,1606,1609]),
('unknown','injury-attribution','主自认无力来自毒而非车祸，额淤/车报废也实在；无完整检查不证完全无创伤，不能把人物归因写医院排除。',[1604,1605]),
('answered','rescue-information','1605慕亲解电话异响断线知出事、逆路寻来；原因获后证，不再是完全未交代，具体定位设备仍无证不造。',[1604,1605]),
('answered','gift-vs-purchase','药库女免费赠粉末，主未付款而许治好后致谢；不替善意赠予补购药支出，后续交药另有实际回执。',[1604,1605]),
('partial','medicine-delivery-and-eyesight','1605药完好实交/医生配用，1606北报何能看北为改善；1609末疗日仍蒙纱，最终拆纱完全永久复明未展示。',[1604,1605,1606,1609]),
('unknown','source-geography','1605离苏赴杭州/余杭途中写抵达苏州继续北行不齐，未见改稿或绕行解释；保地名源差，不擅换杭州或造回苏。',[1605,1606]),
('unrecovered','rent-payment','房东允住/已供食可证租住执行，5000月租未见实际交款；房东厚待与主富有都不能清现金支付账。',[1605,1606,1609]),
('partial','visits-samples-and-return','鬼1606起多次实来送衣/剂，1608仍照护，主也自行抽样/徐报解析；但每日不缺/精确一月回与全部样本逐日送达未给，后记赴美另阶段。',[1605,1606,1607,1608,1609]),
('unknown','traffic-liability','慕靠关系保驾照是她自信话，源无司法/交管处理回执；实际逆行救人不独证法律上无责或现实规则如此。',[1605]),
('answered','risk-and-care','主撞车失力、慕逆路寻救均实际危险，关怀动机不消除风险；药真到不把这套危险做法泛化为照护准则。',[1604,1605]),
('answered','countdown-provenance','23天是陆从先前期限自计，非当日新检测；1608同样倒数属叙事时钟，后记未宣其精确必死日。',[1606,1608,1609]),
('partial','survival-and-treatment','主“会活过限”是愿望/承诺；1609明说仍治疗、林陪赴美与匿名活动强暗示生还，支持活着延续，却未给临床完全根治回执。',[1606,1608,1609]),
('answered','limited-medical-effect','1606再注后部分力回、1608后期几失效/完全无效，是阶段效力衰退；不以暂回力否定此前复发，也不判毒已清。',[1604,1606,1608]),
('answered','memory-vs-current-death','1606旧地回忆心受苏伦害不构新死亡，现实心当时仍活/后记仍寻主；游戏旧伤亡与现实当前状态分层。',[1606,1609]),
('answered','ranking-time','洛267第二为1606当时等级榜，不给终点全服最后名次；神装借出/匿名战士后景也不能重算该榜。',[1606,1609]),
('unknown','predicted-treatment-success','40%+是完全解析前提下的机器设想，1608最近87.2%、1609赴美治疗未展示成功样本率；不能写已成功治疗率40%。',[1607,1608,1609]),
('partial','funding-and-treatment-process','徐述500亿美元协议与董事会推动、后记实际赴美均有推进；银行全款、机器建成运行及完整疗程未展示，不把协议等支付完。',[1607,1609]),
('partial','tournament-and-loan','1608二队推进/主队淘汰，1609李实持世界冠军杯可证结果层；击烛具体局与正式系统MVP、轩辕等逐件归还仍未示，不用唯一MVP陆的情感话清账。',[1607,1608,1609]),
('answered','fictional-science-boundary','伽玛/雷姆数字为小说方案话语，审计只追方案—预测—赴美进程，不扩成现实医疗剂量或安全结论。',[1607,1609]),
('answered','countdown-reading','第17/15等按余日递减，与症状加剧并列；不能写从租住起已过17/15天而倒置先后，源未给精确日历则不补。',[1608]),
('answered','prognosis-vs-clock','倒数由主沿预估自计，不是精确生死时钟；1609仍治疗的明文不允许把余0当已死亡事实。',[1608,1609]),
('unknown','source-calendar','余15又称已住十几日与总30日为宽叙，缺具体日期表，不能硬补年月日来消差；保相对顺序可用。',[1608]),
('answered','care-vow-and-omission','主让鬼不来只是一项命令，鬼当场哭拒式劝生；1609仍与兄弟关切其治疗，留白不证鬼从此永久弃护。',[1608,1609]),
('partial','anonymous-arrival','1608来者捧手/叫小骗子，主近盲未认名；1609明示林独陪赴美强支持林为来者的推断，未把1608本身改写当面实名。',[1608,1609]),
('answered','terminal-evidence-boundary','末主仍治疗中明文与匿名活动强暗示排除直接写已死；同样没有临床百分百根治回执，保持生还暗示和病理未知两层。',[1609]),
('partial','survival-and-anonymous-scene','赴美/治疗中是实名转述，叫逸逸的神装战士与加州镜头强指陆林活动；匿名未全署名、没有疗程报告，推断不充事实直述。',[1609]),
('unknown','anonymous-identities','本书终景龙域241战士、书生今天不吃饭与加州男女未逐一实名；当前正式分卷接口未给这些镜头全部明确同人映射，不从纵横知识/盗版传说补名。陆林线索可强推但分开标识。',[1609]),
('unrecovered','compound-unclosed-accounts','逐项匹配终章后仍无林全排毒/主解析100%与疗程、五亿卡返、借装逐件返、月租实付、药库致谢回执。赴美与活动暗示不能替代这些独立医疗/财物/承诺账。',[1591,1595,1604,1605,1607,1608,1609]),
('answered','paratext-and-reading-boundary','完本感言/斩龙预告属于附文，只登记作品顺序；本代理本任务未取下一书正文，不能将新书预告计本书故事或斩龙已读。',[1609]),
]
assert len(J)==56
out=[dict(candidate_id=rows[i+240]['candidate_id'],status=s,audit_domain=d,rationale=r,later_chapters=c) for i,(s,d,r,c) in enumerate(J)]
p=H/'adjudications-local-note-v08-005.json';p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
md=['# 卷八追加notes原子005组（240—295，可主审）','','末卷新增296原子全部逐项匹配完；这是卷八补洞终判交审，非全书审计完成。','']
for x in out:
 row=next(r for r in rows if r['candidate_id']==x['candidate_id']);md += [f"## {x['candidate_id']} {row['title']}",'',f"{x['status']} / {x['audit_domain']}：{x['rationale']}",'','后证raw：'+', '.join(map(str,x['later_chapters'])),'']
(H/'local-notes-v08-reviewed-005.md').write_text('\n'.join(md),encoding='utf-8')
print(len(out),hashlib.sha256(p.read_bytes()).hexdigest())
