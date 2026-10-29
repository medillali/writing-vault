from pathlib import Path
import json, sys, hashlib, copy, re
from research_data import CHARACTERS, SCENES, PATTERNS, LEDGER_L, NOTES_L

R=Path(__file__).resolve().parents[2]
V=R/'.verify/two-books'
OUT=V/'library/reports/two-books-20261023'
WORK=R/'.planning/two-books-20261023'
sys.path.insert(0,str(R/'distill-novels/scripts'))
from library import execute, parser
from fictionlib.vault import KINDS

def dump(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def md(path,text):
    path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text,encoding='utf-8')
def cli(cmd,*args):
    return execute(parser().parse_args(['--vault',str(V),cmd,*map(str,args)]))
def put(cmd,data,*args):
    tmp=WORK/'current-input.json';dump(tmp,data)
    return cli(cmd,'--file',tmp,*args)
M=json.loads((V/'private-sources/normalized/manifest.json').read_text(encoding='utf-8'))
S={k:next(x for x in M['sources'] if title in x['title']) for k,title in [('z','贼胆'),('l','练级专家')]}
BOOK={'z':'贼胆','l':'网游之练级专家'}
def ev(k,ranges,kind='inference'):
    return [dict(source_id=S[k]['source_id'],revision=S[k]['revision'],chapter_id=f'ch-{c:04}',start_line=a,end_line=b,claim_kind=kind) for c,a,b in ranges]
def e_text(e):
    k=next(k for k in S if S[k]['source_id']==e['source_id'])
    c=next(c for c in S[k]['chapters'] if c['chapter_id']==e['chapter_id'])
    return f"《{BOOK[k]}》{c['title']}，{c['chapter_id']}，L{e.get('start_line',c['start_line'])}–{e.get('end_line',c['end_line'])}"

# 保存对既有未提交文件的指纹；本次结束后逐个检查，不覆盖它们。
import subprocess
g=['git','-c',f'safe.directory={R.as_posix()}/writing-vault','-C',str(R/'writing-vault')]
baseline=WORK/'existing-dirty-fingerprints.json'
if not baseline.exists():
    raw=subprocess.check_output(g+['status','--porcelain','-z']).decode('utf-8')
    files=[entry[3:] for entry in raw.split('\0') if entry and not entry.endswith('/')]
    dump(baseline,{f:hashlib.sha256((R/'writing-vault'/f).read_bytes()).hexdigest() for f in files if (R/'writing-vault'/f).is_file()})

old=R.parent/'Chinese Novel/books/zeidan'
oldm=json.loads((old/'manifest.json').read_text(encoding='utf-8'))
rawz=next(Path('E:/chromedownload').glob('*贼胆*.txt'))
assert hashlib.sha256(rawz.read_bytes()).hexdigest()==oldm['source']['sha256']
assert oldm['source']['decoded_utf8_sha256']==S['z']['revision']
mapping=[]
for oldc,newc in zip(oldm['chapters'],S['z']['chapters'][1:],strict=True):
    assert oldc['title']==newc['title']
    assert (oldc['char_start'],oldc['char_end'],oldc['line_start'],oldc['line_end'])==(newc['start_offset'],newc['end_offset'],newc['start_line'],newc['end_line'])
    mapping.append({'old_id':oldc['id'],'old_sequence':oldc['sequence'],'chapter_id':newc['chapter_id'],'title':newc['title']})
dump(OUT/'zeidan/legacy-chapter-map.json',mapping)
records=[];keymap={}; imported=[];candidates=[]
def save(k,key,typ,title,content,evidence,tags,derived=None,legacy=False):
    aid=f'{KINDS[typ][1]}-twobooks-{k}-{key}'
    data={'asset_id':aid,'asset_type':typ,'scope':'reusable-pattern' if typ=='pattern' else 'source-analysis',
          'origin_key':f"{S[k]['source_id'] if k in S else 'two-books'}/{typ}/{key}",
          'title':title,'tags':tags,'content':content,'evidence':evidence,'derived_from':derived or [],
          'user_notes':'','favorite':False,'review_status':'draft'}
    p=V/'library'/KINDS[typ][0]/f'{aid}.json'
    args=['--generated']
    if p.exists(): args += ['--base-revision',str(json.loads(p.read_text(encoding='utf-8'))['revision'])]
    a=put('asset-put',data,*args)
    records.append(a);keymap[f'{k}/{key}']=a
    if legacy: imported.append(a['asset_id'])
    return a

