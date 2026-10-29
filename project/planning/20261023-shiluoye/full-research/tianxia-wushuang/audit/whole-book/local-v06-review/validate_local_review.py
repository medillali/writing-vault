"""只读验证独立卷六657项；只写本目录回执/交接，不合并主池。"""
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
here=Path(__file__).resolve().parent
root=here.parents[6]
book=here.parents[2]
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assigned=read(here/'assigned-candidates.json')
original={r['candidate_id']:r for r in assigned}
assert len(assigned)==len(original)==657
poolpath=here.parent/'local-question-pool.json'
pool=read(poolpath)
if isinstance(pool,dict): pool=next(pool[k] for k in ('candidates','items','questions') if k in pool)
live={r['candidate_id']:r for r in pool if r['volume']==6}
freeze=read(here.parent/'candidate-id-freeze.json')
freezeids=[x for x in freeze['local']['ids'] if x.startswith('v06-local-')]
assert [r['candidate_id'] for r in assigned]==freezeids
assert len(live)==657 and set(live)==set(original)
source=read(book/'source.json')
chapters={r['chapter_id']:r for r in source['chapters']}
sourcepath=Path(source['normalized_path'])
assert sha(sourcepath)==source['revision']
rows=[]
batches=[]
refs=0
for f in sorted(here.glob('adjudications-local-v06-part*.json')):
    batch=read(f)
    md=f.with_suffix('.md')
    assert isinstance(batch,list) and md.is_file()
    batches.append({'path':f.name,'markdown_path':md.name,'count':len(batch),'by_status':dict(Counter(r['status'] for r in batch)),'sha256':sha(f),'markdown_sha256':sha(md)})
    for r in batch:
        cid=r['candidate_id']
        for k,v in original[cid].items():
            if k!='terminal_assessment':
                assert r.get(k)==v,(cid,'output original changed',k)
                assert live[cid].get(k)==v,(cid,'live pool original changed',k)
        assert r['status'] in ('answered','partial','unknown','unrecovered')
        assert r['rationale'].strip() and r['audit_domain']
        assert r['review_status']=='draft_for_primary_review'
        assert all(type(c) is int and 1<=c<=1609 for c in r['later_chapters'])
        assert len(r['later_chapters'])==len(set(r['later_chapters']))
        assert {f'ch-{c:04d}' for c in r['later_chapters']}<={e['chapter_id'] for e in r['later_evidence']}
        for e in r['original_evidence']+r['later_evidence']:
            assert e['source_id']==source['source_id'] and e['revision']==source['revision'],(cid,e)
            ch=chapters[e['chapter_id']]
            assert ch['start_line']<=e['start_line']<=e['end_line']<=ch['end_line'],(cid,e)
            assert e['claim_kind'] in ('fact','inference','synthesis','plan')
            if e.get('research_path'): assert (root/e['research_path'].split('#',1)[0]).is_file()
            refs+=1
        rows.append(r)
assert len(rows)==len({r['candidate_id'] for r in rows})==657
assert [r['candidate_id'] for r in rows]==freezeids
assert len(batches)==11 and all(b['count']==(57 if i==10 else 60) for i,b in enumerate(batches))
log=read(here/'input-read-log.json')
covered=set()
for entry in log['candidate_record_reads']:
    assert entry['volume']==6 and not entry['truncated_pending']
    covered.update(range(entry['offset'],entry['offset']+entry['count']))
assert covered==set(range(1,658))
for interface in log['interfaces']:
    assert sha(root/interface['path'])==interface['sha256'],interface['path']
cache={}
for n in log.get('complete_derived_notes_read',[]):
    p=root/n['path']
    if p not in cache:
        cache[p]={json.loads(line)['chapter_id']:hashlib.sha256(line.encode('utf-8')).hexdigest() for line in p.read_text(encoding='utf-8-sig').splitlines()}
    assert cache[p][n['chapter_id']]==n['record_sha256'],n['chapter_id']
