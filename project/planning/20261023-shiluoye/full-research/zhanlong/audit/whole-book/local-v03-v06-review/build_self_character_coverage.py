"""装配已手工确认的自辖实体对应表；不改已交人物组或原阶段卡。"""
from pathlib import Path
import json,hashlib,collections,sys
sys.stdout.reconfigure(encoding='utf-8')
R=Path('C:/Users/Administrator/Documents/ChatGPT/Novel');A=Path(__file__).resolve().parent.parent
F=R/'writing-vault/library/reports/zhanlong'
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
roster=load(A/'character-arc-entity-roster-proposal.json')
by_name={'李逍遥':1,'林婉儿':2,'东城月':3,'薛柔':4,'沈冰':5,'东城雷':6,'宋寒':7,'冉闵（玩家老K）':8,'李牧':9,'王翦':10,'白起':11,'廉颇':12,'李梦瑶':13,'狐狸（刘庸）':14,'凫水囡囡':15,'月倾浅':16,'月微凉':17,'林小舞':18,'千顷瑶池':19,'月妖颜':20,'雪域千阳（唐雪）':21,'陈勇洁（一秒英雄）':22,'南宫决':23,'南宫灵':24,'林天南':25,'林成':26,'秦雯':27,'北辰观':28,'王信':29,'邢烈':30,'斧头':31,'汪泽诚':32,'魏凡':33,'欧阳川':34,'游弋（赵冉）':35,'唐琦':36,'秦雨':37,'秦蒙':38,'未具名日本天道流武士':39}
groups=[];rows={};audit_inputs={}
for g in range(1,9):
 p=A/f'character-arcs-part{g:02d}.json';d=load(p);groups.append(d)
 audit_inputs[p.name]=sha(p);audit_inputs[p.with_suffix('.md').name]=sha(p.with_suffix('.md'))
 for r in d['characters']:
  assert r['audit_id'] not in rows;rows[r['audit_id']]=r
assert len(rows)==47
self_entities=[e for e in roster['entities'] if e['proposed_owner']=='zongheng_vol05_full_main_and_reality']
assert len(self_entities)==39 and set(e['name'] for e in self_entities)==set(by_name)
formal={};formal_sha={}
for v in range(1,7):
 p=F/f'vol{v:02d}-cards.json';d=load(p);formal_sha[p.relative_to(R).as_posix()]=sha(p)
 assert sha(p)==roster['input_sha256'][p.relative_to(R).as_posix()]
 items=[x for x in d if x.get('asset_type')=='character' or x.get('kind')=='character' or x.get('card_type')=='character' or x.get('type')=='character'] if isinstance(d,list) else d.get('characters',d.get('character_cards',[]))
 formal[v]=items
assert sum(map(len,formal.values()))==271
mapping=[]
for e in self_entities:
 aid=f"character-arc-{by_name[e['name']]:03d}"
 for c in e['stage_cards']:
  actual=formal[c['volume']][c['index']-1]
  assert actual['title']==c['title'] and actual['origin_key']==c['origin_key']
  assert actual.get('asset_id')==c['asset_id']
  targets=[aid];relation='stage_observation_of_same_entity'
  note='原题与阶段只作历史来源，终态采用对应audit条的分时点研究，不覆盖原卡。'
  if c['volume']==2 and c['index']==6:
   targets=['character-arc-010','character-arc-047'];relation='split_mismerged_historical_card'
   note='旧卡王翦/王将误合：王翦剑士/龙骑及星痕关系归010；王将狂战/第一分盟长老及秦雨告白归047。原唯一asset/origin仅计一张，两个目标不是复制成两张来源卡；正式王身份优先层解释，不改原卡。'
  elif e['name']=='狐狸（刘庸）' and c['volume']==3:
   relation='same_entity_with_external_research_name_correction'
   note='旧题狐狸/慕天为派生误名，正式狐狸优先层指定刘庸/琉璃狐；保旧题作历史检索，不增慕天人物。'
  mapping.append(dict(**c,original_roster_entity=e['name'],audit_ids=targets,mapping_relation=relation,scope_note=note))
