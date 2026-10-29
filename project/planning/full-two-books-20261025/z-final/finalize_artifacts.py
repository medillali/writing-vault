from pathlib import Path
import json,sys
import integrated_notes as N
from final_details import portraits,structure
from write_final_text import render_book,render_audit
P=Path(__file__).parent
V=json.loads((P/'integration-validation.json').read_text(encoding='utf-8'))
assert V['unit_count']==V['unique_unit_count']==463 and not V['missing_units'] and not V['duplicate_units'] and not V['evidence_errors'],V
inv=json.loads((P/'integration-inventory.json').read_text(encoding='utf-8'))
terminal=json.loads((P/'terminal-question-map.json').read_text(encoding='utf-8'))
assert {x['key'] for x in terminal['items']}==set(inv['questions'])
assert all(x['evidence'] for x in terminal['items'])
def write(name,d):(P/name).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
N.write_core('')
book=json.loads((P/'book-synthesis.json').read_text(encoding='utf-8'))
book['structure']=structure
book['major_character_arcs']=portraits
book['ending_audit']='ending-audit.json'
book['terminal_questions']='terminal-question-map.json'
book['causal_relations']='causal-relations.json'
book['research_boundary']='所有论断为研究草稿，不写入用户偏好或原创项目设定；全书读到结尾不等于所有伏笔都已解释。'
write('book-synthesis.json',book)
write('characters-final.json',{'source_key':'z','scope':'全书1–463二次综合；只给核心人物有据终点，不把所有人物均当终章出场','items':portraits})

over={}
def T(keys,status,state,*ev):
 for k in keys:over[k]={'status':status,'state':state,'evidence':N.EV(*ev)}
