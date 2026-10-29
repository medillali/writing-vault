"""按primary实际批准应用两项；先保存旧回执，禁止重跑覆盖旧历史。"""
from pathlib import Path
from copy import deepcopy
from datetime import datetime,timezone
import hashlib
import json
import subprocess
import sys
sys.stdout.reconfigure(encoding='utf-8')
assert sys.argv[1:]==['--approved'], '仅用于primary已批准的这两项'
HERE=Path(__file__).resolve().parent
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,obj): p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
proposal_path=HERE/'same-name-identity-correction-proposal.json'
assert sha(proposal_path)=='91e893ce09b500c851396fbb8ff2548bb2892adc5300eedd60a2991bc4065e33'
proposal=read(proposal_path)
assert proposal['status']=='proposal_only_not_applied_pending_primary_approval'
old_hashes={p.name:sha(p) for p in HERE.glob('adjudications-local-v06-part*.json')}
assert len(old_hashes)==11
for name,h in proposal['frozen_input_sha256'].items(): assert old_hashes[name]==h
old_input_log_sha=sha(HERE/'input-read-log.json')
archive=HERE/'same-name-identity-before-apply'
if archive.exists(): raise FileExistsError('已有旧版归档，不可重跑：'+str(archive))
archive.mkdir()
backup_names=['validation.json','handoff.md','validate_local_review.py',
              'same-name-identity-source-check.json','same-name-identity-scan.json',
              'same-name-identity-proposal-validation.json']
for part in [1,8]:
    backup_names += [f'adjudications-local-v06-part{part:02d}.json',f'adjudications-local-v06-part{part:02d}.md',
                     f'spec-v06-part{part:02d}.json',f'decisions-v06-part{part:02d}.json']
backup_manifest={}
for name in backup_names:
    src=HERE/name
    (archive/name).write_bytes(src.read_bytes())
    backup_manifest[name]=sha(src)
write(archive/'manifest.json',dict(status='immutable_pre_approved_revision_snapshot',files=backup_manifest,
    all_11_batch_json_sha256=old_hashes,input_read_log_sha256=old_input_log_sha))

