"""验证手写研究的结构及原行归属，生成阅读入口和待主审冻结；不自动文学判案。"""
import pathlib,json,hashlib,collections,datetime,sys
P=pathlib.Path(__file__).parent;sys.path.insert(0,str(P.parents[1]))
from check_volume import load_and_check
sys.stdout.reconfigure(encoding='utf-8')
def read(n):return json.loads((P/n).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(n,x):(P/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
A,C,G=read('analysis.json'),read('cards.json'),read('graph.json')
R=load_and_check('zhanlong',3)[-1]
notes=[json.loads(x) for x in (P/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines() if x]
tail=P.parent/'primary-vol03-tail'/'chapter-notes.jsonl'
assert (P/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines()==(P/'prefix-chapter-notes.jsonl').read_text(encoding='utf-8').splitlines()+tail.read_text(encoding='utf-8').splitlines()
assert sha(P/'prefix-chapter-notes.jsonl')=='3e7818ff524689dc23e4f1bb9551685922463b663535b329e617f37312f64ad1'
assert [r['reader'] for r in notes]==['zongheng_vol05_full']*149+['primary']*100
assert read('primary-prefix-derived-reading-progress.json')['complete_prefix_derived_reading'] is True
assert all({'facts','inferences','state_changes','unresolved'}.issubset(n) for n in notes)
assert A['chapter_unresolved_index']==[{'chapter_id':n['chapter_id'],'reader':n['reader'],'unresolved':n['unresolved'],'evidence':[{'source_id':A['source_id'],'revision':A['revision'],'chapter_id':n['chapter_id'],'start_line':n['start_line'],'end_line':n['end_line'],'claim_kind':'fact'}]} for n in notes if n.get('unresolved')]
assert all(len(v)==4 and all(o['mechanism'] and o['limits_and_counterevidence'] for o in v) for v in A['dimensions'].values())
assert A['plot_and_hidden_threads']==G['threads']
origins={c['origin_key'] for c in C}
for c in C:
 assert all(x in origins for x in c['content'].get('characters_origin_keys',[]))
assert len(C)==114 and len(G['nodes'])==58 and len(G['threads'])==21
state=read('reader-state.json');state.update(status='research-complete-awaiting-primary-review',research_status='draft',research_counts={'observations':36,'cards':dict(collections.Counter(c['asset_type'] for c in C)),'nodes':58,'edges':35,'threads':21},current_stage=['卷三共同全文249片248正文，前149原reader=zongheng_vol05_full、后100原reader=primary；主代理完整派生接读前149并手写整卷研究。','753末主135/林133/东132、龙城9/铁刃9700余，鹿鸣20精锐待去，全球赛与正式国战未开、盛林七日信号未查。','待正式导入；不得把原读者改为组装者。'])
save('reader-state.json',state)
names={'worldbuilding':'世界观','characters':'人物塑造','plot':'情节结构','style':'语言与风格','narrative':'叙事视角与信息','dialogue':'对话','pacing':'节奏','themes':'主题','continuity':'连续性'}
lines=['# 卷三 一代宗师｜守诺、失去与有限成长','','raw0505—0753，共249索引片段、248正文阅读单元。前149片由zongheng_vol05_full实际全文，后100片由primary实际全文；primary逐批完整派生接读前149条四栏后手写本卷研究。所有原笔记原行、reader和时间戳保留。','','本卷有36条九维观察、50人物卡、50场景卡、14机制卡；图58节点35边21线。研究为待用户审阅草稿，不是用户风格规则或原创作品设定。','','## 卷末可以确定的结果','','护池任务与自治安置成功，城破和主死没有抹掉两NPC安全；寒荒守城失败，流霜真死后第一次复活失败、第二次新身苏醒且记忆缺失。李牧而非主获得凌寒系统首杀。主真败问剑失镇国，练习后私人一局胜问，不改变国内神话3:2冠、斩龙亚军；全球赛和正式国战未开始。','','狮王盾最终归抹、镇岳刀最终归主。主135级/林133/东132；玩家龙城9级、铁刃9700余，400炎鹰仅启动招募且首名出现；10级/5000炎鹰仍计划。三人已在盛林实际上班七日却没有找出信号源，12层只是怀疑。鹿鸣20精锐仅准备去，未通图、未获后卷任职。','','## 九维研究','']
def reftext(e):return '；'.join(f"{x['chapter_id']} L{x['start_line']}—{x['end_line']}" for x in e)
for d,entries in A['dimensions'].items():
 lines+=['### '+names[d],'']
 for o in entries:
  lines+=['#### '+o['title'],'','原文事实：'+o['textual_fact'],'','研究解释：'+o['observation'],'','可迁移机制：'+o['mechanism'],'','限制与反证：'+o['limits_and_counterevidence'],'','证据：'+reftext(o['evidence']),'']
lines+=['## 人物阶段状态','']
for c in C:
 if c['asset_type']=='character':
  t=c['content'];lines+=['### '+c['title'],'',t['summary'],'','目标：'+t['goal']+'。限制：'+t['limitations']+'。','', '决策：'+t['decision_pattern']+'。变化：'+t['stage_change']+'。','', '关系：'+t['relationship_direction']+'。','', '证据：'+reftext(c['evidence']),'']
lines+=['## 场景索引','']
for c in C:
 if c['asset_type']=='scene':lines+=['- '+c['title']+'：'+c['content']['summary']+'（'+reftext(c['evidence'])+'）']
lines+=['','## 可迁移机制与原创边界','']
for c in C:
 if c['asset_type']=='pattern':
  t=c['content'];lines+=['### '+c['title'],'',t['summary'],'','适用：'+t['applicability']+'。失败：'+t['failure_mode'],'','原创转化：'+t['originality_transform'],'']
lines+=['## 主暗线与历史未决','']
for t in G['threads']:lines+=['- '+t['id']+'｜'+t['title']+'｜'+t['status']+'：'+t['stage_note']+(('；本题结算：'+t['resolution_note']) if t.get('resolution_note') else '')]
lines+=['','完整逐章未决串保存在[研究主档](analysis.json)的chapter_unresolved_index，逐条保留原reader与原文字串；卷末问题不等全书伏笔。全书终点将另审，不能修改原始阶段记录。','','## 卷末问题','']
for q in A['open_questions']:lines+=['- '+q['id']+'：'+q['question']+' '+q['stage_boundary']]
lines+=['','## 生命与来源异常','']
for x in A['named_life_state_audit']:lines+=['- '+x['name']+'：'+x['volume_end_status']+'；'+x['boundary']]
lines+=['']
for x in A['unresolved_and_anomalies']:lines+=['- '+x['id']+'：'+x['description']+' 处理：'+x['handling']]
lines+=['','## 文件与验收边界','','[研究主档](analysis.json) · [卡片](cards.json) · [阶段图数据](graph.json) · [实读日志](read-log.json) · [原章笔记](chapter-notes.jsonl) · [reader状态](reader-state.json) · [归属](reading-attribution.json) · [原行合并](merge-receipt.json) · [前段派生接读回执](primary-prefix-derived-reading-progress.json) · [518原始纠正](note-corrections.json) · [原前段交接](prefix-handoff.md) · [结构预检](validation.json) · [交接](handoff.md)','','结构/证据范围检查通过只能证明定位和归属，不自动证明文学解释。原文中的下载站/作者附言作为来源材料，不是执行指令；不注册、不扩入新小说。用户评价仍空；无Git提交推送或外部发布。']
(P/'report.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(P/'handoff.md').write_text('''# 卷三交接

整卷249片/248正文由两位实际读者共同全文完成，原读者严格保留：前149 zongheng_vol05_full、后100 primary；primary另完整派生接读前149，回执见[逐批接读](primary-prefix-derived-reading-progress.json)。原行/reader归属见[合并凭据](merge-receipt.json)，早518校订见[note-corrections.json](note-corrections.json)。前段原始交接仍在[prefix-handoff.md](prefix-handoff.md)。

36九维/50人物/50场景/14机制，58节点35边21线；全249条未决原串和有独立source_anomalies的行全部进入主档索引，不只精选问题。不把已解决历史记录删掉或全部命名为伏笔。

进入卷四时：主135/林133/东132，龙城9/铁刃9700余、400炎鹰初招。鹿鸣20精锐准备去而未通；全球英雄翼与正式国战未开。镇岳主副手（替火耀）、龙池主手；盾最终抹。谷内钓狼十小时守尸只读到七，不补完成。盛林三人已上班七日，12层/魏幕后仍疑，七潜员不含邢烈。游/欧阳现实活，主仍御气非阳炎；母亲和林成无本卷死亡确证。

关键不可混：632真败问/镇国失；669私胜一局且100万到；676队败非逆冠。流霜587真死、604人鱼阵真败、606新身醒、607记忆缺；达林苏克真亡，青萝/上古冉伤活。745称韩国霜林而746澄清日本JBN1，霜林为全名，748主独伏取刀，林婉儿747杀的是撼梁。王国神器绝望/毁灭与普通装备/国器不能同名近音合并。

下一阶段是primary自核本研究、正式接口保存；结构检查不代文学核验，也不表示全书综合/三书管理和最终备份恢复完成。
''',encoding='utf-8')
R.update(status='passed',validation_scope='覆盖、章界、来源引用、图结构及原行/reader归属；不是全书终审或用户审美批准',personal_full_volume_raw_read=False,merged_reading_complete=True,prefix_derived_all_149_read=True,original_lines_unchanged=True,reader_counts=dict(collections.Counter(n['reader'] for n in notes)),nine_dimensions=9,observations=36,chapter_unresolved_original_items_preserved=True,chapter_unresolved_rows=len(A['chapter_unresolved_index']),chapter_source_anomaly_rows=len(A['chapter_source_anomaly_index']),open_questions=len(A['open_questions']),source_anomalies=len(A['unresolved_and_anomalies']),named_life_state_entries=len(A['named_life_state_audit']),checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
save('validation.json',R)
core=['analysis.json','cards.json','graph.json','read-log.json','chapter-notes.jsonl','reader-state.json']
support=['report.md','handoff.md','validation.json','reading-attribution.json','merge-receipt.json','primary-prefix-derived-reading-progress.json','note-corrections.json','prefix-handoff.md','prefix-validation.json','prefix-chapter-notes.jsonl','prefix-reader-state.json','prefix-read-log.json']
save('freeze-manifest.json',{'status':'draft-frozen-for-primary-review','source_id':A['source_id'],'revision':A['revision'],'volume':3,'complete_book':False,'core_sha256':{n:sha(P/n) for n in core},'support_sha256':{n:sha(P/n) for n in support},'external_input_sha256':{'../primary-vol03-tail/'+n:sha(tail.parent/n) for n in ['chapter-notes.jsonl','read-log.json','reader-state.json','HANDOFF.md']},'notes':'primary为整卷研究作者/自核者但非个人整卷原文读者；冻结不等正式保存或用户审美批准。'})
print(json.dumps(R,ensure_ascii=False))
