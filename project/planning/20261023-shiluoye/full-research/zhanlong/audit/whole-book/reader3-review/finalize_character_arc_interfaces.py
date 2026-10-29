from character_arc_common import *
all_rows=[];files=[];formal={};additional={};slots=[]
for n in range(1,11):
 p=A/f'reader3-character-arcs-part{n:02d}.json';x=json.loads(p.read_text(encoding='utf-8'))
 for rel,digest in x['formal_input_sha256'].items():
  assert rel.startswith('writing-vault/'),rel
  assert sha(ROOT/rel)==digest,(rel,digest,sha(ROOT/rel))
  if rel in formal:assert formal[rel]==digest
  formal[rel]=digest
 for i,r in enumerate(x['characters']):all_rows.append((p,i,r))
 slots+=x.get('unresolved_roster_names',[])
 files.append({'path':str(p.relative_to(ROOT)).replace('\\','/'),'sha256':sha(p),'md_path':str(p.with_suffix('.md').relative_to(ROOT)).replace('\\','/'),'md_sha256':sha(p.with_suffix('.md')),'confirmed_characters':len(x['characters'])})
ids=[r['audit_id'] for _,_,r in all_rows];expected={f'character-arc-r3-{i:03d}' for i in range(1,65)}
assert len(ids)==len(set(ids))==62
assert set(ids)==expected-{'character-arc-r3-046','character-arc-r3-054'}
assert len(slots)==1 and slots[0]['audit_id']=='character-arc-r3-046'
proof=P/'fireli-supplemental-roster-boundary-proposal.json';q=json.loads(proof.read_text(encoding='utf-8'))
dup={'audit_id':'character-arc-r3-054','original_roster_name':scope[53]['name'],'entity_type':'duplicate_or_misdescribed_roster_reference','confirmed_entity':False,'linked_existing_audit_id':'character-arc-r3-015','terminal_assessment':q['proposed_scope_treatment']['text'],'evidence':q['evidence'],'actual_reviewer':'/root/zongheng_vol03_full','scope_treatment_authorized_by_primary':'primary实际复读1041 L76714—20后批准：54仅历史误述/重复引用，不设第二确认实体；原roster不改。非代写primary签收。','review_status':'draft','source_access':q['source_access']}
slots.append(dup)
for p in [roster_path,proof,P/'character-arc-reader3-scope.json']:additional[str(p.relative_to(ROOT)).replace('\\','/')]=sha(p)
unresolved_path=A/'reader3-unresolved-roster-names.json'
unresolved={'section':'unresolved_roster_names','status':'scope-slots-resolved-without-inventing-entities','actual_reviewer':'/root/zongheng_vol03_full','source_id':S['source_id'],'revision':S['revision'],'items':slots,'confirmed_separate_entities_in_this_file':0,'additional_support_sha256':additional}
dump(unresolved_path,unresolved)
unresolved_path.with_suffix('.md').write_bytes(('# reader3补核提案的非确认人物槽\n\n'+ '\n\n'.join(r['audit_id']+' '+r.get('name',r.get('original_roster_name',''))+'：'+r.get('terminal_state',r.get('terminal_assessment','')) for r in slots)+'\n\n两槽均不计独立确认人物；原roster保留，不改正式卡。\n').encode('utf-8'))
mapping=[];refs=0
for p,i,r in all_rows:
 assert r['review_status']=='draft' and r['actual_reviewer']=='/root/zongheng_vol03_full'
 for key in ['initial_comparison_stage','key_decisions','costs','terminal_state','evidence_boundaries','reading_attribution']:assert r.get(key),(r['audit_id'],key)
 for e in r['evidence']:
  c=CH[int(e['chapter_id'][3:])];assert e['source_id']==S['source_id'] and e['revision']==S['revision'] and c['start_line']<=e['start_line']<=e['end_line']<=c['end_line']
  assert e['claim_kind'] in ['fact','inference','synthesis','plan'];refs+=1
 for st in r['stage_card_mapping']:
  cs=json.loads((ROOT/st['material_path']).read_text(encoding='utf-8'));c=cs[st['index']-1]
  for k in ['title','origin_key','asset_id']:assert c[k]==st[k]
  mapping.append({k:st[k] for k in ['volume','index','title','origin_key','asset_id']}|{'audit_id':r['audit_id'],'arc_name':r['name'],'arc_path':str(p.relative_to(ROOT)).replace('\\','/'),'arc_sha256':sha(p),'arc_json_pointer':f'/characters/{i}','stage_material_path':st['material_path'],'stage_material_sha256':st['material_sha256'],'stage_json_pointer':st['json_pointer']})
