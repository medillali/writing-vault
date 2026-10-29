"""本次内容整理批处理：经审核的编辑输入通过既有资料库接口保存。"""
import copy
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'distill-novels/scripts'))
from fictionlib.graph import save_graph, render_graph, validate_graph
from fictionlib.vault import Vault

PLAN = Path(__file__).resolve().parent
VAULT = ROOT / 'writing-vault'
INPUT = json.loads((PLAN / 'zongheng-editorial-input.json').read_text(encoding='utf-8'))
SID = INPUT['source_id']
REPORT = VAULT / 'library/reports' / INPUT['slug']
OUT = REPORT / 'atlas'
OUT.mkdir(exist_ok=True)
(OUT / 'characters').mkdir(exist_ok=True)
graph_path = VAULT / 'library/sources' / SID / 'plot-graph.json'
old_graph = json.loads(graph_path.read_text(encoding='utf-8'))
audits = json.loads((REPORT / 'audit/whole-book/character-arc-audit-draft.json').read_text(encoding='utf-8'))
vault = Vault(VAULT)

# 本进程只修改研究卡与图；来源修订不可变，缓存等同每次读相同的来源表。
source_table = {s['source_id']: s for s in vault.sources()}
original_source = vault._source
vault._source = lambda sid: source_table[sid] if sid in source_table else original_source(sid)
nodes = {n['id']: n for n in old_graph['nodes']}

def unique_evidence(items):
    result = []
    seen = set()
    for item in items:
        clean = {k: v for k, v in item.items() if k in {'source_id', 'revision', 'chapter_id', 'start_line', 'end_line', 'claim_kind'}}
        key = json.dumps(clean, sort_keys=True)
        if key not in seen:
            seen.add(key)
            result.append(clean)
    return result

def evidence_for_node(node_id):
    evidence = unique_evidence(nodes[node_id].get('evidence', []))
    assert evidence, node_id
    vault.validate_evidence(evidence)
    return evidence

new_graph = copy.deepcopy(old_graph)
new_graph['title'] = '《纵横天下》全书剧情：跨卷因果、人物选择与分卷展开'
new_graph['nodes'][0]['title'] = '全书剧情：跨卷关系与分卷证据'
new_graph['nodes'][0]['summary'] = '分卷树保留当时状态；editorial开头的全书剧情线贯通跨卷变化，终局和早期认知分开。'
bridge_ids = set()
for key, start, end, kind, label, summary in INPUT['bridges']:
    assert start != end and start in nodes and end in nodes
    eid = 'editorial-' + key
    bridge_ids.add(eid)
    evidence = unique_evidence(evidence_for_node(start) + evidence_for_node(end))
    edge = {'id': eid, 'from': start, 'to': end, 'kind': kind, 'label': label, 'summary': summary, 'claim_kind': 'inference', 'evidence': evidence}
    new_graph['edges'] = [e for e in new_graph['edges'] if e['id'] != eid] + [edge]
for thread in INPUT['threads']:
    members = thread['nodes']
    assert all(n in nodes for n in members)
    record = {k: v for k, v in thread.items() if k != 'nodes'}
    record['node_ids'] = members
    record['edge_ids'] = [e['id'] for e in new_graph['edges'] if e['from'] in members and e['to'] in members]
    new_graph['threads'] = [t for t in new_graph['threads'] if t['id'] != record['id']] + [record]
new_graph['notes'] = str(old_graph.get('notes', '')) + '\n2026-10-27内容重整：追加跨卷关系和全书线索；旧阶段状态不回填，事实及解释边界见atlas。'
validate_graph(new_graph, vault)

