"""最终装配复核；只有实际读完九组后--reviewed才签本书综合。"""
from pathlib import Path
import argparse,datetime,hashlib,json
B=Path(__file__).resolve().parent;R=B.parents[2];S=B/'zhanlong';A=S/'audit/whole-book';P=A/'reader3-review'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=argparse.ArgumentParser();p.add_argument('--reviewed',action='store_true');args=p.parse_args()
draft=S/'book-synthesis-draft.json';md=S/'book-synthesis-draft.md'
assert sha(draft)=='8976827ae6099697dc00d83c58966e8a6d58f2172376e413c6c62f3365d3ce8d'
d=read(draft);ledger=read(S/'primary-synthesis-dimension-reviews.json');source=read(S/'source.json')
assert ledger['reviewer']=='primary' and len(ledger['groups'])==9
assert d['source_id']==source['source_id'] and d['revision']==source['revision']
assert d['user_evaluation'] is d['user_taste'] is d['original_project_settings'] is None
assert len(d['dimensions'])==9 and sum(map(len,d['dimensions'].values()))==36
text=md.read_text(encoding='utf-8'); group_pins={}
for g in ledger['groups']:
    f=A/g['path'];assert sha(f)==g['sha256'];rows=read(f)['rows']
    assert rows==d['dimensions'][g['dimension']] and [r['id'] for r in rows]==g['reviewed_ids']
    group_pins[g['path']]=g['sha256']
    for row in rows:
        for k in ['claim','fact_summary','mechanism','conditions','limits_and_counterevidence','originality_transform','late_stage_result']:
            assert row[k] in text,(row['id'],k)
        for o in row['supporting_observations']:
            f=R/o['material_path'];assert sha(f)==o['material_sha256'];up=read(f)
            for key in o['json_pointer'].strip('/').split('/'):up=up[int(key)] if isinstance(up,list) else up[key]
            # reported_fact/interpretation为已主审的压缩转述，不冒充上游逐字引文。
            assert up['id']==o['observation_id'] and isinstance(o['reported_fact'],str) and isinstance(o['reported_interpretation'],str)
            if 'reported_fact_boundary' in o:assert o['reported_fact_boundary']['text'] in text
dependencies=0
for group in d['upstream_documents']:
    for doc in group['documents']:
        if doc['exists']:assert sha(R/doc['path'])==doc['sha256'];dependencies+=1
chapters={c['chapter_id']:c for c in source['chapters']};refs=0
def check_refs(x):
    global refs
    if isinstance(x,dict):
        if {'source_id','revision','chapter_id','start_line','end_line'}<=x.keys():
            c=chapters[x['chapter_id']];assert x['source_id']==source['source_id'] and x['revision']==source['revision'] and c['start_line']<=x['start_line']<=x['end_line']<=c['end_line'];refs+=1
        for v in x.values():check_refs(v)
    elif isinstance(x,list):
        for v in x:check_refs(v)
check_refs(d['dimensions'])
assert d['scope']['project_body_units_with_fulltext_records']==1378 and d['scope']['project_indexed_segments_with_fulltext_records']==1386
receipt=dict(status='aggregate-exactly-matches-nine-actually-reviewed-groups',observations=36,dependencies_checked=dependencies,nested_evidence_references_checked=refs,semantic_reading_created_by_validation=False)
if args.reviewed:
    dest=S/'primary-synthesis-review.json';assert not dest.exists()
    old='待主审/未获用户审美批准';new='主代理已审/用户待审';assert text.count(old)==36
    before=P/'synthesis-aggregate-before-primary-status.md';assert not before.exists();before.write_bytes(md.read_bytes())
    md.write_bytes(md.read_bytes().replace(old.encode(),new.encode()))
    write(P/'synthesis-aggregate-primary-status-delta.json',dict(before_sha256=sha(before),after_sha256=sha(md),replacements=36,before=old,after=new,literary_text_unchanged=True))
    receipt.update(status='reviewed_for_library_import',reviewer='primary',source_id=source['source_id'],revision=source['revision'],user_approval=False,reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),input_sha256={draft.name:sha(draft),md.name:sha(md)},signed_dimension_groups=group_pins,dimension_review_ledger_sha256=sha(S/'primary-synthesis-dimension-reviews.json'),verified_corrections=['麒麟铁材料名','降俘退让与矿工未改善的责任层次','现实秦蒙分对象','求援令与实际持刀分开','狮盾期间实用与最终保有分开'],limits='各维36条及继承事实解释由主代理实际逐项阅读；团队全文覆盖归原读者，不冒主代理一人全书重读；人物全弧和整书终审另验，用户审美与原创正典未写入。')
    write(dest,receipt)
print(json.dumps(receipt,ensure_ascii=False))
