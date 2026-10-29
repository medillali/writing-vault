"""仅机械汇总根已实际逐项读审的对象，独立核271旧卡映射；不生成文学判断。"""
from pathlib import Path
import collections,hashlib,json
B=Path(__file__).resolve().parent;R=B.parents[2];S=B/'zhanlong';A=S/'audit/whole-book'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
source=read(S/'source.json');progress=read(S/'primary-research-group-review-progress.json')
characters=[];provenance={};formal={};support={}
for g in progress['groups']:
    p=A/g['path'];assert sha(p)==g['sha256'];d=read(p)
    if g['section']!='characters':continue
    assert [x['audit_id'] for x in d['characters']]==g['reviewed_ids']
    for row in d['characters']:
        assert row['audit_id'] not in provenance
        characters.append(row);provenance[row['audit_id']]={'path':g['path'],'sha256':g['sha256']}
    for name,h in d.get('formal_input_sha256',{}).items():
        assert name.startswith('writing-vault/') and sha(R/name)==h
        assert name not in formal or formal[name]==h;formal[name]=h
    md=p.with_suffix('.md')
    if md.is_file():support[md.relative_to(R).as_posix()]=sha(md)
lookup={x['audit_id']:x for x in characters}
assert len(characters)==161 and collections.Counter('reader3' if x.startswith('character-arc-r3-') else 'reader4' if x.startswith('character-arc-r4-') else 'reader5' for x in lookup)=={'reader3':62,'reader4':52,'reader5':47}
specs=[('character-arcs-self-stage-card-mapping.json','26f724ccaa840bc23bb156f53d6f069a8016c85cbd92bcd376406368262fe727','mappings'),('reader3-stage-card-arc-map.json','209edf88b77ad4e34690e23ff40ff8ff402fc386bd2fe9378bff9e74176cbbe6','mappings'),('reader4-character-review/stage-card-to-character-arc-map.json','78fff66916c3f7c3749a7459244b64cf196e5382ef45b60e66312cf6061080c8','stage_card_rows')]
maps=[];types={};cards={};volhash={}
for v in range(1,7):
    p=R/f'writing-vault/library/reports/zhanlong/vol{v:02d}-cards.json';volhash[v]=sha(p)
    for i,c in enumerate(read(p),1):
        if c['asset_type']=='character':cards[(v,i)]=c
assert len(cards)==271
for name,h,key in specs:
    p=A/name;assert sha(p)==h;d=read(p);support[p.relative_to(R).as_posix()]=h
    for row in d.get('audit_rows',[]):types[row['audit_id']]=row['entity_type']
    for row in d[key]:
        v,i=row['volume'],row['index'];card=cards[(v,i)]
        for field in ['title','origin_key','asset_id']:assert row[field]==card[field],(name,v,i,field)
        ids=row.get('audit_ids') or [row.get('audit_id',row.get('target_audit_id'))]
        assert ids and len(ids)==len(set(ids)) and set(ids)<=set(lookup)
        if 'arc_path' in row:
            p2=R/row['arc_path'];assert sha(p2)==row['arc_sha256'];g=read(p2);entry=g
            for part in row['arc_json_pointer'].strip('/').split('/'):entry=entry[int(part)] if isinstance(entry,list) else entry[part]
            assert entry==lookup[ids[0]] and row['arc_name']==entry['name']
        if 'target_entity_type' in row:types[ids[0]]=row['target_entity_type']
        maps.append({k:row[k] for k in ['volume','index','title','origin_key','asset_id']}|{'audit_ids':ids,'mapping_source':name,'mapping_source_sha256':h,'relation':row.get('mapping_relation','stage_observation_of_same_entity')})
assert len(maps)==len({(x['volume'],x['index']) for x in maps})==len({x['asset_id'] for x in maps})==len({x['origin_key'] for x in maps})==271
assert {(x['volume'],x['index']) for x in maps}==set(cards)
split=[x for x in maps if len(x['audit_ids'])>1];assert len(split)==1 and split[0]['volume']==2 and split[0]['index']==6 and set(split[0]['audit_ids'])=={'character-arc-010','character-arc-047'}
for item_id,row in lookup.items():
    if item_id not in types:types[item_id]=row.get('entity_type','npc' if item_id.startswith('character-arc-r3-') else 'player_person' if int(item_id.rsplit('-',1)[-1])<=32 else 'npc')