expected_st=[st for e in scope[:40] for st in e['stage_cards']]
assert len(mapping)==len(expected_st)
assert {m['asset_id'] for m in mapping}=={m['asset_id'] for m in expected_st}
assert len(mapping)==len({m['asset_id'] for m in mapping})
map_path=A/'reader3-stage-card-arc-map.json'
mapdoc={'status':'reader3-owned-stage-mapping-complete-pending-primary','scope':'仅reader3自辖前40既有人物的原阶段卡；其他代理卡不冒覆盖；全项目271卡由primary合并检查。','actual_reviewer':'/root/zongheng_vol03_full','original_roster_sha256':sha(roster_path),'owned_entity_count_with_stage_cards':40,'owned_stage_card_count':len(mapping),'by_volume':dict(Counter(m['volume'] for m in mapping)),'mappings':mapping,'supplementary_confirmed_entities_without_stage_cards':22,'unresolved_or_duplicate_slots':[{'audit_id':r['audit_id'],'entity_type':r['entity_type']} for r in slots],'formal_input_sha256':formal,'additional_support_sha256':additional}
dump(map_path,mapdoc)
map_path.with_suffix('.md').write_bytes(('\n'.join(['# reader3原阶段卡 → 人物全弧精确映射','','仅自辖40人物，'+str(len(mapping))+'原卡；不声称本代理覆盖全项目271。','', '| 卷/序 | 原title | asset_id | audit_id |','|---|---|---|---|']+[f'| {m["volume"]}/{m["index"]} | {m["title"]} | {m["asset_id"]} | {m["audit_id"]} |' for m in mapping])+'\n').encode('utf-8'))
index_path=A/'reader3-character-arcs-index.json';indexdoc={'status':'authored-complete-awaiting-primary-final-review','section':'characters','actual_reviewer':'/root/zongheng_vol03_full','assignment_roster_slots':64,'confirmed_characters_or_referenced_npc_identities':62,'unresolved_names':1,'duplicate_or_misdescribed_roster_references':1,'original_stage_cards_mapped':len(mapping),'groups':files,'rows':[{'audit_id':r['audit_id'],'name':r['name'],'entity_type':r.get('entity_type','npc'),'path':str(p.relative_to(ROOT)).replace('\\','/'),'sha256':sha(p),'json_pointer':f'/characters/{i}'} for p,i,r in all_rows],'non_character_slot_interface':{'path':str(unresolved_path.relative_to(ROOT)).replace('\\','/'),'sha256':sha(unresolved_path)},'stage_mapping_interface':{'path':str(map_path.relative_to(ROOT)).replace('\\','/'),'sha256':sha(map_path)},'formal_input_sha256':formal,'additional_support_sha256':additional,'reading_attribution':'首次本人原文仅卷1raw2—151、卷4raw754—968；卷1尾primary、本代理全读尾四栏；六卷团队全文覆盖不等个人新全文。本次人物接口逐对象派生接读、另列必要原文复核，不重写旧reader。','new_targeted_original_reads':{'full_chapters':[649,899,999,1000,1101,1162,1288,1362,1366,1375,1382],'ranges':[{'chapter':1385,'start_line':99616,'end_line':99631},{'chapter':1381,'start_line':99312,'end_line':99339},{'chapter':1270,'start_line':91890,'end_line':91904}],'other_bounded_contexts':'969以后火犁全部命中上下文、1345/1357刑天具名上下文；均已实际输出并读，非整章声明。','additional_unique_project_coverage':0},'validation':{'confirmed_rows':62,'all_64_roster_slots_accounted_for':True,'evidence_refs':refs,'fixed_source_revision_range_validation':'passed','formal_hash_validation':'passed','all_formal_inputs_under_writing_vault':True,'stage_card_identity_mapping':'passed','semantic_primary_review':'由primary逐组另签，不由本结构校验替代','user_taste_approval':False}}
dump(index_path,indexdoc)
index_path.with_suffix('.md').write_bytes(('\n'.join(['# 《斩龙》reader3人物全弧交接','','已完成64提案槽核验：62确认人物或有原文依据的NPC身份，罗戟待来源、另一火犁为重复误述，二者独立接口不计新人物。','',f'10组稳定草稿；自辖40既有人物对应{len(mapping)}张阶段卡，asset/vol/index/title逐值映射。其余271全库覆盖由primary合并核查。','',indexdoc['reading_attribution'],'','原文定向复核不增加项目唯一全文覆盖，未改正式卡、两池、原阶段reader与primary账。','', '| 组 | 确认项数 | JSON SHA256 |','|---|---|---|']+[f'| {i+1:02d} | {r["confirmed_characters"]} | {r["sha256"]} |' for i,r in enumerate(files)]+['','结构检查通过：固定SID/rev章行、正式输入SHA、独占scope、无重复audit_id、旧卡映射。根审由primary另行进行；不是用户审美批准。'])+'\n').encode('utf-8'))
receipt={'status':'passed-structure-and-authorship-scope-only','index_json_sha256':sha(index_path),'index_md_sha256':sha(index_path.with_suffix('.md')),'stage_map_sha256':sha(map_path),'unresolved_interface_sha256':sha(unresolved_path),'confirmed_rows':62,'roster_slots':64,'stage_cards':len(mapping),'formal_inputs':len(formal),'refs':refs}
dump(P/'character-arcs-final-structure-validation.json',receipt)
state=P/'character-arc-reader-state.json';s=json.loads(state.read_text(encoding='utf-8'));s['status']='scope-authored-complete-pending-primary';s['non_character_slot_ids']=['character-arc-r3-046','character-arc-r3-054'];s['confirmed_character_count']=62;s['next_onebased_index']=None;s['all_roster_slots_accounted_for']=True;s['final_structure_receipt']=receipt;dump(state,s)
print(json.dumps(receipt,ensure_ascii=False))
