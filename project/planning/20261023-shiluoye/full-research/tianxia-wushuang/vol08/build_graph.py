import json,sys
from common import *
sys.stdout.reconfigure(encoding='utf-8')
cards=R('cards.json');SC={c['origin_key'].rsplit('/',1)[1]:c for c in cards if c['asset_type']=='scene'};CHARS={c['origin_key'].rsplit('/',1)[1]:c for c in cards if c['asset_type']=='character'}
nodes=[dict(id='w08-root',title='卷八 天下无双',kind='story',parent_id=None,summary='105片/104正文由primary与agent3分工全文覆盖；从苏醒、制度和国战转至求治、隐居与后记。结尾明示赴美治疗，匿名镜头强暗示恢复，未给绝对病愈回执。',claim_kind='synthesis',evidence=ev([1505,1609],'synthesis'))]
ARCS=[
('a1','现实苏醒、交易与代理控制',['wake','auction','contract'],[1506,1513]),
('a2','尊严重建与不同成神路径',['pigduel','restart','promotion'],[1514,1526]),
('a3','护送目标与毁炮成本',['escort','cannon'],[1527,1541]),
('a4','技术权威与亲密边界',['lige','intimacy'],[1542,1545]),
('a5','国战防御、反诱与组织归属',['fort','greatwall','lure','chiyu','rescue','join'],[1546,1571]),
('a6','城权收割与身体崩倒',['shield','artillery','yaner','zhuore','tianhuang','qingtu','capitals'],[1572,1588]),
('a7','求治、日常与短暂恢复',['wakeill','cardmoney','public','antigen','family','wel','inhibitor','icecave','eyemed'],[1589,1604]),
('a8','隐居、托付与分层结尾',['hide','handover','countdown','epilogue'],[1605,1609])]
for aid,title,keys,ids in ARCS:
 nodes.append(dict(id='w08-'+aid,title=title,kind='arc',parent_id='w08-root',claim_kind='synthesis',evidence=ev(ids,'synthesis')))
 for key in keys:
  c=SC[key];nodes.append(dict(id='w08-'+key,title=c['title'],kind='scene',parent_id='w08-'+aid,narrative_order=min(int(e['chapter_id'][3:]) for e in c['evidence']),summary=c['content']['summary'],asset_origin_key=c['origin_key'],characters=c['content']['characters'],claim_kind='synthesis',evidence=c['evidence']))
ND={n['id']:n for n in nodes};edges=[]
def edge(k,a,b,t,label,ids):
 edges.append(dict(id='w08-e-'+k,**{'from':'w08-'+a,'to':'w08-'+b},kind=t,label=label,claim_kind='inference',evidence=ev(ids,'inference')))