for name,typ in [('entities','character'),('scenes','scene')]:
    data=json.loads((old/f'distillation/{name}.json').read_text(encoding='utf-8'))
    for x in data:
        ranges=[(e['sequence']+1,e['line_start'],e['line_end']) for e in x['evidence']]
        evidence=ev('z',ranges,'inference')
        for e in evidence:
            c=S['z']['chapters'][int(e['chapter_id'][3:])-1]
            assert c['start_line']<=e['start_line']<=e['end_line']<=c['end_line']
        if x.get('maintenance_depth','').startswith('待补'):
            candidates.append({**x,'mapped_evidence':evidence});continue
        content={'summary':'；'.join(x['facts'][:2]),'legacy_record':x,
                 'provenance_status':'旧研究迁移：原文件、规范化哈希与章节/证据位置已核验；未宣称本次重读全部语义。',
                 'review_boundary':'legacy_record 内 facts/inferences 保留旧研究分类；需用户审阅。阶段记录不自动合并为同一身份。'}
        a=save('z','legacy-'+x['record_id'].lower(),typ,f"《贼胆》{x.get('name',x.get('title'))}〔旧研究 {x['record_id']} / {x['worker_part']}〕",content,evidence,['贼胆','旧研究迁移',x['worker_part']],legacy=True)
    print('MIGRATED',name,len(records),flush=True)
dump(OUT/'zeidan/appearance-candidates.json',candidates)
threads=json.loads((old/'distillation/threads.json').read_text(encoding='utf-8'))
for x in threads:
    x['mapped_evidence']=ev('z',[(e['sequence']+1,e['line_start'],e['line_end']) for e in x['evidence']])
dump(OUT/'zeidan/legacy-threads.json',threads)
notes=[json.loads(line) for line in (old/'distillation/chapter-notes.jsonl').read_text(encoding='utf-8').splitlines() if line.strip()]
assert len(notes)==463 and sorted(x['sequence'] for x in notes)==list(range(1,464))
for x in notes:
    x['current_chapter_id']=f"ch-{x['sequence']+1:04}"
    x['reading_provenance']='旧研究记录迁移；不是本次新增全文阅读'
dump(OUT/'zeidan/legacy-chapter-notes.json',notes)

for k,key,title,ranges,summary,goal,need,conflict,arc in CHARACTERS:
    save(k,key,'character',f'《{BOOK[k]}》{title}',{'summary':summary,'goal':goal,'need':need,'conflict':conflict,'arc':arc,
        'analysis_kind':'文本事实概述与研究推断分栏；need/conflict 为可修订解释。','read_batch':'2026-10-23 实际正文阅读'},ev(k,ranges),[BOOK[k],'首轮细读','人物','阶段性'])
for k,key,title,ranges,goal,obstacle,choice,consequence,state,why,applies,fails in SCENES:
    save(k,key,'scene',f'《{BOOK[k]}》{title}',{'summary':consequence,'goal':goal,'obstacle':obstacle,'choice':choice,'consequence':consequence,'state_change':state,'why_it_works':why,'applicability':applies,'failure_mode':fails,
         'analysis_kind':'goal 至 consequence 为本批事件概述；state_change/why_it_works/applicability/failure_mode 为研究解释。'},ev(k,ranges),[BOOK[k],'首轮细读','因果链','可迁移候选'])
for key,title,refs,summary,applies,fails,exercise in PATTERNS:
    derived=[{'asset_id':keymap[x]['asset_id'],'revision':keymap[x]['revision']} for x in refs]
    evidence=[]
    for ref in refs:
        for e in keymap[ref]['evidence']:
            if e not in evidence: evidence.append({**e,'claim_kind':'synthesis'})
    save('shared',key,'pattern',title,{'summary':summary,'applicability':applies,'failure_mode':fails,'exercise':exercise,
         'status':'跨书综合假设；未成为用户偏好，也未进入原创项目正典。'},evidence,['双书比较','机制','待试用'],derived)