assert set(types)==set(lookup)
exceptions=A/'reader3-unresolved-roster-names.json';assert sha(exceptions)=='efa578c80562ba06915b743361a37e0a65d693af0ded52f9f8c044a7cee280a8'
unresolved=read(exceptions);assert len(unresolved['items'])==2 and all(x.get('confirmed_entity') is False for x in unresolved['items']);support[exceptions.relative_to(R).as_posix()]=sha(exceptions)
resolution={'status':'independently-verified-stage-card-coverage','source_id':source['source_id'],'revision':source['revision'],'unique_stage_cards':271,'target_links':sum(len(x['audit_ids']) for x in maps),'research_rows':len(characters),'individual_subject_research_rows':159,'interface_research_rows':2,'count_boundary':'161为159项单一人物/具名NPC身份研究及2项关联接口；043含3名现实技术来源，046为组织与行动，不冒161名独立人物。','original_card_arrays_sha256':{str(k):v for k,v in volhash.items()},'mappings':sorted(maps,key=lambda x:(x['volume'],x['index'])),'entity_classification':types,'unresolved_or_duplicate_roster_slots':unresolved['items'],'original_cards_unchanged':True,'signed_characters_unchanged':True}
target=A/'character-stage-card-resolution.json';draft=A/'character-arc-audit-draft.json';profile=S/'character-identity-profile.json'
assert not any(p.exists() for p in [target,draft,profile]);write(target,resolution);support[target.relative_to(R).as_posix()]=sha(target)
(A/'character-roster-scope.json').write_bytes(exceptions.read_bytes())
lines=['# 阶段人物卡与全书研究映射','','271张唯一阶段卡全部核至当前研究；王翦/王将旧合卡仅计一张、分别关联两人。161项研究包含159项单一人物或具名NPC身份与2关联接口，不作为独立人数。','','[全书人物研究](character-arc-audit-draft.md) · [精确映射JSON](character-stage-card-resolution.json) · [补核名单边界](character-roster-scope.json)','','| 卷/原序号 | 原阶段标题 | 当前研究ID |','|---|---|---|']
for row in resolution['mappings']:lines.append(f"| {row['volume']}/{row['index']} | {row['title'].replace('|','｜')} | {', '.join(row['audit_ids'])} |")
(A/'character-stage-card-resolution.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
write(profile,{'book':'zhanlong','source_id':source['source_id'],'policy':'原标签保来源；有display_name时可读页显示核准身份。每研究项独立索引，多个component_entities为关联主体而非别名。禁止同字、职称或跨书自动合并。','subjects':{i:{'expected_name':r['name'],'entity_scope':types[i],'boundary':r['evidence_boundaries']} for i,r in lookup.items()},'collision_guards':[]});support[profile.relative_to(R).as_posix()]=sha(profile)
out={'source_id':source['source_id'],'revision':source['revision'],'status':'primary-semantic-reviewed-exact-group-aggregate','review_status':'draft','user_approval':False,'actual_review_method':'根实际逐项读取所有161研究项语义与证据范围后签29组（含24重点）；本脚本只精确聚合，不制造阅读或文学结论。','scope_boundary':resolution['count_boundary'],'formal_input_sha256':formal,'additional_support_sha256':support,'signed_group_provenance':provenance,'stage_card_resolution':'character-stage-card-resolution.json','roster_exceptions':unresolved['items'],'characters':characters}
write(draft,out)
assert all(next(x for x in read(A/provenance[r['audit_id']]['path'])['characters'] if x['audit_id']==r['audit_id'])==r for r in characters)
print(json.dumps({'status':'exact-signed-objects-aggregated','research_rows':len(characters),'unique_stage_cards':271,'target_links':resolution['target_links'],'roster_exceptions':2,'aggregate_sha256':sha(draft),'mapping_sha256':sha(target),'profile_sha256':sha(profile)},ensure_ascii=False))
