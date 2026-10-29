"""B隔离组装器：默认纯只读；root先合池并全部签齐后，--write才冻结。

不生成终评、证据、原文阅读或primary凭据；四包JSON保输入原字节。
validate_material_archive可单独用于正式发布包/隔离恢复，不依赖.planning。
"""
from __future__ import annotations
import argparse, collections, datetime, hashlib, json, os, pathlib, re, sys, uuid
sys.dont_write_bytecode=True

HERE=pathlib.Path(__file__).resolve().parent
BASE=HERE.parents[3]
DEFAULT_ROOT=BASE.parents[2]
MAIN={'characters':('character-arc-audit-draft.json','characters','audit_id'),
      'findings':('end-state-audit-draft.json','findings','key'),
      'historical':('historical-question-pool.json','candidates','candidate_id'),
      'local':('local-question-pool.json','candidates','candidate_id')}
STATUSES={'answered','partial','unknown','unrecovered'}
EKEYS={'source_id','revision','chapter_id','start_line','end_line'}
def require(ok,message):
 if not ok:raise ValueError(message)
def digest(data):return hashlib.sha256(data).hexdigest()
def enc(value):return (json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def read(path):return json.loads(pathlib.Path(path).read_text(encoding='utf-8-sig'))
def safe(root,relative):
 root=pathlib.Path(root).resolve();raw=str(relative).replace('\\','/');p=pathlib.PurePosixPath(raw)
 require(raw and not p.is_absolute() and ':' not in raw and '..' not in p.parts,'路径越界: '+raw)
 target=(root/pathlib.Path(*p.parts)).resolve();require(target.is_relative_to(root),'路径越界: '+raw);return target
def evidence_count(value,source):
 chapters={c['chapter_id']:c for c in source['chapters']};count=0
 def visit(x):
  nonlocal count
  if isinstance(x,dict):
   if EKEYS.issubset(x):
    c=chapters.get(x['chapter_id']);require(c and x['source_id']==source['source_id'] and x['revision']==source['revision'],'证据来源或修订错误')
    require(type(x['start_line']) is int and type(x['end_line']) is int and c['start_line']<=x['start_line']<=x['end_line']<=c['end_line'],'证据行界错误')
    require(x.get('claim_kind') in {'fact','inference','synthesis','plan'},'证据claim_kind错误');count+=1
   for child in x.values():visit(child)
  elif isinstance(x,list):
   for child in x:visit(child)
 visit(value);return count
def material_requests(value):
 """只解析显式研究材料路径；normalized_path/正文TXT不进入包。"""
 found=[]
 def visit(x):
  if isinstance(x,dict):
   for key in ('research_path','material_path'):
    if isinstance(x.get(key),str):found.append((x[key],x.get('material_sha256') or x.get('research_sha256')))
   for key in ('additional_support_sha256',):
    if isinstance(x.get(key),dict):found.extend(x[key].items())
   for key in ('priority_corrections','documents'):
    if isinstance(x.get(key),list):
     for row in x[key]:
      if isinstance(row,dict) and isinstance(row.get('path'),str) and isinstance(row.get('sha256'),str) and row.get('exists',True):found.append((row['path'],row['sha256']))
   for child in x.values():visit(child)
  elif isinstance(x,list):
   for child in x:visit(child)
 visit(value);return found
def render_section(kind,data):
 lines=['# 《斩龙》'+{'characters':'人物全弧','findings':'重点终态','historical':'历史问题与线程','local':'本地原子问题'}[kind]+'审计（研究草稿）','',
        '以下只渲染已签对象；各读者原始归属保留，不冒称组装者重读全书。answered包含失败、规则及证据边界澄清，不等全部伏笔成功回收。','']
 for row in data[MAIN[kind][1]]:
  item_id=row[MAIN[kind][2]];lines+=['## '+item_id+' '+str(row.get('display_name',row.get('name',row.get('title','')))),'']
  if kind in ('historical','local'):
   d=row['terminal_assessment'];lines += [f"原卷：{row['volume']}；原索引：{row.get('original_index')}；原阶段题保留。",'',f"终点：{d['status']}；领域：{d['audit_domain']}",'',d['rationale'],'','后证raw：'+', '.join(str(n) for n in d['later_chapters']),'']
  else:
   fields=('initial_comparison_stage','key_decisions','costs','terminal_state','evidence_boundaries') if kind=='characters' else ('terminal_status','stage_chain','conclusion','limits_and_counterevidence')
   for key in fields:
    value=row.get(key)
    if value is not None:lines += [key+'：'+('\n'.join('- '+str(t) for t in value) if isinstance(value,list) else str(value)),'']
   lines += ['来源引用：'+', '.join(e.get('chapter_id','') for e in row.get('evidence',[])),'']
 return ('\n'.join(lines)+'\n').encode('utf-8')

def prepare(root,stage,*,expected_pool_counts=None,expected_findings=24):
 root=pathlib.Path(root).resolve();stage=pathlib.Path(stage).resolve();audit=stage/'audit/whole-book';require(stage.is_relative_to(root),'暂存目录越出工作区')
 expected_pool_counts=expected_pool_counts or {'historical':232,'local':2462}
 reads={};files={}
 def grab(p):
  p=pathlib.Path(p).resolve();require(p.is_relative_to(root),'输入越出工作区: '+str(p));require(p.is_file(),'缺输入: '+str(p));b=p.read_bytes();reads[str(p)]=digest(b);return b
 def obj(p):return json.loads(grab(p).decode('utf-8-sig'))
 source=obj(stage/'source.json');cp=obj(stage/'primary-audit-review-progress.json');rp=obj(stage/'primary-research-group-review-progress.json')
 package={k:obj(audit/spec[0]) for k,spec in MAIN.items()}
 for kind in ('historical','local'):
  pool=package[kind];require(pool.get('source_id')==source['source_id'] and not pool.get('pending_inputs'),'池仍有未完成输入')
  require(len(pool['candidates'])==expected_pool_counts[kind],'候选池冻结数量变化: '+kind)
 require(len(package['historical']['candidates'])==sum(x.get('open_questions',0)+x.get('graph_threads',0) for x in package['historical']['inputs']),'历史候选与分卷输入覆盖不符')
 local_keys={(r['volume'],r['original_field'],r['original_index']) for r in package['local']['candidates']}
 for group in package['historical'].get('local_issue_records',[]):
  empty=set(group.get('empty_record_indices',[]))
  require(all(type(i) is int and 0<=i<len(group['original_records']) for i in empty),'原本地空记录索引错误')
  for i,original in enumerate(group['original_records']):
   if i in empty:
    require(group['field'] in {'chapter_unresolved_index','chapter_source_anomaly_index'} and isinstance(original,dict) and original.get('unresolved',original.get('original_unresolved',original.get('source_anomalies')))==[],'空记录不可跳过非空原问题')
   else:require((group['volume'],group['field'],i) in local_keys,'原始本地问题缺候选覆盖')
 merge_receipt=obj(audit/'adjudication-progress.json')
 require(merge_receipt.get('status')=='merged-exact-primary-reviewed-decisions' and merge_receipt.get('original_records_unchanged') and merge_receipt.get('exact_evidence_objects_preserved'),'缺root保全原记录/精确证据的合并回执')
 for kind in ('historical','local'):
  p=audit/MAIN[kind][0];require(reads[str(p.resolve())]==merge_receipt['pool_after_sha256'][kind],'root合并后池原记录或字节变化: '+kind)
 require(reads[str((stage/'primary-audit-review-progress.json').resolve())]==merge_receipt['primary_progress_sha256'],'root合并时签收进度已变化')
 expected=[r for k in ('historical','local') for r in package[k]['candidates']];lookup={r['candidate_id']:r for r in expected};require(len(lookup)==len(expected),'原池ID重复')
 signed={};batch_provenance={}
 for group in cp['batches']:
  rel=group['path'];b=grab(safe(audit,rel));require(digest(b)==group['sha256'],'已签批SHA变化: '+rel);rows=json.loads(b)
  require([r['candidate_id'] for r in rows]==group['candidate_ids'] and len(rows)==group['count'],'签批ID/数量变化')
  files[rel]=b
  for row in rows:
   cid=row['candidate_id'];require(cid not in signed and cid in lookup,'签批候选重复/越集: '+cid);signed[cid]=row;batch_provenance[cid]={'path':rel,'sha256':digest(b)}
 require(set(signed)==set(lookup),f'候选尚未签齐: {len(signed)}/{len(lookup)}')
 require(sorted(signed)==cp['distinct_reviewed_candidate_ids'] and len(signed)==cp['distinct_reviewed_candidates'],'签收账本集合不同')
 comparisons=[]
 for row in expected:
  cid=row['candidate_id'];d=row['terminal_assessment'];s=signed[cid]
  require(d.get('review_progress')=='primary-reviewed-draft','池尚未由root合并/未完成: '+cid)
  require(d.get('status') in STATUSES and not d.get('depends_on_volumes'),'合池终评未完成: '+cid)
  for key in ('status','rationale','audit_domain','later_chapters','later_evidence','actual_reviewer'):
   require(d.get(key)==s.get(key),'合池与签批语义/证据逐值不同: '+cid+'/'+key)
  require(set(d['later_chapters'])=={int(e['chapter_id'][3:]) for e in d['later_evidence']},'后证章节集合不同')
  comparisons.append({'candidate_id':cid,'signed_batch':batch_provenance[cid],'status_rationale_domain_later_chapters_equal':True,'later_evidence_objects_equal':True,'original_fields_preserved_by_root_merge':True})
 research={'characters':{},'findings':{}};formal={};group_provenance={}
 for group in rp['groups']:
  section=group['section'];require(section in research,'未知研究组类型');rel=group['path'];b=grab(safe(audit,rel));require(digest(b)==group['sha256'],'已签研究SHA变化: '+rel);value=json.loads(b);rows=value[section];ids=[r[group['id_field']] for r in rows]
  require(ids==group['reviewed_ids'] and len(ids)==group['count'],'研究签组ID/数变化');files[rel]=b
  for k,v in value.get('formal_input_sha256',{}).items():
   require(k not in formal or formal[k]==v,'研究组正式pin冲突');formal[k]=v
  for r,i in zip(rows,ids):require(i not in research[section],'研究ID重复');research[section][i]=r;group_provenance[i]={'path':rel,'sha256':digest(b)}
 for section,rows in research.items():
  require(rows,'研究组尚未签齐: '+section);final=package[section][section];key=MAIN[section][2]
  require(len(final)==len(rows) and {r[key] for r in final}==set(rows),'研究总稿未全部签收: '+section)
  for row in final:require(row==rows[row[key]],'研究最终对象与签组不逐值相等: '+row[key])
 require(len(research['findings'])==expected_findings,'24重点尚未全签/数量变化')
 # 整书九维36条沿现有publish_book_synthesis接口的真实主审凭据验收。
 synthesis_review=obj(stage/'primary-synthesis-review.json')
 require(synthesis_review.get('reviewer')=='primary' and synthesis_review.get('status')=='reviewed_for_library_import' and synthesis_review.get('source_id')==source['source_id'],'36综合尚未主审签收')
 for name in ('book-synthesis-draft.json','book-synthesis-draft.md'):
  b=grab(stage/name);require(digest(b)==synthesis_review['input_sha256'][name],'36综合签后SHA变化');files[('provenance/' if name.endswith('.md') else '')+'input-snapshots/synthesis/'+name]=b
 synthesis=obj(stage/'book-synthesis-draft.json');require(synthesis['validation']['observations']==36 and len(synthesis['dimensions'])==9 and sum(map(len,synthesis['dimensions'].values()))==36 and all(r.get('claim_kind')=='synthesis' for rows in synthesis['dimensions'].values() for r in rows),'综合36条/九维schema不符')
 files['input-snapshots/synthesis/primary-synthesis-review.json']=grab(stage/'primary-synthesis-review.json')
 # 正式六卷各六接口独立核当前SHA；组内旧pin若漂移直接拒绝，不以历史版代替当前输入。
 receipt=audit/'focused-input-receipt.json'
 if receipt.exists():
  for k,v in obj(receipt).get('formal_input_sha256',{}).items():require(k not in formal or formal[k]==v,'正式输入pin冲突');formal[k]=v
 for v in range(1,7):
  for suffix in ('analysis.json','cards.json','graph.json','chapter-notes.jsonl','handoff.md','.md'):
   name=f'vol{v:02d}'+(suffix if suffix=='.md' else '-'+suffix);p=root/'writing-vault/library/reports/zhanlong'/name;rel=p.relative_to(root).as_posix();h=digest(grab(p));require(rel not in formal or formal[rel]==h,'正式分卷输入已变化: '+rel);formal[rel]=h
 for rel,h in formal.items():require(digest(grab(safe(root,rel)))==h,'正式输入SHA不符: '+rel)
 # 末卷原审输入按byte保存；legacy键名仍volume08，明确真实是卷六。
 review_path=stage/'review-vol06.json';review=obj(review_path);frozen={}
 files['input-snapshots/review-vol06.json']=grab(review_path)
 for name,h in review['input_sha256'].items():
  b=grab(safe(stage/'vol06',name));require(digest(b)==h,'卷六原review输入改变: '+name);rel=('provenance/' if name.endswith('.md') else '')+'input-snapshots/vol06/'+name;files[rel]=b;frozen[rel]=h
 for name in ('primary-audit-review-progress.json','primary-research-group-review-progress.json'):
  files['input-snapshots/'+name]=grab(stage/name)
 files['input-snapshots/source-index.json']=grab(stage/'source.json')
 # 签批及受控更改历史均保原JSON；不把before/unsubmitted当新候选合入。
 for p in sorted(audit.rglob('*.json')):
  rel=p.relative_to(audit).as_posix()
  if any(s in p.parts for s in ('assembly-preview','assembly-prep','material-snapshots','materials')):continue
  if any(t in rel.lower() for t in ('delta','proposal','before','correction')) or 'history' in p.parts:files.setdefault(rel,grab(p))
 for name in ('priority-corrections-delta.json','focused-input-receipt.json','adjudication-progress.json','character-stage-card-resolution.json','character-stage-card-resolution.md','character-roster-scope.json'):
  if (audit/name).exists():files.setdefault(name,grab(audit/name))
 # 当前优先层按冻结时观察的实际文件动态保存，绝不锁死97/100字段版本。
 priority_layers=[]
 current_priority=[audit/'priority-corrections-delta.json']+sorted((root/'writing-vault/library/reports/zhanlong/audit').glob('priority-corrections*.json'))
 for p in current_priority:
  if not p.is_file() or any(t in p.name.lower() for t in ('proposal','before')):continue
  b=grab(p);v=json.loads(b);rel='priority-inputs/'+digest(b)+'.json';files[rel]=b
  priority_layers.append({'original_path':p.relative_to(root).as_posix(),'material_sha256':digest(b),'snapshot_path':rel,'observed_primary_status':v.get('primary_approval',{}).get('status',v.get('status','not-stated')),'interpretation':'只保该层原标识与字节，不新增文学结论/用户批准'})
 files['priority-reading-index.json']=enc({'purpose':'当前旧笔记优先层的版本入口；与原研究所引历史版本分别保留','layers':priority_layers,'signed_research_objects_unchanged':True})
 # 接口代码只作原字节依赖归档；独立材料验证函数本身仅依赖标准库。
 dependencies=[]
 if BASE.is_relative_to(root):
  for name in ('book_audit_common.py','record_primary_whole_book_review.py','publish_book_audit.py','merge_zhanlong_adjudications.py','record_primary_research_group.py','publish_book_synthesis.py'):
   p=BASE/name;b=grab(p);rel='input-snapshots/interfaces/'+name;files[rel]=b;dependencies.append({'original_path':p.relative_to(root).as_posix(),'sha256':digest(b),'snapshot_path':rel})
 files['assembly-interface-dependencies.json']=enc({'implementation_dependencies':['Python standard library'],'reviewed_existing_interfaces':dependencies,'production_tools_modified':False,'material_validator_standalone':True})
 # 解析旧版本优先正式material-history清单；再按已知原字节历史查SHA，不替换原路径。
 material_history=root/'writing-vault/library/reports/zhanlong/audit/material-history/manifest.json';history=[]
 if material_history.exists():
  hdata=obj(material_history);history=hdata.get('materials',[]);files['input-snapshots/material-history-manifest.json']=grab(material_history)
 archived_cache=None
 def resolve(path,expected_sha):
  nonlocal archived_cache
  p=safe(root,path);require(p.suffix.lower()!='.txt' and 'private-sources' not in p.parts,'正文TXT禁止打包: '+path)
  if p.is_file():
   b=grab(p)
   if expected_sha is None or digest(b)==expected_sha:return p,b,'current-exact-bytes'
  if expected_sha:
   for h in history:
    if h['original_path'].replace('\\','/')==path.replace('\\','/') and h['original_sha256']==expected_sha:
     hp=safe(root,h['archive_path']);b=grab(hp);require(digest(b)==expected_sha==h['archived_sha256'],'历史材料SHA不符');return hp,b,'formal-material-history-exact-version'
   if archived_cache is None:
    archived_cache={}
    for hp in sorted(audit.rglob('*')):
     if hp.is_file() and hp.suffix.lower() in ('.json','.jsonl','.md') and 'assembly-prep' not in hp.parts:
      hb=grab(hp);archived_cache.setdefault(digest(hb),(hp,hb))
   if expected_sha in archived_cache:return (*archived_cache[expected_sha],'audit-history-exact-version')
  raise ValueError('缺少精确研究材料版本: '+path+' @ '+str(expected_sha))
 requests=[]
 for value in package.values():requests+=material_requests(value)
 active_requests=list(requests)
 active_documents={g['path'] for g in cp['batches']}|{g['path'] for g in rp['groups']}|{v[0] for v in MAIN.values()}
 historical_body_locators=[]
 for name,b in list(files.items()):
  try:value=json.loads(b.decode('utf-8-sig'))
  except (UnicodeError,json.JSONDecodeError):continue
  for original,h in material_requests(value):
   target=safe(root,original)
   is_body=target.suffix.lower()=='.txt' or 'private-sources' in target.parts
   is_unsigned_history=name not in active_documents and any(t in name.lower() for t in ('proposal','before','delta','correction','history'))
   if is_body and is_unsigned_history:
    historical_body_locators.append({'history_path':name,'original_path':original,'recorded_sha256':h,'reason':'未采用历史方案中的正文定位，仅保存方案原字节，不作为当前研究材料依赖'})
   else:
    requests.append((original,h))
    if not is_unsigned_history:active_requests.append((original,h))
 files['historical-body-locators-not-packaged.json']=enc({'history_bytes_preserved':True,'active_signed_source_body_dependency_still_rejected':True,'entries':historical_body_locators})
 requests += list(formal.items())
 requests += [(x['original_path'],x['material_sha256']) for x in priority_layers]
 active_requests += list(formal.items())+[(x['original_path'],x['material_sha256']) for x in priority_layers]
 # 活动材料按精确版本递归核依赖；被签组引用的proposal不能因文件名获得历史豁免。
 active_seen=set()
 while active_requests:
  original,h=active_requests.pop();key=(original,h)
  if key in active_seen:continue
  active_seen.add(key);p,b,method=resolve(original,h);requests.append((original,digest(b)))
  try:active_requests+=material_requests(json.loads(b.decode('utf-8-sig')))
  except (UnicodeError,json.JSONDecodeError):pass
 mappings={}
 for original,h in requests:
  p,b,method=resolve(original,h);h=digest(b);key=(original,h)
  if key in mappings:continue
  ext=p.suffix.lower();snapshot=('provenance/' if ext=='.md' else '')+'materials/'+h+(ext if ext in ('.json','.jsonl','.md') else '.bin');files[snapshot]=b
  mappings[key]={'original_path':original,'material_sha256':h,'snapshot_path':snapshot,'resolved_from':p.relative_to(root).as_posix(),'resolution_method':method,'bytes_unchanged':True}
 resolution={'schema_version':1,'purpose':'原路径和SHA映射至包内原字节；不改签收对象的research_path/material_path','entries':sorted(mappings.values(),key=lambda x:(x['original_path'],x['material_sha256'])),'body_txt_included':False,'standalone_no_planning_dependency':True}
 files['material-resolution-index.json']=enc(resolution)
 counts={'character_arcs':len(research['characters']),'focused_findings':len(research['findings']),'historical_candidates':len(package['historical']['candidates']),'local_candidates':len(package['local']['candidates']),'evidence_references_checked':sum(evidence_count(v,source) for v in package.values())}
 for k,(name,_,_) in MAIN.items():files[name]=grab(audit/name);files[name[:-5]+'.md']=render_section(k,package[k])
 signed_progress={p.relative_to(root).as_posix():reads[str(p)] for p in (stage/'primary-audit-review-progress.json',stage/'primary-research-group-review-progress.json')}
 merge={'status':'passed-exact-already-merged-signed-objects','candidate_semantic_objects_compared':len(comparisons),'candidate_comparisons':comparisons,'research_objects_exactly_equal_signed_groups':True,'research_object_counts':{k:len(v) for k,v in research.items()},'signed_candidate_batches':len(cp['batches']),'signed_research_groups':len(rp['groups']),'signed_progress_sha256':signed_progress,'no_evidence_enrichment_or_regeneration':True,'original_four_json_bytes_preserved':True}
 files['merge-validation.json']=enc(merge)
 validation={'status':'passed_structure_provenance_and_signed_semantic_equality',**counts,'pending_inputs':[],'unadjudicated_candidates':[],'frozen_volume08_unchanged':True,'legacy_frozen_volume08_actual_volume':6,'candidate_semantic_equality':True,'research_semantic_equality':True,'answered_is_not_all_story_payoffs':True,'semantic_review_owned_by_primary':True,'material_resolution_entries':len(mappings),'raw_source_txt_copied':False}
 files['audit-validation.json']=enc(validation)
 lines=['# 《斩龙》终点审计组装交接（研究草稿）','',f"已签候选{len(expected)}：历史{counts['historical_candidates']}、本地{counts['local_candidates']}；人物{counts['character_arcs']}、重点{counts['focused_findings']}；动态引用{counts['evidence_references_checked']}。",'','四包JSON保root已合并/已签总稿原字节；未生成证据或新文学判断。原文实读归属保各读者，不冒称本组装者全书重读。','', '[人物弧](character-arc-audit-draft.md) · [重点终态](end-state-audit-draft.md) · [历史池](historical-question-pool.md) · [本地池](local-question-pool.md)','', '[签组语义比对](merge-validation.json) · [精确材料版本解析](material-resolution-index.json) · [验证](audit-validation.json)','', '旧路径与旧SHA原样保留，通过material-resolution-index定位包内原字节（包括旧priority a60版本）。恢复检查可独立调用组装器validate_material_archive，不需要.planning；正文TXT未复制，仍沿标准来源位置/独立备份管理。','', 'legacy frozen_volume08_hashes在本书明确表示卷六原review输入byte快照，不表示存在卷八。主审进度、签批和delta历史独立保存；不要把这些历史文件当额外候选重复合池。','', 'root下一步独立整体主审，才运行record_primary_whole_book_review.py与publish_book_audit.py。本脚本不签primary，不写正式库；用户审美仍draft。']
 if 'priority-corrections-delta.json' in files:lines[2:2]=['[优先旧笔记纠正](priority-corrections-delta.json)：检索旧分卷时同步看纠正叠加；原件保历史。','']
 lines += ['', '[当前优先层版本入口](priority-reading-index.json)另列冻结时存在的最新层；原研究所引旧版保原SHA，不用新层倒填旧阅读。']
 lines += ['', '[已审36综合原输入](input-snapshots/synthesis/book-synthesis-draft.json)与[真实综合主审](input-snapshots/synthesis/primary-synthesis-review.json)只作依赖快照，不在此重写综合或代签。']
 files['whole-book-audit-handoff.md']=('\n'.join(lines)+'\n').encode('utf-8')
 report=['# 《斩龙》终点审计组装统计','',f"人物{counts['character_arcs']}、重点{counts['focused_findings']}、候选{len(expected)}；来源引用{counts['evidence_references_checked']}。",'', 'answered含失败、规则解释与证据约束澄清；unknown是已匹配后的具体证据不足，不是未查或作者忘记。','', '| 池/领域 | answered | partial | unrecovered | unknown |','|---|---:|---:|---:|---:|']
 for kind in ('historical','local'):
  domains=collections.defaultdict(collections.Counter)
  for r in package[kind]['candidates']:d=r['terminal_assessment'];domains[d['audit_domain']][d['status']]+=1
  for domain,c in sorted(domains.items()):report.append('| '+kind+'/'+domain+' | '+' | '.join(str(c.get(k,0)) for k in ('answered','partial','unrecovered','unknown'))+' |')
 report += ['', '[完整交接](whole-book-audit-handoff.md) · [材料独立解析](material-resolution-index.json) · [逐对象比对](merge-validation.json)']
 files['whole-book-audit-report.md']=('\n'.join(report)+'\n').encode('utf-8')
 # 既有可读页若将换成结构化重渲染，先把旧字节作为历史输入；JSON一律不改。
 for name in list(files):
  p=safe(audit,name)
  if name.endswith('.md') and p.is_file() and p.read_bytes()!=files[name]:files['provenance/input-snapshots/previous-markdown/'+name]=grab(p)
 files['assembly-prep/assemble_zhanlong_signed_audit.py']=pathlib.Path(__file__).read_bytes()
 manifest={'status':'draft_frozen_for_final_primary_review_not_user_approval','source_id':source['source_id'],'revision':source['revision'],'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'audit_sha256':{n:digest(b) for n,b in files.items()},'formal_input_sha256':formal,'frozen_volume08_hashes':frozen,'legacy_frozen_volume08_actual_volume':6,'signed_progress_sha256':signed_progress,'counts':counts,'material_resolution_index':'material-resolution-index.json','body_txt_included':False}
 files['audit-freeze-manifest.json']=enc(manifest)
 return {'status':'ready-no-write','root':str(root),'stage':str(stage),'audit':str(audit),'files':files,'read_set':reads,'counts':counts,'material_resolution':resolution,'signed_batches':len(cp['batches']),'signed_groups':len(rp['groups'])}

def archive_path(audit,name):
 p=safe(audit,name)
 if p.is_file():return p
 # 发布器把.py源码移入provenance；材料数据原路径不变。
 q=safe(audit,'provenance/'+name);require(q.is_file(),'缺包内文件: '+name);return q
def validate_material_archive(root_or_audit,book=None):
 """纯只读；原研究路径不必存在，以原path+SHA匹配内容寻址快照。"""
 p=pathlib.Path(root_or_audit).resolve();audit=p if (p/'material-resolution-index.json').is_file() else p/'writing-vault/library/reports'/str(book or 'zhanlong')/'audit/whole-book'
 index=read(audit/'material-resolution-index.json');manifest=read(audit/'audit-freeze-manifest.json');seen={}
 for row in index['entries']:
  key=(row['original_path'],row['material_sha256']);require(key not in seen,'材料原path/SHA映射重复');snapshot=safe(audit,row['snapshot_path']);require(snapshot.is_file() and digest(snapshot.read_bytes())==row['material_sha256'],'包内精确材料SHA错误');require(snapshot.suffix.lower()!='.txt','不允许正文TXT');seen[key]=row
 for kind,(name,_,_) in MAIN.items():
  for original,h in material_requests(read(audit/name)):
   matches=[k for k in seen if k[0]==original and (h is None or k[1]==h)];require(matches,'原研究路径没有精确包内解析: '+original)
 for name,h in manifest['audit_sha256'].items():require(digest(archive_path(audit,name).read_bytes())==h,'冻结文件SHA错误: '+name)
 for name,h in manifest['frozen_volume08_hashes'].items():require(digest(archive_path(audit,name).read_bytes())==h,'卷六快照SHA错误')
 return True
verify_portable=validate_material_archive

def commit(plan,output):
 """只供明确--write/隔离测试调用；不触发合池、主审签名或正式发布。"""
 output=pathlib.Path(output).resolve();require(output.is_relative_to(pathlib.Path(plan['root']).resolve()),'冻结输出越出隔离工作区');require(not (output/'audit-freeze-manifest.json').exists(),'冻结清单已存在，不覆盖')
 for name,h in plan['read_set'].items():p=pathlib.Path(name);require(p.is_file() and digest(p.read_bytes())==h,'准备期间输入变化: '+name)
 require('primary-whole-book-review.json' not in plan['files'],'禁止伪造primary凭据')
 output.mkdir(parents=True,exist_ok=True);temp=output/('.assembly-tmp-'+uuid.uuid4().hex[:12]);temp.mkdir()
 for name,b in plan['files'].items():p=safe(temp,name);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
 validate_material_archive(temp)
 # 调用现有发布共用schema验证，不调用任何签收/发布动作。
 if (BASE/'book_audit_common.py').is_file():
  sys.path.insert(0,str(BASE));from book_audit_common import load_package
  load_package(temp,read(temp/'input-snapshots/source-index.json'))
 for name,h in plan['read_set'].items():require(digest(pathlib.Path(name).read_bytes())==h,'冻结准备期间输入变化: '+name)
 for name,b in plan['files'].items():
  if name=='audit-freeze-manifest.json':continue
  target=safe(output,name);target.parent.mkdir(parents=True,exist_ok=True)
  if target.is_file() and target.read_bytes()==b:continue
  os.replace(safe(temp,name),target)
 os.replace(temp/'audit-freeze-manifest.json',output/'audit-freeze-manifest.json')
 # 不递归删临时目录，留下无副作用的准备现场；便于审计失败/重复字节。
 validate_material_archive(output)
 return {'status':'frozen-pending-real-primary-final-review','manifest_sha256':digest((output/'audit-freeze-manifest.json').read_bytes()),'counts':plan['counts'],'formal_writes':False,'primary_credentials_created':False}

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=pathlib.Path,default=DEFAULT_ROOT);p.add_argument('--stage',type=pathlib.Path,default=BASE/'zhanlong');p.add_argument('--write',action='store_true');p.add_argument('--validate-material-archive',type=pathlib.Path);p.add_argument('--book',default='zhanlong');a=p.parse_args()
 if a.validate_material_archive:
  validate_material_archive(a.validate_material_archive,a.book);print(json.dumps({'status':'material-archive-passed','read_only':True},ensure_ascii=False));return
 try:plan=prepare(a.root,a.stage)
 except (ValueError,KeyError,OSError) as e:
  print(json.dumps({'status':'not-ready-no-write','reason':str(e),'write_requested':a.write,'formal_writes':False,'primary_credentials_created':False},ensure_ascii=False))
  if a.write:raise SystemExit(1)
  return
 if a.write:result=commit(plan,plan['audit'])
 else:result={'status':plan['status'],'counts':plan['counts'],'signed_batches':plan['signed_batches'],'signed_groups':plan['signed_groups'],'planned_files':len(plan['files']),'write_performed':False,'formal_writes':False,'primary_credentials_created':False}
 print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':
 sys.stdout.reconfigure(encoding='utf-8');main()