# 全量预检先于第一笔写入，不将待考称号自动建立为一个独立人物。
existing_assets = {a['asset_id']: a for a in vault.search(asset_type='character')}
profiles = []
pending_subjects = []
for row in audits['characters']:
    if '称号／实体未合案' in row['name']:
        pending_subjects.append(row)
        continue
    key = row['audit_id']
    core = INPUT['core_profiles'].get(key)
    evidence = unique_evidence(row['evidence'])
    if core:
        for node_id in core['map_nodes']:
            evidence += evidence_for_node(node_id)
    evidence = unique_evidence(evidence)
    vault.validate_evidence(evidence)
    asset_id = 'chr-' + hashlib.sha256((SID + '/editorial-person/' + key).encode()).hexdigest()[:32]
    content = {
        'summary': core['overview'] if core else row['initial_comparison_stage'] + '。其后：' + row['key_decisions'] + '。',
        '人物': row['name'],
        '档案定位': '全书人物主档；原阶段卡为依据，身份不按相近姓名自动合并。',
        '起点与处境': row['initial_comparison_stage'],
        '选择与变化': core['turning_points'] if core else row['key_decisions'],
        '代价与限制': row['costs'],
        '结局与最后可靠状态': row['terminal_state'],
        '证据与未知边界': row['evidence_boundaries'],
        '相关剧情事件': core['map_nodes'] if core else [],
        '编辑深度': '人物选择与创作研究' if core else '已有人物全弧统一档案；创作专题未另加解释',
        '上游人物审计': key
    }
    if core:
        content.update({'目标怎样变化': core['drive'], '关系怎样变化': core['relationships'], '塑造方法': core['craft'], '方法的失效条件': core['limit']})
    record = {'asset_id': asset_id, 'asset_type': 'character', 'scope': 'source-analysis', 'title': row['name'] + '｜全书人物档案', 'origin_key': SID + '/editorial-person/' + key, 'tags': ['作者:失落叶', '作品:网游之纵横天下', '全书人物主档', '内容重整:20261027'], 'content': content, 'evidence': evidence, 'user_notes': '', 'favorite': False, 'review_status': 'draft'}
    profiles.append((row, record, core))

before_users = {aid: {k: a[k] for k in ['user_notes', 'favorite', 'review_status']} for aid, a in existing_assets.items()}
saved_profiles = []
for row, record, core in profiles:
    current = existing_assets.get(record['asset_id'])
    saved = vault.put_asset(record, base_revision=current['revision'] if current else None, generated=True)
    saved_profiles.append((row, saved, core))
saved_graph = save_graph(vault, 'source', SID, new_graph, old_graph['revision'])

def md_evidence(evidence):
    source = source_table[SID]
    revisions = {r['revision']: {c['chapter_id']: c for c in r['chapters']} for r in source['revisions']}
    rows = ['| 章节 | 全文行号 |', '|---|---|']
    seen = set()
    for ev in evidence:
        key = (ev['chapter_id'], ev.get('start_line'), ev.get('end_line'))
        if key in seen:
            continue
        seen.add(key)
        chapter = revisions[ev['revision']][ev['chapter_id']]
        span = f"{ev.get('start_line', chapter['start_line'])}—{ev.get('end_line', chapter['end_line'])}"
        rows.append(f"| {chapter['title']}（{ev['chapter_id']}） | {span} |")
    return '\n'.join(rows)

profile_index = ['# 《纵横天下》人物库', '', '[剧情地图](map.md) · [本书内容入口](README.md)', '', '每人以一份主档贯通起点、选择、代价和终态。重点人物另有关系变化与塑造方法。原阶段卡保留为证据，主档中的研究解释仍待你审阅。', '', '| 人物 | 本轮整理深度 |', '|---|---|']
character_links = {}
for row, asset, core in saved_profiles:
    key = row['audit_id']
    filename = key + '.md'
    character_links[key] = 'characters/' + filename
    profile_index.append(f"| [{row['name']}](characters/{filename}) | {'选择、关系与创作研究' if core else '统一全书事实与变化；创作专题未扩写'} |")
    c = asset['content']
    body = ['# ' + row['name'], '', '[人物库](../characters.md) · [剧情地图](../map.md)', '', c['summary'], '', '## 起点与处境', '', c['起点与处境']]
    if core:
        body += ['', '## 目标与内在矛盾', '', core['drive'], '', '## 真正改变人物的选择', '']
        body += [f"{i}. {text}" for i, text in enumerate(core['turning_points'], 1)]
        body += ['', '## 关系怎样变化', '', core['relationships']]
    else:
        body += ['', '## 行动与变化', '', row['key_decisions'].replace('→', '；随后，')]
    body += ['', '## 代价与不能跳过的部分', '', row['costs'], '', '## 结局与最后可靠状态', '', row['terminal_state'], '', '## 仍不能确定的事', '', row['evidence_boundaries']]
    if core:
        body += ['', '## 从这条人物线研究创作', '', core['craft'], '', '这种方法会在哪里失效：' + core['limit'], '', '## 回到剧情地图', '']
        body += [f"- [{nodes[n]['title']}](../map.md#event-{n})" for n in core['map_nodes']]
    body += ['', '<details>', '<summary>章节依据与旧研究</summary>', '', '事实与结局沿用正式全书审计；本轮目标、关系和方法解释属于研究综合。并非声明本轮重新通读全部正文。', '', md_evidence(asset['evidence']), '', f"[完整版本主档](../../../../characters/{asset['asset_id']}.json) · [上游全书人物审计](../../audit/whole-book/character-arc-audit-draft.md)", '', '</details>', '', '## 你的取舍', '', asset['user_notes'] or '尚未填写。研究判断没有自动成为你的个人风格。', '']
    (OUT / 'characters' / filename).write_text('\n'.join(body), encoding='utf-8')