assigned=read(HERE/'assigned-candidates.json')
ordinals={r['candidate_id']:i+1 for i,r in enumerate(assigned)}
changes=[]
for item in proposal['proposals']:
    path=HERE/item['path']
    old=read(path)
    assert len(old)==60
    idx=next(i for i,r in enumerate(old) if r['candidate_id']==item['candidate_id'])
    assert old[idx]==item['before']
    merged=deepcopy(old)
    merged[idx]=deepcopy(item['proposed_after'])
    assert sum(a==b for a,b in zip(old,merged))==59
    changed_fields=[k for k in old[idx] if old[idx][k]!=merged[idx][k]]
    assert set(changed_fields)=={'rationale','later_chapters','later_evidence'}
    for key in ['candidate_id','volume','original_path','original_field','original_index','atomic_index',
                'original_record','title','original_evidence','status','audit_domain','reviewer','review_status']:
        assert old[idx][key]==merged[idx][key]
    write(path,merged)
    decision_name=path.stem.replace('adjudications-local','decisions')
    md=['# 无双本地候选终点评定：'+decision_name,'',
        '本文件为独立待主审裁定；保留原记录，非池主档。chapter号均为raw。其他卷派生输入不冒称原文复读。','']
    for row in merged:
        md.extend(['## '+row['candidate_id'],'','- 原子项：'+row['title'],
                   '- 完整原记录：'+json.dumps(row['original_record'],ensure_ascii=False),
                   '- 终点：'+row['status']+'；领域：'+row['audit_domain'],
                   '- 理由：'+row['rationale'],
                   '- 后证：'+(', '.join(f'{c:04d}' for c in row['later_chapters']) or '无新增回收证；原始证据保留在JSON，未知不等作者遗忘。'),''])
    path.with_suffix('.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
    # 只同步两个人工决策源的同一理由/章列表；不重跑旧finalize，避免覆盖新增直接原文证据。
    number=ordinals[item['candidate_id']]
    for prefix,id_key in [('spec',number),('decisions',item['candidate_id'])]:
        src=HERE/(path.stem.replace('adjudications-local',prefix)+'.json')
        data=read(src); before_src=deepcopy(data)
        position=next(i for i,r in enumerate(data) if r[0]==id_key)
        data[position][3]=merged[idx]['rationale']
        data[position][4]=merged[idx]['later_chapters']
        assert all(a==b for j,(a,b) in enumerate(zip(before_src,data)) if j!=position)
        assert all(before_src[position][j]==data[position][j] for j in range(len(data[position])) if j not in (3,4))
        write(src,data)
    changes.append(dict(candidate_id=item['candidate_id'],path=item['path'],changed_fields=changed_fields,
        before=old[idx],after=merged[idx],unchanged_other_items=59,
        original_fields_preserved=True,status_and_domain_preserved=True,
        before_json_sha256=old_hashes[path.name],after_json_sha256=sha(path),
        after_markdown_sha256=sha(path.with_suffix('.md'))))

modified={c['path'] for c in changes}
assert len(modified)==2
for f,h in old_hashes.items():
    if f not in modified: assert sha(HERE/f)==h
assert sha(HERE/'input-read-log.json')==old_input_log_sha

source_check=read(HERE/'same-name-identity-source-check.json')
source_check.update(revision_status='approved_terminal_correction_applied_pending_new_root_sha_signature',
    applied_candidate_ids=[c['candidate_id'] for c in changes],
    read_attribution_unchanged=True,full_raw_rereads_this_revision=[1098,1209],
    original_frozen_volume_notes_unchanged=True,
    prior_read_receipt='same-name-identity-before-apply/same-name-identity-source-check.json')
write(HERE/'same-name-identity-source-check.json',source_check)
scan=read(HERE/'same-name-identity-scan.json')
scan.update(status='complete_after_approved_two_item_revision',
    input_sha256={p.name:sha(p) for p in HERE.glob('adjudications-local-v06-part*.json')},
    corrected_candidate_ids=[c['candidate_id'] for c in changes],
    remaining_new_correction_candidate_ids=[],
    prior_scan='same-name-identity-before-apply/same-name-identity-scan.json')
for entry in scan['matches']:
    current=next(r for r in read(HERE/entry['file']) if r['candidate_id']==entry['candidate_id'])
    if entry['candidate_id'] in {c['candidate_id'] for c in changes}:
        entry['disposition']='approved-research-misattribution-corrected-original-history-retained'
        for field in entry['matched_fields']:
            if field['field']=='rationale': field['text']=current['rationale']
write(HERE/'same-name-identity-scan.json',scan)

delta=dict(status='applied_after_primary_semantic_approval_pending_root_resign_of_new_sha',
    applied_at_utc=datetime.now(timezone.utc).isoformat(),
    primary_authorization='primary已完整读两项before/proposed_after，批准仅这2项列字段应用；保两批其余各59及全部原字段，要求保存before/merged delta后重签。',
    approved_proposal_sha256=sha(proposal_path),
    error_class='derived-research-entity-misattribution-not-novel-source-anomaly',
    changed_items=changes,unchanged_other_items_per_batch=59,unaffected_other_batch_count=9,
    before_manifest='same-name-identity-before-apply/manifest.json',
    reading_log_unchanged_sha256=old_input_log_sha,
    supplemental_source_check='same-name-identity-source-check.json',
    source_check_sha256=sha(HERE/'same-name-identity-source-check.json'),
    revised_scan='same-name-identity-scan.json',revised_scan_sha256=sha(HERE/'same-name-identity-scan.json'),
    no_new_whole_book_reading_claim=True,
    regeneration_boundary='spec/decisions仅同步这两个理由和章列表；不要重跑旧finalize覆盖两条新增直接原文后证。')
write(HERE/'same-name-identity-merged-delta.json',delta)

validator=HERE/'validate_local_review.py'
code=validator.read_text(encoding='utf-8')
old="'deltas':['part08-sky-return-delta.json','part10-agency-delta.json']"
new="'deltas':['part08-sky-return-delta.json','part10-agency-delta.json','same-name-identity-merged-delta.json']"
assert code.count(old)==1
code=code.replace(old,new)
needle="(here/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\\n',encoding='utf-8')"
insert="""result['post_approval_identity_revision']={'candidate_ids':['v06-local-issue_log-001-01','v06-local-chapter_unresolved_index-151-02'],'status':'semantic-change-approved-new-batch-sha-pending-primary-resign','delta_path':'same-name-identity-merged-delta.json','delta_sha256':sha(here/'same-name-identity-merged-delta.json'),'source_check_sha256':sha(here/'same-name-identity-source-check.json'),'revised_scan_sha256':sha(here/'same-name-identity-scan.json'),'source_raw_chapters_reread':[1098,1209],'original_reading_log_unchanged':True,'error_class':'derived-research-entity-misattribution-not-source-anomaly'}
"""
assert code.count(needle)==1
code=code.replace(needle,insert+needle)
needle2="(here/'handoff.md').write_text('\\n'.join(md)+'\\n',encoding='utf-8')"
insert2="""md.extend(['','## 已批准两项身份研究误配修订','','primary原文复读发现后，已批准仅issue_log-001-01与chapter_unresolved_index-151-02理由/后证字段应用；status/domain及原记录全部保留，两批其余各59逐值不变。旧签回执保存在same-name-identity-before-apply；新批SHA等待primary重签。','1098三同ID均为吻痕，中国165刺所属【谁与争锋】是公会名；1209另有巴西谁与争锋212级锋芒盟主，不能据会名增造中美同名谁。此为派生研究误配纠正，不是小说异常或新伏笔回收。','本轮仅新增1098/1209两原章完整回读；既有175片/primary尾60与282派生笔记归属均不改。','[完整before/merged delta](same-name-identity-merged-delta.json) · [修后657检索](same-name-identity-scan.json) · [原文核验归属](same-name-identity-source-check.json)。不要重跑旧finalize覆盖新增直接原文后证。'])
"""
assert code.count(needle2)==1
code=code.replace(needle2,insert2+needle2)
validator.write_text(code,encoding='utf-8')
subprocess.run([sys.executable,str(validator)],check=True)
assert sha(HERE/'input-read-log.json')==old_input_log_sha
for f,h in old_hashes.items():
    if f not in modified: assert sha(HERE/f)==h
receipt=dict(status='passed_applied_approved_fields_only_pending_primary_resign',
    changed_candidate_count=2,all_original_fields_preserved=True,
    status_domain_unchanged=True,unchanged_other_59_each=True,other_9_batches_unchanged=True,
    input_reading_log_unchanged=True,old_receipts_preserved=True,
    original_volume_and_pool_not_modified=True,
    output_sha256={n:sha(HERE/n) for n in ['adjudications-local-v06-part01.json','adjudications-local-v06-part01.md',
        'adjudications-local-v06-part08.json','adjudications-local-v06-part08.md','same-name-identity-merged-delta.json',
        'same-name-identity-source-check.json','same-name-identity-scan.json','validation.json','handoff.md']})
write(HERE/'same-name-identity-apply-receipt.json',receipt)
print(json.dumps(receipt,ensure_ascii=False,indent=2))