edge('restart','pigduel','restart','cause','旧号自删后另建新号，陆安排现实见面、装备与带练；不是系统复活旧号。',[1519,1522,1523,1524])
edge('newpig','restart','yaner','payoff','新战士号在燕耳实际救林、杀雷洛，1580才向林揭小猪身份；归来不撤消本次游戏阵亡。',[1522,1524,1579,1580])
edge('godescort','promotion','escort','setup','伙伴成神和各职业能力为护车协作提供条件，仍有失败概率、护送目标与不可参战NPC限制。',[1514,1526,1527,1530,1531,1535])
edge('cannonmission','escort','cannon','cause','护送途中发现战略炮威胁，三车实际交付成功后另组织毁炮，不能把任务交付并成毁炮奖励。',[1530,1535,1536,1541])
edge('othercannon','cannon','greatwall','echo','先前十炮实毁，与另一基地/长城三炮并存；呼应战略威胁，非前十炮复活。',[1541,1555,1556,1557,1558])
edge('control','lige','greatwall','echo','两局决斗和长城战都把控制、免伤与恢复拆成窗口；只作机制比较，不说决斗直接造成攻城成功。',[1543,1544,1556,1557])
edge('chiyu','chiyu','zhuore','payoff','何艺工匠先实架七器，灼热战再部署十一蚩尤翎点敌机，幕后研发经后场实际调用。',[1564,1581])
edge('counterlure','lure','rescue','echo','己方落雁诱敌获胜后，盟友在婆娑被反诱；比较知情、诱饵与救援代价，不硬立敌计划由此模仿。',[1559,1560,1561,1563,1566,1567])
edge('newalliance','rescue','join','cause','救援与战后协商推动魂归骨干选择加入，1571换真实第二独立分盟徽；灭神伪徽仍另层归属。',[1566,1570,1571])
edge('regroup','rescue','shield','setup','救援后的伤亡与重组是新一轮增援攻燕耳的条件；不把陆下线前所有调兵都说已兑现。',[1570,1571,1572,1573,1574])
edge('alarm','shield','artillery','cause','外围暂退后真实休息，随后天岭警报中断睡眠；陆重返战场侦炮、踩点传军。',[1574,1575,1576])
edge('twolines','artillery','yaner','echo','陆守天岭与林攻燕耳双线并行；陆到时林已完成最后双杀，不能倒灌其为林胜因。',[1576,1578,1579,1580])
edge('nextcity','yaner','zhuore','setup','燕耳本次已废弃，转灼热成下一战略部署；不是所有燕耳参战者即时恢复后都能随军。',[1579,1580,1581])
edge('tianhuang','zhuore','tianhuang','cause','灼热攻势受野性王座领地与NPC援军牵制，陆查资源与权限后转攻天荒。',[1581,1582,1583,1584,1585])
edge('priority','tianhuang','qingtu','cause','野王主力死亡、盟友趁空取城使战略优先转向青土；不是天荒废弃自动给青土产权。',[1585,1586])
edge('conquer','qingtu','capitals','echo','都把斩首、取权杖、选择征服和战后确认分开；英雄王死但英雄城终被守住，构成边界反证。',[1586,1587,1588,1589])
edge('collapse','capitals','wakeill','cause','英雄王战后游戏身体消散，现实昏迷四日才醒；胜局和现实失能分别结算。',[1588,1589,1590])
edge('depend','wakeill','wel','cause','脑延与现实失能使参赛方案改为队友、宠与预判；五场小组胜仍非冠军，后来缺席淘汰。',[1590,1594,1597,1598,1606,1608])
edge('entrust','wakeill','cardmoney','cause','死亡风险和时间压力推动孝养委托，鬼实收卡是代保，未显示钱已花、父母义务已尽。',[1589,1590,1591])
edge('research','public','antigen','setup','行云实送资料与已开始的抗原采样汇入研究；送资料并非此前取样的原因，取样者身份到1595才明揭。',[1593,1594,1595])
edge('drug','antigen','inhibitor','cause','取样和模拟衰毒过程支持编号抑制剂研发，初次自感恢复仍要与当天失效及未来机器方案区分。',[1595,1597,1599,1600,1604,1608])
edge('playagain','inhibitor','icecave','payoff','首剂后实际反应恢复支持冰窟双人采集战，不倒推为根治或终生稳定。',[1599,1600,1601,1602,1603])
edge('notcure','inhibitor','eyemed','echo','同日取眼药途中毒发失力，给初次恢复以反证；不说抑制剂导致何艺先天眼疾。',[1599,1600,1603,1604])
edge('hide','eyemed','hide','cause','何需休养、主衰败加剧推动假出国真实藏余杭；保护意图不等被隐瞒者已同意。',[1604,1605,1606])
edge('decline','hide','countdown','setup','独居、供药与寻人构成末段日常条件，症状来自冰毒进展，不能说隐居造成病衰。',[1605,1606,1607,1608])
edge('lend','hide','handover','cause','无法继续赛事且预备后事时，主实际把七神装借李，保留一月归还约；不只口头祝胜。',[1606,1607,1608])
edge('cup','handover','epilogue','payoff','借装后二队实胜三队，后记李持冠军杯；具体最后击烛与系统MVP、神装归还均未展示。',[1607,1608,1609])
edge('return','countdown','epilogue','payoff','来者叫小骗子后，后记明确林独陪赴美治疗，再以匿名生活/游戏镜头强暗示恢复；主文未写死亡、机器治愈过程未展示。',[1608,1609])
def know(node,who,text,ids,state='knows',kind='fact',belief=None):
 d=dict(observer='reader' if who=='reader' else CHARS[who]['origin_key'],state=state,content=text,at_chapter_id=CH[ids[-1]]['chapter_id'],claim_kind=kind,evidence=ev(ids,kind))
 if belief:d['belief']=belief
 ND['w08-'+node].setdefault('knowledge',[]).append(d)
