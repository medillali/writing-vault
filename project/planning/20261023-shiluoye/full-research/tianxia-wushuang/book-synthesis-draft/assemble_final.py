"""只组装已实际阅过的八卷研究材料，输出书根兼容草稿；不写正式库。"""
import json,hashlib,copy,sys,collections
from pathlib import Path
from datetime import datetime,timezone
sys.stdout.reconfigure(encoding='utf-8')
P=Path(__file__).parent;B=P.parent;ROOT=P.parents[4];FORMAL=ROOT/'writing-vault/library/reports/tianxia-wushuang'
def R(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def W(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def plain(x):return x.get('text',x) if isinstance(x,dict) else x
def relative(p):return p.relative_to(ROOT).as_posix()
def doc(p,kind,status):return dict(kind=kind,path=relative(p),exists=p.is_file(),sha256=sha(p) if p.is_file() else None,version_location=status)
S=R(B/'source.json');seed=R(P/'final-seed.json');receipt=R(P/'late-material-read-log.json');now=datetime.now(timezone.utc).isoformat()
assert receipt['complete_volumes']==[6,7,8] and receipt['full_original_book_read_by_synthesizer'] is False
stages={};inputs=[];readers=[];raw_union=[];raw_interfaces=[];checks=[]
for spec in S['volumes']:
 v=spec['volume'];D=B/f'vol{v:02d}'
 for name in ['analysis.json','cards.json','graph.json','read-log.json','chapter-notes.jsonl','reader-state.json','report.md','handoff.md','validation.json']:assert (D/name).is_file(),(v,name)
 analysis_stage=R(D/'analysis.json');state=R(D/'reader-state.json');log=R(D/'read-log.json')
 assert state['complete_volume'] and not state.get('next_chapter_id')
 assert analysis_stage['source_id']==S['source_id'] and analysis_stage['revision']==S['revision']
 if v<=5:
  old=next(x for x in R(P/'basis-snapshot.json')['materials'] if x['volume']==v)
  assert sha(D/'analysis.json')==old['sha256'],('early_material_changed_reread_required',v)
 else:
  old=next(x for x in receipt['volumes'] if x['volume']==v)
  for item in old['documents']:assert sha(ROOT/item['path'])==item['sha256'],('late_material_changed_reread_required',v,item['path'])
 formal=FORMAL/f'vol{v:02d}-analysis.json';ap=formal if formal.is_file() else D/'analysis.json';a=R(ap)
 assert a['dimensions']==analysis_stage['dimensions'],('formal_stage_semantics_differ',v)
 stages[v]=dict(data=a,path=ap,sha256=sha(ap),state=state,log=log)
 ds=[doc(ap,'analysis','formal' if formal.is_file() else 'staging-reviewed-frozen')]
 for name,formalname,kind in [('read-log.json',f'vol{v:02d}-read-log.json','read-log'),('report.md',f'vol{v:02d}.md','report'),('handoff.md',f'vol{v:02d}-handoff.md','handoff')]:
  fp=FORMAL/formalname;dp=fp if fp.is_file() else D/name;ds.append(doc(dp,kind,'formal' if fp.is_file() else 'staging-reviewed-frozen'))
 # 卡图用于机制/归属边界复核，不把其条数当原文阅读证明。
 ds += [doc(D/'cards.json','cards','staging-reviewed-frozen'),doc(D/'graph.json','graph','staging-reviewed-frozen')]
 expected=[c['chapter_id'] for u in spec['units'] for c in u['segments']]
 assert [c['chapter_id'] for c in log['chapters']]==expected and all(c['full_text_read'] for c in log['chapters'])
 raw_union += expected
 group=collections.Counter(c.get('reader',log.get('reader',state.get('reader','unknown'))) for c in log['chapters'])
 for reader,count in group.items():readers.append(dict(volume=v,reader=reader,raw_segments=count,attribution_basis=relative(D/'read-log.json')))
 inputs.append(dict(volume=v,documents=ds,body_units=spec['body_units'],read_record_count=len(expected),read_first=expected[0],read_last=expected[-1],analysis_basis='formal' if formal.is_file() else 'staging-reviewed-frozen'))
 checks.append(dict(volume=v,stage_analysis_sha256=sha(D/'analysis.json'),selected_analysis_sha256=sha(ap),dimensions_identical=True,reader_state_complete_volume=True))
 if v>1:raw_interfaces.append(dict(before=f'ch-{int(expected[0][3:])-1:04d}',after=expected[0],check='按source spec连续分卷；研究读取不虚增正文覆盖'))
supp=R(B/'supplementary-read-log.json');assert len(supp['chapters'])==1 and supp['chapters'][0]['chapter_id']=='ch-0001' and supp['chapters'][0]['full_text_read']
readers.append(dict(volume='frontmatter',reader='primary',raw_segments=1,attribution_basis=relative(B/'supplementary-read-log.json')))
raw_union += ['ch-0001'];assert len(raw_union)==len(set(raw_union))==1609
assert set(raw_union)=={c['chapter_id'] for c in S['chapters']}
assert sum(v['body_units'] for v in S['volumes'])==1599
inputs.append(dict(volume='frontmatter',documents=[doc(B/'supplementary-read-log.json','read-log','staging-primary-fulltext-record')],read_record_count=1,scope='简介/附表/独立番外与主线canon分层；综合者未亲读该正文，不将其241级快照当终态。'))
inputs.append(dict(volume='source-metadata',documents=[doc(B/'source.json','source-spec','frozen-per-book-metadata')],scope='来源身份、修订、八卷spec与合章片段映射；不以元数据替代实际全文记录。'))
DIM_NAMES=dict(worldbuilding='世界观与规则',characters='人物与关系',plot='情节组织',style='语言与文风',narrative='叙事与知识差',dialogue='对话',pacing='节奏',themes='主题与价值张力',continuity='连续性与阶段边界')
dimensions={};refs=0;observations=set();support_count=0
for d,rows in seed.items():
 assert d in DIM_NAMES and len(rows)==4
 out=[]
 for i,row in enumerate(rows):
  supporting=[];evidence={}
  assert len({x[0] for x in row['sources']})>=3 and any(x[0]>=6 for x in row['sources'])
  for v,dim,index in row['sources']:
   info=stages[v];o=info['data']['dimensions'][dim][index];observations.add((v,dim,index));support_count+=1
   pointer=f'/dimensions/{dim}/{index}'
   supporting.append(dict(volume=v,dimension=dim,index_zero_based=index,observation_id=o.get('id',o.get('key')),title=o.get('title'),reported_observation=plain(o['fact']),reported_interpretation=plain(o.get('inference','')),upstream_claim_kind=o.get('claim_kind','synthesis'),material_path=relative(info['path']),material_sha256=info['sha256'],json_pointer=pointer,source_reader=info['state'].get('reader'),synthesizer_original_read_scope='卷三全部原片' if v==3 else '仅卷八raw1573—1609原文，其余依primary逐章笔记' if v==8 else '该卷研究材料，非综合者亲读原文'))
   for oe in o['evidence']:
    e=copy.deepcopy(oe);k=(e['source_id'],e['revision'],e['chapter_id'],e['start_line'],e['end_line'],e['claim_kind'])
    if k not in evidence:e['research_material_attribution']=[];evidence[k]=e
    evidence[k]['research_material_attribution'].append(dict(volume=v,dimension=dim,index_zero_based=index,material_path=relative(info['path']),source_reader=info['state'].get('reader'),original_reread_by_this_synthesis=False))
  out.append(dict(id=f'wushuang-book-{d}-{i+1:02d}',key=row['key'],title=row['title'],claim_kind='synthesis',claim=row['claim'],fact_summary=row['fact'],supporting_observations=supporting,mechanism=row['mechanism'],limits_and_counterevidence=row['limits'],originality_transform=row['transform'],literary_choice=dict(take=row['take'],leave=row['leave'],claim_kind='inference',user_approval=False),late_stage_result=row['late_stage_result'],evidence=list(evidence.values()),review_status='draft'))
  refs+=len(evidence)
 dimensions[d]=out
assert len(dimensions)==9 and sum(map(len,dimensions.values()))==36
sourcech={c['chapter_id']:c for c in S['chapters']}
for rows in dimensions.values():
 for row in rows:
  for e in row['evidence']:
   c=sourcech[e['chapter_id']];assert e['source_id']==S['source_id'] and e['revision']==S['revision'] and c['start_line']<=e['start_line']<=e['end_line']<=c['end_line']
V=dict(observations=36,dimensions=9,inherited_evidence_references_checked=refs,upstream_observation_references=support_count,unique_upstream_observations=len(observations),body_coverage_union=1599,raw_coverage_union=1609,volume_raw_segments=1608,frontmatter_coverage_union=1,raw_interfaces_checked=7,all_eight_stage_inputs_read=True,selected_formal_analysis_volumes=[x['volume'] for x in inputs if isinstance(x['volume'],int) and x['analysis_basis']=='formal'],selected_staging_analysis_volumes=[x['volume'] for x in inputs if isinstance(x['volume'],int) and x['analysis_basis']!='formal'],input_sha256_rechecked=True,result='passed-source-locators-and-derivation-structure',boundary='只证明继承定位/覆盖/输入版本可解析；文学解释待primary逐条核，用户审美/原创canon未获批准。')
data=dict(schema_version=1,artifact_type='derived-book-synthesis',source_id=S['source_id'],revision=S['revision'],author='失落叶',work_title='网游之天下无双',title='全书九维综合｜分工阅读后的派生研究草稿',review_status='draft',claim_kind='synthesis',status='draft-ready-for-primary-review',scope=dict(volumes=list(range(1,9)),project_body_units_with_fulltext_records=1599,project_frontmatter_segments_with_fulltext_records=1,project_indexed_segments_with_fulltext_records=1609,source_indexed_segments=1609,project_read_record_union_complete=True,new_fulltext_reads_by_this_synthesis=0,personal_complete_book_read=False),derivation_boundary='综合者亲读卷三raw0229—0606共378片/376正文，以及卷八raw1573—1609共37片/37正文；完整读卷八primary68条逐章笔记。其他卷全文由其各自真实读者完成，本文件基于八卷已完成研究材料派生，不冒称独自全书亲读，不替代人物全弧/问题终点审计，不读取斩龙。',upstream_reader_attribution=readers,upstream_documents=inputs,raw_interfaces=raw_interfaces,upstream_revision_checks=checks,evidence_policy='源证据定位与其原claim_kind继承；每条研究综合本身claim_kind=synthesis，supporting_observations保原卷/字段/原读者/文件SHA。继承引用不等综合者逐段重读他卷正文。',dimensions=dimensions,user_evaluation=None,user_taste=None,original_project_settings=None,pending_acceptance=['primary逐条语义审阅并钉最终JSON/MD SHA','正式全书覆盖验收通过后由primary发布','用户审阅文学取舍；不自动收藏或成为原创设定'],cross_volume_guards=seed.get('_guards',[]) if isinstance(seed,dict) else [],validation=V,created_at=now)
data['validation']['all_eight_analysis_dimension_texts_read']=data['validation'].pop('all_eight_stage_inputs_read')
data['research_material_read_log']=relative(P/'late-material-read-log.json')
data['cross_volume_guards']=[
 '分工全文覆盖与综合者亲读范围分别声明；继承证据不等综合者再次亲读他卷原文。',
 '游戏玩家资格/国籍、现实法律与国家身份分域；角色技术和医疗解释均限小说情境。',
 '同ID依服务器/职业/组织分实体，称号与身体/灵魂操控分层；不从纵横或斩龙倒灌履历。',
 'NPC群体比例恢复不自动套具名者；误认死亡、真死后复生、断肢仍活与出图失资格分别结算。',
 '三魂和寻剑的系统形式成功不担保委托人道德、被救者恢复与物品后续控制权。',
 '神位/神格/技能激活/转职学习与装备持有/资格/实用按具体时点分开，不把历史优势永久相加。',
 '杀君主/持杖/选择模式/战终保持主权有不同回执，英雄王死不等英雄城征服。',
 '款项与承诺逐笔主体/用途/币种追踪；未见履约为未知，不能肯定实际没有发生。',
 '主文未宣死；后记赴美治疗明示、匿名镜头强示恢复，未绝对病愈，何末疗仍纱。',
 '作者月恒三部曲说明与用户提供三书管理顺序分开；宣传预告不当斩龙实际阅读。']
W(B/'book-synthesis-draft.json',data)
lines=['# 《网游之天下无双》全书九维综合（待审稿）','','八卷1599正文、1609原片由团队按真实读者分工全文覆盖；本稿是阅读完成材料上的36条派生研究。综合者亲读卷三及卷八尾37片，其余依据各卷原读者研究材料，不冒称一人独读全书。','','原来只覆盖卷一至五的partial草稿保留在book-synthesis-draft/analysis.json与report.md；本文件新增卷六至八的反证、结算和适用边界，不以36条数齐备替代全书材料齐备。源事实、综合解释、原创转化与用户取舍分层；用户尚未批准任何观察成为个人风格。','']
for d,rows in dimensions.items():
 lines += ['## '+DIM_NAMES[d],'']
 for i,row in enumerate(rows,1):
  lines += [f"### {i}. {row['title']}",'','跨卷事实：'+row['fact_summary'],'','综合解释：'+row['claim'],'','可操作机制：'+row['mechanism'],'','反证与边界：'+row['limits_and_counterevidence'],'','原创转化：'+row['originality_transform'],'','取舍草案：保留'+row['literary_choice']['take']+'；舍弃或限制：'+row['literary_choice']['leave'],'','后段检验结果：'+row['late_stage_result'],'','依据：'+'；'.join(f"卷{x['volume']} {x['json_pointer']}（{x['source_reader']}）" for x in row['supporting_observations'])+'。','']
lines += ['## 覆盖、版本与发布边界','', '卷三378原片含raw0399误识别片，实际376正文；卷八105片含卷标题、实际104正文。书首raw0001由primary另读，不把附表或独立番外倒灌主线。八卷/书首日志并集1609片完整，无重复/缺口；本综合新增原文阅读数为0。','', '每卷选用正式analysis优先，否则选主审冻结暂存版，具体路径、exists和SHA在[机器可检验稿](book-synthesis-draft.json)的upstream_documents中；正式与暂存九维语义逐项相同才可切换。全部继承定位已本地核验，不能代替primary语义签审和用户文学判断。','', '结尾保赴美治疗明示/恢复强暗示，不写绝对病愈或何已拆纱；旧债、借物、计划依后证逐项结，不以巨富、荣耀或圆满氛围自动清账。人物弧和历史问题终点另由独立audit负责，本稿不改其结论。作者所称月恒三部曲与用户提供三书列表分开；斩龙尚未由本综合实际阅读。','']
(B/'book-synthesis-draft.md').write_text('\n'.join(lines),encoding='utf-8')
W(P/'final-validation.json',dict(**V,input_documents_verified=sum(len(x['documents']) for x in inputs),output_sha256={n:sha(B/n) for n in ['book-synthesis-draft.json','book-synthesis-draft.md']},formal_library_modified=False,primary_review_forged=False))
W(P/'synthesis-state.json',dict(status='full_eight_volume_draft_ready_for_primary_review',complete_book_research_materials=True,full_book_synthesis_complete=True,personal_complete_book_read=False,included_volumes=list(range(1,9)),pending_volumes=[],observations=36,output_files=[relative(B/'book-synthesis-draft.json'),relative(B/'book-synthesis-draft.md')],updated_at=now))
print(json.dumps(V,ensure_ascii=False))
