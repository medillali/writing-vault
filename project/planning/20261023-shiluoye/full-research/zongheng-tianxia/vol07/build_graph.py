import json,pathlib
P=pathlib.Path(__file__).parent
S=json.loads((P.parent/'source.json').read_text(encoding='utf-8'))
N=[json.loads(x) for x in (P/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines()]
BY={int(x['chapter_id'][3:]):x for x in N};SID=S['source_id'];REV=S['revision']
C=json.loads((P/'cards.json').read_text(encoding='utf-8'))
CH={x['origin_key'].rsplit('/',1)[1]:x for x in C if x['asset_type']=='character'}
SC={x['origin_key'].rsplit('/',1)[1]:x for x in C if x['asset_type']=='scene'}
def ev(ids,kind='fact'):
 return [dict(source_id=SID,revision=REV,chapter_id=BY[i]['chapter_id'],start_line=BY[i]['start_line'],end_line=BY[i]['end_line'],claim_kind=kind) for i in dict.fromkeys(ids)]
nodes=[dict(id='v07-root',title='卷七 圣域年代',kind='story',parent_id=None,claim_kind='fact',summary='raw0776—1060共285正文；两实际读者175+110全文覆盖，研究草稿。',evidence=ev([776,1060]))]
ARCS=[
 ('a1','败城、归零与协作重练',['relevel','lifeduel','qingfeng','sagelong','s3'],[776,826]),
 ('a2','远征成本与S4职业重组',['gale','s4'],[827,863]),
 ('a3','拆盟、现实自主与城毁重建',['split','business','destroy','mine'],[864,890]),
 ('a4','再取白云与军团生产',['bloodblade','industry','minewar','aryan'],[891,925]),
 ('a5','秦韵返回、日更据点和安定—烈虎',['qinreturn','points','annight','tiger','bait'],[926,962]),
 ('a6','遗迹财富、现实断裂与新合作',['relic','icewolf','redtrauma','canglong','recruit'],[963,1000]),
 ('a7','共同防御、梦境与蛮荒夺权',['threecities','audan','luoyue','dragonrace','wilds','dal','tianyao'],[1001,1039]),
 ('a8','关系知情差、逃亡和新门槛',['qinamerica','flowers','manhunt','xun','s6threshold'],[1040,1060])]
for aid,title,keys,ids in ARCS:
 nodes.append(dict(id='v07-'+aid,title=title,kind='arc',parent_id='v07-root',claim_kind='synthesis',evidence=ev(ids,'synthesis')))
 for key in keys:
  c=SC[key];nodes.append(dict(id='v07-'+key,title=c['title'],kind='scene',parent_id='v07-'+aid,narrative_order=min(int(e['chapter_id'][3:]) for e in c['evidence']),claim_kind='synthesis',summary=c['content']['summary'],asset_origin_key=c['origin_key'],characters=c['content']['characters'],evidence=c['evidence']))
ND={n['id']:n for n in nodes};edges=[]
def edge(key,a,b,kind,label,ids):
 edges.append(dict(id='v07-e-'+key,**{'from':'v07-'+a,'to':'v07-'+b},kind=kind,label=label,claim_kind='inference',evidence=ev(ids,'inference')))
edge('shield','qingfeng','sagelong','payoff','清风奖励150盾原105不能用，萨任务后159才实际装',[799,817])
edge('tank','sagelong','s3','setup','新盾先在九天塔前段验证；最终玄武暴露硬扛边界，秦发现死后续毒',[817,819,821,824,825,826])
edge('exile','split','business','cause','拆盟后父撤工作室与两选，书拒卡离苏在南京开店',[867,868,869])
edge('qreturn','split','qinreturn','payoff','空房删友不是永久消失，控诉与退租/返程/入会逐次修复',[867,918,933,935,936,937])
edge('mine','destroy','mine','cause','雨露重建需矿产，金窟救矿工接入村庄资源增长',[876,877,879,880])
edge('cavalry','industry','minewar','cause','银曜与毁灭剑军团在紫矿/平原正面检验，仍须弓控与点杀',[909,910,911,912])
edge('ally','qinreturn','points','cause','秦重新入会后与书香留守分兵主盟，三线险胜获分',[937,941,944])
edge('failure','annight','tiger','reversal','安定收回却知敌转曙光，于是毁烈虎传送、向其本城进攻',[949,951,952,953])
edge('bait','tiger','bait','cause','城破民心未零且敌千万来援，雪出两道牺牲线争主动',[957,958,959])
edge('p7','points','relic','payoff','据点积分带强化到赤霄+7并实际用在遗迹；连续退阶代价保留',[939,944,962,968,971])
edge('north','relic','icewolf','cause','野蛮多线来攻及青云委托把遗迹打宝者召回集团战',[973,974,975,976])
edge('violence','icewolf','redtrauma','setup','血饮临走现实威胁先出现，后来案情转述；只作线索不证明定罪',[979,980,981,982])
edge('kin','redtrauma','recruit','cause','红决定重建后花资源请书组队、买装/发薪，五核实际接受',[994,995,996,997,999])
edge('armor','canglong','threecities','payoff','龙丹交付学有限光辉圣甲、小青养到200，安定/暮色战实际使用',[992,993,1002,1005,1006])
edge('enemy','threecities','audan','reveal','最后敌首奥丹有人心存活，守城成功后切入净化梦任务',[1010,1011,1012,1013])
edge('human','audan','luoyue','echo','护民新统帅与主角争药商独家并列，随后圈地争端检验公益话语；比较而非直接因果',[1015,1016,1018])
edge('cave','luoyue','dragonrace','cause','战后主盟留冰巢，冰茶另派勇十万火巢，分兵被七星利用',[1020,1021,1022])
edge('exilewild','dragonrace','wilds','setup','冰火后随风追魂归入蛮荒，乱舞十万探索与小青运六人实入',[1023,1024,1025])
edge('city','wilds','dal','cause','救出卡洛琳返城交付时发现零坐标天钥，材料制甲再领军攻城',[1028,1029,1030,1031])
edge('deathloot','dal','tianyao','reversal','杀达尔同时死亡失去落地城权，七星实占，书北冥绑仓后返追索',[1035,1036,1037,1038,1039])
edge('bloodcontract','tianyao','manhunt','payoff','天钥换互援地齿承诺；书禁骑时先发百万援，七星后实际护书归营',[1038,1047,1054,1055])
edge('absence','qinamerica','s6threshold','payoff','登机、抵美后跨洋上线分阶段；五人实际聚S6而非约定即到，不宣称专线安装已证',[1042,1056,1058,1059,1060])
edge('branch','flowers','manhunt','cause','恋人已送花仍双死，书雪主动选屠镇复仇，禁骑通缉十二小时实触发',[1045,1046,1047])
edge('rumor','xun','s6threshold','setup','荀挑战经孤远侄资源进入带练，雪赴S6时新关系风险仍未决',[1057,1058,1059,1060])
def know(node,observer,content,ids,kind='fact',state='knows',belief=None):
 k=dict(observer='reader' if observer=='reader' else CH[observer]['origin_key'],state=state,content=content,claim_kind=kind,at_chapter_id=f'ch-{ids[-1]:04d}',evidence=ev(ids,kind))
 if belief:k['belief']=belief
 ND['v07-'+node].setdefault('knowledge',[]).append(k)
know('relevel','shusheng','早期按旧印象判断坐骑等级门槛；该信念尚未实测。',[779,781],state='misbelieves',belief='烈焰战马必须到100级才可召。')
know('relevel','shusheng','787在50级实际召烈焰战马，推翻先前100级门槛判断。',[787])
know('qinreturn','shusheng','918尚不知秦一直自租、从未与战魂成员同住。',[918],state='unknown')
know('qinreturn','shusheng','935秦亲述自己一直自租、从未住战魂，书此刻才得新信息。',[935])
know('qinreturn','qinyun','自己离开后未被挽留与一直独租，是其亲历信息；愿返晚于一次野外救助。',[933,935])
know('annight','shusheng','948估安定回防十万足守，只是预测。',[948],'inference',state='suspects')
know('annight','shusheng','949新报安定被屠、951再知王座转曙光，按新报更新。',[949,951])
know('redtrauma','reader','得知犯罪仍经围观/电话/论坛；红亲刺是书猜，七涉案全死无确证。',[980,982,987],'synthesis')
know('dragonrace','reader','raw1021私谈提前得知韩信等怨偏新人且拟献蛋回红。',[1021])
know('dragonrace','shusheng','冰巢抢尾后到安定才亲见五人换月神徽、蛋在红手。',[1022])
know('audan','reader','系统陨落结算后看见奥丹存活，人心与净化另开任务。',[1012,1013])
know('audan','audan','经历贵族杀亲又见茉莉追责/村人接待，自己出手后区分护民与护王。',[1014,1015],'synthesis')
know('qinamerica','shusheng','知道自己和秦已性关系，机场仍用醉酒搪塞雪。',[1041,1042])
know('qinamerica','lingyue','机场私问暗示猜到，但未见她已获全套细节；宽容自述不能替雪许可。',[1042],'inference',state='suspects')
know('qinamerica','lingxue','知书秦整夜未接；对酒店性关系细节未明确知悉，1056齿痕问题未追不等知允。',[1042,1056],'synthesis',state='unknown')
know('xun','shusheng','荀受孤带练为实报，孤借侄打压雪只内心推测。',[1059],'inference',state='suspects')
threads=[]
def thread(key,title,kind,status,keys,edgekeys,note,ids,resolution=None):
 t=dict(id='v07-t-'+key,title=title,kind=kind,status=status,node_ids=['v07-'+k for k in keys],edge_ids=['v07-e-'+k for k in edgekeys],stage_note=note,evidence=ev(ids,'synthesis'))
 if resolution:t['resolution_note']=resolution;t['resolution_evidence']=ev(ids)
 threads.append(t)
thread('growth','玩家圣域与装备使用门槛','main','partial',['relevel','lifeduel','qingfeng','sagelong','s3','canglong','threecities','tianyao','manhunt','s6threshold'],['shield','tank','armor'],'书270五永恒/苍穹盾已用；北冥275不能用，S6首王未战。',[779,817,993,1036,1055,1060])
thread('organization','雪月重建、军团生产与治理','main','partial',['split','business','destroy','mine','industry','minewar','points','wilds','tianyao'],['exile','mine','cavalry'],'重建与三郡一王实成，城市资源/分红/公开原则有持续张力；不是全书称霸终局。',[867,877,909,944,996,1029,1040])
thread('wars','大陆国战及边疆互守','main','open',['qingfeng','gale','bloodblade','annight','tiger','bait','icewolf','threecities','dal','tianyao','manhunt'],['failure','bait','deathloot','bloodcontract'],'多次主城回收与地齿守成，战争仍持续，不以一次退敌写全服灭绝。',[799,845,902,962,979,1055])
thread('qinreturn','秦韵出走及回归','subplot','resolved',['split','qinreturn','points'],['qreturn','ally'],'回归这一阶段已实证；身体/出国/多方感情另线仍开。',[867,935,936,937],'936退租返南京、937上线正式入雪月。')
thread('romance','多方关系与知情不对称','subplot','open',['qinreturn','qinamerica','xun','s6threshold'],['absence','rumor'],'秦关系已越身体界限、月主动吻且两人赴美；雪未明确知酒店、冰醉吻未定恋；荀新挑战。',[934,936,1013,1023,1041,1042,1058,1059])
thread('seal','灵儿封印和神格复苏','subplot','partial',['aryan','canglong','wilds','s6threshold'],[],'第三道即最后封：922解除宣布飞升/神格复苏，963醒后展示归零裸装；不是两道封或第四封。985明确228战神；母亲信息仍非已解。',[922,923,963,985,995,1037,1060])
thread('red','红绫受害、案情来源与重建','subplot','partial',['icewolf','redtrauma','recruit','dragonrace'],['violence','kin'],'现实案犯/复仇归因未定，红重建与收旧属已实，不能把该组织成就等创伤痊愈。',[979,980,982,987,994,999,1022])
thread('audan','奥丹恨意及保护对象转变','subplot','resolved',['threecities','audan'],['enemy'],'净化/梦境任务/正式授职已完成；安妮为何不可同法和要塞待建另未决。',[1012,1013,1015,1016],'1015梦境任务完成，1016菲雅正式授第九军团统帅并赴任。')
thread('moonreturn','旧属暗谈与两巢归蛋','hidden','resolved',['dragonrace','recruit'],[],'读者1021先知不倒灌主角；主角1022亲见徽记与红蛋。',[1021,1022],'1022五人已月神徽、红实际持冰龙蛋，私谈意图在行为兑现。')
thread('city','天钥实际归属','main','resolved',['wilds','dal','tianyao'],['city','deathloot'],'本次夺城已成，但守城、招兵、收益与互援承诺仍需后续。',[1029,1035,1036,1039,1040],'1039第一次杀实时城主七星，系统正式把天钥转雪；1040建设实用。')
thread('revenger','送花转复仇通缉','subplot','resolved',['flowers','tianyao','manhunt'],['branch','bloodcontract'],'12h生存惩罚任务已成；两恋真死、屠镇事实不被奖励撤销。',[1046,1047,1051,1054,1055],'1055系统确认血之复仇成功，骑乘恢复，苍穹盾实际穿。')
thread('s6','S6首通与新强化材料','main','open',['qinamerica','s6threshold'],['absence'],'已入本清一层小怪10火魄，首王祝融仅识面板和战策；未开打。',[1058,1059,1060])
G=dict(title='卷七 圣域年代：门槛、组织与知识边界',source_id=SID,revision=REV,review_status='draft',coverage=[dict(source_id=SID,revision=REV,chapter_ids=[n['chapter_id'] for n in N],complete=False,complete_volume=True,note='285正文全量由两读者分段全文覆盖，complete:false指尚非全书。')],nodes=nodes,edges=edges,threads=threads)
(P/'graph.json').write_text(json.dumps(G,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
A=json.loads((P/'analysis.json').read_text(encoding='utf-8'));A['threads']=threads;(P/'analysis.json').write_text(json.dumps(A,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('graph nodes',len(nodes),'edges',len(edges),'threads',len(threads))
