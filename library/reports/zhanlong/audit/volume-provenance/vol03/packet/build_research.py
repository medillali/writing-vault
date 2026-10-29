"""序列化primary手写研究；阅读证据来自两位实际原文读者及完整派生接读。"""
import pathlib,json,collections,sys
sys.stdout.reconfigure(encoding='utf-8')
P=pathlib.Path(__file__).parent;S=json.loads((P.parent/'source.json').read_text(encoding='utf-8'))
SID,REV=S['source_id'],S['revision'];SPEC=next(v for v in S['volumes'] if v['volume']==3)
CH={int(c['chapter_id'][3:]):c for c in S['chapters']};IDS=[c['chapter_id'] for u in SPEC['units'] for c in u['segments']]
NOTES=[json.loads(x) for x in (P/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines() if x]
assert [n['chapter_id'] for n in NOTES]==IDS
def save(n,x):(P/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def ev(nums,kind='fact'):
 return [{'source_id':SID,'revision':REV,'chapter_id':CH[n]['chapter_id'],'start_line':CH[n]['start_line'],'end_line':CH[n]['end_line'],'claim_kind':kind} for n in dict.fromkeys(nums)]
def origin(t,k):return f'{SID}/full-20261025/vol03/{t}/{k}'
dimensions={d:[] for d in ['worldbuilding','characters','plot','style','narrative','dialogue','pacing','themes','continuity']}
def obs(d,title,fact,interpretation,mechanism,limits,nums):
 dimensions[d].append({'id':f'v03-{d}-{len(dimensions[d])+1:02d}','title':title,'claim_kind':'inference','textual_fact':fact,'observation':interpretation,'mechanism':mechanism,'limits_and_counterevidence':limits,'evidence':ev(nums),'interpretation_evidence':ev(nums,'inference'),'review_status':'draft'})
exec((P/'research_dimensions.py').read_text(encoding='utf-8'))
CARDS=[];CHARACTERS={};SCENES={};PATTERNS={}
def card(t,key,title,content,nums):
 c={'asset_type':t,'scope':'reusable-pattern' if t=='pattern' else 'source-analysis','title':title,'origin_key':origin(t,key),'tags':['作者:失落叶','作品:斩龙','卷3','待审阅'],'content':content,'evidence':ev(nums,'synthesis' if t=='pattern' else 'fact'),'user_notes':'','favorite':False,'review_status':'draft'}
 CARDS.append(c);return c
def char(key,name,summary,goal,limits,decision,change,relations,nums):
 c=card('character',key,name+'｜卷三阶段',{'summary':summary,'goal':goal,'limitations':limits,'decision_pattern':decision,'stage_change':change,'relationship_direction':relations,'claim_kind':'inference','valid_at':'raw0505—0753卷末，非全书终点'},nums);CHARACTERS[key]=c
def scene(key,title,summary,goal,obstacle,choice,result,state,why,applicability,failure,nums,people):
 c=card('scene',key,title,{'summary':summary,'goal':goal,'obstacle':obstacle,'choice':choice,'consequence':result,'state_change':state,'why_it_works':why,'applicability':applicability,'failure_mode':failure,'characters_origin_keys':[origin('character',k) for k in people],'claim_kind':'inference','narrative_order':max(nums)},nums);SCENES[key]=c
def pattern(key,title,summary,steps,conditions,failure,transform,keys,nums):
 c=card('pattern',key,title,{'summary':summary,'causal_steps':steps,'applicability':conditions,'failure_mode':failure,'originality_transform':transform,'derived_from_origin_keys':[origin('scene',k) for k in keys],'claim_kind':'synthesis'},nums);PATTERNS[key]=c
exec((P/'research_characters.py').read_text(encoding='utf-8'))
exec((P/'research_scenes.py').read_text(encoding='utf-8'))
exec((P/'research_supplements.py').read_text(encoding='utf-8'))
exec((P/'research_graph.py').read_text(encoding='utf-8'))
A={'source_id':SID,'revision':REV,'volume':3,'title':'卷三 一代宗师｜九维研究草稿','read_chapter_ids':IDS,'review_status':'draft','coverage':{'raw_fragments':249,'body_units':248,'complete_volume':True,'complete_book':False,'reading_attribution':'reading-attribution.json'},'method':'前149片zongheng_vol05_full实际全文，尾100片primary实际全文。primary按批完整派生读前149条四栏后手写整卷研究，保原行/reader/时间戳。章界引用通过逐章notes细定位；不冒称个人整卷原文阅读。','dimensions':dimensions,'major_character_states':[{'origin_key':c['origin_key'],'name':c['title'],'summary':c['content']['summary'],'stage_change':c['content']['stage_change'],'relationships':c['content']['relationship_direction'],'evidence':c['evidence']} for c in CHARACTERS.values()],'plot_and_hidden_threads':GRAPH['threads'],'open_questions':QUESTIONS,'unresolved_and_anomalies':ANOMALIES,'named_life_state_audit':LIFE_STATES,'chapter_unresolved_index':[{'chapter_id':n['chapter_id'],'reader':n['reader'],'unresolved':n['unresolved'],'evidence':ev([int(n['chapter_id'][3:])])} for n in NOTES if n.get('unresolved')],'chapter_source_anomaly_index':[{'chapter_id':n['chapter_id'],'reader':n['reader'],'source_anomalies':n['source_anomalies'],'evidence':ev([int(n['chapter_id'][3:])])} for n in NOTES if n.get('source_anomalies')],'transferable_patterns':[{'origin_key':c['origin_key'],'summary':c['content']['summary'],'evidence':c['evidence']} for c in PATTERNS.values()],'literary_limits':['第一人称身体凝视、性化玩笑和民族/性别贬词保为文本现象，不采为用户风格。','保护弱者的自述与抢资源、守尸、亲疏偏袒并列，研究不替角色作无条件道德背书。','原文事实/角色转述或推测/研究解释分层；用户评价空，原创设定未生成。','卷末135级、9级龙城、9700余铁刃、全球赛/正式国战未开始，不能倒灌后卷。'],'user_evaluation':None}
save('analysis.json',A);save('cards.json',CARDS);save('graph.json',GRAPH)
save('research-checkpoint.json',{'status':'core-artifacts-written-draft','reading_complete':True,'personal_full_volume_read':False,'counts':{'observations':sum(map(len,dimensions.values())),'cards':dict(collections.Counter(c['asset_type'] for c in CARDS)),'nodes':len(GRAPH['nodes']),'edges':len(GRAPH['edges']),'threads':len(GRAPH['threads'])},'next_work':'报告、原行/定位与图预检、主代理语义核验后正式入库'})
print(json.dumps(json.loads((P/'research-checkpoint.json').read_text(encoding='utf-8')),ensure_ascii=False))
