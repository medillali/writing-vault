from pathlib import Path
import json,subprocess,sys
from build import BOOK,ROOT,refs
p=ROOT/'b01.py';s=p.read_text(encoding='utf-8').replace('两NPC生命线结束，空间器已实际往返；笔记谜题开始。','两NPC生命线结束，空间器双点已设置；笔记谜题开始。');p.write_text(s,encoding='utf-8')
subprocess.run([sys.executable,str(p)],check=True)
U={x['unit_id']:x for x in BOOK['units']};errors=[]
def walk(x,loc):
 if isinstance(x,dict):
  if {'chapter_id','start_line','end_line'}<=x.keys():
   u=U.get(x['chapter_id'])
   if not u or not u['start_line']<=x['start_line']<=x['end_line']<=u['end_line']:errors.append({'location':loc,'evidence':x,'bounds':None if not u else [u['start_line'],u['end_line']]})
  for k,v in x.items():walk(v,loc+'/'+k)
 elif isinstance(x,list):
  for i,v in enumerate(x):walk(v,loc+f'/{i}')
d=json.loads((ROOT/'batch-01.json').read_text(encoding='utf-8'));walk(d,'batch-01.json')
assert [x['ordinal'] for x in d['units']]==list(range(371,391))
assert all(u['events'] and u['evidence'] for u in d['units'])
assert set(d['dimensions'])==set('worldbuilding characters plot style narrative dialogue pacing themes continuity'.split())
assert all(d['dimensions'][k] and all(x['evidence'] for x in d['dimensions'][k]) for k in d['dimensions'])
assert len(d['scenes'])>=3 and len(d['patterns'])>=2
assert all(s['goal'] and s['obstacle'] and s['choice'] and s['consequence'] and s['state_change'] and s['why_it_works'] and s['applicability'] and s['failure_mode'] and s['evidence'] for s in d['scenes'])
assert all(q['kind'] in {'promise','misbelief','rule','anomaly','unresolved'} for q in d['questions'])
coverage={'source_key':'z','source_id':BOOK['source_id'],'source_revision':BOOK['revision'],'assigned_unit_start':371,'assigned_unit_end':390,'total_source_units':len(BOOK['units']),'full_read_intervals':[[371,390]],'read_unit_count':20,'missing_units':[],'saved_batches':[{'file':'batch-01.json','unit_start':371,'unit_end':390}],'method':'read_source.py每次2–3实际reading-units全文模型阅读，所有输出完整；不用目录、搜索、旧摘要或自动循环替代阅读。','next_boundary':{'ordinal':391,'unit_id':BOOK['units'][390]['unit_id'],'start_line':BOOK['units'][390]['start_line']},'evidence':refs([[371,22348,22428],[390,23752,23816]])}
(ROOT/'read-coverage.json').write_text(json.dumps(coverage,ensure_ascii=False,indent=2),encoding='utf-8')
handoff={
 'source_key':'z','coverage':[371,390],'source_id':BOOK['source_id'],
 'priority_updates':[
 {'key':'father-approval','status':'resolved','state':'380父亲本人试探阶层压力后认可、邀二人新星；381赵理解已获父承认，双方同意迁移。z-d391后沉默不等于全书未回收。','evidence':refs([[380,23036,23067],[381,23106,23113]])},
 {'key':'marriage-promise','status':'partial','state':'381提出到新星结婚赵应，实际已同室亲密而未性交；463后仍无婚礼/法律婚或抵达画面。','evidence':refs([[381,23116,23132]])},
 {'key':'shadowsand-organization','status':'partial','state':'386明确现实佣兵有偿雇凶组织，游戏收益；影砂先死、其余五人两死三逃，388三逃者放弃再纠缠。未组织全灭或现实惩处。','evidence':refs([[386,23462,23468],[386,23524,23528],[388,23670,23685]])},
 {'key':'sode-end','status':'resolved','state':'371索德燃命同归五黑精灵、巨人阖眼永远沉睡；回忆补守族神器承诺和救巨人。空间器地下/冥夜双点实际设置，不擅补未写传送动作。','evidence':refs([[371,22371,22417]])},
 {'key':'grandmaster-complete','status':'resolved','state':'375突破最后1熟练系统大宗师、野性药实际制作；373双高级瞬回配方实交风野换后勤承诺。','evidence':refs([[373,22539,22550],[375,22634,22650]])},
 {'key':'otran-complete','status':'resolved','state':'红月笔记显亡魂，克主动到，带回魂师友谊已系统完成329000经验并50级；地下要塞消息另外10万荣8000功。笔记毁不在本段，391接。','evidence':refs([[389,23731,23749],[390,23771,23791]])},
 {'key':'wufunosi-start','status':'open','state':'海蓝心已交、探索已接每方圆1公里200荣加击杀，极效虚无配方已得（免任物魔、慢90%、不可攻2分冷30分、6000金材料）；未开始探图。','evidence':refs([[390,23797,23814]])},
 {'key':'rank-boundary','status':'partial','state':'371实际领侯爵/准将勋，385升将军血8000余；388三十多万、390加10万后四十多万仍差准帅。旧勋不等当前军衔。','evidence':refs([[371,22417,22420],[385,23420,23424],[388,23687,23687],[390,23790,23791]])},
 {'key':'siege-boundary','status':'partial','state':'杀狂龙开缺口但索菲亚仍巷战炮威胁，到389未全城胜，因红月任务离开；圣光也尚在临要塞、死幕、下位神鏖战阶段。','evidence':refs([[385,23425,23447],[389,23691,23713]])},
 ],
 'source_issues':[
 {'state':'索德/格里奥前称本段未解释，别名只标待核。','evidence':refs([[371,22383,22398]])},
 {'state':'牙刃场主角说未和刺刀打过，与同段曾遭遇和视频学习并存；视为尚未正式决斗不抹早先相遇。','evidence':refs([[376,22771,22779]])},
 {'state':'379排明夜红月后夜刺刀再刺杀；后391以后刺杀先实际进行，排程意向不能替事实。','evidence':refs([[379,22999,23007]])},
 {'state':'388末说影妖和影魔释放魂；影魔只在此命名，行为链是死去冰法，勿凭名新并早期别人物。','evidence':refs([[388,23670,23685]])},
 ],
 'craft_pointers':['索德苟活重释与最终牺牲需保代价，不能只洗白。','录像模仿有八成与个人取舍，70%反背抢时有具体原创变化。','攻城团队授权与狂龙无副手对照；有治疗卡位的胜利不能变单挑。','隐虚步用知识差诱走位，等候付比蒙牺牲和赵残血成本。']
}
walk(handoff,'handoff.json');walk(coverage,'read-coverage.json')
(ROOT/'handoff.json').write_text(json.dumps(handoff,ensure_ascii=False,indent=2),encoding='utf-8')
counts={k:len(d[k]) for k in ['units','characters','scenes','patterns','threads','questions']}
report={'status':'pass' if not errors else 'fail','source_id':BOOK['source_id'],'coverage':[371,390],'counts':counts,'evidence_errors':errors,'scope':'结构与证据行界审计，仅此范围；不宣称机器证明研究解释正确。'}
(ROOT/'audit-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
(ROOT/'progress.md').write_text('# 贼胆补段进度\n\n实际371–390全部全文读完并正式保存batch-01.json，九维及7人物、5场景4机制、9线索8问题齐。read-coverage.json、handoff.json与audit-report.json已生成。结构/行界审计'+report['status']+'。后段391–463另在z-d已完成。\n',encoding='utf-8')
(ROOT/'part-synthesis.md').write_text('''# 《贼胆》补段：实际371–390

20单元已逐单元全文阅读。正式研究见batch-01.json，终态纠偏与391衔接见handoff.json，行界审计见audit-report.json。

最重要的新证据是380赵父本人会面：阶层阻恋实际为试探，之后认可、嘱照顾并邀共同赴新星（ch-0381 L23036–23067）。381两人共同同意迁移，并明确承诺到新星结婚；同室亲密而未性交，承诺不等于婚礼已成（ch-0382 L23106–23132）。这纠正“391后没再提父亲”被误读为全书无回收。

影砂六人组386明确现实雇佣兵有偿雇凶组织，游戏获利；影砂被先诱杀，后五人中影妖与冰法死、其余三法果断逃并不再纠缠（ch-0387 L23462–23468；ch-0389 L23670–23685）。这完成当场遭遇，不等于组织全灭或现实惩罚。

索德和五追兵燃命同归、巨人永眠，回忆把贪谄求生重释为守族神器承诺，空间转换双点设下（ch-0372 L22371–22417）。主角从录像学刺刀而保退路发展个人风格，反手背刺70%完成抢时间破反制，是学习机制的具体实例（ch-0377 L22771–22779；ch-0380 L22961–22964）。不宜把“学八成”抽成照抄整套风格，文字也强调独立领会。

攻城高潮的因果不是主角单人硬杀战士：切掉高位牧、队友卡位、己治疗、单目标嗜血长期叠加共同成立。主角不善指挥便授权，而狂龙为加强控制不设副队，死亡后队乱（ch-0385 L23325–23378；ch-0386 L23391–23430）。局部破缺口已成，索菲亚仍巷战未下，红月到主角必须离开。

奥特兰旧笔记由找信转让亡魂本人传情报，委托在390已系统完成，升50；另补地下要塞情报得10万荣8000功。海蓝心探索乌星任务刚接，极效虚无配方刚得，后续探图不提前算完成（ch-0391 L23771–23814）。神级战视频先展示普通玩家不能参与，再用引导任务给能力通路，为391后刺杀提供规则前置。

有价值机制：把表象人物用最后选择和具体记忆重释；模仿后以目标和风险取舍成自己；指挥可替代性转化组织结果；未知技能的敌方误读转为空间陷阱；旧物在特定时令恢复本人发言。每项批卡都写适用与失效，源文女性物化、富家标签、性别泛化和父亲试探撤回压力的便捷处理也要保留批评，不能无条件作为用户风格规则。
''',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
