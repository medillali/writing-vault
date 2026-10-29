"""只序列化本代理全文阅读后手写的卷五研究；不生成阅读事实、不修改其他卷。"""
import pathlib,json,collections,hashlib,sys
sys.stdout.reconfigure(encoding='utf-8')
P=pathlib.Path(__file__).resolve().parent
if (P/'freeze-manifest.json').exists():raise SystemExit('本卷核心已冻结；后续只用获主审批准的精准proposal差分，不再重建。')
S=json.loads((P.parent/'source.json').read_text(encoding='utf-8')); SID,REV=S['source_id'],S['revision']
SPEC=next(v for v in S['volumes'] if v['volume']==5)
CH={int(c['chapter_id'].split('-')[1]):c for c in S['chapters']}
IDS=[s['chapter_id'] for u in SPEC['units'] for s in u['segments']]
NOTES=[json.loads(x) for x in (P/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines() if x]
assert [n['chapter_id'] for n in NOTES]==IDS and len(IDS)==211
assert all(n['reader']=='/root/zongheng_vol04_full' and n['full_text_read'] for n in NOTES)
def save(n,x):(P/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def ev(nums,kind='fact'):
 return [dict(source_id=SID,revision=REV,chapter_id=CH[n]['chapter_id'],start_line=CH[n]['start_line'],end_line=CH[n]['end_line'],claim_kind=kind) for n in dict.fromkeys(nums)]
def origin(t,k):return f'{SID}/full-20261025/vol05/{t}/{k}'
dimensions={d:[] for d in ['worldbuilding','characters','plot','style','narrative','dialogue','pacing','themes','continuity']}
def obs(d,title,fact,inference,mechanism,limits,nums):
 dimensions[d].append(dict(id=f'v05-{d}-{len(dimensions[d])+1:02}',title=title,claim_kind='inference',textual_fact=fact,observation=inference,mechanism=mechanism,limits_and_counterevidence=limits,evidence=ev(nums),interpretation_evidence=ev(nums,'inference'),review_status='draft'))
exec((P/'research_dimensions.py').read_text(encoding='utf-8'))
CARDS=[];CHARACTERS={};SCENES={};PATTERNS={}
def card(t,k,title,content,nums):
 c=dict(asset_type=t,scope='reusable-pattern' if t=='pattern' else 'source-analysis',title=title,origin_key=origin(t,k),tags=['作者:失落叶','作品:斩龙','卷5','待审阅'],content=content,evidence=ev(nums,'synthesis' if t=='pattern' else 'fact'),user_notes='',favorite=False,review_status='draft');CARDS.append(c);return c
def char(k,name,summary,goal,limits,decision,change,relations,nums):
 c=card('character',k,name+'｜卷五阶段',dict(summary=summary,goal=goal,limitations=limits,decision_pattern=decision,stage_change=change,relationship_direction=relations,claim_kind='inference',valid_at='raw0969—1179卷末，不是全书终点'),nums);CHARACTERS[k]=c
def scene(k,title,summary,goal,obstacle,choice,result,state,why,applicability,failure,nums,people,landing=None):
 c=card('scene',k,title,dict(summary=summary,goal=goal,obstacle=obstacle,choice=choice,consequence=result,state_change=state,why_it_works=why,applicability=applicability,failure_mode=failure,characters_origin_keys=[origin('character',x) for x in people],claim_kind='inference',narrative_order=landing or max(nums)),nums);SCENES[k]=c
def pattern(k,title,summary,steps,conditions,failure,transform,keys,nums):
 c=card('pattern',k,title,dict(summary=summary,causal_steps=steps,applicability=conditions,failure_mode=failure,originality_transform=transform,derived_from_origin_keys=[origin('scene',x) for x in keys],claim_kind='synthesis'),nums);PATTERNS[k]=c
exec((P/'research_characters.py').read_text(encoding='utf-8'))
exec((P/'research_scenes.py').read_text(encoding='utf-8'))
exec((P/'research_patterns.py').read_text(encoding='utf-8'))
exec((P/'research_graph.py').read_text(encoding='utf-8'))
exec((P/'research_supplements.py').read_text(encoding='utf-8'))
exec((P/'research_refinement.py').read_text(encoding='utf-8'))
A=dict(source_id=SID,revision=REV,volume=5,title='卷五｜军权、龙域与两种成长的代价',read_chapter_ids=IDS,review_status='draft',coverage=dict(raw_fragments=211,body_units=210,complete_volume=True,complete_book=False,reading_attribution='本卷全部原文实读：/root/zongheng_vol04_full'),method='每1—2片read_chapters.py完整BEGIN-END；每2—4片四栏手写落盘。未亲读卷一三四，前史仅本卷回述/正式接口层，不以他卷终点倒灌。',dimensions=dimensions,major_character_states=[dict(origin_key=c['origin_key'],name=c['title'],summary=c['content']['summary'],stage_change=c['content']['stage_change'],relationships=c['content']['relationship_direction'],evidence=c['evidence']) for c in CHARACTERS.values()],plot_and_hidden_threads=GRAPH['threads'],open_questions=QUESTIONS,unresolved_and_anomalies=ANOMALIES,chapter_unresolved_index=[dict(chapter_id=n['chapter_id'],reader=n['reader'],unresolved=n['unresolved'],evidence=ev([int(n['chapter_id'].split('-')[1])])) for n in NOTES if n['unresolved']],chapter_source_anomaly_index=[dict(chapter_id=n['chapter_id'],reader=n['reader'],source_anomalies=n['source_anomalies'],evidence=ev([int(n['chapter_id'].split('-')[1])])) for n in NOTES if n.get('source_anomalies')],named_life_state_audit=LIFE_STATES,transferable_patterns=[dict(origin_key=c['origin_key'],summary=c['content']['summary'],evidence=c['evidence']) for c in PATTERNS.values()],literary_limits=['本卷阶段研究；未把本代理卷二前缀亲读或尾派生读扩称个人全书全文。','量化面板与精数可能源异文；证据范围有效不保证解释正确，源差和角色猜测不强行合解。','身体凝视、民族化辱骂与性化玩笑保为叙述风格和价值局限，不自动转为用户审美或原创规范。','权力有效不等行为正当；死亡、强迁、俘捕与趁神智未复订契保代价及主体同意边界。'],user_evaluation=None)
A['title']='卷五 群雄并起｜军权、龙域与两种成长的代价'
# 原notes没有独立source_anomalies字段时，仍将本次手工源疑索引按章显式列出；原unresolved逐串保留。
anomaly_by_ch={}
for a in ANOMALIES:
 for e in a['evidence']:
  anomaly_by_ch.setdefault(e['chapter_id'],[]).append(dict(anomaly_id=a['id'],description=a['description'],handling=a['handling'],status=a['status'],audit_domain=a['audit_domain']))
A['chapter_source_anomaly_index']=[dict(chapter_id=cid,reader='/root/zongheng_vol04_full',source_anomalies=items,evidence=ev([int(cid.split('-')[1])])) for cid,items in sorted(anomaly_by_ch.items())]
save('analysis.json',A);save('cards.json',CARDS);save('graph.json',GRAPH)
save('research-checkpoint.json',dict(status='core-written-draft',reading_complete=True,counts=dict(observations=sum(map(len,dimensions.values())),cards=dict(collections.Counter(c['asset_type'] for c in CARDS)),nodes=len(GRAPH['nodes']),edges=len(GRAPH['edges']),threads=len(GRAPH['threads'])),next_work='report/handoff/verification/primary文学审阅'))
print(json.dumps(dict(volume_spec=SPEC.get('title'),checkpoint=json.loads((P/'research-checkpoint.json').read_text(encoding='utf-8'))),ensure_ascii=False))
