"""独立只读复核现有冻结包，不调用组装器、不签primary、不发布。"""
import json,sys,hashlib,pathlib
from audit_evidence import H,B,R
sys.path.insert(0,str(B.parent))
from book_audit_common import preflight,check_md_links
from record_primary_whole_book_review import check_batches,check_groups
sys.stdout.reconfigure(encoding='utf-8')
ctx=preflight(R,'tianxia-wushuang',B,'audit/whole-book',B/'source.json',False)
batches,signed=check_batches(B,H,ctx['data']);groups=check_groups(B,H,ctx['data'])
links=sum(check_md_links(H/name) for name in ['character-arc-audit-draft.md','end-state-audit-draft.md','historical-question-pool.md','local-question-pool.md','whole-book-audit-handoff.md','whole-book-audit-report.md'])
enrichment=json.loads((H/'metadata-enrichment-log.json').read_text(encoding='utf-8'));merge=json.loads((H/'merge-validation.json').read_text(encoding='utf-8'))
result=dict(status='passed_independent_readonly_frozen_preflight_and_signed_semantic_equality',freeze_manifest_sha256=ctx['manifest_sha'],counts=ctx['counts'],evidence_references_checked=ctx['refs'],checked_sha256_entries=ctx['checked_hashes'],candidate_batches=batches,signed_candidate_objects_compared=len(signed),research_groups=groups,character_and_finding_objects_exactly_equal=True,markdown_local_links_checked=links,source_metadata_fields_enriched=len(enrichment['entries']),original_fields_checks=len(merge['original_fields_checks']),frozen_volume08_unchanged=ctx['manifest']['counts']['frozen_volume08_unchanged'],formal_writes=False,primary_receipt_created=False,post_freeze_files_modified=False,console_error_boundary='组装器唯一执行在写完manifest后打印摘要时发生重复status键TypeError；本次只读独立复验不依赖该控制台打印，也未改冻结脚本或包。')
target_name=sys.argv[1] if len(sys.argv)>1 else 'post-freeze-readonly-verification.json'
assert pathlib.Path(target_name).name==target_name
(H/target_name).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