mapping.sort(key=lambda x:(x['volume'],x['index']))
origins=[x['origin_key'] for x in mapping];assets=[x['asset_id'] for x in mapping]
assert len(origins)==len(set(origins))==len(set(assets))
reverse=[]
real_only=set(range(25,36))|{38,39,40,41,42,44,45}
for aid,row in sorted(rows.items()):
 n=int(aid[-3:]);etype=row.get('entity_type') or ('real_person' if n in real_only else 'player_and_real_person')
 source_cards=[x['origin_key'] for x in mapping if aid in x['audit_ids']]
 reverse.append(dict(audit_id=aid,name=row['name'],entity_type=etype,source_stage_card_origins=source_cards,
  scope='stage_card_entity_or_approved_identity_split' if source_cards else 'approved_supplementary_source_interface_no_standalone_stage_card',
  component_entities=row.get('component_entities',[])))
assert sum(not x['source_stage_card_origins'] for x in reverse)==7
priority={p.relative_to(R).as_posix():sha(p) for p in [F/'audit/priority-corrections-fox-identity.json',F/'audit/priority-corrections-wang-identity.json',F/'audit/priority-corrections-dongcheng-kinship.json']}
out=dict(status='self_scope_mapping_for_primary_review_no_signed_rows_changed',actual_reviewer='zongheng_vol05_full',
 source_roster_sha256=sha(A/'character-arc-entity-roster-proposal.json'),formal_input_sha256=formal_sha,
 priority_interpretation_sha256=priority,audit_group_sha256=audit_inputs,
 counts=dict(global_stage_cards=271,self_original_roster_entities=39,self_unique_stage_cards=len(mapping),
  self_unique_origins=len(set(origins)),self_audit_rows=47,individual_person_research_rows=45,
  interface_rows=2,additional_supplementary_rows_without_standalone_stage_card=7,
  mismerged_stage_cards_split=1,target_links=sum(len(x['audit_ids']) for x in mapping)),
 count_boundary='47是研究条目数，含043三个现实原型实体的技术接口及046组织接口，不称47名独立人物。旧271张卡的全局唯一origin计数不因本区一张卡拆两个人而增加。',
 mappings=mapping,audit_rows=reverse,
 assertions=dict(self_original_39_entities_all_mapped=True,original_card_asset_volume_index_title_preserved=True,
  unique_source_origins_counted_once=True,split_010_047_relation_explicit=True,no_other_agent_scope_claimed=True,
  signed_group_rows_unchanged=True),
 reading_attribution='六卷271人物卡已完整实际接读，handoff及必要四栏/指定原文另见阅读进度。本人的全章初读只有卷三505—653、卷六1180—1386；其他原reader保留。映射是派生研究身份对齐，不新增全书原文覆盖。')
p=A/'character-arcs-self-stage-card-mapping.json';assert not p.exists();dump(p,out)
md=['# 《斩龙》自辖人物阶段卡与全弧条目映射','','只读来源映射，未改任何已签人物对象、冻结卡或正式库。','',f"自辖39个原归并实体，共{len(mapping)}张唯一阶段卡；拆出王将后连至40条人物研究，另7补核（其中2接口），合47研究条。全六卷271卡仍按唯一origin计数。",'',out['count_boundary'],'','|卷/序|原题|asset_id|原origin_key|audit_id|映射关系|','|---|---|---|---|---|---|']
for x in mapping:md.append('|'+ '|'.join([f"{x['volume']}/{x['index']}",x['title'],x['asset_id'],x['origin_key'],', '.join(x['audit_ids']),x['mapping_relation']])+'|')
md+=['','卷二第6张旧卡仅一asset/origin，010/047分别接收王翦与王将所证信息。旧卡不复制计数，也不再当小说改名。卷三狐狸旧题“慕天”只保历史标题，按正式优先层归刘庸。','','无独立阶段卡的补核入口：']
for x in reverse:
 if not x['source_stage_card_origins']:md.append(f"- {x['audit_id']} {x['name']}（{x['entity_type']}）")
p.with_suffix('.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
print(json.dumps(dict(counts=out['counts'],json_sha256=sha(p),md_sha256=sha(p.with_suffix('.md'))),ensure_ascii=False,indent=2))