for k,last,dims in [('z',11,['worldbuilding','characters','plot','style','narrative','dialogue','pacing','themes','continuity']),('l',14,['worldbuilding','characters','plot','style','narrative','dialogue','pacing','themes','continuity'])]:
    completed=[c['chapter_id'] for c in S[k]['chapters'][1:last]]
    put('checkpoint',{'run_id':f'run-two-books-20261023-{k}','source_id':S[k]['source_id'],'source_revision':S[k]['revision'],
       'completed_chapters':completed,'pending_chapters':[c['chapter_id'] for c in S[k]['chapters'][last:]],
       'excluded_chapters':['ch-0001'],'exclusion_reason':'章前书名/简介；未记作正文蒸馏。','dimensions':dims,
       'notes':('本批贼胆实读1–10章，旧全书研究另有迁移检查点。' if k=='z' else '本批实读序章和1–12章；下一批从第13章继续，先核对组队分配、治疗变化与头骨任务。')})
put('checkpoint',{'run_id':'run-zeidan-legacy-migration-20261023','source_id':S['z']['source_id'],'source_revision':S['z']['revision'],
    'completed_chapters':[c['chapter_id'] for c in S['z']['chapters'][1:]],'pending_chapters':[],
    'excluded_chapters':['ch-0001'],'dimensions':['characters','plot','narrative'],
    'reading_origin':'2026-10-19 至 21 旧研究；本次只核验哈希、章映射、记录与证据行界。',
    'notes':'463章旧研究保留；未声称已逐卡重审、全书九维完成或用户认可。'})

# 小范围关系图仅包含本轮实读场景；不把相邻章节自动当因果。
for k,keys in [('z',['care','practice','backstab','contract']),('l',['clock','gated_reward','ring','mana','counterstealth','team'])]:
    nodes=[{'id':'story','title':BOOK[k]+'：本批开篇结构','kind':'story','parent_id':None,'claim_kind':'inference'}]
    for order,key in enumerate(keys,1):
        a=keymap[f'{k}/{key}']
        nodes.append({'id':key,'title':a['title'],'kind':'scene','parent_id':'story','narrative_order':order,'claim_kind':'inference','summary':a['content']['summary'],'evidence':a['evidence']})
    if k=='z':
        pairs=[('practice','backstab','cause','基础动作训练支持后续技巧'),('backstab','contract','cause','熟练度满引出升级费用与委托')]
        ts=[{'id':'livelihood','title':'正当收入与试玩期限','kind':'main','status':'open','node_ids':['care','practice','backstab','contract'],'edge_ids':['e1','e2']},
            {'id':'aode','title':'奥德失物与委托动机','kind':'hidden','status':'open','node_ids':['contract'],'edge_ids':[]}]
    else:
        pairs=[('clock','gated_reward','cause','获得图纸后才出现材料门槛'),('ring','mana','cause','获得职业技能后试验战斗能力'),('mana','counterstealth','echo','已示范的控制技能用于反潜')]
        ts=[{'id':'growth','title':'生产积累转为战斗与协作','kind':'main','status':'partial','node_ids':keys,'edge_ids':['e1','e2','e3']},
            {'id':'treasure','title':'尚未兑现的图纸与宝藏','kind':'subplot','status':'open','node_ids':['clock','gated_reward'],'edge_ids':['e1']},
            {'id':'revenge','title':'败者的再战意向','kind':'hidden','status':'open','node_ids':['counterstealth'],'edge_ids':[]}]
        nodes[-2]['knowledge']=[{'observer':'reader','state':'knows','belief':'败者记住萧翎并想再战。'}, {'observer':keymap['l/xiaoling']['asset_id'],'state':'unknown','belief':'未获知败后对话与人脉。'}]
    edges=[{'id':f'e{i}','from':a,'to':b,'kind':kind,'label':label,'claim_kind':'inference','evidence':keymap[f'{k}/{a}']['evidence']+keymap[f'{k}/{b}']['evidence']} for i,(a,b,kind,label) in enumerate(pairs,1)]
    graph={'title':BOOK[k]+' · 本次阅读范围内的因果与未解线','coverage':[{'source_id':S[k]['source_id'],'revision':S[k]['revision'],'chapter_ids':[c['chapter_id'] for c in S[k]['chapters'][1:11 if k=='z' else 14]],'complete':False}], 'nodes':nodes,'edges':edges,'threads':ts}
    p=V/f"library/sources/{S[k]['source_id']}/plot-graph.json"
    args=['--owner-kind','source','--owner-id',S[k]['source_id']]
    if p.exists(): args+=['--base-revision',str(json.loads(p.read_text(encoding='utf-8'))['revision'])]
    put('graph-save',graph,*args)
    cli('graph-render','--owner-kind','source','--owner-id',S[k]['source_id'],'--output',OUT/('zeidan' if k=='z' else 'leveling')/'plot')
    print('GRAPH',k,flush=True)

