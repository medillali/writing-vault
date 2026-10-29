from save_batch import *
from collections import defaultdict
batches=[json.loads(f.read_text(encoding='utf-8')) for f in sorted(P.glob('batch-*.json'))]
def dump(name,obj): (P/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
hist=defaultdict(list)
for b in batches:
 for c in b['characters']: hist[c['key']].append({'unit_start':b['unit_start'],'unit_end':b['unit_end'],**c})
dump('characters-final.json',{'source_key':'z','scope':'仅321..370本段末态，非全书终态','unit_end':370,'characters':[{'key':k,'name':v[-1]['name'],'last_observed':v[-1],'history':v} for k,v in hist.items()],'identity_cautions':[{'keys':['hols','holes'],'note':'同名霍尔斯分批key差异；保历史，整合可规范中文同名。'},{'keys':['grio','sord'],'note':'巨人先称格里奥，画像主人系统索德且实际认主，但正文无明确别名解释；保两档及identity-link异常。'},{'keys':['xiao-yu','xiao-yu-sister'],'note':'萧御与小雨不同人，不因字面前缀相近归并。'}]})
th=defaultdict(list)
for b in batches:
 for t in b['threads']:th[t['key']].append({'unit_start':b['unit_start'],'unit_end':b['unit_end'],**t})
updates={
'zhao-romance':('partial','初期口头未允已被346叙述确认与358公开女友补足；恋爱确认，后续家庭与性边界独立。',[ev(347,19374,19387),ev(359,21263,21268)]),
'blood-loyalty':('resolved','霍尔斯被赵梦魇杀，列昂给解除药并留洞叙述必死，萧赵喝药恢复人。',[ev(346,19282,19324),ev(347,19362,19374)]),
'black-horse':('resolved','黑龙驹353二级358三级，已实际进阶。',[ev(354,20068,20083),ev(359,21041,21057)]),
'z-c-t-pradilok':('partial','巨人锁开、索德救出，大地之心已交；巨人断后坠地与索德燃命战未结。',[ev(363,21650,21659),ev(370,22192,22217),ev(371,22300,22345)])}
for k,(status,state,e) in updates.items():
 if k in th:th[k].append({'unit_end':370,'key':k,'status':status,'state':state,'evidence':e,'terminal_reconciliation':True})
dump('threads.json',{'source_key':'z','scope':'321..370阶段线索归并，非全书结局','threads':[{'key':k,'status':v[-1]['status'],'state':v[-1]['state'],'evidence':v[-1]['evidence'],'history':v} for k,v in th.items()]})
qm={}
for b in batches:
 for q in b['questions']:qm[q['key']]=q
overrides={
'ghost-capture-done':('resolved','324实际捕成，一级宠成长重建；后至365宠33并得抗体。',[ev(325,17865,17886),ev(366,21855,21860)]),
'zhao-official':('resolved','初期先不允的状态已经346叙述确认恋爱、358公开女友且赵无否认回收。',[ev(347,19374,19387),ev(359,21263,21268)]),
'father-obstacle':('open','至370未亲见父亲态度，风野的支持保证仍不是父本人同意。',[ev(334,18473,18482)]),
'blood-freedom':('resolved','列昂主动解精神束；任务后赠药，萧赵喝药恢复人，临时后裔属性撤回。',[ev(342,18961,19023),ev(347,19362,19374)]),
'horse-evolve':('resolved','353二级，358三级200%移速龙威腾空，预兆已兑现。',[ev(354,20068,20083),ev(359,21041,21057)]),
'focus-crafting':('partial','越级熟练增长与实际成功有证，专注提高成功率的因果仍无独立验证。',[ev(335,18531,18563)]),
'z-c-q-blood-victory':('resolved','霍尔斯赵梦魇系统尾刀；列昂洞塌留内被叙述明确必死。',[ev(346,19282,19324)]),
'z-c-q-soul-next':('partial','只第一封已解，石魔和女王继续吸魂无新解封消息。',[ev(346,19312,19320),ev(363,21644,21649),ev(367,21864,21869)]),
'z-c-q-couple-status':('partial','恋爱已叙述与公开称谓确认；至370无现实性关系完成，次夜仅同房约定保边界。',[ev(347,19374,19387),ev(359,21263,21268),ev(360,21359,21368)]),
'z-c-q-a-box':('resolved','携A箱活到5小时传返，9.98A级转职奖励结算。',[ev(351,19590,19694)]),
'z-c-q-guild-war':('open','转职差距、正式同盟已成，但六隐藏小会夺两镇迫风改稳推，魔域未灭。',[ev(364,21705,21744)]),
'z-c-q-xiaoling-kin':('unknown','墓碑同名只是联想，眼前本家只指同姓，尚未认亲。',[ev(354,20112,20113),ev(355,20315,20316)]),
'z-c-q-holy-clean':('resolved','圣水天池实际洗净圣言匕属性。',[ev(358,20939,20944)]),
'z-c-q-nightmare-gate':('resolved','恶魔角实插槽，翡翠梦魇门已开，后说明永久存在。',[ev(360,21377,21386),ev(368,22002,22003)]),
'z-c-q-pradilok':('partial','巨人已解锁，索德已被救出并大地之心结算；后巨人重伤坠地索德燃命，生死未结。',[ev(363,21650,21659),ev(370,22192,22217),ev(371,22300,22345)]),
'z-c-q-task-numbers':('unknown','第七城主又称第八/第三的环次差异仍保留；后明确第九五天后，不能自行改正文。',[ev(355,20404,20420),ev(358,20913,20916)]),
'z-c-q-dark-control':('unknown','开启暗影克制仍写凿击/迅击晕，与此前属性和白狼实测自身控制无效冲突，未说明中途切换。',[ev(355,20189,20192),ev(358,20844,20863)]),
'z-c-q-ufnos':('open','异星门确发现，1.6万晶；侍者潜伏与触发点为萧推理，尚未接任务或入异星。',[ev(368,21987,22016),ev(369,22033,22051)]),
'z-c-q-space-fate':('open','普拉迪洛克断后坠地，索德燃生命交戒正对五超阶，当前尚未结算。',[ev(371,22300,22345)]),
'z-c-q-space-unseal':('open','空间戒已交但仅封印传说，五传点最多两人，解封实用待后。',[ev(371,22339,22345)]),
'z-c-q-sord-name':('unknown','原口称格里奥与实际索德画像同主，未有别名解释。',[ev(361,21504,21511),ev(369,22107,22110),ev(370,22192,22199)]),
'z-c-q-armor-delivery':('partial','风野一千万已打卡，特萨甲明确等出副本再给。',[ev(368,21914,21917)]),
'z-c-q-eternal-price':('unknown','永恒血瓶初价1200晶后称需5000，两方总5800；不强造统一价。',[ev(368,21940,21943),ev(368,21962,21977)])}
assert qm.keys()==overrides.keys(),(qm.keys()-overrides.keys(),overrides.keys()-qm.keys())
dump('terminal-question-map.json',{'source_key':'z','scope':'本段321..370末态；后段研究须继续更新，非全书终态','items':[{'key':k,'final_status':s,'answer':a,'evidence':e} for k,(s,a,e) in overrides.items()]})
audit={
'source_key':'z','scope':'321..370，分界交接审计，非全书结局','read_units':list(range(321,371)),'last_unit_id':'ch-0371','last_line':22347,
'completed_results':[
 {'claim':'捕比蒙已成并养成，原30强化不是即得战力。','evidence':[ev(325,17865,17918),ev(366,21855,21860)]},
 {'claim':'逐风/阳炎两黑赛实胜，不召比蒙；刺刀未对战。','evidence':[ev(330,18203,18218),ev(333,18450,18462),ev(364,21743,21745)]},
 {'claim':'霍尔斯死亡，列昂留洞叙述必死；临时后裔属性解除。','evidence':[ev(346,19282,19324),ev(347,19362,19374)]},
 {'claim':'萧赵恋爱已确认，尚不可推现实性行为。','evidence':[ev(347,19374,19387),ev(359,21263,21268),ev(360,21359,21368)]},
 {'claim':'圣言实净，恶魔角实开永久梦魇门，锁定/破魔斩实学且后者斩火球实用。','evidence':[ev(355,20410,20410),ev(358,20939,20944),ev(360,21377,21386),ev(370,22179,22182)]},
 {'claim':'索罗城主死，攻塔占城实成，萧侯爵准将，全队准将；公共守城最后听尚待援。','evidence':[ev(357,20793,20796),ev(358,20877,20928),ev(359,21074,21081)]},
 {'claim':'巨人解锁，索德救出，大地之心实交；空间转换封印戒也实得。','evidence':[ev(363,21650,21659),ev(370,22192,22217),ev(371,22339,22345)]}],
'unsettled_at_boundary':[
 {'claim':'巨人断后坠地/索德燃命对五超阶生死未结。','evidence':[ev(371,22300,22345)]},
 {'claim':'异星门发现和沃克任务推理不能当已接/已进入。','evidence':[ev(368,21987,22016),ev(369,22033,22051)]},
 {'claim':'魔域隐小会反击，风野改慢推，公会战争与刺刀赛尚未结。','evidence':[ev(364,21719,21745)]},
 {'claim':'噬魂后续封印、双戒纸在本段无新解释；只第一封解。','evidence':[ev(346,19312,19320),ev(363,21644,21649),ev(367,21864,21869)]}],
'source_anomalies':[
 {'claim':'格里奥/索德身份名称未解释。','evidence':[ev(361,21504,21511),ev(369,22107,22110)]},
 {'claim':'369开头把救索德写救赵岚馨；370L22329把伪装主体写普拉迪洛克。','evidence':[ev(370,22150,22153),ev(371,22323,22329)]},
 {'claim':'永恒血瓶1200/5000晶与两方5800价冲突。','evidence':[ev(368,21940,21943),ev(368,21962,21977)]},
 {'claim':'第七/八/第三任务环次称谓摇摆。','evidence':[ev(355,20404,20420),ev(358,20913,20916)]},
 {'claim':'暗影克制自身无控说明与开后击晕冲突。','evidence':[ev(355,20189,20192),ev(358,20844,20863)]},
 {'claim':'霍尔斯强化/超阶标签变化；巨人称伯爵与萧系统侯爵不一致。','evidence':[ev(345,19150,19217),ev(357,20793,20796),ev(363,21650,21659)]}],
'sensitive_depiction':[
 {'claim':'357–358黑龙驹对惊惧独角兽强迫交配，以幽默和坐骑奖励收尾；不能当相互同意恋爱机制。','evidence':[ev(358,20995,21007),ev(359,21011,21058)]},
 {'claim':'359赵明确性边界，萧数次试探后停止；后邀请只是同房，不能倒推前接触全程同意。','evidence':[ev(360,21359,21368)]},
 {'claim':'索罗杀平民取证和屠城有明写，角色胜者伦理不直接转研究推荐。','evidence':[ev(356,20575,20589),ev(357,20756,20763)]}],
'validation':{'method':'validate_research.py checks all evidence within normalized chapter bounds; manual full-text reading distinct from retrieval receipts','last_result':'2026-10-25 导出后已运行，全JSON章界0错误。'} }
dump('ending-audit.json',audit)
dump('handoff-to-next.json',{'source_key':'z','completed_start':321,'completed_end':370,'next_unit':371,'next_unit_id':'ch-0372','last_state':'索德燃命把封印空间转换交萧，巨人坠地，五超阶战未结。','required_followups':[{'key':k,'state':a,'evidence':e} for k,(s,a,e) in overrides.items() if s in ['partial','open','unknown']],'earlier_external_followups':[{'key':'ancient-curse','state':'古德剩十天诅咒实际结算、沃卡德复生/存魂、黑幽灵与童灵关系，本段未找到新解答。'},{'key':'opening-necromancer','state':'40任务哈蒙斯，47–48哺血故事，320萧推克文图斯；本段未确认别名或身份，不归并。'},{'key':'other-old-lines','state':'哈格多藏宝图/人偶C核/刀伤真实因/罪恶值1/影砂组织，本段未找到新解答。'}],'do_not_reopen':['捕比蒙324完成','圣言净化357完成','恶魔角359开门','深白包311已交/猴子269入游（上段核）','猴子358养家和友谊再确','糖果赌约250取消280替代（上段核）'],'files':['batch-01.json','batch-02.json','batch-03.json','characters-final.json','threads.json','terminal-question-map.json','ending-audit.json']})
print(f'exported {len(hist)} character keys; {len(th)} thread keys; {len(qm)} unique question keys')