T(['legitimate-living'],'resolved','千元、28000和630万实到账后原生计门槛已越；415近30亿并自认最初目标已完成。',(69,3043,3053),(113,4859,4860),(202,9771,9776),(415,25487,25528))
T(['house-goal'],'partial','已有自主居住选择和足够财力，263选择留赵家、416留别墅交吴照看，463起飞；未独立写萧御自购住房或新星安家。',(263,14010,14022),(416,25532,25555),(463,28883,28894))
T(['zhao-romance','z-c-t-romance'],'resolved','恋爱公开确认，380赵父本人认可、381双方约到新星结婚；终共同起飞。没有婚礼或法律婚姻完成证据。',(346,19374,19387),(358,21263,21268),(380,23036,23067),(381,23127,23131),(463,28883,28894))
T(['chosen-home'],'resolved','从贫困寄居变263主动选择归属，终与家人伴侣共同迁移离地。',(263,14010,14022),(463,28883,28894))
T(['snow-orchid','snoworchid-deadline'],'resolved','191采草实际交回获突进与风速靴；沃思支线断裂是独立代价。',(190,9109,9111),(191,9117,9119),(191,9151,9158))
T(['holy-dagger-restoration','z-c-t-holy-dagger'],'resolved','357圣水天池实际清洗恢复圣言属性，401旧匕12万转糖果；冠军天之圣水是另一新奖。',(357,20939,20944),(401,24480,24488),(453,28185,28186))
T(['wokade-rebody'],'unknown','肉身自毁、祭灵珠暂存魂，山德鲁赐身未保证；后续未明确复生，不判弃线。',(149,6439,6444),(152,6578,6580))
T(['friendship-growth'],'resolved','承认缺朋友后愿协作、授艺但可分开、接受组织救尸，终与最高对手认输共饮；独行边界扩大而非全变固定队。',(158,6920,6948),(299,16289,16296),(305,16690,16714),(463,28873,28882))
T(['monkey-new-path'],'resolved','269自立拒接济，35833级养家、41050级攒200万入公会，452全服第六并守誓让赛。',(269,14402,14411),(358,21263,21279),(410,25109,25118),(448,27876,27877),(452,28160,28160))
T(['black-match','bayonet-challenge'],'resolved','热身牙刃等已胜，414实际最高黑赛胜刺刀，415收入兑现；不能以379赛程计划替实际举行顺序。',(378,22909,22921),(414,25443,25481),(415,25487,25528))
T(['soul-ring','soul-ring-seal','z-c-t-soul-ring'],'partial','345只解第一封；之后吸石魔女王无新解封，埃莫/双戒纸与余封无完整解释。',(93,4133,4140),(94,4145,4150),(345,19312,19320),(362,21644,21649),(366,21864,21869))
T(['nightmare-cave','z-c-t-nightmare'],'partial','359恶魔角已重开梦魇门，后深入地下城、救NPC与取空间器；未见整个梦魇世界全清的独立宣告。',(107,4682,4703),(359,21377,21386),(370,22300,22345),(371,22371,22417))
T(['shenbai-bags'],'resolved','311五个28格包已实际交付；40960格市场变化不替此旧约，旧约本身早已回收。',(311,17008,17057))
T(['summon-undead','ghost-behemoth','ghost-capture'],'resolved','324实际以尖牙招魂捕获幽灵比蒙，重置一级、325灵魂珠提高成长与忠诚。',(324,17865,17918),(325,17924,17932))
T(['shenghen-barter'],'resolved','232议价后，233已实际换得裂爆及护肩。',(233,11819,11895))
T(['dy-defense','z-c-t-state-task','assassination-ten'],'resolved','各环条件另结算，408实际交第十与十环全奖励、升55解队；不把某次击杀提前当全十环完成。',(250,13069,13074),(261,13908,13909),(408,24953,24979))
T(['candy-contest'],'resolved','250公平取消计数赌、280石剪布分装，451循环真战圆糖果愿，未胜但造成麻烦。',(250,13041,13059),(280,15045,15057),(451,28055,28056))
T(['hunter-black-match'],'resolved','329实际胜猎人逐风，宠物现场为火焰螳螂；此前暴风狮情报不升级为当场宠。',(307,16807,16817),(329,18149,18220))
T(['kevintus-identity'],'resolved','320推断390被叙述和本人应称确认古墓老者即克文图斯；40哈蒙斯称名仍保冲突。',(40,1717,1726),(320,17606,17619),(390,23761,23771))
T(['blood-loyalty','z-c-t-blood'],'resolved','赵梦魇杀霍尔斯，两人药恢复；列昂给药出口后留塌洞，叙述判必死。先前威胁另有未真想伤赵的动机澄清。',(341,18961,18987),(345,19282,19324),(346,19362,19395))
T(['black-horse'],'resolved','黑龙驹353二级、358三级开龙威腾空，454六级会飞；幼崽出生来源仍单列未明。',(353,20068,20091),(358,21011,21068),(454,28224,28291))
T(['z-c-t-guild','moyu-merger'],'resolved','转职优势曾被隐小会反击校准，415附属谈判后428魔域已同意成为风野附属；不是简单全会灭亡。',(363,21719,21744),(415,25513,25517),(428,26394,26394))
T(['z-c-t-pradilok','space-conversion-sacrifice'],'resolved','巨人与画像主人曾救出、奖励实交，371索德与五敌同归、巨人永眠，生命线已结；格里奥异名未解释。',(369,22192,22217),(370,22300,22345),(371,22371,22398))
T(['z-c-t-ufnos','wufunosi','wufunosi-exploration'],'resolved','390已接克探索，418实际入乌星；427交光神荒漠定位、428交克探五迪雅。完成指定任务而非全图清尽。',(390,23797,23814),(418,25659,25693),(427,26354,26383),(428,26403,26422))
T(['z-c-t-space-artifact','space-conversion'],'resolved','370得封印器，371实际设两点；458解封开光门、460再开暗门并释同门错位两面。设点不补成已描写往返。',(370,22339,22345),(371,22398,22417),(458,28466,28475),(460,28594,28601))
T(['new-star','romance-migration','new-star-migration'],'partial','380父认可、381两人约到新星结婚，391订票，463实际登机起飞；未写抵达、婚礼或落地生活。',(380,23036,23067),(381,23127,23131),(391,23857,23865),(463,28883,28894))
T(['dark-fortress'],'partial','安府地下要塞与复活耶罗情报已听报并领奖，420和解撤要塞；耶罗任务全部结果不由本书主角全知，不用另一书代补。',(396,24121,24140),(401,24521,24526),(420,25791,25815))
T(['sofia-siege'],'partial','守缺杀狂龙引援成功，389索菲亚仍未全陷、萧因红月任务离开；后文圣光城是另一战役，不代补索菲亚明确终态。',(385,23425,23447),(389,23702,23713))
T(['shadowsand-organization'],'partial','现实雇佣兵有偿凶杀背景386已明，影砂先死后五人二死三逃，三人放弃纠缠；没有组织全灭或现实惩处。',(386,23462,23468),(386,23524,23528),(388,23658,23685))
threads=[]
for k,h in inv['threads'].items():
 latest=max(h,key=lambda x:x['through']);row={a:latest[a] for a in ['key','title','kind','status','state','unit_ordinals','evidence']}
 if k in over:row.update(over[k])
 elif row['status']=='open':row.update(status='unknown',state='全文新研究未见更明确的独立结算。最后有据状态：'+row['state'])
 row['history']=h;threads.append(row)
