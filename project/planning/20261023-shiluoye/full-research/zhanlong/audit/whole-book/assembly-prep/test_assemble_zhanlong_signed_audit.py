"""隔离小样只验证组装守卫/字节保全，不生成真实主审或文学结论。"""
import copy, hashlib, importlib.util, json, pathlib, tempfile, unittest

HERE=pathlib.Path(__file__).resolve().parent
SCRIPT=HERE/'assemble_zhanlong_signed_audit.py'
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def digest(b):return hashlib.sha256(b).hexdigest()
def put(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(enc(x));return digest(p.read_bytes())
def module():
 spec=importlib.util.spec_from_file_location('zl_assembly_guard',SCRIPT);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

class Guards(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory(prefix='zl-assembly-guard-');self.root=pathlib.Path(self.temp.name).resolve();self.stage=self.root/'stage/zhanlong';self.audit=self.stage/'audit/whole-book';self.audit.mkdir(parents=True)
  self.source={'source_id':'sid-test','revision':'rev-test','chapters':[{'chapter_id':'ch-0001','start_line':1,'end_line':3}]};put(self.stage/'source.json',self.source)
  self.formal={}
  for v in range(1,7):
   for suffix in ['analysis.json','cards.json','graph.json','chapter-notes.jsonl','handoff.md','.md']:
    name=f'vol{v:02d}'+(suffix if suffix=='.md' else '-'+suffix);p=self.root/'writing-vault/library/reports/zhanlong'/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(('fixture '+name+'\n').encode());self.formal[p.relative_to(self.root).as_posix()]=digest(p.read_bytes())
  self.material=self.root/'stage/zhanlong/evidence.json';self.old=enc({'speaker':'fixture-original-reader','fact':'explicit fixture'});self.material.write_bytes(self.old)
  self.ev={'source_id':'sid-test','revision':'rev-test','chapter_id':'ch-0001','start_line':1,'end_line':3,'claim_kind':'fact','research_path':self.material.relative_to(self.root).as_posix(),'material_sha256':digest(self.old),'source_reader':'original-reader'}
  self.decisions=[]
  for kind in ['historical','local']:
   cid=kind+'-test-1';row={'candidate_id':cid,'status':'partial','audit_domain':'fixture-boundary','rationale':'fixture结论不可改','later_chapters':[1],'later_evidence':[copy.deepcopy(self.ev)],'actual_reviewer':'fixture-reviewer'};self.decisions.append(row)
   final={k:copy.deepcopy(row[k]) for k in ['status','audit_domain','rationale','later_chapters','later_evidence','actual_reviewer']};final.update(review_progress='primary-reviewed-draft',depends_on_volumes=[])
   pool={'source_id':'sid-test','revision':'rev-test','pending_inputs':[],'inputs':[{'open_questions':1,'graph_threads':0}] if kind=='historical' else [],'candidates':[{'candidate_id':cid,'volume':1,'title':'fixture原题','original_field':'chapter_unresolved_index','original_index':0,'original_path':'fixture','original_record':{'untouched':True},'terminal_assessment':final}]};put(self.audit/f'{kind}-question-pool.json',pool)
  batch='signed/batch.json';h=put(self.audit/batch,self.decisions);self.cp={'batches':[{'path':batch,'sha256':h,'candidate_ids':[r['candidate_id'] for r in self.decisions],'count':2}],'distinct_reviewed_candidate_ids':sorted(r['candidate_id'] for r in self.decisions),'distinct_reviewed_candidates':2};put(self.stage/'primary-audit-review-progress.json',self.cp)
  put(self.audit/'adjudication-progress.json',{'status':'merged-exact-primary-reviewed-decisions','original_records_unchanged':True,'exact_evidence_objects_preserved':True,'pool_after_sha256':{k:digest((self.audit/f'{k}-question-pool.json').read_bytes()) for k in ('historical','local')},'primary_progress_sha256':digest((self.stage/'primary-audit-review-progress.json').read_bytes())})
  self.char={'audit_id':'character-arc-1','name':'fixture人','terminal_state':'fixture终态','initial_comparison_stage':'起点','key_decisions':'行动','costs':'代价','evidence_boundaries':'非真实小说判断','evidence':[copy.deepcopy(self.ev)]}
  self.find={'key':'fixture-finding','title':'fixture重点','terminal_status':'partial','stage_chain':['fixture阶段'],'conclusion':'fixture结论','limits_and_counterevidence':'fixture限制','evidence':[copy.deepcopy(self.ev)]}
  groups=[]
  for section,filename,key,rows in [('characters','character-arc-audit-draft.json','audit_id',[self.char]),('findings','end-state-audit-draft.json','key',[self.find])]:
   obj={'source_id':'sid-test','revision':'rev-test','formal_input_sha256':self.formal,section:rows};put(self.audit/filename,obj);path='signed/'+section+'.json';h=put(self.audit/path,obj);groups.append({'path':path,'sha256':h,'section':section,'id_field':key,'reviewed_ids':[r[key] for r in rows],'count':len(rows)})
  put(self.stage/'primary-research-group-review-progress.json',{'groups':groups});put(self.audit/'focused-input-receipt.json',{'formal_input_sha256':self.formal})
  core=self.stage/'vol06/analysis.json';h=put(core,{'unchanged_fixture':True});put(self.stage/'review-vol06.json',{'input_sha256':{'analysis.json':h}})
  synthesis={'validation':{'observations':36},'dimensions':{f'fixture{i}':[{'id':f'fixture-{i}-{j}','claim_kind':'synthesis'} for j in range(4)] for i in range(9)}};j=put(self.stage/'book-synthesis-draft.json',synthesis);md=self.stage/'book-synthesis-draft.md';md.write_bytes(b'fixture synthesis only\n');put(self.stage/'primary-synthesis-review.json',{'reviewer':'primary','status':'reviewed_for_library_import','source_id':'sid-test','user_approval':False,'input_sha256':{'book-synthesis-draft.json':j,'book-synthesis-draft.md':digest(md.read_bytes())}})
 def tearDown(self):self.temp.cleanup()
 def plan(self):return module().prepare(self.root,self.stage,expected_pool_counts={'historical':1,'local':1},expected_findings=1)
 def tree(self):return {str(p.relative_to(self.root)):digest(p.read_bytes()) for p in self.root.rglob('*') if p.is_file()}
 def test_script_exists_before_any_execution(self):self.assertTrue(SCRIPT.is_file(),'先实现默认只读组装器')
 def test_ready_dry_run_does_not_write(self):
  before=self.tree();p=self.plan();self.assertEqual(p['status'],'ready-no-write');self.assertEqual(before,self.tree());self.assertEqual(p['counts']['evidence_references_checked'],4);self.assertNotIn('primary-whole-book-review.json',p['files'])
 def test_missing_signature_rejects(self):
  self.cp['batches'][0]['candidate_ids']=self.cp['batches'][0]['candidate_ids'][:1];self.cp['batches'][0]['count']=1;put(self.stage/'primary-audit-review-progress.json',self.cp)
  with self.assertRaisesRegex(ValueError,'签'):self.plan()
 def test_unmerged_pool_rejects(self):
  p=self.audit/'local-question-pool.json';v=json.loads(p.read_bytes());v['candidates'][0]['terminal_assessment']['review_progress']='pending-manual-adjudication';put(p,v)
  with self.assertRaisesRegex(ValueError,'合并|未完成'):self.plan()
 def test_pool_semantic_change_rejects(self):
  p=self.audit/'local-question-pool.json';v=json.loads(p.read_bytes());v['candidates'][0]['terminal_assessment']['rationale']='漂移';put(p,v)
  with self.assertRaisesRegex(ValueError,'语义|逐值|合并'):self.plan()
 def test_research_final_change_rejects(self):
  p=self.audit/'end-state-audit-draft.json';v=json.loads(p.read_bytes());v['findings'][0]['conclusion']='漂移';put(p,v)
  with self.assertRaisesRegex(ValueError,'研究|逐值'):self.plan()
 def test_signed_bytes_change_rejects(self):
  p=self.audit/'signed/batch.json';p.write_bytes(p.read_bytes()+b'\n')
  with self.assertRaisesRegex(ValueError,'SHA|签'):self.plan()
 def test_historical_material_exact_version_is_packaged(self):
  self.material.write_bytes(b'new live version');archive=self.audit/'history/old-evidence.json';archive.parent.mkdir();archive.write_bytes(self.old);p=self.plan();mapping=p['material_resolution']['entries'];hit=[m for m in mapping if m['original_path']==self.ev['research_path'] and m['material_sha256']==digest(self.old)];self.assertEqual(len(hit),1);self.assertEqual(p['files'][hit[0]['snapshot_path']],self.old);self.assertEqual(json.loads(p['files']['end-state-audit-draft.json'])['findings'][0],self.find)
 def test_missing_exact_material_version_rejects(self):
  self.material.write_bytes(b'new without history')
  with self.assertRaisesRegex(ValueError,'材料|版本'):self.plan()
 def test_formal_history_registry_restores_old_priority_version(self):
  self.material.write_bytes(b'new current priority');h=digest(self.old);archive=self.root/'writing-vault/library/reports/zhanlong/audit/material-history'/f'{h}.json';archive.parent.mkdir(parents=True);archive.write_bytes(self.old);put(archive.parent/'manifest.json',{'materials':[{'original_path':self.ev['research_path'],'original_sha256':h,'archive_path':archive.relative_to(self.root).as_posix(),'archived_sha256':h}]});p=self.plan();hit=[x for x in p['material_resolution']['entries'] if x['original_path']==self.ev['research_path']][0];self.assertEqual(hit['resolution_method'],'formal-material-history-exact-version');self.assertEqual(p['files'][hit['snapshot_path']],self.old)
 def test_synthesis_priority_and_upstream_paths_are_explicit_material_requests(self):
  m=module();v={'priority_corrections':[{'path':'root/priority.json','sha256':'abc','application':'fixture'}],'upstream_documents':[{'documents':[{'path':'root/doc.json','sha256':'def','exists':True}]}]};self.assertEqual(set(m.material_requests(v)),{('root/priority.json','abc'),('root/doc.json','def')})
 def test_formal_pin_drift_rejects_even_if_archived(self):
  p=self.root/next(iter(self.formal));old=p.read_bytes();(self.audit/'old-formal.json').write_bytes(old);p.write_bytes(b'changed')
  with self.assertRaisesRegex(ValueError,'正式'):self.plan()
 def test_historical_input_coverage_mismatch_rejects(self):
  p=self.audit/'historical-question-pool.json';v=json.loads(p.read_bytes());v['inputs'][0]['open_questions']=2;put(p,v)
  with self.assertRaisesRegex(ValueError,'历史|覆盖'):self.plan()
 def test_original_pool_bytes_drift_after_root_merge_rejects(self):
  p=self.audit/'local-question-pool.json';v=json.loads(p.read_bytes());v['candidates'][0]['original_record']['untouched']=False;put(p,v)
  with self.assertRaisesRegex(ValueError,'合并|原记录'):self.plan()
 def test_missing_36_synthesis_primary_review_rejects(self):
  (self.stage/'primary-synthesis-review.json').unlink()
  with self.assertRaisesRegex(ValueError,'综合|synthesis'):self.plan()
 def test_material_path_escape_rejects(self):
  m=module()
  with self.assertRaises(ValueError):m.safe(self.root,'../outside')
 def test_unsubmitted_proposal_body_locator_is_history_not_active_dependency(self):
  name='rejected-evidence-proposal.json';value={'status':'proposal_pending_primary_not_applied','research_path':'writing-vault/private-sources/normalized/raw.txt','research_sha256':'old-locator'};put(self.audit/name,value)
  before=self.tree();p=self.plan();self.assertEqual(before,self.tree());self.assertEqual(p['files'][name],enc(value));self.assertFalse(any(x['original_path'].endswith('raw.txt') for x in p['material_resolution']['entries']))
  log=json.loads(p['files']['historical-body-locators-not-packaged.json']);self.assertEqual(log['entries'][0]['history_path'],name);self.assertTrue(log['history_bytes_preserved'])
 def test_signed_wrapper_body_dependency_still_rejects(self):
  path=self.audit/'signed/characters.json';value=json.loads(path.read_bytes());value['additional_support_sha256']={'writing-vault/private-sources/raw.txt':'forbidden'};put(path,value)
  p=self.stage/'primary-research-group-review-progress.json';progress=json.loads(p.read_bytes());progress['groups'][0]['sha256']=digest(path.read_bytes());put(p,progress)
  with self.assertRaisesRegex(ValueError,'正文TXT'):self.plan()
 def test_preferred_display_does_not_rewrite_historical_name(self):
  value=copy.deepcopy(self.char);value['name']='历史误述';value['display_name']='已核身份';before=copy.deepcopy(value)
  rendered=module().render_section('characters',{'characters':[value]}).decode('utf-8');self.assertIn('## character-arc-1 已核身份',rendered);self.assertNotIn('## character-arc-1 历史误述',rendered);self.assertEqual(value,before)
 def test_active_reference_to_proposal_body_dependency_still_rejects(self):
  linked=self.audit/'approved-proposal.json';h=put(linked,{'research_path':'writing-vault/private-sources/raw.txt','research_sha256':'forbidden'})
  path=self.audit/'signed/characters.json';value=json.loads(path.read_bytes());value['additional_support_sha256']={linked.relative_to(self.root).as_posix():h};put(path,value)
  p=self.stage/'primary-research-group-review-progress.json';progress=json.loads(p.read_bytes());progress['groups'][0]['sha256']=digest(path.read_bytes());put(p,progress)
  with self.assertRaisesRegex(ValueError,'正文TXT'):self.plan()
 def test_markdown_and_code_materials_are_portable_source_archives(self):
  md=self.audit/'linked.md';md.write_bytes(b'[original navigation](old-context.json)\n');py=self.audit/'linked.py';py.write_bytes(b'# archived source only\n')
  path=self.audit/'signed/characters.json';value=json.loads(path.read_bytes());value['additional_support_sha256']={p.relative_to(self.root).as_posix():digest(p.read_bytes()) for p in [md,py]};put(path,value)
  p=self.stage/'primary-research-group-review-progress.json';progress=json.loads(p.read_bytes());progress['groups'][0]['sha256']=digest(path.read_bytes());put(p,progress)
  plan=self.plan();rows={x['original_path']:x for x in plan['material_resolution']['entries']}
  self.assertTrue(rows[md.relative_to(self.root).as_posix()]['snapshot_path'].startswith('provenance/'));self.assertTrue(rows[py.relative_to(self.root).as_posix()]['snapshot_path'].endswith('.bin'))
  for original in [md,py]:self.assertEqual(plan['files'][rows[original.relative_to(self.root).as_posix()]['snapshot_path']],original.read_bytes())
 def test_new_formal_priority_layer_is_snapshotted_without_editing_findings(self):
  layer=self.root/'writing-vault/library/reports/zhanlong/audit/priority-corrections-new.json';put(layer,{'primary_approval':{'status':'approved-for-library-reading-overlay'},'statement':'fixture层'});p=self.plan();self.assertIn('priority-reading-index.json',p['files']);idx=json.loads(p['files']['priority-reading-index.json']);hit=[x for x in idx['layers'] if x['original_path']==layer.relative_to(self.root).as_posix()];self.assertEqual(len(hit),1);self.assertEqual(p['files'][hit[0]['snapshot_path']],layer.read_bytes());self.assertEqual(json.loads(p['files']['end-state-audit-draft.json'])['findings'][0],self.find)
 def test_fixture_commit_is_portable_and_preserves_core(self):
  m=module();p=self.plan();originals={n:(self.audit/n).read_bytes() for n in ['historical-question-pool.json','local-question-pool.json','character-arc-audit-draft.json','end-state-audit-draft.json']};portable=self.root/'portable';m.commit(p,portable)
  for n,b in originals.items():self.assertEqual((portable/n).read_bytes(),b);self.assertEqual((self.audit/n).read_bytes(),b)
  self.assertTrue(m.verify_portable(portable));manifest=json.loads((portable/'audit-freeze-manifest.json').read_bytes());self.assertEqual(manifest['legacy_frozen_volume08_actual_volume'],6);self.assertTrue(manifest['frozen_volume08_hashes']);self.assertFalse((self.stage/'primary-whole-book-review.json').exists())
  self.material.unlink();self.assertTrue(m.validate_material_archive(portable))
 def test_input_change_between_plan_commit_rejects(self):
  m=module();p=self.plan();self.material.write_bytes(b'changed after plan')
  with self.assertRaisesRegex(ValueError,'准备|变化'):m.commit(p,self.root/'portable')
 def test_no_overwrite_existing_manifest(self):
  m=module();p=self.plan();out=self.root/'portable';out.mkdir();(out/'audit-freeze-manifest.json').write_bytes(b'existing')
  with self.assertRaisesRegex(ValueError,'冻结|存在'):m.commit(p,out)

if __name__=='__main__':unittest.main(verbosity=2)