know('wake','xin','醒前担心现实的另一世界没有哥哥；这是恐惧而非已被证明的信念。',[1506],state='suspects',kind='inference')
know('wake','xin','现实醒后以触碰、相见确认陆存在；仍需学步/护理。',[1508,1513])
know('contract','xin','对产权与巨额财产意义理解不足；签字不等充分懂所有制度后果。',[1509,1512],state='unknown',kind='inference')
know('promotion','lu','幸运50或可三次必神属自己的预期，林与何的实际试晶有失败，不能当系统保证。',[1514,1519],state='suspects',kind='inference')
know('cannon','reader','观察范围是三成品加七在铸，1541十炮被毁，未观察全世界全部炮。',[1536,1541])
know('greatwall','lu','从侦报获知另炮基地与三炮，不能把旧十炮毁作当前无炮的充分证据。',[1555,1556])
know('fort','reader','1569外部镜头显示维也纳调天岭计，陆此时未在场，后来需靠警报/侦察得知。',[1569],kind='synthesis')
know('join','lu','灭神只是伪徽同色，魂归1571才正式第二独立分盟；两者权限不能合并。',[1566,1571])
know('yaner','lin','战斗后获新号本人保密揭名，才确认小猪身份；此前读者与陆的知识不自动共享给她。',[1579,1580])
know('qingtu','xu','实接王者权杖并获得当前NPC指挥权；不自动知道最终国战与90日后效全部兑现。',[1586])
know('capitals','reader','当场杀英雄君主不能判征服，1589战后确认四城而英雄被保。',[1588,1589])
know('antigen','lu','见血样/前情推测抗原取自林，1595才现场与本人、取样者及徐宁确认。',[1594],state='suspects',kind='inference')
know('antigen','lu','1595现场得知林自愿抗原采样的代价与程序，留下陪她；七日排净/30%仍是研究者预测。',[1595])
know('inhibitor','lu','首次给药十分钟后当前反应恢复，有实战验证；不知道是否根治，后续实际反复。',[1599,1600,1604])
know('eyemed','he','慕隐瞒返程车祸，何没有完整得知主取药途中失能的代价；暂放心不是知情同意。',[1605],state='unknown',kind='inference')
know('hide','he','识出国说辞可疑，持续试图追寻；不可写她已相信主真实出国。',[1605,1606],state='suspects',kind='inference')
know('hide','gui','实际代驾并独知精确住址，送样药衣物；其他人只知江南小镇或寻找线路。',[1605,1606,1607])
know('countdown','lu','近盲时只听来者叫小骗子，文本强指林，主文当场未实名来者。',[1608],state='suspects',kind='inference')
know('epilogue','reader','林独陪陆赴美治疗明示；匿名加州亲密/金剑斗罡叫逸逸强暗示陆林及活动恢复，临床治愈与何拆纱未知。',[1609],state='suspects',kind='synthesis')
threads=[]
def thread(k,title,kind,status,keys,edgekeys,note,ids,res=None):
 t=dict(id='w08-t-'+k,title=title,kind=kind,status=status,node_ids=['w08-'+x for x in keys],edge_ids=['w08-e-'+x for x in edgekeys],stage_note=note,claim_kind='synthesis',evidence=ev(ids,'synthesis'))
 if res:t.update(resolution_note=res,resolution_evidence=ev(ids))
 threads.append(t)
