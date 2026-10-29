"""首次最终验收输出可自引用；pending占位绝不当成功回执。"""
from pathlib import Path
import json
from validate_final_collection import check
B=Path(__file__).resolve().parent;R=B.parents[2];p=R/'writing-vault/library/reports/collection/full-project-validation.json'
if not p.exists():p.write_text(json.dumps({'status':'pending-actual-final-validation','is_acceptance_receipt':False},ensure_ascii=False)+'\n',encoding='utf-8')
result=check(R,True)
print(json.dumps({k:result[k] for k in ['status','vault','reading_unit_segments_exactly_once','checkpoint_partitions_verified','reachable_local_links_checked','backup_candidate_files','backup_candidate_bytes','elapsed_seconds']},ensure_ascii=False),flush=True)
