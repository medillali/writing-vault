"""冻结已生成现件，并生成主审要求的精准提案；不重建或修改六核心。"""
import pathlib,json,hashlib,copy,datetime,sys
P=pathlib.Path(__file__).resolve().parent;sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,str(P.parents[1]))
from check_volume import load_and_check
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(n):return json.loads((P/n).read_text(encoding='utf-8'))
def save(n,x):(P/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
core=['analysis.json','cards.json','graph.json','chapter-notes.jsonl','read-log.json','reader-state.json']
hashes={n:h(P/n) for n in core}
before=P/'review-corrections'/'primary-before';before.mkdir(parents=True,exist_ok=False)
for n in core:(before/n).write_bytes((P/n).read_bytes())
save('review-corrections/primary-before/snapshot.json',dict(core_sha256=hashes,status='preserved-before-primary-proposals',generated_at=datetime.datetime.now(datetime.timezone.utc).isoformat()))
A,C,G=read('analysis.json'),read('cards.json'),read('graph.json')
result=load_and_check('zhanlong',5)[-1]
rows=[json.loads(x) for x in (P/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines() if x]
assert read('reader-state.json')['notes_sha256']==h(P/'chapter-notes.jsonl')
assert len({c['origin_key'] for c in C})==len(C)
assert all(len(x)==5 and all(y.get('mechanism') and y.get('limits_and_counterevidence') for y in x) for x in A['dimensions'].values())
assert len({c['content']['applicability'] for c in C if c['asset_type']=='scene'})==54
assert len({c['content']['failure_mode'] for c in C if c['asset_type']=='scene'})==54
assert {n['chapter_id'] for n in rows if n['unresolved']}=={n['chapter_id'] for n in A['chapter_unresolved_index']}
result.update(status='passed',validation_scope='全文覆盖/精确章界/claim引用/卡片关系/图端点线程闭包及原notes四栏；不是文学主审',observations=45,independent_mechanism_fields=45,independent_limits_fields=45,scene_specific_applicability_fields=54,scene_distinct_failure_fields=54,notes_sha256=h(P/'chapter-notes.jsonl'),open_questions=len(A['open_questions']),source_anomalies=len(A['unresolved_and_anomalies']),named_life_states=len(A['named_life_state_audit']),original_notes_preserved=True,complete_book=False)
save('validation.json',result)
rechecked=[981,982,983,984,985,986,992,993,994,995,996,997,1004,1005,1006,1016,1017,1020,1037,1038,1039,1040,1041,1078,1079,1080,1081,1085,1086,1087,1088,1089,1090,1091,1108,1109,1110,1111,1112,1113,1114,1115,1116,1117,1118,1119,1120,1121,1122,1123,1124,1125,1126,1127,1128,1129,1130,1131,1132,1133,1134,1138,1139,1140]
save('self-review-receipt.json',dict(reader='/root/zongheng_vol04_full',kind='draft-self-review-not-primary-signoff',source_id=A['source_id'],revision=A['revision'],raw_reading=dict(chapter_ids=A['read_chapter_ids'],fragments=211,body_units=210,truncated_pending=[]),derived_notes_reread_for_locator_alignment=dict(chapter_ids=[f'ch-{n:04d}' for n in sorted(set(rechecked))],input_sha256=h(P/'chapter-notes.jsonl'),scope='本代理自己的原实读笔记复核，不计新增原文阅读'),targeted_original_reread_for_primary=dict(chapter_ids=['ch-1091','ch-1092','ch-1093','ch-1094'],method='本次重新BEGIN-END全文完成，无截断',scope='核Wuhan同一商场分区与上海小队身份'),draft_locator_corrections=['ALLSTAR结果1006而非1004前八强','会猎1039印度阵营胜/主个人MVP，非1040朝廷追责','雷丁1125死/1126铠复制与雷首交；1127为三魂条件','1133炮实到/第二魂实交；1134四将落成/第三魂定位'],core_sha256=hashes,limits='自核不代主审，后续精准修改保before/after，不静改原notes'))
changes=[]
def propose(file,path,after,reason):
 obj=read(file)
 for p in path:obj=obj[p]
 changes.append(dict(file=file,path=path,before=copy.deepcopy(obj),after=after,reason=reason))
continuity=[
 dict(observation='本人当面认多别名、另人的自我介绍和亲属说明，逐步把失联时的陌生行动接回旧关系；同名NPC与玩家的不同场面又保住世界的辨识度。',mechanism='重逢先让角色亮面板/说出熟悉称呼，再由本人承认使前面的礼物、援军和回避获得新意义；另以不同职业、地点与亲属对话区分相似名字。',limits_and_counterevidence='主早用外貌等级排除牛奶是薛仍只是判断，1006颜沫本人自报才加新证；后泛称姐妹不会推翻先前堂妹说明，不能靠同名省掉辨识成本。'),
 dict(observation='物品从约定到接收、装用的间隔，使获得感延后且可追；真正交到手的一幕又能给旧期待明确收束。',mechanism='先让物承载愿望或关系，再以寄存/代送暂缓兑现；在后场面用亲捧、交首或即时换装给可见完成动作，未落槌的拍卖则把期待留到下一章。',limits_and_counterevidence='镇岳挽亲收、龙牙林立即实装已经足以闭局部期待，不能一律当没交；车钥与旧膝代送缺本人使用，价格叫到千万仍不等售成。'),
 dict(observation='玩家可复活维持长战，NPC与现实身体的不同恢复代价仍使风险有层次；具名死者让胜后奖励不能把全场痛感清零。',mechanism='在同一战争中交叉写掉级后归队、重伤再起、尸体确认和系统部分恢复，让读者比较哪些损失能补、补到什么程度；现实断肋再转训练，使武力成长回应具体脆弱。',limits_and_counterevidence='韩穿胸后起身并非先死后复，兰有明确救醒过程；徐焰尸证不能由泛称普通军恢复自动推翻，而铁靴游戏再现也不能当现实死者复生。'),
 dict(observation='装备名称和数值无说明滑移，会迫使读者反复重算人物当前能做什么，削弱规则作为预判依据的可信度。',mechanism='御天活体限制后举野猪、已换双剑后又称冠军之刃、神威射程从两千到三千，都使熟悉前条件的读者产生识别停顿；明确说明改造或规则变动本可承接，当前这些地方没有。',limits_and_counterevidence='不能把每次省略都当冲突：王域近两小时叙述未列完整时间，冷却是否真改仍难定；星辰戒面板与东口述有别而尚未实测，不能择一补成隐藏连段。'),
 dict(observation='系统奖励关闭局部行动，同时把新资源、未触发条件和关系承诺推向下一段，既给本卷完成感又保继续阅读的方向。',mechanism='征岛任务用等级奖励与实运补给收束，转头以主替兄弟求龙骑接新目标；野域双王死/群龙迁回完成后，天界封神、一周点将和拍卖落槌仍各缺一个具体事件。',limits_and_counterevidence='留下一步不等前任务失败：百岛SSS与抢龙SSS已完成；子舒受群龙效忠还不是正式龙神，千万叫价也不会自动代下章成交。')
]
for i,delta in enumerate(continuity):
 old=A['dimensions']['continuity'][i];new=copy.deepcopy(old);new.update(delta)
 assert new['textual_fact']==old['textual_fact'] and new['evidence']==old['evidence'] and new['interpretation_evidence']==old['interpretation_evidence']
 propose('analysis.json',['dimensions','continuity',i],new,'将研究操作口吻改为小说如何维持/削弱连续阅读的文学观察；事实证据逐值不动。')
boost_i=next(i for i,c in enumerate(C) if c['origin_key'].endswith('/scene/boost'))
boost=copy.deepcopy(C[boost_i]);boost['content'].update(summary='武汉同一商场北片普通持刀者被杭州小队击杀且当地平民无伤；李转南区援上海小队后亲见十余平民尸/唐林伤，A破甲伤李，最终两个C留活。',obstacle='同一商场南北分区袭击/不同等级殖装人，北片成功不代表南片已安全。',choice='先护北片平民，奉王信命令南援；以狙击和阳炎应战、留两C研究。',why_it_works='用同一现场不同分区和小队损失对照，局部迅速制止袭击不能遮盖南区平民死亡与主本人的轻伤。',applicability='同一现场有多分区和不同队伍应对，读者必须区分队伍归属城市与当时地理位置，局部成功不能覆盖另一片伤亡。',failure_mode='上海是小队归属而非本场另一城市；北片普通持刀者并非殖装人，不能把主对北片无伤推广全场，技术源仍未查明。')
boost['evidence']=[dict(source_id=A['source_id'],revision=A['revision'],chapter_id=f'ch-{n:04d}',start_line=next(x for x in rows if x['chapter_id']==f'ch-{n:04d}')['start_line'],end_line=next(x for x in rows if x['chapter_id']==f'ch-{n:04d}')['end_line'],claim_kind='fact') for n in [1091,1092,1093,1094]]
propose('cards.json',[boost_i],boost,'重新全文回读1091—94确认主现场武汉；原标题正确保留，原summary误把同场分区/小队籍属写跨地，逐字段纠正。')
node_i=next(i for i,n in enumerate(G['nodes']) if n['id']=='v05-s-boost')
node=copy.deepcopy(G['nodes'][node_i]);node.update(summary=boost['content']['summary'],evidence=boost['evidence'])
propose('graph.json',['nodes',node_i],node,'同步同场分区的summary及新增1091地点证据，不动关系和线程结论。')
cannon_i=next(i for i,c in enumerate(C) if c['origin_key'].endswith('/scene/cannon'))
cannon=copy.deepcopy(C[cannon_i]);cannon['content']['characters_origin_keys']=[x for x in cannon['content']['characters_origin_keys'] if not x.endswith('/character/police')]
propose('cards.json',[cannon_i],cannon,'游戏神威炮场没有现实王信参与，只撤其人物关系引用，其他字段不动。')
cn_i=next(i for i,n in enumerate(G['nodes']) if n['id']=='v05-s-cannon');cn=copy.deepcopy(G['nodes'][cn_i]);cn['character_origin_keys']=cannon['content']['characters_origin_keys']
propose('graph.json',['nodes',cn_i],cn,'同步移除炮场节点的王信引用。')
propose('analysis.json',['named_life_state_audit',12,'name'],'五名A级袭击者（其中一名日本活口已核）','只一人日本国籍被核，四死者国籍未明；state与证据不改。')
impact=[]
needles=['跨地','跨地域','别地','北普通殖装','日本五A']
def scan(x,path):
 if isinstance(x,dict):
  for k,v in x.items():scan(v,path+[k])
 elif isinstance(x,list):
  for i,v in enumerate(x):scan(v,path+[i])
 elif isinstance(x,str) and any(n in x for n in needles):impact.append(dict(path=path,value=x))
for file,obj in [('analysis.json',A),('cards.json',C),('graph.json',G)]:scan(obj,[file])
save('primary-review-impact-scan.json',dict(core_sha256=hashes,matches=impact,meaning='核武汉误分区与五A国籍扩写传播；所有已发现路径均在提案内或需主审另核。'))
save('primary-review-proposal.json',dict(status='proposal-pending-primary-review-not-applied',source_id=A['source_id'],revision=A['revision'],volume=5,before_core_sha256=hashes,before_snapshot='review-corrections/primary-before/snapshot.json',changes=changes,unchanged='原四栏notes/read-log/reader-state不动；连续性五项事实/证据不动；除列明对象外其他核心内容逐值不动。',recheck='raw1091—1094本次再次BEGIN-END完整亲读，无截断；王信现实人物不得放入游戏炮场。',user_approval=False))
for n in ['report.md','handoff.md']:
 t=(P/n).read_text(encoding='utf-8').replace('20项源疑/改规','19项源疑').replace('20源疑/改规','19源疑')
 (P/n).write_text(t,encoding='utf-8')
support=['report.md','handoff.md','validation.json','self-review-receipt.json','research-checkpoint.json','primary-review-proposal.json','primary-review-impact-scan.json','review-corrections/primary-before/snapshot.json']
save('freeze-manifest.json',dict(status='draft-frozen-before-primary-proposals',source_id=A['source_id'],revision=A['revision'],volume=5,complete_book=False,core_sha256=hashes,support_sha256={n:h(P/n) for n in support},external_input_sha256={'../source.json':h(P.parent/'source.json'),'collection/reading-units.json':h(P.parents[4]/'writing-vault/library/reports/collection/reading-units.json')},notes='冻结现件不重跑builder；提案尚未合入，主审批准后只应用精准路径并保差分。此冻结不等文学签收。'))
assert hashes=={n:h(P/n) for n in core}
print(json.dumps(dict(core_sha256=hashes,manifest_sha256=h(P/'freeze-manifest.json'),proposal_sha256=h(P/'primary-review-proposal.json'),change_count=len(changes),impact_count=len(impact),validation=result),ensure_ascii=False))
