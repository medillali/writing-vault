"""独立核验最终派生包的结构、上游SHA和证据定位；无正式库写入。"""
import json,hashlib,sys,re
from pathlib import Path
from datetime import datetime,timezone
sys.stdout.reconfigure(encoding='utf-8');P=Path(__file__).parent;B=P.parent;ROOT=P.parents[4]
R=lambda p:json.loads(p.read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
S=R(B/'source.json');A=R(B/'book-synthesis-draft.json');C={c['chapter_id']:c for c in S['chapters']}
assert A['source_id']==S['source_id'] and A['revision']==S['revision']
assert A['review_status']=='draft' and A['claim_kind']=='synthesis'
assert not A['scope']['personal_complete_book_read'] and A['scope']['new_fulltext_reads_by_this_synthesis']==0
assert A['user_evaluation'] is None and A['user_taste'] is None and A['original_project_settings'] is None
assert len(A['dimensions'])==9 and all(len(rows)==4 for rows in A['dimensions'].values())
rows=[x for xs in A['dimensions'].values() for x in xs];assert len(rows)==len({r['id'] for r in rows})==36
checked=0;upstreams={};documents=0;volume_refs=set();support_count=0
for group in A['upstream_documents']:
 for doc in group['documents']:
  assert not Path(doc['path']).is_absolute() and not re.match(r'^[A-Za-z]:',doc['path'])
  p=ROOT/doc['path'];assert doc['exists'] and p.is_file() and sha(p)==doc['sha256'],doc
  documents+=1
  if doc['kind']=='analysis':upstreams[group['volume']]=(R(p),doc)
assert set(upstreams)==set(range(1,9))
for row in rows:
 assert row['claim_kind']=='synthesis' and row['review_status']=='draft'
 assert all(row[k] for k in ['claim','fact_summary','mechanism','limits_and_counterevidence','originality_transform','late_stage_result','supporting_observations','evidence'])
 assert len({b['volume'] for b in row['supporting_observations']})>=3
 assert any(b['volume']>=6 for b in row['supporting_observations'])
 assert '等交接/冻结' not in row['late_stage_result'] and '仍待读取' not in row['late_stage_result']
 for basis in row['supporting_observations']:
  v=basis['volume'];volume_refs.add(v);support_count+=1;up,doc=upstreams[v]
  original=up['dimensions'][basis['dimension']][basis['index_zero_based']]
  fact=original['fact'].get('text',original['fact']) if isinstance(original['fact'],dict) else original['fact']
  assert basis['reported_observation']==fact and basis['material_path']==doc['path'] and basis['material_sha256']==doc['sha256']
 for e in row['evidence']:
  assert e['source_id']==S['source_id'] and e['revision']==S['revision'] and e['claim_kind'] in ['fact','inference','synthesis','plan']
  c=C[e['chapter_id']];assert c['start_line']<=e['start_line']<=e['end_line']<=c['end_line']
  assert e['research_material_attribution'] and all(x['original_reread_by_this_synthesis'] is False for x in e['research_material_attribution'])
  checked+=1
assert volume_refs==set(range(1,9)) and checked==A['validation']['inherited_evidence_references_checked']
assert sum(x['raw_segments'] for x in A['upstream_reader_attribution'])==1609
md=(B/'book-synthesis-draft.md').read_text(encoding='utf-8');assert len(md)>10000 and md.count('### ')==36
result=dict(status='passed-final-derived-draft-local-checks',source_id=S['source_id'],revision=S['revision'],observations=36,dimensions=9,referenced_volumes=sorted(volume_refs),upstream_documents_verified=documents,supporting_observations_checked=support_count,inherited_evidence_references_checked=checked,reading_attribution_raw_segments=1609,body_units=1599,personal_complete_book_read=False,new_original_fulltext_read_by_synthesis=0,formal_library_modified=False,primary_review_forged=False,outputs={n:dict(path=(B/n).relative_to(ROOT).as_posix(),sha256=sha(B/n)) for n in ['book-synthesis-draft.json','book-synthesis-draft.md']},checked_at=datetime.now(timezone.utc).isoformat(),limits='引用定位/输入版本/结构校验不代替primary文学语义审阅，更不等用户审美批准。')
(P/'final-preflight.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