profile_index += ['', '## 身份待考', '']
for row in pending_subjects:
    profile_index += ['### ' + row['name'], '', row['key_decisions'], '', row['evidence_boundaries'], '']
(OUT / 'characters.md').write_text('\n'.join(profile_index), encoding='utf-8')

focus_ids = set(n for t in INPUT['threads'] for n in t['nodes'])
focus_ids.update(n for p in INPUT['core_profiles'].values() for n in p['map_nodes'])
focus_ids.update(n for b in INPUT['bridges'] for n in b[1:3])
for node_id in list(focus_ids):
    current = nodes[node_id]
    while current.get('parent_id'):
        focus_ids.add(current['parent_id'])
        current = nodes[current['parent_id']]
focus_graph = copy.deepcopy(saved_graph)
focus_graph['title'] = '《纵横天下》全书重点线索探索图'
focus_graph['nodes'] = [n for n in saved_graph['nodes'] if n['id'] in focus_ids]
focus_graph['edges'] = [e for e in saved_graph['edges'] if e['from'] in focus_ids and e['to'] in focus_ids]
focus_graph['threads'] = [t for t in saved_graph['threads'] if t['id'].startswith('editorial-')]
for t in focus_graph['threads']:
    t['edge_ids'] = [eid for eid in t['edge_ids'] if any(e['id'] == eid for e in focus_graph['edges'])]
render_graph(focus_graph, OUT / 'map')

payload = {'source_id': SID, 'source_revision': source_table[SID]['revision'], 'graph_revision': saved_graph['revision'], 'bridge_ids': sorted(bridge_ids), 'profile_assets': {row['audit_id']: {'asset_id': asset['asset_id'], 'revision': asset['revision'], 'name': row['name'], 'deep_creative_analysis': bool(core)} for row, asset, core in saved_profiles}, 'pending_subjects': [r['name'] for r in pending_subjects], 'focus_node_ids': sorted(focus_ids)}
(OUT / 'editorial-manifest.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
(PLAN / 'saved-profile-links.json').write_text(json.dumps(character_links, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
(PLAN / 'graph-before.json').write_text(json.dumps(old_graph, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
(PLAN / 'graph-after.json').write_text(json.dumps(saved_graph, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
after_assets = {a['asset_id']: a for a in vault.search(asset_type='character')}
assert all({k: after_assets[aid][k] for k in ['user_notes','favorite','review_status']} == fields for aid, fields in before_users.items())
receipt = {'checked_at_utc': datetime.now(timezone.utc).isoformat(), 'source_id': SID, 'old_graph_revision': old_graph['revision'], 'new_graph_revision': saved_graph['revision'], 'original_nodes_preserved': len(old_graph['nodes']), 'original_edges_preserved': len(old_graph['edges']), 'added_relations': len(INPUT['bridges']), 'whole_book_threads': len(INPUT['threads']), 'unified_person_profiles': len(saved_profiles), 'creative_analysis_profiles': len(INPUT['core_profiles']), 'unresolved_identity_groups': len(pending_subjects), 'existing_user_fields_preserved': len(before_users), 'git_push_performed': False}
(OUT / 'content-reorganization-receipt.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps(receipt, ensure_ascii=False))
