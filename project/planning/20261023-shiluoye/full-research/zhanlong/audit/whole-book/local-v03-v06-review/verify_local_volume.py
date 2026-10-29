"""只读逐值核验已手写批次并保存独立回执，不改候选池或已签批。"""
from pathlib import Path
import collections,hashlib,json,sys,datetime
sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent;A=H.parent;B=A.parents[1];R=B.parents[3]
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
v=int(sys.argv[1]);manifest=read(H/'input-manifest.json');pool=A/'local-question-pool.json'
assert sha(pool)==manifest['input_sha256'][pool.relative_to(R).as_posix()]
original={x['candidate_id']:x for x in read(pool)['candidates']}
chapters={x['chapter_id']:x for x in read(B/'source.json')['chapters']}
paths=sorted(A.glob(f'adjudications-local-v{v:02d}-batch*.json'));rows=[]
for p in paths:
    part=read(p);assert 0<len(part)<=20
    for item in part:
        old=original[item['candidate_id']]
        for k,value in old.items():
            if k!='terminal_assessment':assert item[k]==value,(item['candidate_id'],k)
        assert item['status'] in ['answered','partial','unrecovered','unknown']
        assert item['actual_reviewer']=='zongheng_vol05_full'
        assert len(item['rationale'])>=35 and item['later_evidence']
        assert item['later_chapters']==list(dict.fromkeys(int(e['chapter_id'][3:]) for e in item['later_evidence']))
        for e in item['later_evidence']:
            c=chapters[e['chapter_id']]
            assert c['start_line']<=e['start_line']<=e['end_line']<=c['end_line']
            assert e['source_id']=='src-20f2d16e3d1b472fa4b230ab0e1770c9'
            assert e['revision']=='61ab0b114c76446fda554abfafdac8c432cd88afaba7c2541f4473a3902134e3'
            assert e['claim_kind'] in ['fact','inference','synthesis','plan']
    rows+=part
expected=manifest['assigned_candidate_ids'][str(v)]
assignment=None
if v==6:
    assignment=read(H/'assignment-update-v06.json')
    owned=assignment['current_owned_slice']
    expected=expected[owned['start_inclusive']:owned['end_exclusive']]
assert [x['candidate_id'] for x in rows]==expected
receipt={'status':'mechanical_checks_passed_pending_primary_semantic_review','volume':v,'actual_reviewer':'zongheng_vol05_full','verified_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'count':len(rows),'batches':len(paths),'counts':dict(collections.Counter(x['status'] for x in rows)),'exact_assigned_id_order':True,'original_fields_preserved':True,'fixed_source_evidence_bounds':True,'pool_unchanged':True,'pool_sha256':sha(pool),'input_manifest_sha256':sha(H/'input-manifest.json'),'batch_sha256':{p.name:sha(p) for p in paths},'limitation':'结构/行号/逐值检查不代替primary语义主审；answered含研究约束，不等所有剧情成功回收。'}
if assignment:
    receipt.update(scope='volume6-local-candidates-0-based-0:200-only',assignment_update_sha256=sha(H/'assignment-update-v06.json'),not_claimed='reader4负责201—399，原卷全文仍按真实原reader，不冒本代理全399终评')
(H/f'volume{v:02d}-aggregate-validation.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(receipt,ensure_ascii=False,indent=2))
