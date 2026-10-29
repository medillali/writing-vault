"""primary授权的一次受控支持文件补齐，不调用组装器，不改四包或签组。"""
import json,hashlib,copy
from audit_evidence import H,R
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
mp=H/'audit-freeze-manifest.json';before=mp.read_bytes();manifest=json.loads(before);before_manifest_sha=sha(mp)
assert before_manifest_sha=='1aedb7337b1288ac0a743e72683780ae2ddaecc80177cd9fb4867e6797c5f892'
core_names=['character-arc-audit-draft.json','end-state-audit-draft.json','historical-question-pool.json','local-question-pool.json']
core_hashes={name:sha(H/name) for name in core_names}
assert all(manifest['audit_sha256'][name]==digest for name,digest in core_hashes.items())
signed_paths=[]
for filename,field in [('primary-audit-review-progress.json','batches'),('primary-research-group-review-progress.json','groups')]:
 p=H.parents[1]/filename;x=json.loads(p.read_text(encoding='utf-8'))
 for g in x[field]:assert sha(H/g['path'])==g['sha256'];signed_paths.append((g['path'],g['sha256']))
archive=H/'reviewed-batches';archive.mkdir(exist_ok=True)
old_manifest=archive/'audit-freeze-manifest-before-support-path-amendment.json';assert not old_manifest.exists();old_manifest.write_bytes(before)
pp=H/'priority-corrections-delta.json';old_priority=archive/'priority-corrections-before-support-path-amendment.json';assert not old_priority.exists();old_priority.write_bytes(pp.read_bytes());overlay=json.loads(pp.read_text(encoding='utf-8'));old_pointer=overlay['impact_scan'];assert old_pointer=='note-1117-impact-scan.json'
overlay['impact_scan']='local-v06-review/note-1117-impact-scan.json';dump(pp,overlay)
supports=['local-v06-review/note-1117-mother-attribution-overlay-proposal.json','local-v06-review/note-1117-mother-attribution-overlay-proposal.md','local-v06-review/note-1117-impact-scan.json','local-v06-review/note-1117-overlay-proposal-validation.json']
support_hashes={name:sha(H/name) for name in supports}
assert support_hashes[supports[0]]==overlay['primary_approval']['proposal_sha']
targets_unchanged={target['path']:sha(R/target['path'])==target['sha256_before'] for target in overlay['targets']};assert all(targets_unchanged.values())
amendment=dict(status='controlled_packaging_reference_amendment_pending_final_primary_receipt',authorization='root明确批准修priority impact_scan相对路径、冻结四份实际支持材料，保当前manifest为before，不重跑assembler，四包/全部签组不变。',before_manifest_sha256=before_manifest_sha,before_manifest_snapshot=old_manifest.relative_to(H).as_posix(),pointer_correction=dict(path='priority-corrections-delta.json',field='impact_scan',before=old_pointer,after=overlay['impact_scan'],before_sha256=sha(old_priority),after_sha256=sha(pp),semantic_correction_content_unchanged=True),support_files_added=support_hashes,unchanged_four_package_sha256=core_hashes,unchanged_signed_files_count=len(signed_paths),unchanged_original_note_copies=targets_unchanged,assembler_not_rerun=True,console_summary_bug='旧唯一组装在写完清单后打印重复status键出错；独立只读验证已过，冻结assembler不修改。')
ap=H/'freeze-support-path-amendment.json';assert not ap.exists();dump(ap,amendment)
doc=H/'freeze-support-path-amendment.md';doc.write_text('# 冻结清单支持引用受控补齐\n\n原draft清单保留为reviewed-batches/audit-freeze-manifest-before-support-path-amendment.json。只把priority overlay的impact_scan改为local-v06-review/note-1117-impact-scan.json，并将提案JSON/MD、impact-scan、proposal-validation四份实际支持材料纳入冻结。四包与77候选批、11研究组SHA全部保持。原四份notes副本不改。\n\n[完整变更记录](freeze-support-path-amendment.json) · [读者优先纠正](priority-corrections-delta.json)\n',encoding='utf-8')
after=copy.deepcopy(manifest);after['audit_sha256']['priority-corrections-delta.json']=sha(pp);after['audit_sha256'].update(support_hashes)
for p in [old_manifest,old_priority,ap,doc]:after['audit_sha256'][p.relative_to(H).as_posix()]=sha(p)
after['amendments']=[dict(record=ap.name,before_manifest_sha256=before_manifest_sha,scope='支持指针/材料打包补齐，无研究语义变化')]
assert all(sha(H/name)==digest for name,digest in core_hashes.items());assert all(sha(H/name)==digest for name,digest in signed_paths)
dump(mp,after)
print(json.dumps(dict(new_manifest_sha256=sha(mp),priority_overlay_sha256=sha(pp),support_files=support_hashes,four_package_sha256=core_hashes,unchanged_signed_files=len(signed_paths),original_note_copies_unchanged=targets_unchanged),ensure_ascii=False))
