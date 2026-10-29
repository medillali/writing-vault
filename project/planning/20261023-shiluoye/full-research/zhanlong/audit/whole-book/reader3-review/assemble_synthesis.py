"""只聚合已稳定、已主审维度组；不改文学字段，不代写primary回执。"""
from synthesis_common import *
from collections import Counter
from copy import deepcopy
A=P.parent
out=B/'book-synthesis-draft.json';md=B/'book-synthesis-draft.md'
assert not out.exists() and not md.exists(),'已交总稿只能精确delta，禁止整生成器覆盖'
groups=[];dims={};group_manifest=[]
pr=json.loads((B/'primary-synthesis-dimension-reviews.json').read_text(encoding='utf-8'));review_by={x['dimension']:x for x in pr['groups']}
assert set(review_by)==set(DIMENSIONS),'待root九组全签后聚合，不能自代主审'
for d in DIMENSIONS:
 p=P/f'synthesis-{d}.json';g=json.loads(p.read_text(encoding='utf-8'));assert len(g['rows'])==4 and sha(p)==review_by[d]['sha256']
 dims[d]=deepcopy(g['rows']);group_manifest.append({'dimension':d,'json':str(p.relative_to(ROOT)).replace('\\','/'),'json_sha256':sha(p),'md_sha256':sha(p.with_suffix('.md')),'primary_reviewed_group_sha256':review_by[d]['sha256'],'assembly_values_equal':True})

# 当前正式依赖重新取指纹；旧开工收据保留，绝不以stage hash填写formal路径。
for n in range(1,7):
 docs=[]
 for kind,suffix in [('analysis','-analysis.json'),('cards','-cards.json'),('graph','-graph.json'),('read-log','-read-log.json'),('chapter-notes','-chapter-notes.jsonl'),('handoff','-handoff.md'),('report','.md')]:
  p=F/f'vol{n:02d}{suffix}';assert p.is_file();docs.append({'kind':kind,'exists':True,'path':str(p.relative_to(ROOT)).replace('\\','/'),'sha256':sha(p),'version_location':'formal','reading_boundary':'analysis全部语义字段已读；handoff完整读；notes/card/graph的文件存在和指纹不声明综合阶段逐项重新读完。'})
 groups.append({'volume':n,'documents':docs})
additional=[F/'vol02-primary-corrections.json',F/'audit/full-reading-validation.json']+sorted((F/'audit').glob('priority-corrections-*.json'))+sorted((F/'audit/primary-rereads').glob('*.json'))
groups.append({'volume':'current-priority-reading','documents':[{'kind':'correction-or-reread','path':str(p.relative_to(ROOT)).replace('\\','/'),'exists':True,'sha256':sha(p),'version_location':'formal','reading_boundary':'纠正与独立复读归其实际审阅人；不转换成综合者新原文覆盖。'} for p in additional]})
poolpaths=[A/'historical-question-pool.json',A/'local-question-pool.json']
groups.append({'volume':'terminal-assessment-reference','documents':[{'kind':'root-merged-terminal-pool','path':str(p.relative_to(ROOT)).replace('\\','/'),'exists':True,'sha256':sha(p),'version_location':'staging-primary-merged','reading_boundary':'仅引用已主审终评；本人亲裁卷1/4局部840，不冒本人读全2694候选。'} for p in poolpaths]})
groups.append({'volume':'collection-source-map','documents':[{'kind':'source-manifest','exists':True,'path':str((B/'source.json').relative_to(ROOT)).replace('\\','/'),'sha256':sha(B/'source.json'),'version_location':'source-metadata'}]})

