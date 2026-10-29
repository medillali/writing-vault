"""独立读取最终文件核publisher必需结构、组等值、来源与定位；不发布。"""
from synthesis_common import *
from collections import Counter
p=B/'book-synthesis-draft.json';m=p.with_suffix('.md');a=json.loads(p.read_text(encoding='utf-8'));fail=[]
assert a['artifact_type']=='derived-book-synthesis' and a['source_id']==S['source_id'] and a['revision']==S['revision']
assert a['claim_kind']=='synthesis' and a['validation']['observations']==36 and len(a['dimensions'])==9
assert a['scope']['personal_complete_book_read'] is False and a['scope']['new_unique_fulltext_coverage_by_this_synthesis']==0
pr=json.loads((B/'primary-synthesis-dimension-reviews.json').read_text(encoding='utf-8'));rm={x['dimension']:x for x in pr['groups']}
assert len(rm)==9
for d in DIMENSIONS:
 gp=P/f'synthesis-{d}.json';g=json.loads(gp.read_text(encoding='utf-8'));assert a['dimensions'][d]==g['rows'] and sha(gp)==rm[d]['sha256']
 assert len(g['rows'])==4 and all(x['claim_kind']=='synthesis' for x in g['rows'])
 for r in g['rows']:
  assert r['id'] in m.read_text(encoding='utf-8')
  for k in ['claim','fact_summary','mechanism','conditions','limits_and_counterevidence','originality_transform','late_stage_result']:
   assert r[k] in m.read_text(encoding='utf-8'),(r['id'],k)
docs=[]
for g in a['upstream_documents']:
 for d in g['documents']:
  assert d['exists'] and (ROOT/d['path']).is_file() and sha(ROOT/d['path'])==d['sha256'],d['path'];docs.append(d['path'])
assert len(docs)==68
assert all(not d['path'].endswith('-proposal.json') for d in a['current_priority_reading'])
assert len(a['current_priority_reading'])==8
def walk(x):
 if isinstance(x,dict):
  if all(k in x for k in ['source_id','revision','chapter_id','start_line','end_line']):yield x
  for v in x.values():yield from walk(v)
 elif isinstance(x,list):
  for v in x:yield from walk(v)
refs=list(walk(a['dimensions']))
for e in refs:
 c=CH[int(e['chapter_id'][3:])];assert e['source_id']==S['source_id'] and e['revision']==S['revision'] and c['start_line']<=e['start_line']<=e['end_line']<=c['end_line']
 assert e['claim_kind'] in ['fact','inference','synthesis','plan']
v=json.loads((F/'audit/full-reading-validation.json').read_text(encoding='utf-8'));assert v['status']=='passed' and v['body_units']==1378 and v['indexed_segments']==1386
for name,digest in v['formal_input_sha256'].items():assert sha(F/name)==digest,name
assert b'\r\r\n' not in m.read_bytes()
assert len(a['stable_dimension_groups'])==9 and sum(len(x) for x in a['dimensions'].values())==36
topfacts=''.join(r['fact_summary'] for rs in a['dimensions'].values() for r in rs)
for bad in ['百炼铁','秦王救援','压制矿夫','亲自选择杀降','不救盛林']:assert bad not in topfacts,bad
result={'status':'passed-structure-provenance-and-exact-aggregation','reviewer':'/root/zongheng_vol03_full','not_primary_acceptance':True,'json_sha256':sha(p),'md_sha256':sha(m),'dimensions':9,'observations':36,'upstream_documents_verified':68,'current_approved_priority_layers':8,'archived_proposals_not_current':3,'source_refs_verified':len(refs),'exact_primary_reviewed_groups':9,'all_36_objects_equal_to_stable_groups':True,'formal_coverage_validation_sha256':sha(F/'audit/full-reading-validation.json'),'scope':a['scope'],'new_fulltext_rereads':6,'new_unique_coverage':0,'limits':'本回执不是primary最终收据、正式发布或用户审美批准；未写正式库/六卷/候选池/primary收据。'}
dump(P/'synthesis-independent-preflight.json',result);print(json.dumps(result,ensure_ascii=False))
