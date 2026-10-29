"""序列化本代理手写的分卷研究，不通过检索或自动摘要生成阅读结论。"""
import pathlib,json,hashlib,collections,sys
sys.stdout.reconfigure(encoding='utf-8')
P=pathlib.Path(__file__).parent;S=json.loads((P.parent/'source.json').read_text(encoding='utf-8'))
SID,REV=S['source_id'],S['revision'];SPEC=next(v for v in S['volumes'] if v['volume']==2)
CH={int(c['chapter_id'].split('-')[1]):c for c in S['chapters']}
IDS=[s['chapter_id'] for u in SPEC['units'] for s in u['segments']]
NOTES=[json.loads(x) for x in (P/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines() if x]
assert [n['chapter_id'] for n in NOTES]==IDS
def save(n,x):(P/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def ev(nums,kind='fact'):
 return [{'source_id':SID,'revision':REV,'chapter_id':CH[n]['chapter_id'],'start_line':CH[n]['start_line'],'end_line':CH[n]['end_line'],'claim_kind':kind} for n in dict.fromkeys(nums)]
def origin(t,k):return f'{SID}/full-20261025/vol02/{t}/{k}'
DIMS=['worldbuilding','characters','plot','style','narrative','dialogue','pacing','themes','continuity'];dimensions={d:[] for d in DIMS}
def obs(d,title,fact,inference,mechanism,limits,nums):
 dimensions[d].append({'id':f'v02-{d}-{len(dimensions[d])+1:02}','title':title,'claim_kind':'inference','textual_fact':fact,'observation':inference,'mechanism':mechanism,'limits_and_counterevidence':limits,'evidence':ev(nums),'interpretation_evidence':ev(nums,'inference'),'review_status':'draft'})
exec((P/'research_dimensions.py').read_text(encoding='utf-8'))
CARDS=[];CHARACTERS={};SCENES={};PATTERNS={}
def card(t,key,title,content,nums):
 c={'asset_type':t,'scope':'reusable-pattern' if t=='pattern' else 'source-analysis','title':title,'origin_key':origin(t,key),'tags':['作者:失落叶','作品:斩龙','卷2','待审阅'],'content':content,'evidence':ev(nums,'synthesis' if t=='pattern' else 'fact'),'user_notes':'','favorite':False,'review_status':'draft'}
 CARDS.append(c);return c
def char(key,name,summary,goal,limits,decision,change,relations,nums):
 c=card('character',key,name+'｜卷二阶段',{'summary':summary,'goal':goal,'limitations':limits,'decision_pattern':decision,'stage_change':change,'relationship_direction':relations,'claim_kind':'inference','valid_at':'raw0252—0504卷末，不是全书终点'},nums);CHARACTERS[key]=c
def scene(key,title,summary,goal,obstacle,choice,result,state,why,applicability,failure,nums,people,landing=None):
 c=card('scene',key,title,{'summary':summary,'goal':goal,'obstacle':obstacle,'choice':choice,'consequence':result,'state_change':state,'why_it_works':why,'applicability':applicability,'failure_mode':failure,'characters_origin_keys':[origin('character',k) for k in people],'claim_kind':'inference','narrative_order':landing or max(nums)},nums);SCENES[key]=c
def pattern(key,title,summary,steps,conditions,failure,transform,keys,nums):
 c=card('pattern',key,title,{'summary':summary,'causal_steps':steps,'applicability':conditions,'failure_mode':failure,'originality_transform':transform,'derived_from_origin_keys':[origin('scene',k) for k in keys],'claim_kind':'synthesis'},nums);PATTERNS[key]=c
exec((P/'research_characters.py').read_text(encoding='utf-8'))
exec((P/'research_scenes.py').read_text(encoding='utf-8'))
exec((P/'research_supplements.py').read_text(encoding='utf-8'))
exec((P/'research_graph.py').read_text(encoding='utf-8'))
A={'source_id':SID,'revision':REV,'volume':2,'title':'卷二 英雄崛起｜九维研究草稿','read_chapter_ids':IDS,'review_status':'draft','coverage':{'raw_fragments':253,'body_units':252,'complete_volume':True,'complete_book':False,'reading_attribution':'reading-attribution.json'},'method':'raw252—404由本代理实际全文，405—504由primary实际全文；本代理分13批完整读其100条四栏派生，原行合并保reader。章界证据可沿四栏细定位。','dimensions':dimensions,'major_character_states':[{'origin_key':c['origin_key'],'name':c['title'],'summary':c['content']['summary'],'stage_change':c['content']['stage_change'],'relationships':c['content']['relationship_direction'],'evidence':c['evidence']} for c in CHARACTERS.values()],'plot_and_hidden_threads':GRAPH['threads'],'open_questions':QUESTIONS,'unresolved_and_anomalies':ANOMALIES,'chapter_unresolved_index':[{'chapter_id':n['chapter_id'],'reader':n['reader'],'unresolved':n['unresolved'],'evidence':ev([int(n['chapter_id'].split('-')[1])])} for n in NOTES if n['unresolved']],'transferable_patterns':[{'origin_key':c['origin_key'],'summary':c['content']['summary'],'evidence':c['evidence']} for c in PATTERNS.values()],'literary_limits':['第一人称常用身体凝视/性化辱骂制造亲疏，不作为用户审美或原创规范。','数字/面板与口语不齐另存，不以引用范围有效保证解释正确。','以本卷时点为限；后卷薛柔身份与帝国后态均不倒灌，未亲读卷一只用本卷回述。'],'user_evaluation':None}
A['title']='卷二 英雄崛起｜九维研究草稿'
A['named_life_state_audit']=LIFE_STATES
A['chapter_source_anomaly_index']=[{'chapter_id':n['chapter_id'],'reader':n['reader'],'source_anomalies':n['source_anomalies'],'evidence':ev([int(n['chapter_id'].split('-')[1])])} for n in NOTES if n.get('source_anomalies')]
save('analysis.json',A);save('cards.json',CARDS);save('graph.json',GRAPH)
save('research-checkpoint.json',{'status':'core-artifacts-written-draft','counts':{'observations':sum(map(len,dimensions.values())),'cards':dict(collections.Counter(c['asset_type'] for c in CARDS)),'nodes':len(GRAPH['nodes']),'edges':len(GRAPH['edges']),'threads':len(GRAPH['threads'])},'reading_complete':True,'personal_full_volume_read':False,'next_work':'report/handoff/只读预检与主审'})
print(json.dumps(json.loads((P/'research-checkpoint.json').read_text(encoding='utf-8')),ensure_ascii=False))