coverage=json.loads((F/'audit/full-reading-validation.json').read_text(encoding='utf-8'));assert coverage['status']=='passed'
assert coverage['body_units']==1378 and coverage['indexed_segments']==1386
for name,digest in coverage['formal_input_sha256'].items():assert sha(F/name)==digest,name
union=set();attrs=[];rawsum=0
for n in range(1,7):
 lp=F/f'vol{n:02d}-read-log.json';log=json.loads(lp.read_text(encoding='utf-8'))
 np=F/f'vol{n:02d}-chapter-notes.jsonl';notes=[json.loads(x) for x in np.read_text(encoding='utf-8').splitlines() if x.strip()]
 note_by={x['chapter_id']:x for x in notes};seen=set();counts=Counter()
 for x in log['chapters']:
  cid=x['chapter_id'];assert x['full_text_read'] is True and cid not in seen;seen.add(cid);union.add(cid)
  assert cid in note_by;reader=x.get('reader',log.get('reader',note_by[cid].get('reader')));assert reader
  counts[reader]+=1
 rawsum+=len(seen)
 for reader,num in counts.items():attrs.append({'volume':n,'reader':reader,'raw_segments':num,'attribution_basis':str(lp.relative_to(ROOT)).replace('\\','/'),'attribution_sha256':sha(lp),'notes_metadata_basis':str(np.relative_to(ROOT)).replace('\\','/'),'note':'逐行读取者缺省时仅由同章notes.reader补明确元数据；此解析不冒新文学阅读。'})
expected={c['chapter_id'] for c in S['chapters'][1:]};assert union==expected and rawsum==1385
assert sum(v['body_units'] for v in S['volumes'])==1378

material_log=json.loads((P/'synthesis-material-read-log.json').read_text(encoding='utf-8'));assert len(material_log['sections'])==54
for x in material_log['sections']:assert x['all_semantic_fields_read'] and sha(ROOT/x['path'])==x['sha256']
semantic_count=sum(len(json.loads((F/f'vol{n:02d}-analysis.json').read_text(encoding='utf-8'))['dimensions'][d]) for n in range(1,7) for d in DIMENSIONS);assert semantic_count==243
rereads=json.loads((P/'synthesis-approved-selfcheck-combined-delta.json').read_text(encoding='utf-8'))['actual_source_rereads']
assert len(rereads)==6
dump(P/'synthesis-source-reread-log.json',{'actual_reader':'/root/zongheng_vol03_full','method':'本轮原文逐行BEGIN/END实际完整阅读，source_selfcheck输出无截断；与项目首读覆盖重叠，不改原reader/read_at。','chapters':rereads,'new_unique_source_coverage':0})

def walk_refs(x):
 if isinstance(x,dict):
  if all(k in x for k in ['source_id','revision','chapter_id','start_line','end_line']):yield x
  for v in x.values():yield from walk_refs(v)
 elif isinstance(x,list):
  for v in x:yield from walk_refs(v)
def check_ref(e):
 assert e['source_id']==S['source_id'] and e['revision']==S['revision'];c=CH[int(e['chapter_id'][3:])]
 assert c['start_line']<=e['start_line']<=e['end_line']<=c['end_line'],e
 assert e['claim_kind'] in ['fact','inference','synthesis','plan']
ev=list(walk_refs(dims))
for e in ev:check_ref(e)
supports=[]
for d,rows in dims.items():
 assert len(rows)==4
 for r in rows:
  assert r['claim_kind']=='synthesis' and all(r.get(k) for k in ['fact_summary','mechanism','conditions','limits_and_counterevidence','originality_transform','late_stage_result','evidence'])
  for su in r['supporting_observations']:
   p=ROOT/su['material_path'];assert sha(p)==su['material_sha256'];a=json.loads(p.read_text(encoding='utf-8'));o=a['dimensions'][su['dimension']][su['index_zero_based']]
   s,_=support(su['volume'],su['dimension'],su['index_zero_based']+1)
   assert all(su[k]==v for k,v in s.items()),(r['id'],su)
   supports.append((su['volume'],su['dimension'],su['index_zero_based']))
  for pc in r.get('priority_corrections',[]):assert sha(ROOT/pc['path'])==pc['sha256']