dump(OUT/'batch-assets.json',[{'asset_id':a['asset_id'],'revision':a['revision'],'title':a['title'],'type':a['asset_type'],'imported_legacy':a['asset_id'] in imported} for a in records])
metadata={}
for k,s in S.items():
    raw=next(Path('E:/chromedownload').glob(f'*{BOOK[k]}*.txt'))
    metadata[k]={'title':BOOK[k],'author':'发飙的蜗牛','source_id':s['source_id'],'revision':s['revision'],'raw_sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),'encoding':'gb18030','indexed_segments':len(s['chapters']),'new_read_segments':10 if k=='z' else 13,'new_read_characters':sum(c['end_offset']-c['start_offset'] for c in s['chapters'][1:11 if k=='z' else 14]),'full_new_read':False}
dump(OUT/'coverage.json',{'date':'2026-10-23','sources':metadata,'legacy_zeidan':{'chapters':463,'characters':183,'scenes':109,'candidate_names':60,'thread_records':69,'hash_and_chapter_mapping_verified':True,'semantic_reread_complete':False},'new_cards':len(records)-len(imported),'legacy_cards':len(imported),'all_user_review_pending':True})
dump(OUT/'leveling/question-ledger.json',[{'title':t,'summary':s,'status':st,'evidence':ev('l',ee)} for t,s,st,ee in LEDGER_L])
dump(OUT/'leveling/chapter-notes.json',[{'chapter_id':f'ch-{i+2:04}','title':t,'summary':s,'reading_status':'full_text_read_this_batch','user_evaluation':None} for i,(t,s) in enumerate(NOTES_L)])
print('SAVED',len(imported),'legacy +',len(records)-len(imported),'new cards',flush=True)

# Markdown 为可重建阅读副本；事实与解释在卡片内容中保留自己的字段。
LABELS={'summary':'概述','goal':'目标','need':'内在需求（研究推断）','conflict':'矛盾与边界','arc':'本批阶段变化','obstacle':'障碍','choice':'选择','consequence':'后果','state_change':'状态变化','why_it_works':'机制解释','applicability':'适用条件','failure_mode':'失效风险','exercise':'创作检验问题','facts':'旧研究事实概述','inferences':'旧研究推断','user_feedback':'用户反馈','name':'名称','title':'标题','provenance_status':'研究来源','review_boundary':'审阅边界','analysis_kind':'事实与解释边界','status':'状态','evidence':'旧证据','legacy_record':'旧研究原记录','record_id':'旧记录编号','worker_part':'原工作段','relations':'关系','relationships':'关系','desires':'欲望','constraints':'约束','limits':'局限','source_anomalies':'源文异常','maintenance_depth':'研究深度','causal_importance':'因果作用','prehistory':'前情','result':'结果','interesting_unresolved':'保留问题','aliases':'别名候选'}
def prose(value):
    if isinstance(value,list):return '\n'.join('- '+prose(v).replace('\n','；') for v in value) or '无已记录条目。'
    if isinstance(value,dict):return '\n'.join(f"**{LABELS.get(k,k)}**：{prose(v)}" for k,v in value.items())
    return '未填写' if value is None else str(value)
for a in records:
    body=f"# {a['title']}\n\n返回[双书入口](../README.md)。\n\n主档 `{a['asset_id']}` · v{a['revision']} · {a['scope']}\n\n"
    for key,val in a['content'].items():body+=f"## {LABELS.get(key,key)}\n\n{prose(val)}\n\n"
    body+='## 当前证据\n\n'+'\n'.join('- '+e_text(e) for e in a['evidence'])+'\n\n'
    body+='## 你的评价\n\n尚未收藏或认可。可记录：值得保留的细节、不同意的解释、想尝试的变化、实际使用后的反馈。\n'
    md(OUT/'cards'/f"{a['asset_id']}.md",body)
for k,folder in [('z','zeidan'),('l','leveling')]:
    lines=[f'# 《{BOOK[k]}》完整章节索引','','完整索引不等于本批全文阅读。行号对应指定修订的本机规范化TXT；Git不含原文。',f"\n来源：`{S[k]['source_id']}`\n\n修订：`{S[k]['revision']}`\n"]
    for c in S[k]['chapters']:
        lines += [f"<a id=\"{c['chapter_id']}\"></a>\n\n### {c['chapter_id']} · {c['title']}\n\nL{c['start_line']}–{c['end_line']} · 字符区间 [{c['start_offset']}, {c['end_offset']})\n"]
    md(OUT/folder/'chapter-index.md','\n'.join(lines))
    for typ,file,title in [('character','characters','人物卡'),('scene','scenes','场景卡')]:
        matched=[a for a in records if a['asset_type']==typ and any(e['source_id']==S[k]['source_id'] for e in a['evidence'])]
        md(OUT/folder/f'{file}.md',f'# 《{BOOK[k]}》{title}\n\n旧研究分段档案与本批卡片分别保留，不能当作独立人物总数。\n\n'+'\n'.join(f"- [{a['title']}](../cards/{a['asset_id']}.md) · v{a['revision']}" for a in matched)+'\n')
md(OUT/'patterns.md','# 可用于原创的机制候选\n\n以下都是研究假设，尚未自动成为你的风格规则。点开查看适用条件、失效风险和固定版本来源。\n\n'+'\n'.join(f"- [{a['title']}](cards/{a['asset_id']}.md)" for a in records if a['asset_type']=='pattern')+'\n')
md(OUT/'leveling/chapter-notes.md','# 本批逐章记录\n\n'+'\n\n'.join(f"## {t}\n\n{s}\n\n定位：ch-{i+2:04}；见[章节索引](chapter-index.md#ch-{i+2:04})。" for i,(t,s) in enumerate(NOTES_L))+'\n')
md(OUT/'leveling/question-ledger.md','# 第12章结束时的未解线与一致性问题\n\n'+'\n\n'.join(f"## {t} · {st}\n\n{s}\n\n"+'；'.join(e_text(e) for e in ev('l',ee)) for t,s,st,ee in LEDGER_L)+'\n')
md(OUT/'zeidan/legacy-chapter-notes.md','# 旧研究的463章逐章记录\n\n来源哈希与本次文件一致；保留旧阅读范围，不算本次新读。阶段疑问必须结合后文，不能当全书最终未解项。\n\n'+'\n\n'.join(f"## {x['sequence']:03} · {x['title']}\n\n"+prose(x['facts'])+f"\n\n定位：[章节索引](chapter-index.md#{x['current_chapter_id']})，L{x['source_line_start']}–{x['source_line_end']}。\n\n阶段问题："+prose(x.get('open_questions',[])) for x in notes)+'\n')
md(OUT/'zeidan/legacy-threads.md','# 旧研究的69份剧情线记录\n\n这是分段记录数，不是69条独立主线。状态保留其发生阶段；不得把早期未回收直接当最终未回收。\n\n'+'\n\n'.join(f"## {x['record_id']} · {x['name']}\n\n原工作段：{x['worker_part']}\n\n"+prose({k:v for k,v in x.items() if k not in ['mapped_evidence','evidence','record_id','name','worker_part']})+'\n\n证据：'+'；'.join(e_text(e) for e in x['mapped_evidence']) for x in threads)+'\n')
md(OUT/'zeidan/appearance-candidates.md','# 60条仅定位称呼\n\n未升级为完整人物卡；同名、泛称、异写需要进一步辨认。\n\n'+'\n\n'.join(f"## {x['record_id']} · {x['name']}\n\n"+prose(x['facts'])+'\n\n'+'；'.join(e_text(e) for e in x['mapped_evidence']) for x in candidates)+'\n')
dump(WORK/'build-result.json',{'new_cards':len(records)-len(imported),'legacy_cards':len(imported),'source_ids':{k:s['source_id'] for k,s in S.items()},'output':str(OUT)})
print('READING_FILES_READY',flush=True)
