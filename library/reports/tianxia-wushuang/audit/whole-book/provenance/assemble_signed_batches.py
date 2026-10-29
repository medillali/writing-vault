"""仅按primary实际签收白名单组装四包；默认只查就绪，不生成任何阅读。"""
from __future__ import annotations
import argparse,collections,copy,datetime,hashlib,json,pathlib,sys
from audit_evidence import H,B,R,source,chapters,volume_by_id
sys.stdout.reconfigure(encoding='utf-8')
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def require(ok,msg):
 if not ok:raise ValueError(msg)
def json_digest(x):return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def chapter_ref(n):
 c=chapters[n];v=volume_by_id[c['chapter_id']]
 return dict(source_id=source['source_id'],revision=source['revision'],chapter_id=c['chapter_id'],start_line=c['start_line'],end_line=c['end_line'],claim_kind='fact',access_level='assembled-from-primary-signed-later-chapter-list-not-new-reading',research_path=f'writing-vault/library/reports/tianxia-wushuang/vol{v:02}-analysis.json')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args()
 candidate_progress=B/'primary-audit-review-progress.json';research_progress=B/'primary-research-group-review-progress.json'
 progress_hashes={str(p.relative_to(R).as_posix()):sha(p) for p in [candidate_progress,research_progress]}
 cp,rp=read(candidate_progress),read(research_progress)
 pools={k:read(H/f'{k}-question-pool.json') for k in ['historical','local']}
 pool_input_sha={k:sha(H/f'{k}-question-pool.json') for k in pools}
 expected={x['candidate_id']:x for p in pools.values() for x in p['candidates']}
 require(len(expected)==4130 and len(pools['historical']['candidates'])==214 and len(pools['local']['candidates'])==3916,'候选池ID或预期4130/214/3916改变')
 signed={};candidate_provenance={};frozen_files={};invalid=[]
 for g in cp['batches']:
  path=H/g['path'];actual=sha(path)
  if actual!=g['sha256']:invalid.append(dict(path=g['path'],signed_sha256=g['sha256'],actual_sha256=actual));continue
  rows=read(path);require([r['candidate_id'] for r in rows]==g['candidate_ids'] and len(rows)==g['count'],'候选签组ID/数变化')
  frozen_files[g['path']]=actual
  for row in rows:
   cid=row['candidate_id'];require(cid not in signed,'重复候选签收: '+cid);require(cid in expected,'签收ID不在池: '+cid)
   signed[cid]=row;candidate_provenance[cid]=dict(path=g['path'],sha256=actual,scope=g['scope'])
 research={'characters':{},'findings':{}};research_provenance={}
 for g in rp['groups']:
  path=H/g['path'];actual=sha(path)
  if actual!=g['sha256']:invalid.append(dict(path=g['path'],signed_sha256=g['sha256'],actual_sha256=actual));continue
  rows=read(path)[g['section']];ids=[r[g['id_field']] for r in rows];require(ids==g['reviewed_ids'] and len(ids)==g['count'],'研究签组ID/数变化')
  frozen_files[g['path']]=actual
  for row,item in zip(rows,ids):
   require(item not in research[g['section']],'研究ID重复: '+item);research[g['section']][item]=row;research_provenance[item]=dict(path=g['path'],sha256=actual)
 missing=sorted(set(expected)-set(signed));result=dict(status='ready' if not missing and not invalid and len(research['characters'])==115 and len(research['findings'])==30 else 'not_ready',signed_candidates=len(signed),expected_candidates=len(expected),missing_candidates=len(missing),missing_ids=missing,invalid_signed_files=invalid,signed_characters=len(research['characters']),signed_findings=len(research['findings']))
 if not args.write:
  result['missing_id_sample']=missing[:8];result.pop('missing_ids',None);print(json.dumps(result,ensure_ascii=False));return
 require(result['status']=='ready','尚未全部实际签收，不得组装: '+json.dumps(result,ensure_ascii=False))
 require(not (H/'audit-freeze-manifest.json').exists(),'冻结清单已存在；不重建已冻结包。')
 output_dir=H/'assembly-preview';final_outputs={}
 def output(name,value):
  path=output_dir/name;write(path,value);final_outputs[name]=path
 def output_text(name,value):
  path=output_dir/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(value,encoding='utf-8');final_outputs[name]=path
 inventory=read(H/'input-inventory.json')
 for name,digest in inventory['formal_input_sha256'].items():require(sha(R/name)==digest,'正式分卷输入变化: '+name)
 review08=read(B/'review-vol08.json');v8hash={}
 for name,digest in review08['input_sha256'].items():
  require(sha(B/'vol08'/name)==digest,'卷八冻结输入变化: '+name)
  dst=H/'input-snapshots/vol08'/name;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes((B/'vol08'/name).read_bytes());v8hash[dst.relative_to(H).as_posix()]=digest
 for p in [candidate_progress,research_progress]:
  require(sha(p)==progress_hashes[p.relative_to(R).as_posix()],'组装中primary签表变化，先停再核')
  dst=H/'input-snapshots'/p.name;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(p.read_bytes())
 for k,obj in pools.items():
  dst=H/'input-snapshots/pools'/f'{k}-question-pool-before-final-assembly.json'
  if dst.exists():require(sha(dst)==pool_input_sha[k],'原候选快照不符，不覆写')
  else:dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes((H/f'{k}-question-pool.json').read_bytes())
 enrichment=[];comparisons=[];orig_checks=[]
 for kind,pool in pools.items():
  for original in pool['candidates']:
   cid=original['candidate_id'];row=signed[cid];terminal=copy.deepcopy({k:v for k,v in row.items() if k!='candidate_id'})
   require(terminal['status'] in {'answered','partial','unrecovered','unknown'} and terminal.get('rationale') and terminal.get('audit_domain'),'终评关键字段缺失: '+cid)
   require(isinstance(terminal['later_chapters'],list) and all(isinstance(n,int) for n in terminal['later_chapters']),'后证章节非整数列表: '+cid)
   if 'later_evidence' not in terminal:terminal['later_evidence']=[chapter_ref(n) for n in sorted(set(terminal['later_chapters']))]
   def enrich(value,path):
    if isinstance(value,dict):
     if {'chapter_id','start_line','end_line'}.issubset(value):
      c=next((c for c in chapters.values() if c['chapter_id']==value['chapter_id']),None)
      require(c is not None and c['start_line']<=value['start_line']<=value['end_line']<=c['end_line'],'终评后证范围无效: '+cid)
      for key,expected_value in [('source_id',source['source_id']),('revision',source['revision'])]:
       if value.get(key) is None:
        enrichment.append(dict(candidate_id=cid,json_path=path+'/'+key,before=value.get(key),after=expected_value,reason='固定来源索引已核，补签收批派生notes证据缺失的来源元数据，不改判断或后证章节',signed_batch=candidate_provenance[cid]));value[key]=expected_value
       else:require(value[key]==expected_value,'来源元数据冲突而非缺失: '+cid)
      require(value.get('claim_kind') in ['fact','inference','synthesis','plan'],'后证缺claim_kind: '+cid)
     for key,child in value.items():enrich(child,path+'/'+key)
    elif isinstance(value,list):
     for i,child in enumerate(value):enrich(child,path+'/'+str(i))
   enrich(terminal['later_evidence'],'terminal_assessment/later_evidence')
   for key in ['status','rationale','audit_domain','later_chapters']:require(terminal[key]==row[key],'终评语义变化: '+cid+'/'+key)
   require(sorted({int(e['chapter_id'][3:]) for e in terminal['later_evidence']})==sorted(set(row['later_chapters'])),'后证集合不同: '+cid)
   terminal['review_progress']='primary-signed-semantic-adjudication'
   terminal['adjudication_origin']=dict(candidate_provenance[cid],first_person_scope='签收批中第一人称/原文实读归属仅指该批原裁定者，不是组装代理重新阅读全文。')
   require(not terminal.get('depends_on_volumes'),'终评仍待卷: '+cid)
   original_before=copy.deepcopy(original);original['terminal_assessment']=terminal
   a={k:v for k,v in original_before.items() if k!='terminal_assessment'};b={k:v for k,v in original.items() if k!='terminal_assessment'};require(a==b,'候选原字段被变更: '+cid)
   orig_checks.append(dict(candidate_id=cid,original_fields_sha256=json_digest(a),unchanged=True))
   comparisons.append(dict(candidate_id=cid,signed_batch=candidate_provenance[cid]['path'],status_rationale_domain_later_chapters_equal=True,later_evidence_chapter_set_equal=True))
  pool.update(status='draft_all_candidates_primary_reviewed_pending_whole_package_acceptance',pending_inputs=[],unadjudicated_candidates=[])
  pool['adjudication_method']='只复制primary逐项实际签收的独立终评，不由本脚本生成判断；元数据缺失补全单列日志。'
  pool['terminal_statistics']=dict(statuses=dict(collections.Counter(r['terminal_assessment']['status'] for r in pool['candidates'])),by_audit_domain={domain:dict(collections.Counter(r['terminal_assessment']['status'] for r in pool['candidates'] if r['terminal_assessment']['audit_domain']==domain)) for domain in sorted({r['terminal_assessment']['audit_domain'] for r in pool['candidates']})})
  output(f'{kind}-question-pool.json',pool)
 for section,filename in [('characters','character-arc-audit-draft.json'),('findings','end-state-audit-draft.json')]:
  rows=list(research[section].values())
  if section=='characters':rows.sort(key=lambda r:int(r['audit_id'].rsplit('-',1)[1]))
  for row in rows:
   key=row['audit_id'] if section=='characters' else row['key'];require(row==research[section][key],'研究对象变化: '+key)
  output(filename,dict(status='draft_primary_groups_reviewed_pending_whole_package_acceptance',scope='无双八卷正式研究的终点派生审计；本代理亲读卷五/七，不冒称个人重新全文读1599正文。',source_id=source['source_id'],revision=source['revision'],formal_input_sha256=inventory['formal_input_sha256'],group_provenance=research_provenance,**{section:rows}))
 output('metadata-enrichment-log.json',dict(status='source-metadata-only-enrichment',fixed_source_id=source['source_id'],fixed_revision=source['revision'],entries=enrichment,no_signed_batch_modified=True,no_semantic_conclusion_changed=True))
 merge=dict(status='passed',signed_progress_sha256=progress_hashes,input_pool_sha256=pool_input_sha,candidate_semantic_objects_compared=len(comparisons),candidate_comparisons=comparisons,original_fields_checks=orig_checks,research_objects_exactly_equal_signed_groups=True,research_object_counts={k:len(v) for k,v in research.items()},source_metadata_enrichments=len(enrichment),signed_candidate_batches=len(cp['batches']),signed_research_groups=len(rp['groups']),first_person_attribution_limits='各阅读者原记录与裁定归属保留，组装只派生引用，不生成新的逐章全文阅读。')
 output('merge-validation.json',merge)
 refs=0
 def validate_evidence(x):
  nonlocal refs
  if isinstance(x,dict):
   if {'source_id','revision','chapter_id','start_line','end_line'}.issubset(x):
    require(x['source_id']==source['source_id'] and x['revision']==source['revision'],'整包证据来源不符')
    c=next((c for c in chapters.values() if c['chapter_id']==x['chapter_id']),None);require(c is not None and c['start_line']<=x['start_line']<=x['end_line']<=c['end_line'],'整包证据范围不符')
    require(x.get('claim_kind') in ['fact','inference','synthesis','plan'],'整包证据claim_kind不符');refs+=1
   for child in x.values():validate_evidence(child)
  elif isinstance(x,list):
   for child in x:validate_evidence(child)
 for filename in ['character-arc-audit-draft.json','end-state-audit-draft.json','historical-question-pool.json','local-question-pool.json']:validate_evidence(read(output_dir/filename))
 validation=dict(status='passed_structure_provenance_and_signed_semantic_equality',character_arcs=len(research['characters']),focused_findings=len(research['findings']),historical_candidates=214,local_candidates=3916,evidence_references_checked=refs,pending_inputs=[],unadjudicated_candidates=[],frozen_volume08_unchanged=all(sha(B/'vol08'/name)==digest for name,digest in review08['input_sha256'].items()),candidate_semantic_equality=True,research_semantic_equality=True,answered_is_not_all_story_payoffs=True,semantic_review_owned_by_primary=True)
 output('audit-validation.json',validation)
 # 可读页只渲染已签对象，既不重判也不生成新文学事实。
 charrows=read(output_dir/'character-arc-audit-draft.json')['characters']
 lines=['# 无双人物全弧审计（研究草稿）','','本代理亲读卷五/七，其余依据各卷正式研究与必要接口派生；各对象与primary已签分组逐值相等。','']
 for row in charrows:
  lines+=['## '+row['audit_id']+' '+row['name'],'']
  for key,label in [('initial_comparison_stage','起点'),('key_decisions','选择与阶段'),('costs','代价'),('terminal_state','终态'),('evidence_boundaries','来源边界')]:lines += [label+'：'+row[key],'']
  lines+=['证据raw：'+', '.join(e['chapter_id'][3:] for e in row['evidence']),'']
 output_text('character-arc-audit-draft.md','\n'.join(lines))
 findings=read(output_dir/'end-state-audit-draft.json')['findings'];lines=['# 无双全书终点重点审计（研究草稿）','','30项已签重点结论的原对象渲染；unknown/partial保具体限制，不表示未执行后文匹配。','']
 for row in findings:
  lines+=['## '+row['key']+' '+row['title'],'','终点类型：'+row['terminal_status'],'']+[f'- {s}' for s in row['stage_chain']]+['','结论：'+row['conclusion'],'','限制与反证：'+row['limits_and_counterevidence'],'','证据raw：'+', '.join(e['chapter_id'][3:] for e in row['evidence']),'']
 output_text('end-state-audit-draft.md','\n'.join(lines))
 for kind,label in [('historical','历史问题与线程'),('local','本地原子问题')]:
  lines=['# 无双'+label+'终点审计（研究草稿）','','保留原ID、原阶段和原记录；完整原记录在同名JSON。answered包含明确失败、规则解释与记录边界澄清，不等全部人物愿望成功。','']
  for row in pools[kind]['candidates']:
   d=row['terminal_assessment'];lines+=['## '+row['candidate_id']+' '+str(row['title']),'','原卷：'+str(row['volume'])+'；原记录：'+str(row['original_path'])+'；原序号：'+str(row['original_index']),'','终点：'+d['status']+'；审计领域：'+d['audit_domain'],'',d['rationale'],'','后证raw：'+', '.join(f'{n:04}' for n in d['later_chapters']),'']
  output_text(f'{kind}-question-pool.md','\n'.join(lines))
 lines=['# 无双全书审计交接（待最终整体签收）','','四包：115人物弧、30重点、214历史问题/线程、3916本地原子，共4130候选。原图和分卷阶段状态不改；研究仍为用户draft。','','本代理实际全文亲读卷五265正文/266片与卷七210正文/211片。八卷团队已覆盖1599正文/1609原片，不等本代理个人重新阅读全文；额外定向全文与派生接口读取见research-interface-read-log.json。','','组装只复制primary已逐项语义审阅并签SHA的分组；候选三个判断字段及原后证数组/集合逐ID相等，人物/重点对象逐值相等。merge-validation.json记录比对，metadata-enrichment-log.json仅记录来源ID/revision补齐。签批原文未改，第一人称归属保原裁定者。','','原卷八六核心已按review-vol08.json逐一核原SHA并拷输入快照，没有重生或覆盖卷八。原卷七211notes与原候选误读保历史；raw1305 minutes误读指已存旧正式snapshot，终点评定区分研究纠正与真实规模未知。','','primary后续：实际核冻结四包/可读页与merge-validation，再运行record_primary_whole_book_review.py tianxia-wushuang --reviewed，之后按既有publish_book_audit.py以--audit-subdir audit/whole-book发布并独立验收。本代理不生成primary凭据、不写正式库、不读斩龙。','','[人物弧](character-arc-audit-draft.md) · [重点](end-state-audit-draft.md) · [历史池](historical-question-pool.md) · [原子池](local-question-pool.md) · [验证](audit-validation.json) · [语义比对](merge-validation.json)','']
 output_text('whole-book-audit-handoff.md','先读[核源纠正叠加](priority-corrections-delta.json)：旧notes与旧正式派生的受影响文字以此叠加为解释优先，原件作为历史输入保留；不回写冻结分卷、不改变已签候选/研究结论。\n\n'+'\n'.join(lines))
 lines=['# 无双终点审计结果与边界','','正式分卷输入八卷已齐；本包已完成签组比对，等待primary整体凭据/发布验收。研究不等用户审美批准。','','| 项目 | 数量 |','|---|---:|','| 人物弧 | 115 |','| 重点结论 | 30 |','| 历史候选（含旧resolved） | 214 |','| 本地原子（含漏栏追加1291） | 3916 |',f'| 校验来源引用 | {refs} |','','候选ID和原字段保留，终点评定另层。answered是“该题已有可引用答案”，包含失败、拒绝、规则解释与记录约束；不能把answered总数宣传成全部故事伏笔成功回收。','']
 for kind,label in [('historical','历史池'),('local','原子池')]:
  lines+=['## '+label+'按领域与终点状态','', '| 领域 | answered | partial | unrecovered | unknown |','|---|---:|---:|---:|---:|']
  for domain,counts in pools[kind]['terminal_statistics']['by_audit_domain'].items():lines.append('| '+domain+' | '+' | '.join(str(counts.get(k,0)) for k in ['answered','partial','unrecovered','unknown'])+' |')
  lines.append('')
 lines+=['来源异常、作者明确改字与研究误读纠正分别保留。unknown是全文团队资料匹配后的具体证据限制，不是用通用“无后证”替代审计；每条理由与后证在两池独立可查。','','[完整交接](whole-book-audit-handoff.md) · [来源元数据补齐](metadata-enrichment-log.json) · [原字段与签组语义比对](merge-validation.json)','']
 output_text('whole-book-audit-report.md','先读[核源纠正叠加](priority-corrections-delta.json)：旧notes与旧正式派生的受影响文字以此叠加为解释优先，原件作为历史输入保留；不回写冻结分卷、不改变已签候选/研究结论。\n\n'+'\n'.join(lines))
 # 再调用发布共用校验；不调用发布、不生成primary整书签收。
 sys.path.insert(0,str(B.parent));from book_audit_common import load_package
 load_package(output_dir,source)
 for p in [candidate_progress,research_progress]:require(sha(p)==progress_hashes[p.relative_to(R).as_posix()],'冻结前primary签表变化')
 for name,path in final_outputs.items():(H/name).write_bytes(path.read_bytes())
 names=['character-arc-audit-draft.json','end-state-audit-draft.json','historical-question-pool.json','local-question-pool.json','audit-validation.json','merge-validation.json','metadata-enrichment-log.json','input-inventory.json','audit-method.md','research-interface-read-log.json','character-interface-reading.json','character-arc-audit-draft.md','end-state-audit-draft.md','historical-question-pool.md','local-question-pool.md','whole-book-audit-handoff.md','whole-book-audit-report.md','assemble_signed_batches.py','audit_evidence.py']
 for name in names:frozen_files[name]=sha(H/name)
 for pattern in ['*-delta.json','*-proposal.json']:
  for path in H.glob(pattern):frozen_files[path.relative_to(H).as_posix()]=sha(path)
 for path in (H/'reviewed-batches').glob('*.json'):frozen_files[path.relative_to(H).as_posix()]=sha(path)
 for path in (H/'input-snapshots').rglob('*'):
  if path.is_file():frozen_files[path.relative_to(H).as_posix()]=sha(path)
 manifest=dict(status='draft_frozen_for_final_primary_review_not_user_approval',source_id=source['source_id'],revision=source['revision'],created_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),audit_sha256=frozen_files,formal_input_sha256=inventory['formal_input_sha256'],frozen_volume08_hashes=v8hash,signed_progress_sha256=progress_hashes,counts=validation)
 write(H/'audit-freeze-manifest.json',manifest)
 print(json.dumps(dict(status='assembled_and_frozen_pending_final_primary_review',manifest_sha256=sha(H/'audit-freeze-manifest.json'),**validation),ensure_ascii=False))
if __name__=='__main__':main()