priority=[{'path':str(p.relative_to(ROOT)).replace('\\','/'),'sha256':sha(p),'application':'优先采用已批准纠正；原字段字面与原始读者保留，不据旧误读新造情节。'} for p in additional if 'priority-corrections-' in p.name or p.name=='vol02-primary-corrections.json']
scope={'volumes':list(range(1,7)),'project_body_units_with_fulltext_records':1378,'project_frontmatter_segments_with_fulltext_records':1,'project_indexed_segments_with_fulltext_records':1386,'source_indexed_segments':1386,'project_read_record_union_complete':True,'personal_complete_book_read':False,'new_fulltext_reads_by_this_synthesis':6,'new_fulltext_reads_are_rereads':True,'new_unique_fulltext_coverage_by_this_synthesis':0,'volume_raw_segments':1385}
data={'schema_version':1,'artifact_type':'derived-book-synthesis','source_id':S['source_id'],'revision':S['revision'],'author':'失落叶','work_title':'斩龙','title':'全书九维综合｜分工阅读后的派生研究草稿','review_status':'draft','claim_kind':'synthesis','status':'draft-ready-for-primary-review','scope':scope,
'derivation_boundary':'六卷由团队真实分工全文覆盖。综合者首次亲读卷1 raw2—151（150片/148正文）及卷4 raw754—968（215片/214正文）；卷1尾152—251由primary亲读，本人完整派生读100条四栏。其余卷采用最终正式九维与交接及已主审纠正，不冒独自全书原文阅读。本次另完整复读356/821/941/965/1384/1385共6章，新增项目唯一覆盖为0；support中的original_read_scope指首次分工范围而非否认另记复读。综合不替代全历史问题/人物弧审计，研究未获用户审美批准。',
'upstream_reader_attribution':attrs,'frontmatter_attribution_boundary':'raw1覆盖仅依正式full-reading-validation的1386片验收结论；本综合未重写首读署名或另称新读。',
'upstream_documents':groups,'raw_interfaces':[{'before':S['volumes'][i]['units'][-1]['segment_ids'][-1],'after':S['volumes'][i+1]['units'][0]['segment_ids'][0],'check':'按source合章/误片映射连接；raw片段与body单元分别计数。'} for i in range(5)],
'evidence_policy':'36条文学判断为synthesis；支持观察保正式文件、指针、原事实和解释、SHA。顶层evidence定位源事实，事实链仍受原文渠道约束；继承定位不等本人重读所有他卷原文。两处reported_fact_boundary明确限制冻结旧串的使用强度，当前priority-reading解释优先。',
'current_priority_reading':priority,'dimensions':dims,'user_evaluation':None,'user_taste':None,'original_project_settings':None,
'pending_acceptance':['primary核总稿精确等于九个已审稳定组并签最终JSON/MD SHA','由primary运行发布及整书验收；本代理不代执行','用户审阅文学取舍；不自动收藏或写入原创正典'],
'cross_volume_guards':['分工全文覆盖与个人原文阅读分别声明；研究材料读取不冒新的全书原文阅读。','314斩华是流霜佩剑，巴林权力剑另物；狮盾十小时内争夺不等十小时后才可装备，王域自身可分指各友方目标。','乘风845当前十剑、942实十五与潜力二十七相容，不沿用硬上限十层的研究误读。','百里若风/百里伦分玩家与NPC，龙忠/龙硎分人，秦烨不另造秦龙；雷为养子、月亲女，狐狸刘庸不并慕天。','918个人cap、931军团申请与975军团二十万获批分期；上限不等实编。938首次半矿履行、1240—41炼魂面板与实战已成，不沿旧未决。','燕1192自荐、1234代理、1244正式；833问剑系统尾杀与1174李回顾归功流霜分渠道，不让后叙覆盖实战。','NPC死亡/魂体恢复/借体、伤后再现/补员、玩家复活、现实死亡/数字记忆分域；龙硎骨折不推截肢。','城市系统国属、治理、税收、NPC资源与军事指挥分别判断；七大一级主城不等全部次级城。','镇国刀末期仅有令取求援和方回报，未独演实际持刀；款物承诺、交接、资格与实用分步，不以镜头省略一律否认后证。','结尾七晶已毁/裂缝一周后实闭未演；战皇活/镇天关已建/KILLS新职未实战；白墨颜数字上线与雷计划分开；订婚非婚礼。','己方伤亡、平民镇压、杀白旗使与保护弱者誓言并置，不因统一或救援把政治伦理残余洗除。'],
'validation':{'observations':36,'dimensions':9,'inherited_evidence_references_checked':len(ev),'upstream_observation_references':len(supports),'unique_upstream_observations':len(set(supports)),'upstream_semantic_observations_actually_read':243,'all_six_analysis_dimension_texts_read':True,'semantic_sections_read':54,'body_coverage_union':1378,'raw_coverage_union':1386,'volume_raw_segments':1385,'frontmatter_coverage_union':1,'raw_interfaces_checked':5,'selected_formal_analysis_volumes':list(range(1,7)),'selected_staging_analysis_volumes':[],'input_sha256_rechecked':True,'stable_group_values_preserved':True,'actual_synthesis_rereads':6,'unique_coverage_increment':0,'result':'passed-source-locators-derivation-and-stable-group-structure','boundary':'只证明来源、定位、覆盖元数据与装配等值，不由脚本生成文学判断；主审凭据和发布另由primary负责，用户审美未获批准。'},
'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'research_material_read_log':str((P/'synthesis-material-read-log.json').relative_to(ROOT)).replace('\\','/'),'source_reread_log':str((P/'synthesis-source-reread-log.json').relative_to(ROOT)).replace('\\','/'),'stable_dimension_groups':group_manifest}
dump(out,data)
lines=['# 《斩龙》全书九维综合草稿','','成长不断扩大可选动作，也扩大其代价；组织胜利、个人关系与生命损失始终不能互相结账。以下36条把这类阅读效果拆成可迁移机制，并保留原作的失效条件和伦理残余。','','团队1378正文/1386片段真实分工全文覆盖；综合者并非独自全书亲读。六卷243条九维观察语义栏与六份交接已完整派生读，另记6章原文复读，未增加唯一覆盖。研究与原创取舍均为draft，用户尚未批准。','','本稿按九组已主审对象逐值聚合；最终SHA签收、正式发布和独立验收由primary执行。本稿不代全问题账本或人物全弧。','','[机器可核JSON](book-synthesis-draft.json)','','## 阅读与证据边界','',''+data['derivation_boundary'],'','当前解释先读正式纠正层；冻结旧reported_fact字面保留时，以条内明确boundary约束其推论。无需把研究误读变成原文规则缺陷。','']
for d in DIMENSIONS:lines += [f'# {LABELS[d]}','']+render_rows(dims[d])
lines += ['# 当前优先解释层','']+[f'- {p["path"]} · SHA `{p["sha256"]}`' for p in priority]+['','# 验证与待办','','36条、9维各4条；固定SID/rev/章行、上游当前SHA和九组装配等值已本地检查。该检查不替代primary语义审阅或用户审美批准。','','六卷原文阅读归属按正式read-log与同章notes元数据保留；卡图文件的依赖指纹不声明本综合阶段已重新逐项读遍全部卡图。','','待primary核总稿与最终指纹后发布；本代理不写正式库、原六卷、候选池或primary收据。','']
md.write_bytes(('\n'.join(lines)).encode('utf-8'));assert b'\r\r\n' not in md.read_bytes()
manifest={'status':'draft-ready-for-primary-final-review','json_path':str(out.relative_to(ROOT)).replace('\\','/'),'json_sha256':sha(out),'md_path':str(md.relative_to(ROOT)).replace('\\','/'),'md_sha256':sha(md),'observations':36,'groups':group_manifest,'upstream_documents':sum(len(g['documents']) for g in groups),'validation':data['validation'],'limits':'未代写primary签收/发布，未修改正式库/六卷/候选池。'}
dump(P/'synthesis-final-assembly-validation.json',manifest)
stp=P/'reader-state.json';st=json.loads(stp.read_text(encoding='utf-8'));st['synthesis_status']='draft-complete-local-validated-awaiting-primary-final-review';st['synthesis_final_manifest']=str((P/'synthesis-final-assembly-validation.json').relative_to(ROOT)).replace('\\','/');dump(stp,st)
print(json.dumps({k:v for k,v in manifest.items() if k not in ['groups','validation']},ensure_ascii=False));print(json.dumps(data['validation'],ensure_ascii=False))
