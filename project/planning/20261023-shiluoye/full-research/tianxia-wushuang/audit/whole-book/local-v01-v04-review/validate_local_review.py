"""只读核923项独立裁定，生成本目录回执，不合并主池。"""
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
here=Path(__file__).resolve().parent
root=here.parents[6]
book=here.parents[2]
sha=lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
assigned=read(here/'assigned-candidates.json')
assigned_by_id={r['candidate_id']:r for r in assigned}
assert len(assigned)==len(assigned_by_id)==923
pool_path=here.parent/'local-question-pool.json'
pool=read(pool_path)
if isinstance(pool,dict):
    pool=next(pool[k] for k in ('candidates','items','questions') if k in pool)
pool_by_id={r['candidate_id']:r for r in pool}
source=read(book/'source.json')
chapters={r['chapter_id']:r for r in source['chapters']}
source_path=Path(source['normalized_path'])
assert sha(source_path)==source['revision']
original_keys=[k for k in assigned[0] if k!='terminal_assessment']
files=sorted(here.glob('adjudications-local-v*.json'))
rows=[]
batches=[]
refs=0
for f in files:
    batch=read(f)
    assert isinstance(batch,list),f
    md=f.with_suffix('.md')
    assert md.exists(),md
    batches.append({'path':f.name,'markdown_path':md.name,'count':len(batch),'by_status':dict(Counter(r['status'] for r in batch)),'sha256':sha(f),'markdown_sha256':sha(md)})
    for r in batch:
        cid=r['candidate_id']
        assert cid in assigned_by_id,cid
        original=assigned_by_id[cid]
        assert cid in pool_by_id,cid
        for key,value in original.items():
            if key=='terminal_assessment':
                continue
            assert r.get(key)==value,(cid,'output changed original',key)
            assert pool_by_id[cid].get(key)==value,(cid,'pool changed original',key)
        assert r['status'] in ('answered','partial','unrecovered','unknown'),cid
        assert r['audit_domain'] and r['rationale'].strip(),cid
        assert r['review_status']=='draft_for_primary_review',cid
        assert all(type(ch) is int and 1<=ch<=1609 for ch in r['later_chapters']),cid
        assert len(r['later_chapters'])==len(set(r['later_chapters'])),cid
        later_cids={e['chapter_id'] for e in r['later_evidence']}
        assert all(f'ch-{c:04d}' in later_cids for c in r['later_chapters']),cid
        for e in r['original_evidence']+r['later_evidence']:
            assert e['source_id']==source['source_id'] and e['revision']==source['revision'],(cid,e)
            bounds=chapters[e['chapter_id']]
            assert bounds['start_line']<=e['start_line']<=e['end_line']<=bounds['end_line'],(cid,e,bounds)
            assert e['claim_kind'] in ('fact','inference','synthesis','plan'),(cid,e)
            if e.get('research_path'):
                assert (root/e['research_path'].split('#',1)[0]).is_file(),(cid,e['research_path'])
            refs+=1
    rows.extend(batch)
ids=[r['candidate_id'] for r in rows]
assert len(ids)==len(set(ids))==923
assert set(ids)==set(assigned_by_id)
log=read(here/'input-read-log.json')
covered={v:set() for v in (1,2,3,4)}
for entry in log['candidate_record_reads']:
    v=int(entry['volume'])
    covered[v].update(range(entry['offset'],entry['offset']+entry['count']))
for v,n in ((1,27),(2,493),(3,22),(4,381)):
    assert covered[v]==set(range(1,n+1)),(v,len(covered[v]))
    assert sum(r['volume']==v for r in rows)==n
interfaces=[]
for item in log['interfaces']:
    p=root/item['path']
    assert sha(p)==item['sha256'],('interface changed',item['path'])
    interfaces.append(item)
notes_by_path={}
for item in log.get('complete_derived_notes_read',[]):
    p=root/item['path']
    if p not in notes_by_path:
        notes_by_path[p]={}
        for line in p.read_text(encoding='utf-8-sig').splitlines():
            n=json.loads(line)
            notes_by_path[p][n['chapter_id']]=sha_value=hashlib.sha256(line.encode('utf-8')).hexdigest()
    assert notes_by_path[p][item['chapter_id']]==item['record_sha256'],('note changed',item['chapter_id'])
result={'status':'passed','scope':'923 original stable local candidates, volumes 1—4; structural/provenance validation only','candidate_count':len(rows),'by_volume':dict(Counter(r['volume'] for r in rows)),'by_status':dict(Counter(r['status'] for r in rows)),'batch_count':len(batches),'evidence_refs_with_repeats':refs,'all_ids_exactly_once':True,'all_original_fields_preserved':True,'all_assigned_pool_originals_unchanged':True,'original_source_sha256':sha(source_path),'assigned_snapshot_sha256':sha(here/'assigned-candidates.json'),'pool_sha256_current':sha(pool_path),'input_read_log_sha256':sha(here/'input-read-log.json'),'complete_derived_notes_read':len(log.get('complete_derived_notes_read',[])),'interfaces_unchanged':interfaces,'primary_review_status':'以root独立逐项审阅与primary-audit-review-progress为准；本脚本不伪填文学审阅。','reader_attribution':'本人原亲读卷四、卷六raw1059—1233；本次卷一至三及其他卷后证按派生notes/正式交接读取。专项全文复读仅另列653/694/719，未冒一人全书重读。','current_audit_original_rereads':[{'raw_chapter':653,'start_line':55558,'end_line':55609},{'raw_chapter':694,'start_line':58439,'end_line':58511},{'raw_chapter':719,'start_line':60243,'end_line':60312}],'batches':batches}
(here/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
lines=['# 无双本地卷一至四923项独立终点评定交接','','923项稳定ID全部覆盖且逐项裁定，不改主池、分卷、正式库；agent4为唯一组装人。全部JSON保待主审状态，root语义审阅回执独立保管。','','- 分卷数：卷1 27、卷2 493、卷3 22、卷4 381。','- 状态数：'+json.dumps(result['by_status'],ensure_ascii=False)+'。','- answered包含已落实的身份/数值/来源记录约束，不可全称剧情伏笔已回收。','- 校验passed：923 ID恰一次、原记录字段保留、证据章行/来源revision有效、派生输入与读取日志SHA一致。结构通过不等语义结论自动正确。','- 阅读归属：本人原亲读卷四、卷六前175片；1—3正式接口与后卷notes按原读者归属。此次额外全文复读653/694/719；未称重读全书。','- 定向修订：037-02补935暗月正式10级但796仍9；047-02删除无证北冥/鬼谷血缘断言；issue030-01与170-02补860新版20码神泣实际可用，旧全屏删号形式与后改版分层。before/delta文件均保留。','- 下一授权：独占旧卷六657稳定本地候选，另目录输出，不碰历史v6域。','','详见[validation.json](validation.json)与[input-read-log.json](input-read-log.json)。','', '| 文件 | 项数 | JSON SHA256 |','|---|---:|---|']
for b in batches:
    lines.append(f"| [{b['path']}]({b['path']}) / [MD]({b['markdown_path']}) | {b['count']} | {b['sha256']} |")
(here/'handoff.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps({k:result[k] for k in ('status','candidate_count','by_volume','by_status','batch_count','evidence_refs_with_repeats','complete_derived_notes_read')},ensure_ascii=False))
print(json.dumps({'validation_sha256':sha(here/'validation.json'),'handoff_sha256':sha(here/'handoff.md')},ensure_ascii=False))
