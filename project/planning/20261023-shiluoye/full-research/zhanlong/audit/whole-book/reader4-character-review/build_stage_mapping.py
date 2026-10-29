import json, hashlib
from pathlib import Path

D = Path(__file__).resolve().parent
A = D.parent
ROOT = D.parents[6]
F = ROOT/'writing-vault/library/reports/zhanlong'
def rd(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def wr(p, x): p.write_text(json.dumps(x, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

dest = D/'stage-card-to-character-arc-map.json'
assert not dest.exists(), 'Mapping output already exists; use an explicit delta rather than overwrite.'
receipt = rd(D/'input-receipt.json')
assigned = receipt['assignment']
groups = sorted(A.glob('reader4-character-arcs-part[0-9][0-9].json'))
rows = {}
pins = {}
for p in groups:
 pins[p.relative_to(ROOT).as_posix()] = sha(p)
 for row in rd(p)['characters']:
  assert row['audit_id'] not in rows
  rows[row['audit_id']] = (row, p)
assert len(rows) == len(assigned) == 52
special = {
 17:'原卡题“上将星痕”与新弧采用星痕的规范指向并列保存；不以标题前缀增造第二人。658实际ID说明已列本组证据。',
 22:'原卷四题“美丽清眸”不按标题直接并人；861指挥与系统公告、898延续场景的限定原文核对支持清眸拓墨。原题、asset与索引原样保留。',
 28:'玩家百里若风与NPC百里伦独立；本条补核玩家，没有占用或复用NPC卡。',
 36:'本弧仅九霄夏火统领弗雷；472八荒宫廷魔导师同名缺跨职务桥，不据同字强并，也不凭空添一张旧卡。傅雷伪装工匠另人。',
 37:'原卡summary的御林归属已另提最小外置纠正；本弧据1001狂雷任命及1067死亡保存真实军属。映射不改原卡。',
 42:'实体目标为佩儿身体内的西瓦娜意志；身体连续不等原佩与占据者无条件同一实体。',
 46:'原origin尾名lanse保留，但卡题与内容明确目标为兰蔻，不由机器键把祖父兰斯并入。'
}
entities = []
flat = []
without_cards = []
seen = set()
for number, original in enumerate(assigned, 1):
 aid = f'character-arc-r4-{number:03}'
 row, gp = rows[aid]
 assert row['stage_card_mapping'] == original['stage_cards']
 kind = 'player_person' if number <= 32 else 'npc_person'
 e = {'audit_id':aid, 'entity_name':row['name'], 'entity_type':kind,
      'assignment_roster_name':original['name'], 'original_proposed_owner':original['proposed_owner'],
      'current_owner':'/root/zongheng_vol04_full', 'character_group_path':gp.relative_to(ROOT).as_posix(),
      'stage_cards':original['stage_cards'],
      'mapping_basis':special.get(number,'已完整接读对应卡content/evidence与analysis同源阶段状态；按卡的行动者指向对应单一人物，不把其所属组织另当人物。')}
 entities.append(e)
 if not original['stage_cards']:
  without_cards.append({'audit_id':aid,'entity_name':row['name'],'entity_type':kind,'stage_card_count':0,'reason':'获授权补核实体；真实旧阶段卡为零，不凭空生成旧asset。'})
 for m in original['stage_cards']:
  p = F/f"vol{m['volume']:02}-cards.json"
  cs = rd(p); c = cs[m['index']-1]
  assert all(c[k] == m[k] for k in ['title','origin_key','asset_id'])
  key = (m['volume'],m['index']); assert key not in seen; seen.add(key)
  pins[p.relative_to(ROOT).as_posix()] = sha(p)
  flat.append({**m,'index_convention':'one-based-full-original-card-array','source_cards_path':p.relative_to(ROOT).as_posix(),
               'source_cards_sha256':sha(p),'original_asset_type':c.get('asset_type',c.get('type','character-card-with-no-explicit-type-key')),
               'target_audit_id':aid,'target_entity_name':row['name'],'target_entity_type':kind,
               'character_group_path':gp.relative_to(ROOT).as_posix(),'mapping_basis':e['mapping_basis']})
out = {'status':'stable-mapping-draft-pending-primary-review','scope':'仅reader4获授权的32玩家与20NPC；不声称覆盖其他reader的人物或全部全书卡。',
       'source_id':rd(groups[0])['source_id'],'revision':rd(groups[0])['revision'],
       'counts':{'entities':52,'player_person':32,'npc_person':20,'stage_cards':len(flat),'supplementary_entities_without_stage_cards':len(without_cards),'assigned_organization_or_nonentity_stage_cards':0},
       'entity_classification_boundary':'本辖52目标均为单一人物。神话、锋芒、英雄冢、龙翔、六宫粉黛等是人物所属或对阵组织，职衔与会名不另计人物；未把场景、军团、神格或物品建为人物。此说明不替其他reader的组织接口分类。',
       'input_sha256':pins,'roster_path':(A/'character-arc-entity-roster-proposal.json').relative_to(ROOT).as_posix(),
       'roster_sha256':sha(A/'character-arc-entity-roster-proposal.json'),
       'assignment_receipt_path':(D/'input-receipt.json').relative_to(ROOT).as_posix(),'assignment_receipt_sha256':sha(D/'input-receipt.json'),
       'stage_card_rows':flat,'entities':entities,'supplementary_entities_without_stage_cards':without_cards,
       'verification':'52目标ID恰一次、各stage_card_mapping与已交组逐值相等、每个旧卷/索引恰一次、asset/origin/title与正式卡数组实值完全相等；不改任何原卡或已交组。'}
wr(dest,out)
md = ['# reader4旧阶段卡与人物全弧映射（待主审）','','仅本辖32玩家、20NPC；原卷、原卡索引、标题、asset与origin保持。各目标为单一人物，所属组织不另算实体。','',f"共52人物、{len(flat)}张旧阶段卡；{len(without_cards)}名补核人物没有旧卡，不伪造asset。",'','|原卷/索引|原标题|原asset|对应人物弧|','|---|---|---|---|']
for x in flat: md.append(f"|v{x['volume']}/{x['index']}|{x['title'].replace('|','／')}|{x['asset_id']}|{x['target_audit_id']} {x['target_entity_name']}|")
md += ['','## 补核但没有旧阶段卡','']
md += [f"- {x['audit_id']} {x['entity_name']}：旧卡0；证据与弧见对应分组。" for x in without_cards]
md += ['','## 指代边界','']
md += [f"- character-arc-r4-{n:03}：{s}" for n,s in special.items()]
dest.with_suffix('.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
print(json.dumps({'mapping_sha256':sha(dest),'md_sha256':sha(dest.with_suffix('.md')),'counts':out['counts']},ensure_ascii=False))