write('threads.json',{'source_key':'z','policy':'保留每个研究key与阶段历史，终态按全书新研究重算；同一语义的不同key可有共同结论，未提不判abandoned。','items':threads})
write('question-ledger.json',{'source_key':'z','items':[{**q,'question_history':inv['questions'][q['key']]} for q in terminal['items']]})

identity=json.loads((P/'identity-links.draft.json').read_text(encoding='utf-8'));identity['status']='complete'
item=identity['items'][0]
item.update(relation='same_story_figure_with_name_conflict',status='partial',claim='40任务面板明确哈蒙斯，47–48本人未报姓名；320为主角推断，390叙述确认古墓老者为克文图斯且本人应称。叙事身份联系已证，哈蒙斯称名与克文图斯间无别名解释，保两档及来源差异，不静默删除或列已证别名。')
item['evidence']+=N.EV((390,23761,23771))
identity['items'].append({'from_key':'grio','to_key':'sord','relation':'same_portrait_with_name_conflict','status':'partial','claim':'巨人最早称主人格里奥，后画像对象系统名索德且获巨人认可；没有明确别名解释，保两档并链接同画像关系。','evidence':N.EV((360,21504,21511),(368,22107,22110),(369,22192,22199),(371,22383,22398))})
write('identity-links.json',identity)
(P/'book-synthesis.md').write_text(render_book(),encoding='utf-8')
(P/'ending-audit.md').write_text(render_audit(),encoding='utf-8')
write('integration-manifest.json',{'source_key':'z','status':'complete','collective_actual_read_units':463,'this_agent_actual_full_units':[1,232],'additional_targeted_raw_checks':[{'ordinal':451,'start_line':28048,'end_line':28058},{'ordinal':390,'start_line':23752,'end_line':23776}],'secondary_read_batches':V['batches'],'basis':'本代理除1–232正文外逐批阅读全部新增分工研究并核对终态；针对性片段审计不冒充追加全章覆盖。','old_research_used_as_new_reading':False,'destination_boundary':'仅.planning研究草稿；未改真实writing-vault、Git或生产工具。'})
(P/'progress.md').write_text('''# 《贼胆》全书二次综合已完成

本代理实际全文读1–232，共232单元；另定点复核390身份与451糖果约战，不将片段算新增全章。root读233–320、z-c读321–370、z-c2读371–390、z-d读391–463。本代理已二次逐批读完28份新研究，集体463/463无缺重复，不用旧研究冒充阅读。

正式产物：book-synthesis.md/json、ending-audit.md/json（33项）、terminal-question-map.json（115独特key逐键有证）、causal-relations.json（20条）、characters-final.json（16核心人物弧）、threads.json（85key与历史）、question-ledger.json、identity-links.json、integration-manifest.json。

validation核章界、单元连续、问题全键、九维、scene引用和Markdown引用。技术验证不替代解释质量或用户偏好认可。最高决斗标题已改“最终友谊决斗”，保下位神/凡体差；萧御与赵人物弧补463起飞证据。

371仅设两传点，不补往返。390证古墓老者为克文图斯，但40哈蒙斯称名无别名解释，保档链接；格里奥/画像索德同样保称名冲突。父亲380认可、381新星婚约、圣言净化、恶魔角、糖果451真约战等早伏均按后文更新。未知不凭沉默判弃线。

终局双冠、神战及友战完成；现实只到三人起飞，未写抵达或婚礼。所有阶段快照保历史；只写.planning，未改vault、Git或生产工具。root负责入库及跨书综合。
''',encoding='utf-8')
print('complete',len(V['batches']),'batches',len(terminal['items']),'questions',len(threads),'threads',len(portraits),'core characters',len(N.audits),'ending checks')
