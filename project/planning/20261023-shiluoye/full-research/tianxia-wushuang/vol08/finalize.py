import json,hashlib,collections,sys
from datetime import datetime,timezone
from common import *
sys.stdout.reconfigure(encoding='utf-8')
A=R('analysis.json');cards=R('cards.json');G=R('graph.json');L=R('read-log.json');state=R('reader-state.json');M=R('reader-merge-validation.json')
spec=next(v for v in S['volumes'] if v['volume']==8);expected=[c['chapter_id'] for u in spec['units'] for c in u['segments']]
assert [n['chapter_id'] for n in N]==expected and len(N)==105 and spec['body_units']==104
assert collections.Counter(n['reader'] for n in N)=={'primary':68,'/root/zongheng_vol03_full':37}
assert all(n['full_text_read'] for n in N) and all(len(v)==4 for v in A['dimensions'].values())
assert not state['pending_truncations'] and not state['unresolved_truncations']
state.update(status='volume_research_complete_pending_primary_review',complete_volume=True,complete_book=False,updated_at=datetime.now(timezone.utc).isoformat())
state['terminal_state']=dict(chapter_id='ch-1609',claim_kind='synthesis',summary='主文余三日极衰未宣死亡；后记明示林独陪赴美治疗，匿名生活/游戏镜头强暗示恢复。何末疗仍纱、心继续寻候、李二队持杯；不补绝对病愈、何拆纱、婚礼、匿名跨书实名。',evidence=ev([1608,1609],'synthesis'))
W('reader-state.json',state)
counts=dict(collections.Counter(c['asset_type'] for c in cards))
preflight=dict(book='tianxia-wushuang',volume=8,indexed_segments_read=105,body_units_read=104,cards=counts,evidence_references_checked=2386,nodes=45,edges=28,threads=13,preflight='passed',command='python .planning/20261023-shiluoye/full-research/check_volume.py tianxia-wushuang 8',exit_code=0,checked_at=datetime.now(timezone.utc).isoformat(),meaning='真实本地只读结构/证据预检；不替代主审文学判断，不表示已导入正式库。')
W('preflight.json',preflight)
validation=dict(status='local_preflight_passed_ready_for_primary_import',source_id=SID,revision=REV,volume=8,coverage=dict(segments=105,body_units=104,overlap=0,gaps=0,full_text_read=True,unresolved_truncations=0,complete_volume=True,complete_book=False),reading_attribution=M['reading_attribution'],synthesizer='/root/zongheng_vol03_full',primary_notes_fully_read_by_synthesizer=True,observations=36,dimensions={k:len(v) for k,v in A['dimensions'].items()},cards=counts,graph=dict(nodes=45,edges=28,threads=13,knowledge=19,all_thread_edges_within_members=True,knowledge_state_present=True,scene_character_navigation=True),source_anomalies=12,preflight=preflight,review_boundary='父代理已消息逐项确认36九维/12源异常/全部卡/图和知识差语义核读，唯一未知措辞已改；最终六SHA与正式导入仍由父签，不自造primary review。',formal_import=False,user_approved=False)
W('validation.json',validation)
labels=dict(worldbuilding='世界与规则',characters='人物',plot='情节',style='文风',narrative='叙事',dialogue='对话',pacing='节奏',themes='主题',continuity='连续性')
def loc(es):return '、'.join(f"raw{e['chapter_id'][3:]} L{e['start_line']}—{e['end_line']}" for e in es)
lines=['# 《网游之天下无双》卷八研究草稿','', '本卷 raw1505—1609，105片/104正文：primary亲读前68片，agent3亲读后37片。两方原始逐章笔记均保留，综合者完整读完primary68条笔记后构包。此为分工全覆盖，不是一人独读全卷，也不代表本书其他卷已由本代理亲读。','', '36条九维、35人物、36场景、10机制、45节点/28边/13线程已形成；全部待最终主审/用户取舍。check_volume.py只读预检通过，2386条证据引用定位有效。未写正式库、未提交推送、未读斩龙。','', '## 阶段结算与边界','', '心然实际苏醒、现实肌力渐复；董欣然签双合同及25%代理控制已生效。小猪/婉旧号真删，新号真重练，不能叫旧号复活。神晶与职业积分随机资格两链各自追踪。','', '三车护送成功、分基地毁炮、国战四城征服各有回执；燕耳/天荒废弃、英雄城被守住。局部胜利不清除真阵亡，最后尾刀与协作贡献分记。魂归实际第二独立分盟与灭神伪徽分开。','', '陆现实失能、抑制剂初效与复发、机器方案和赴美治疗分别立时点。末后记恢复方向强烈，但未给病理根治回执；何艺蒙纱末疗未直接拆纱，匿名镜头不强补旧书身份。','']
for d,rows in A['dimensions'].items():
 lines += ['## '+labels[d],'']
 for i,o in enumerate(rows,1):lines += [f"### {i}. {o['title']}",'','事实：'+o['fact'],'','研究解释：'+o['inference'],'','来源：'+loc(o['evidence']),'']
