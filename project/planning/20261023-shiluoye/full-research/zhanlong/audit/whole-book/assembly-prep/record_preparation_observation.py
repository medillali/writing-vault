"""只记录本目录测试/只读观察与依赖SHA；不冻结四包或生成primary凭据。"""
import datetime,hashlib,json,pathlib,subprocess,sys
sys.stdout.reconfigure(encoding='utf-8');P=pathlib.Path(__file__).resolve().parent;A=P.parent;B=A.parents[1];BASE=B.parent;ROOT=BASE.parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v):p.write_bytes((json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
protected=[A/n for n in ('historical-question-pool.json','local-question-pool.json','character-arc-audit-draft.json','end-state-audit-draft.json','audit-freeze-manifest.json')]+[B/'primary-whole-book-review.json']
before={str(p.relative_to(ROOT)).replace('\\','/'):sha(p) if p.is_file() else None for p in protected}
test_cmd=[sys.executable,'-m','unittest','discover','-s',str(P),'-p','test_assemble_zhanlong_signed_audit.py'];t=subprocess.run(test_cmd,capture_output=True,text=True,encoding='utf-8',errors='replace');assert t.returncode==0,t.stderr
dry_cmd=[sys.executable,str(P/'assemble_zhanlong_signed_audit.py')];d=subprocess.run(dry_cmd,capture_output=True,text=True,encoding='utf-8');assert d.returncode==0,d.stderr;dry=json.loads(d.stdout)
after={str(p.relative_to(ROOT)).replace('\\','/'):sha(p) if p.is_file() else None for p in protected};assert before==after
deps={n:sha(BASE/n) for n in ('book_audit_common.py','record_primary_whole_book_review.py','publish_book_audit.py','merge_zhanlong_adjudications.py','record_primary_research_group.py','publish_book_synthesis.py')}
review=json.loads((B/'review-vol06.json').read_text(encoding='utf-8'));last={name:sha(B/'vol06'/name) for name in review['input_sha256']};assert last==review['input_sha256']
v={'status':'preparation-tested-not-frozen-not-published','observed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'test_exit_code':t.returncode,'test_output':t.stdout+t.stderr,'read_only_invocation':dry,'protected_before_sha256':before,'protected_after_sha256':after,'protected_bytes_unchanged':True,'implementation_sha256':sha(P/'assemble_zhanlong_signed_audit.py'),'tests_sha256':sha(P/'test_assemble_zhanlong_signed_audit.py'),'read_existing_interface_sha256':deps,'implementation_dependencies':['Python 3 standard library'],'write_invoked_against_real_package':False,'primary_credentials_generated':False,'raw_body_txt_copied':False}
v['vol06_original_review_inputs_actual_verified']=last;v['legacy_frozen_volume08_actual_volume']=6
write(P/'preparation-validation.json',v)
q=A/'local-v06-tail-review';progress=json.loads((B/'primary-audit-review-progress.json').read_text(encoding='utf-8'));groups={g['path']:g for g in progress['batches']};checks=[]
for i in range(1,11):
 p=q/f'adjudications-local-v06-tail-batch{i:03d}.json';rel=p.relative_to(A).as_posix();g=groups[rel];rows=json.loads(p.read_text(encoding='utf-8'));assert sha(p)==g['sha256'] and [r['candidate_id'] for r in rows]==g['candidate_ids'];checks.append({'path':rel,'sha256':sha(p),'count':len(rows),'matches_actual_primary_signed_group':True})
write(q/'primary-signed-reconciliation.json',{'status':'all-199-already-primary-signed-and-current-bytes-equal','candidate_count':sum(c['count'] for c in checks),'primary_progress_sha256':sha(B/'primary-audit-review-progress.json'),'groups':checks,'semantic_review_performed_by':'primary','semantic_reading_created_by_this_check':False})
print(json.dumps({'script_sha256':v['implementation_sha256'],'test_sha256':v['tests_sha256'],'preparation_validation_sha256':sha(P/'preparation-validation.json'),'dry_run':dry,'tail199_signed_reconciliation_sha256':sha(q/'primary-signed-reconciliation.json')},ensure_ascii=False))