thread('wake','心然现实苏醒与代理控制','main','partial',['wake','contract','restart','countdown','epilogue'],[],'真醒、双合同签字和总公司确认已成；现实理解/独立生活仍渐进。后记心寻乡未相见，未用游戏全能补现实成年。',[1507,1508,1512,1526,1608,1609])
thread('auction','噬灵鞭竞拍与返款','subplot','resolved',['auction'],[],'仅关闭本次竞拍/返款，不关周未来安全与护卫谈判；金币与RMB不按未知汇率强算总净利。',[1509,1510,1511],'1510—1511成交扣费兑钱，2亿RMB实际返周，周已实际召虎。')
thread('pig','小猪尊严与另号重建','subplot','partial',['pigduel','restart','yaner'],['restart','newpig'],'旧号真删、新号真重练；燕耳林获知身份，小猪本次游戏又死。赤龙臂1592录像转述有使用，交还动作未场景化。',[1516,1519,1522,1524,1579,1580,1592])
thread('growth','神级资格、职业与操作边界','subplot','partial',['promotion','escort','greatwall','wakeill','wel','inhibitor','icecave'],['godescort','depend','playagain'],'神晶和职业积分第一随机两链分开；神级仍需要条件、治疗与同伴。病者恢复只短效，不借终章暗示补全根治。',[1514,1519,1526,1557,1562,1578,1590,1599,1600,1604])
thread('cannon','护送与分基地毁炮','main','resolved',['escort','cannon','greatwall','fort','chiyu','artillery','zhuore'],['cannonmission','othercannon','chiyu'],'本卷可核三车交付、十炮毁、长城三炮毁、天岭三炮团毁；不泛称世界永久无炮，器械金属规则冲突另列。',[1535,1541,1558,1564,1578,1580],'1535三车任务成功，1541十炮实毁，1558长城破，1578—1580三炮团实毁。')
thread('authority','公共权威与盲战控制','subplot','partial',['lige','greatwall','public'],['control'],'离歌两局真败、第三因照护中止；公证600万未给实际到账。现实对手致敬也不撤游戏竞争。',[1542,1543,1544,1557,1593])
thread('war','国战指挥、诱敌与不可兼救','main','partial',['fort','greatwall','lure','rescue','join','shield','artillery','yaner'],['counterlure','newalliance','regroup','alarm','twolines'],'救援部分成功、8394己方真亡。战天一亿实到陆而逐人分赔未兑现且币量有冲突；斗游戏死而现实火锅，不能以主胜抹亡者。',[1554,1563,1569,1570,1571,1574,1579,1580])
thread('recruit','真假徽记与自主入盟','subplot','partial',['pigduel','restart','rescue','join'],['restart','newalliance'],'雇佣/结盟/伪徽/独立分盟区别；魂归1571实际换徽，后居住建议还不是搬家回执。',[1519,1520,1522,1566,1570,1571,1592])
thread('cities','征服、废弃、城权与盟友利益','main','resolved',['yaner','zhuore','tianhuang','qingtu','capitals','wakeill'],['nextcity','tianhuang','priority','conquer','collapse'],'本次国战终判关闭，不声称此后90日所有约束实际完整执行；巨象俄控、燕耳与天荒废弃，英雄城保留。',[1579,1585,1586,1588,1589],'1589终战报告明确征服青土/七星/泰坦/灼热四城、英雄城被保；单杀君主不替代此终判。')
thread('money','财产、孝养与组织资源','subplot','partial',['contract','cardmoney','public','hide','handover','epilogue'],['lend','cup'],'25%签字/代理已生效，估值不是现金；五亿鬼代保未返未花、借装未明还、500亿美元协议和机器尚不能记治愈完成。',[1512,1526,1591,1594,1607,1608,1609])
thread('care','抗原研究、照护与知情权','main','partial',['wakeill','cardmoney','public','antigen','family','wel','inhibitor','icecave','eyemed','hide','countdown','epilogue'],['entrust','depend','research','drug','playagain','notcure','hide','decline','return'],'采样先秘密后明揭、自主付出和隐瞒代价并列。抑制初效/再失效/机器解析87.2%/赴美实治不同层，后记强暗示恢复非临床根治。',[1589,1591,1593,1595,1599,1604,1605,1606,1608,1609])
thread('wel','WEL参与权、借装与冠军杯','subplot','partial',['wakeill','wel','hide','handover','epilogue'],['depend','lend','cup'],'首夜五胜→主队缺席最终淘汰；二队持杯有物证，最终击烛具体局/系统MVP/借装归还未给。',[1594,1598,1606,1607,1608,1609])
thread('intimacy','多方亲密与结尾辨识边界','subplot','partial',['intimacy','family','eyemed','hide','countdown','epilogue'],['hide','decline','return'],'林独陪赴美明示，匿名生活/游戏镜头强指陆林；何1609末疗蒙纱、心未成年仍受护，不补全排他协议/婚礼/绝对病愈。',[1545,1595,1596,1605,1608,1609])
for t in threads:
 for eid in t['edge_ids']:
  e=next(e for e in edges if e['id']==eid)
  assert e['from'] in t['node_ids'] and e['to'] in t['node_ids'],(t['id'],eid)
G=dict(title='无双卷八：制度、国战与求治的分层收束',source_id=SID,revision=REV,review_status='draft',reading_attribution=R('reader-merge-validation.json')['reading_attribution'],coverage=[dict(source_id=SID,revision=REV,chapter_ids=[n['chapter_id'] for n in N],complete=False,complete_volume=True,note='105片/104正文分工全覆盖；primary亲读1505—1572共68片，agent3亲读1573—1609共37片。图为agent3读完两方逐章笔记后综合，complete:false非全书独读。')],nodes=nodes,edges=edges,threads=threads)
W('graph.json',G);A=R('analysis.json');A['threads']=threads;W('analysis.json',A)
print(json.dumps(dict(nodes=len(nodes),edges=len(edges),threads=len(threads),knowledge=sum(len(n.get('knowledge',[])) for n in nodes)),ensure_ascii=False))