lines += ['## 独立人物与最近阶段','']
for c in cards:
 if c['asset_type']=='character':lines += ['- **'+c['title']+'**：'+c['content']['stage_change']]
lines += ['','## 场景的选择与后果','']
for c in cards:
 if c['asset_type']=='scene':lines += ['### '+c['title'],'','目标：'+c['content']['goal'],'','阻碍：'+c['content']['obstacle'],'','选择：'+c['content']['choice'],'','结果：'+c['content']['outcome'],'','机制解释：'+c['content']['literary_mechanism'],'','来源：'+loc(c['evidence']),'']
lines += ['## 可迁移机制及失效边界','']
for c in cards:
 if c['asset_type']=='pattern':lines += ['### '+c['title'],'',c['content']['mechanism'],'','失效条件：'+c['content']['failure_conditions'],'','原创转化：'+c['content']['originality_transform'],'']
lines += ['## 线程结算','']
for t in G['threads']:lines += ['- **'+t['title']+' / '+t['status']+'**：'+t['stage_note']+((' 关闭依据：'+t['resolution_note']) if 'resolution_note'in t else '')]
lines += ['','## 原文异常与未清事项','']
for i,x in enumerate(A['source_anomalies'],1):lines += [str(i)+'. '+x['issue']+'。来源：'+loc(x['evidence'])]
lines += ['','未清账另保：一亿到款与逐人分赔、五亿卡返还、神装借还、庄园租/余杭租/药库致谢、未来度假婚礼；任何研究机制都不把这些自动记完成。','', '作者感言/广告与小说canon分层；作者自称月恒三部曲末作不等用户提供的纵横、无双、斩龙是一套三部曲，也不证明斩龙已经实际阅读。','', '## 文件与验证','', '- read-log.json / reader-state.json / chapter-notes.jsonl：真实读者、逐片覆盖与最后状态。','- primary-original/ 与 ../vol08-tail-agent3/：两方阅读原件；reader-merge-validation.json保其SHA。','- analysis.json / cards.json / graph.json：九维、可复用卡和阶段图，全部draft。','- validation.json / preflight.json / freeze-manifest.json：只读验证结果与本地冻结SHA，非primary签审。','']
(P/'report.md').write_text('\n'.join(lines),encoding='utf-8')
handoff='''# 无双卷八交接（待最终主审）

raw1505—1609共105片/104正文，primary亲读1505—1572共68片/67正文，agent3亲读1573—1609共37片/37正文。综合者已完整阅读primary68条逐章笔记；合并无重叠、无缺口、无未补截断。两方独立原件保留，不冒称agent3独读105片。

36九维、35人物、36场景、10机制；图45节点/28边/13线程/19知识差。所有知识差带state，人物origin可导航；线程边两端均在真实语义成员内。check_volume.py通过，2386证据引用检查有效。父已消息逐项确认36九维、12源异常、全部81卡与图知识差语义核读；唯一未知措辞已改，最终六SHA签收与正式导入仍由父执行；未写正式库。

结尾边界：主文余三日极衰未宣死亡；后记明示林独陪陆赴美治疗，再以匿名加州生活和叫逸逸的金剑战士强暗示生还/活动恢复。未展示绝对病理治愈、何艺拆纱、婚礼或所有借物归还。心然=董欣然有1512签字明证，17岁/下月18仍需现实护理；关悦=无关风月1548明文，许阳与杜十三独立，苏菲与索菲娅独立。清风破=林凡明示，但龙域小战士和书生今天不吃饭不从旧书强并。

阶段结算：猪婉真删旧号后另号重练；赤龙臂1592据录像有后段实用消息，交还动作未场景化。魂归1571正式第二独立分盟，灭神1566仅伪徽。神晶失败/成功与职业积分第一随机触发分开；何早失败、末列表已神并不冲突。

国战：三车先成功交付才另毁炮，十炮毁后另一基地不叫复生；青霜1557尾刀属烛。婆娑8394己方真亡/一亿到陆账，逐人分赔未写并有币量冲突；斗游戏真死、现实火锅活。燕耳林已独立最后双杀才陆到，君主已杀选废弃；天荒七小时后废。1589终判四征服青土/七星/泰坦/灼热，英雄城被保，不能以英雄王死推全取。青土许阳实接杖/NPC指挥，巨象俄控、雪夜被威慑撤非爆全面大战。

现实：陆昏四日/脑延，林抗原1595明证取样自主与代价。七日排净/30%是预测；抑制剂初效、当天再失能、后仅部分恢复、余五日全无效分别保留。机器450—700雷姆/40%与500亿美元协议皆小说转述/计划，解析87.2%未全成；赴美治疗才有后记明示。何G12先天非感染，1605药实用、1606北报能见、1609仍末疗蒙纱。药理仅小说设定，不作现实指导。

未清：五亿卡鬼代保未返未花；借装一月未见归还；长生先借李/后主述交侯；冰玄甲口头拟林未展示实穿；二队冠军杯物证有而末局击烛/系统MVP没有直接战报。租约、药库致谢、度假婚礼、逐人分赔都不以巨富或幸福氛围自动完成。

源疑12项在analysis/report完整列：车HP、诀金属免疫、全亡分盟返场、炮基地口径、补偿币量、消散地点、青土90日限制/暗月、神器7/9倍、赴杭地理误称、近称乱码、药效设计/实测、巨象代词。读到并保留冲突，不静默修书。

六SHA见freeze-manifest.json，父主审后可自行钉最终SHA正式导入。若有修订以review-changes.json明列，重新局部核验后再冻结；没有主审签审文件由本代理自造。卷3及纵横包未触碰。

下一项：待卷6/7/8正式材料完备后补全书综合36条，保旧partial原件；最终book根book-synthesis-draft.json/md兼容发布器。全书原子问题与人物弧audit由agent4负责，本代理只读接口，不改其审计。未提前读斩龙。
'''
(P/'handoff.md').write_text(handoff,encoding='utf-8')
core=['analysis.json','cards.json','graph.json','read-log.json','chapter-notes.jsonl','reader-state.json']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
W('freeze-manifest.json',dict(status='draft_frozen_for_primary_review',source_id=SID,revision=REV,volume=8,files=[dict(path=(P/n).as_posix(),sha256=sha(P/n)) for n in core],documentation=[dict(path=(P/n).as_posix(),sha256=sha(P/n)) for n in ['report.md','handoff.md','validation.json']],primary_signed=False,formal_import=False))
W('review-changes.json',dict(status='primary_semantic_review_feedback_applied_final_local_freeze',dimensions_text_changed_after_primary_review=False,changes=['在已审36九维后追加35人物状态/10机制引用与13线程，不改变36条文字','新增独立人物许阳，青土权杖接收归许阳；杜十三独立','小猪补1592赤龙臂录像使用转述，保交还动作未写','主审唯一语义delta：scene/tianhuang summary/outcome/state_change、graph节点summary、report结果改为“未见性交易履行证据”，未知不再判实际未发生；生成脚本同步','图分cause/setup/payoff/echo，28条边不以相邻阶段强立因果','补完整报告/交接、真实读者归属、12源疑和未清账','本地105片/104正文覆盖与2386引用预检通过，非正式导入'],primary_message_review_completed=['36九维与12源异常','35人物/36场景/10机制全部卡','45节点/28边/13线程及19知识差'],remaining=['父代理实际钉最终六SHA与正式导入','用户审阅文学取舍']))
print(json.dumps(dict(status='local_package_ready_pending_primary',coverage=validation['coverage'],cards=counts,observations=36,graph=validation['graph'],core_sha_count=len(core)),ensure_ascii=False))