result={'status':'passed','scope':'旧卷六657稳定本地原子项；结构与来源校验，不替代root语义主审','candidate_count':657,'by_status':dict(Counter(r['status'] for r in rows)),'batch_count':11,'evidence_refs_with_repeats':refs,'all_ids_exactly_once':True,'freeze_id_order_matches':True,'all_original_fields_preserved':True,'live_pool_originals_unchanged':True,'complete_candidate_record_reads':657,'truncated_pending':False,'complete_derived_notes_logged':len(log.get('complete_derived_notes_read',[])),'source_sha256':sha(sourcepath),'assigned_snapshot_sha256':sha(here/'assigned-candidates.json'),'assigned_ids_sha256':hashlib.sha256(json.dumps(freezeids,ensure_ascii=False,separators=(',',':')).encode('utf-8')).hexdigest(),'candidate_freeze_sha256':sha(here.parent/'candidate-id-freeze.json'),'pool_sha256_current':sha(poolpath),'input_read_log_sha256':sha(here/'input-read-log.json'),'reader_attribution':log['attribution'],'primary_review_status':'独立由root逐项签，见primary-audit-review-progress；本脚本不伪填已审','batches':batches,'deltas':['part08-sky-return-delta.json','part10-agency-delta.json','same-name-identity-merged-delta.json']}
result['post_approval_identity_revision']={'candidate_ids':['v06-local-issue_log-001-01','v06-local-chapter_unresolved_index-151-02'],'status':'semantic-change-approved-new-batch-sha-pending-primary-resign','delta_path':'same-name-identity-merged-delta.json','delta_sha256':sha(here/'same-name-identity-merged-delta.json'),'source_check_sha256':sha(here/'same-name-identity-source-check.json'),'revised_scan_sha256':sha(here/'same-name-identity-scan.json'),'source_raw_chapters_reread':[1098,1209],'original_reading_log_unchanged':True,'error_class':'derived-research-entity-misattribution-not-source-anomaly'}
(here/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
md=['# 无双旧卷六657项独立终点评定交接','','全部657稳定ID逐项覆盖，共11批（前十各60、末57）。仅本目录独立草稿，不改池主档、分卷或正式库；agent4唯一组装，root逐项语义主审另存。','','- 状态数：'+json.dumps(result['by_status'],ensure_ascii=False)+'。','- answered含身份消歧、来源/数值边界及研究记录约束，不能全部称为剧情伏笔回收。unknown不等作者遗忘。','- 校验passed：657 ID恰一次且顺序匹配freeze、全部原字段保留、章行/revision/链接有效、完整原候选读取无待补截断、已记录派生输入SHA一致。结构通过不证明每条解释自动正确。','- 阅读归属：本人原全文读卷六raw1059—1233共175片，primary原全文读1234—1293共60片；本人原构建时完整读尾60notes，保其原件/归属。此次逐项读657完整原记录与必要派生后证，不冒一人全卷或全书原文重读。','- 补证：0935—38龙鳞复制沿用龙曜番号；1328唐案终监为乱月转报；1571魂归实入古二分盟；1221天空七日期满实际回归；1344十三药实给/1471真用；1295龙战真结、1452米死、1456明死。','- 施为边界：原林浅独立悔意/早由谁发话未独证；当前借体者吞魂背约与艾听转述停攻自刎分别存，不能倒推原王子全部真意。','- NPC群损、具名幸存、1194 87%/1239 80%系统恢复分别存；不得无证全复或永久全灭。','- primary0089原章回读已纠：掉级不卸装可续用，1293继续用青龙盾不是门槛冲突；原尾记录只保历史并附纠正归属。','- 定向delta保留完整before：part08两项补1221回城；part10三项只收窄施为理由，其余57/全部状态证据不动。','', '详见[validation.json](validation.json)、[input-read-log.json](input-read-log.json)。','', '| 文件 | 项数 | JSON SHA256 |','|---|---:|---|']
for b in batches: md.append(f"| [{b['path']}]({b['path']}) / [MD]({b['markdown_path']}) | {b['count']} | {b['sha256']} |")
md.extend(['','## 已批准两项身份研究误配修订','','primary原文复读发现后，已批准仅issue_log-001-01与chapter_unresolved_index-151-02理由/后证字段应用；status/domain及原记录全部保留，两批其余各59逐值不变。旧签回执保存在same-name-identity-before-apply；新批SHA等待primary重签。','1098三同ID均为吻痕，中国165刺所属【谁与争锋】是公会名；1209另有巴西谁与争锋212级锋芒盟主，不能据会名增造中美同名谁。此为派生研究误配纠正，不是小说异常或新伏笔回收。','本轮仅新增1098/1209两原章完整回读；既有175片/primary尾60与282派生笔记归属均不改。','[完整before/merged delta](same-name-identity-merged-delta.json) · [修后657检索](same-name-identity-scan.json) · [原文核验归属](same-name-identity-source-check.json)。不要重跑旧finalize覆盖新增直接原文后证。'])
(here/'handoff.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
print(json.dumps({k:result[k] for k in ('status','candidate_count','by_status','batch_count','evidence_refs_with_repeats','complete_derived_notes_logged')},ensure_ascii=False))
print(json.dumps({'validation_sha256':sha(here/'validation.json'),'handoff_sha256':sha(here/'handoff.md')},ensure_ascii=False))
