from pathlib import Path
import json
P=Path(__file__).parent
d=json.loads((P/'causal-relations.draft.json').read_text(encoding='utf-8'))
d['items'].extend([
 {'from_scene_key':'calm-control','to_scene_key':'zc01-capture','kind':'payoff','label':'童灵友情链的安抚与招魂，加上后获魂珠和公会控血，真正捕获幽灵比蒙；情感赠物进入长期养成链。','evidence':[{'chapter_id':'ch-0140','start_line':5898,'end_line':5918},{'chapter_id':'ch-0325','start_line':17865,'end_line':17918},{'chapter_id':'ch-0326','start_line':17924,'end_line':17932}]},
 {'from_scene_key':'z-scene-yuebai-shadow','to_scene_key':'z-scene-bayonet-last','kind':'setup','label':'第十环月白的影子职业让主角明确预习刺刀；正式赛仍须辨认影子战神130%及其控制、血量条件，不把两职业视为同物。','evidence':[{'chapter_id':'ch-0406','start_line':24767,'end_line':24779},{'chapter_id':'ch-0414','start_line':25326,'end_line':25392},{'chapter_id':'ch-0415','start_line':25414,'end_line':25424}]}
])
skip={('elf-teaches-enemy','withheld-racial-counter'),('withheld-racial-counter','first-paid-upset'),('old-kick-new-system','z-scene-god-kill-relay'),('friend-boss-key','good-npc-misread')}
d['items']=[x for x in d['items'] if (x['from_scene_key'],x['to_scene_key']) not in skip]
d['items'].extend([
 {'from_scene_key':'romance-account-reversal','to_scene_key':'z-scene-first-gift-chain','kind':'payoff','label':'矿洞爱情悲剧所获首赠饰物，后来因赵一直珍戴而在被围掉落时推动追还；属性旧了，记忆仍能造成行动。','evidence':[{'chapter_id':'ch-0180','start_line':8305,'end_line':8310},{'chapter_id':'ch-0424','start_line':26080,'end_line':26090},{'chapter_id':'ch-0428','start_line':26335,'end_line':26343}]},
 {'from_scene_key':'z-scene-conditional-duel','to_scene_key':'z-scene-last-duel','kind':'payoff','label':'先前约定停手且双方藏主力，最终两萧再邀无保留友战、白昼比试，实际分出萧御胜后仍共饮；两次结果分别保留。','evidence':[{'chapter_id':'ch-0409','start_line':24934,'end_line':24949},{'chapter_id':'ch-0464','start_line':28779,'end_line':28799},{'chapter_id':'ch-0464','start_line':28863,'end_line':28882}]},
 {'from_scene_key':'z-c-s-master-reversal','to_scene_key':'z-scene-coupled-god-battle','kind':'setup','label':'返救与索德燃命使空间转换交到主角，后解封充当光暗两门钥匙，才让单人隐秘任务与万人神战汇合。设传点不补成实际往返动作。','evidence':[{'chapter_id':'ch-0371','start_line':22300,'end_line':22345},{'chapter_id':'ch-0459','start_line':28466,'end_line':28475},{'chapter_id':'ch-0461','start_line':28594,'end_line':28601},{'chapter_id':'ch-0463','start_line':28719,'end_line':28739}]},
 {'from_scene_key':'zc01-mana','to_scene_key':'z-scene-mana-bottleneck','kind':'echo','label':'早期阳炎以技能数量压制却受法力上限反制，末段执金无限治疗又以切蓝池破局；两次呼应资源轴转换，非声称文本明写回忆前战。','evidence':[{'chapter_id':'ch-0333','start_line':18393,'end_line':18410},{'chapter_id':'ch-0333','start_line':18435,'end_line':18462},{'chapter_id':'ch-0458','start_line':28436,'end_line':28457}]}
])
v=json.loads((P/'integration-validation.json').read_text(encoding='utf-8'))
d['status']='complete' if v['unique_unit_count']==463 and not v['missing_units'] else 'draft-awaiting-ending'
name='causal-relations.json' if d['status']=='complete' else 'causal-relations.provisional.json'
(P/name).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(name,len(d['items']))
