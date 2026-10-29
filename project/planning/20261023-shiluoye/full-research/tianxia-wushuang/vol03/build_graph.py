import json
from pathlib import Path
P=Path(__file__).parent;S=json.loads((P.parent/'source.json').read_text(encoding='utf-8'))
SID,REV=S['source_id'],S['revision'];N=[json.loads(x) for x in (P/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()];C={int(x['chapter_id'][3:]):x for x in N}
cards=json.loads((P/'cards.json').read_text(encoding='utf-8'));CH={x['origin_key'].rsplit('/',1)[1]:x for x in cards if x['asset_type']=='character'};SC={x['origin_key'].rsplit('/',1)[1]:x for x in cards if x['asset_type']=='scene'}
def es(ids,k='fact'):
 return [dict(source_id=SID,revision=REV,chapter_id=C[i]['chapter_id'],start_line=C[i]['start_line'],end_line=C[i]['end_line'],claim_kind=k) for i in dict.fromkeys(ids)]
nodes=[dict(id='w03-root',title='卷三 群雄并起',kind='story',parent_id=None,summary='raw0229—0606共378片/376正文全读；本卷阶段已完成研究，末段两场领地战仍未终结。',claim_kind='synthesis',evidence=es([229,606],'synthesis'))]
ARCS=[
('a1','兄妹、疗伤与紫罗兰复国',['tower','auction','father','medicine','violet','escort'],[230,312]),
('a2','现实冲突、职业成长与谁主沉浮',['assault','dragonblade','shieldcraft','tournament'],[337,426]),
('a3','领地、生产与寒刃战争',['firstcity','darkmoon','tiya','bridge','coldblade','fiveturn'],[437,503]),
('a4','生活、第二城与职业化',['countryside','secondcity','sponsor','underground'],[504,528]),
('a5','九龙争夺与工具回收',['entry','goldice','earth','nine'],[529,564]),
('a6','俱乐部、事业独立与回家',['club','raincube','tigeralchemy','home'],[565,584]),
('a7','招募、组织信用与承诺战争',['lubu','xiaoman','promise','valley'],[585,606])]
for aid,title,keys,ids in ARCS:
 nodes.append(dict(id='w03-'+aid,title=title,kind='arc',parent_id='w03-root',claim_kind='synthesis',evidence=es(ids,'synthesis')))
 for key in keys:
  c=SC[key];nodes.append(dict(id='w03-'+key,title=c['title'],kind='scene',parent_id='w03-'+aid,narrative_order=min(int(x['chapter_id'][3:]) for x in c['evidence']),summary=c['content']['summary'],asset_origin_key=c['origin_key'],characters=c['content']['characters'],claim_kind='synthesis',evidence=c['evidence']))
ND={n['id']:n for n in nodes};edges=[]
def edge(k,a,b,t,label,ids):edges.append(dict(id='w03-e-'+k,**{'from':'w03-'+a,'to':'w03-'+b},kind=t,label=label,claim_kind='inference',evidence=es(ids,'inference')))
edge('sword','tower','violet','payoff','先前实际交付的镇魔剑在紫罗兰封门复国阶段使用；不是王剑化尘后获得另一武器。',[234,302,303])
edge('healing','father','medicine','cause','心然反噬/替伤产生疗药需求，花需实际交付才治疗，而非击杀道格斯即愈。',[254,255,259,274])
edge('return','medicine','violet','payoff','心然疗伤后在复国战实际回归主伤，陆只是最后补击。',[274,302,303])
edge('blade','dragonblade','tournament','payoff','105实穿偷天、群技与四转在竞技中使用，仍2:1险胜烛/1:2真败雪银。',[368,371,372,415,421,423])
edge('shield','shieldcraft','firstcity','setup','制作与实穿先增强何前排条件，领地厅内实战仍有多角色死亡与换锋。',[389,442,448,450])
edge('economy','firstcity','darkmoon','cause','系统古剑占城并授陆管理之后才有建设、传送广告和分红生产。',[450,453,455,518])
edge('drugs','tiya','coldblade','payoff','试炼得破魔/烈刃后真实用于舞神/寒刃战争，破魔面对大招等级差会失效或只削一半。',[465,469,489,490,499])
edge('invasion','bridge','coldblade','cause','叛王保杖导致桥夜灵入、求卡援，十波守城继而发生。',[473,474,475,479,497])
edge('promotion','coldblade','fiveturn','setup','寒刃战争提供向导师交付的任务恢复条件；501真实交付才五转白金，502另付学费学技，不以战后相邻顺序直接立因果。',[500,501,502])
edge('mobility','darkmoon','secondcity','payoff','领地分兵/火马重练与名将编组用于第二领地，古剑主攻后换盟友雪银取得产权。',[460,510,512,515])
edge('fame','sponsor','club','cause','华硕先商谈再签约开业，公开品牌义务/嘉宾身份带来两俱乐部友谊赛压力。',[525,526,566,567,568])
edge('identity','underground','nine','setup','地下匿名红毛550才揭百战者/战天第一分盟，现实报复通过同一人接入九龙的敌会冲突。',[527,528,550,551,555])
edge('tank','goldice','nine','payoff','金王赤岩甲已穿，血煞与旧神怒在九层反击真正联动；仍由慕/吻/洛接救收尾。',[536,560,561])
edge('learning','goldice','earth','payoff','乱月四骨镰现场简易穿、碎石首学后在隐洞内清路，获得让尾新名将。',[544,546,548,549])
edge('loss','nine','club','echo','九龙先险胜并不消除操作差/赛制不利，线下1:4真败后队友KOF另胜；仅作两种团队评估比较。',[561,564,568,570,571,572])
edge('funding','sponsor','raincube','setup','合同提供持续收入预期，何决裂GGS后现金紧，实际支持仍是陆售装与两笔1000万转款；不是年薪已全付。',[525,574,575,584])
edge('care','raincube','home','cause','两女为筹公司分赴沪杭，慕已签先发协议返程遇事故，取包与救人同属真实后果。',[579,581,582,583])
edge('recooking','tigeralchemy','valley','payoff','灵烹8的力量药实际制/分许杜，降低五转力量门槛；谷战壁垒锋线显示组织产能，不声称每位五转都由该药促成。',[581,584,589,590,604,605])
edge('cavalry','tigeralchemy','valley','payoff','从青虎捕获100/400到3097真成，外线机动追杀并切骑神，谷军为其争回城时间。',[578,588,598,600,604,606])
edge('scholar','nine','lubu','payoff','九龙灼热扇与血颅紫龙书先存后实际交吕，603才报已学，未成为名将。',[544,580,588,589,603])
edge('accountability','lubu','xiaoman','cause','为吕收第八/允自治后，零度用古剑名清场伤人，招小蛮须承担该组织信用债。',[588,589,591,594,595,596,597])
edge('debt','club','promise','payoff','WSL制1:4赌的第三城不争在598明确仍有效，外围截杀为角色规避方案，非赌已撤。',[568,570,571,572,598])
edge('split','promise','valley','cause','暗月诸侯令迫分兵：鬼青虎继续西外截，陆七千青石谷挡援、杜薛护传送；需撑时而非独歼30万。',[598,599,600,604])
edge('plunder','earth','valley','payoff','让尾得掠夺，末606乱月以高爆率击杀拾斧刺客，追回斗卓越无敌仍包中，未复活斗。',[549,602,606])
def know(node,who,text,ids,state='knows',kind='fact',belief=None):
 d=dict(observer='reader' if who=='reader' else CH[who]['origin_key'],state=state,content=text,at_chapter_id=C[ids[-1]]['chapter_id'],claim_kind=kind,evidence=es(ids,kind))
 if belief:d['belief']=belief
 ND['w03-'+node].setdefault('knowledge',[]).append(d)
know('entry','lu','看金光冲入前误以为是可拾金币。',[531],state='misbelieves',belief='山谷闪光是可拾金币。')
know('entry','lu','冲入后观察确认只是金色石头，且已引出怪。',[531])
know('entry','reader','该批怪没有针雨由鬼指出，不能把刚前门解法无差别套所有木刺猬。',[531])
know('underground','lu','红毛身份/后台尚未知，一流与背后大势只是根据操作推测。',[528],state='suspects',kind='inference')
know('underground','lu','550面对面互认红发百战者，再由主盟援兵确认战天第一分盟链。',[550,551])
know('goldice','reader','林自述杀生命龙但木鳞烛拿，系统换层公告证烛持木；尾刀不等持物。',[537])
know('nine','lu','自己临返反击将殿后李被钉的同岩壁用来钉烛，鬼预随施者死清。',[560,561])
know('home','lu','失联时只猜堵路或信号；初见车型无A8误放心，直到埋土车尾555才确认。',[581,582],state='suspects',kind='inference')
know('home','reader','慕车内未动不等已经死亡；醒活后急诊仅额伤/留观一夜。',[582,583])
know('raincube','he','581只确定蓝星合作意向，没有正式协议，要注册后凌雪查看实力。',[581])
know('lubu','reader','586被杀的是75%分身，587明揭；本体不死、无掉级与不死触发。',[586,587])
know('lubu','lu','起初以吕旧恩与抗敌表现判断零度可靠，后目睹他主导清场，选择因吕暂保他。',[588,594,595],state='suspects',kind='inference')
know('xiaoman','xiaoman','亲历第八清场，拒七件补装/先拒古剑，第二救援后按条件加入主盟。',[594,595,596,597,598])
know('promise','luanyue','三会攻城时推测十月唆使，尚未直接验证。',[598],state='suspects',kind='inference')
know('promise','lu','599得凌雪殇小道消息游说链，仍不是亲见秘密会议或系统定因。',[599],state='suspects',kind='inference')
know('valley','reader','本卷末斗已真死，斧在乱包、双弓已被陆北合杀；5000幽灵骑才出现，后战结果未知。',[606])
threads=[]
def thread(k,title,kind,status,keys,edgekeys,note,ids,res=None):
 t=dict(id='w03-t-'+k,title=title,kind=kind,status=status,node_ids=['w03-'+x for x in keys],edge_ids=['w03-e-'+x for x in edgekeys],stage_note=note,evidence=es(ids,'synthesis'))
 if res:t.update(resolution_note=res,resolution_evidence=es(ids))
 threads.append(t)
thread('growth','职业/种族/装备与技能门槛','main','partial',['tower','dragonblade','tournament','coldblade','fiveturn','goldice','nine','tigeralchemy','valley'],['blade','promotion','tank','recooking'],'陆143修罗王/五转，150骑与新境界未到；竞技实用新装、寒刃任务交付条件与谷战药产能均属成长检验，源规则冲突另列。',[371,415,501,502,563,579,580,581,604,606])
thread('xin','心然兄妹、封印与记忆','subplot','partial',['tower','father','medicine','violet','coldblade'],['healing','return'],'解主仆为兄妹/疗伤/复国回归已成，四骨毁，寒刃断腿逃；记忆与全部封力仍未完，不并入玩家进阶。',[255,274,302,498,499,500])
thread('violet','紫罗兰复国阶段','main','resolved',['tower','violet'],['sword'],'政治后续仍开放；本次复国封门及奖励已完成。',[234,302,303],'302—303索封门/紫罗兰复国结算，陆MVP装备到手。')
thread('firstcity','首领地归属与经营','main','resolved',['firstcity','darkmoon'],['economy'],'本次夺首城已系统归古剑，非全部未来守城已完成；经营与后掠夺另线开放。',[450,453,455],'450系统确认古剑占首城并授陆管理，随后实际建设。')
thread('cold','寒刃入侵与五转任务','main','resolved',['tiya','bridge','coldblade','fiveturn'],['drugs','invasion','promotion'],'本次保城/职业任务已完，寒刃活逃、心记忆未全复，不代表打败全部夜灵。',[474,498,499,500,501,502],'500毁杖桥消/政权交接，501系统战争胜并实际交导师五转，502新技能付学。')
thread('romance','共同生活、多方亲密与边界','subplot','open',['auction','tournament','firstcity','countryside','sponsor','home','xiaoman'],[],'林何慕各有吻/爱或喜欢话语，陆答爱不知，未排他定约；救命不兑换性关系。',[425,451,452,507,583,590,593])
thread('second','第二城联盟分配','main','resolved',['darkmoon','secondcity'],['mobility'],'古剑先打换雪银、君临协力，第二城系统归雪银；第三城承诺另开放。',[510,512,514,515],'515系统第二领地归雪银，古剑外围协助已执行。')
thread('nine','九龙九鳞交付与奖励','main','resolved',['entry','goldice','earth','nine'],['tank','learning'],'任务完成伴诸多真死与盟友交鳞换装，不能写陆独杀九王；原队装备补偿有后述确认。',[535,543,549,559,560,561,562,563,564],'562九鳞实齐、563实际交公主，系统青冥/等级/幸运/城级奖，青冥140实穿。')
thread('anonymous','地下红毛身份','hidden','resolved',['underground','nine'],['identity'],'百战者互认已证，不扩大到现实后台或司法已结。',[527,528,550,551],'550红发百战与陆互认断手腿旧事，主盟援兵/归属后证。')
thread('club','赞助与公开切磋','subplot','partial',['sponsor','club','promise'],['fame','debt'],'联想/华硕/苹果签约分别有后证但工资未见首付。两赛1:4/5:0分账、免跪；第三城不争承诺仍引外围干预争议。',[525,565,568,570,572,598])
thread('business','雨立方筹建与家','subplot','partial',['sponsor','raincube','home','tigeralchemy'],['funding','care'],'赞助合同只给持续收入预期，雨立方实际出资另记；何慕办手续/产业转移仍忙，蓝星正式签未证、腾龙先发已签，陆2000万实付、慕轻伤已出行，不能以百亿评估当现金。',[525,574,579,581,582,583,584,603])
thread('kaxiu','猎神者救治与灵烹','subplot','resolved',['tigeralchemy'],[],'药牙只是前段，头交才疗并传；学习声望3000万异常保原。',[575,577,578,580,581],'581头实交、系统任务完成/实学，卡修真抹药起身离开。')
thread('recruit','吕布衣、小蛮与第八治理','subplot','open',['nine','lubu','xiaoman','valley'],['scholar','accountability'],'九龙所得书扇实际交吕构成招募资源，吕603已紫龙约70仍第八/未名将，零度未踢；小蛮八人主盟/第九未建，入盟事实不与第三城赌约强立因果。',[544,580,588,589,594,595,597,598,603])
thread('war','第三城/暗月掠夺双线','main','open',['tigeralchemy','earth','promise','valley'],['split','cavalry','plunder'],'青虎产能和掠夺技能均有此战调用：谷7000耗至约2000、斗真死斧乱保；鬼3097骑团外线损500+尚未返、五千幽灵刚出现。两城本卷未终判。',[549,578,588,598,599,600,604,605,606])
G=dict(title='无双卷三：群雄、治理和未结双线战',source_id=SID,revision=REV,review_status='draft',coverage=[dict(source_id=SID,revision=REV,chapter_ids=[n['chapter_id'] for n in N],complete=False,complete_volume=True,note='378原片=376正文，全部本代理实际全文阅读；complete:false表示不是全书覆盖。')],nodes=nodes,edges=edges,threads=threads)
(P/'graph.json').write_text(json.dumps(G,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
A=json.loads((P/'analysis.json').read_text(encoding='utf-8'));A['threads']=threads;(P/'analysis.json').write_text(json.dumps(A,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
state=json.loads((P/'reader-state.json').read_text(encoding='utf-8'));state['terminal_state']={'chapter_id':'ch-0606','summary':'陆143修罗王/白金、谷约2000；斗真死卓越无敌在乱包；幽灵铁骑近5000刚现未攻，青虎尚外线，何慕南京未上线。暗月6仍古剑，掠夺与第三城均未结。','open_items':['吕仍第八已学紫龙未名将','蓝星正式签约未证','原五万材料欠款未清证','明镜解鬼预未实测','三生条件援未到','青虎回城未到'],'evidence':es([598,603,604,606],'synthesis')};(P/'reader-state.json').write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(nodes=len(nodes),edges=len(edges),threads=len(threads),knowledge=sum(len(n.get('knowledge',[])) for n in nodes)),ensure_ascii=False))
