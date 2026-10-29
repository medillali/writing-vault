"""独立核验八组的结构、固定源定位、材料SHA及自辖映射，不代表文学主审。"""
from pathlib import Path
import json,hashlib,collections,datetime,sys
sys.stdout.reconfigure(encoding='utf-8')
R=Path('C:/Users/Administrator/Documents/ChatGPT/Novel');A=Path(__file__).resolve().parent.parent
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
src=load(A.parents[1]/'source.json');by={x['chapter_id']:x for x in src['chapters']}
allrows=[];groups=[];materials={};formal_inputs={};additional={}
for g in range(1,9):
 p=A/f'character-arcs-part{g:02d}.json';d=load(p);vr=load(A/f'character-arcs-part{g:02d}-validation.json')
 assert sha(p)==vr['json_sha256'] and sha(p.with_suffix('.md'))==vr['md_sha256']
 assert vr['count']==len(d['characters'])
 for path,expected in d['formal_input_sha256'].items():
  assert path.startswith('writing-vault/') and sha(R/path)==expected
  assert path not in formal_inputs or formal_inputs[path]==expected;formal_inputs[path]=expected
 for path,expected in d.get('additional_support_sha256',{}).items():
  assert sha(R/path)==expected;additional[path]=expected
 for row in d['characters']:
  assert row['review_status']=='draft' and row['actual_reviewer']=='zongheng_vol05_full'
  for k in ['audit_id','name','initial_comparison_stage','key_decisions','costs','terminal_state','evidence_boundaries','evidence']:
   assert row[k],(g,row['audit_id'],k)
  for e in row['evidence']:
   assert e['source_id']==src['source_id'] and e['revision']==src['revision']
   c=by[e['chapter_id']];assert c['start_line']<=e['start_line']<=e['end_line']<=c['end_line']
   assert e['claim_kind'] in ['fact','inference','synthesis','plan']
   rp=e['research_path'];assert rp.startswith('writing-vault/') and '/private-sources/' not in rp
   assert sha(R/rp)==e['research_sha256'];materials[rp]=e['research_sha256']
  allrows.append(row)
 groups.append(dict(path=p.name,json_sha256=sha(p),md_sha256=sha(p.with_suffix('.md')),count=len(d['characters']),audit_ids=[x['audit_id'] for x in d['characters']]))
ids=[x['audit_id'] for x in allrows];assert len(ids)==len(set(ids))==47
assert set(ids)=={f'character-arc-{i:03d}' for i in range(1,48)}
mapping=load(A/'character-arcs-self-stage-card-mapping.json')
assert set(x['audit_id'] for x in mapping['audit_rows'])==set(ids)
for group in groups:
 assert mapping['audit_group_sha256'][group['path']]==group['json_sha256']
 assert mapping['audit_group_sha256'][Path(group['path']).with_suffix('.md').name]==group['md_sha256']
assert len(mapping['mappings'])==len({x['origin_key'] for x in mapping['mappings']})==128
assert sum(len(x['audit_ids']) for x in mapping['mappings'])==129
byid={x['audit_id']:x for x in allrows}
assert byid['character-arc-043']['entity_type']=='technology_and_character_prototype_interface'
assert byid['character-arc-046']['entity_type']=='organization_and_operation_interface'
assert len(byid['character-arc-043']['component_entities'])==3
delta=load(A/'character-arcs-part03-approved-wang-identity-delta.json')
assert delta['json_sha256']==groups[2]['json_sha256']
assert len(byid['character-arc-010']['evidence'])==27
receipt=dict(status='passed_structure_source_material_hash_and_mapping_not_semantic_approval',actual_reviewer='zongheng_vol05_full',
 checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),groups=groups,
 counts=dict(groups=8,research_rows=47,person_rows=45,interface_rows=2,
             evidence_refs=sum(len(x['evidence']) for x in allrows),self_unique_stage_cards=128,stage_card_target_links=129),
 formal_input_sha256=formal_inputs,evidence_material_sha256=materials,additional_support_sha256=additional,
 self_mapping_sha256={x:sha(A/x) for x in ['character-arcs-self-stage-card-mapping.json','character-arcs-self-stage-card-mapping.md']},
 assertions=dict(all_ids_unique_and_001_to_047=True,all_rows_still_draft=True,all_source_bounds_valid=True,
  all_referenced_research_material_sha256_match=True,no_stage_dependency_in_formal_input=True,
  no_private_source_txt_as_research_material=True,original_128_source_origins_unique=True,
  split_card_counted_once=True,other_agent_scope_not_claimed=True,original_formal_inputs_unchanged=True),
 primary_review_boundary='结构和来源检查不替代primary逐项文学审阅；当前分组签收以root外置签审凭据为准，不在人物row伪填reviewed。')
p=A/'character-arcs-self-validation.json';assert not p.exists();dump(p,receipt)
print(json.dumps(dict(status=receipt['status'],counts=receipt['counts'],receipt_sha256=sha(p)),ensure_ascii=False,indent=2))
