"""补足空说明并生成地图共用事件登记；不重写既有阶段卡。"""
import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'distill-novels/scripts'))
from fictionlib.graph import save_graph, render_graph
from fictionlib.vault import Vault

V = ROOT / 'writing-vault'
OUT = V / 'library/reports/zongheng-tianxia/atlas'
SID = 'src-2a13958390274509b2af019f6b12d981'
inp = json.loads(Path(__file__).with_name('zongheng-editorial-input.json').read_text(encoding='utf-8'))
mf = json.loads((OUT / 'editorial-manifest.json').read_text(encoding='utf-8'))
g = json.loads((V / 'library/sources' / SID / 'plot-graph.json').read_text(encoding='utf-8'))
vault = Vault(V)
sources = {s['source_id']: s for s in vault.sources()}
fallback = vault._source
vault._source = lambda sid: sources[sid] if sid in sources else fallback(sid)
updated = copy.deepcopy(g)
summaries = {
    'v1-poor': '失业与缺钱使购买头盔、支付房租都成为问题。后续的帮助改变现实行动条件，不只是制造一次偶遇。',
    'v1-gift': '凌雪发现头盔已经绑定书生后，决定赠出；随后留下1000元与蓝星求职去处。早期援助同时提供游戏工具与工作入口。',
    'v1-team': '冰茶接纳凌雪引荐的书生，说明职业工作室的安排，并传达首夜10级和2金币的指标。机会随即变成需要履行的任务。'
}
for n in updated['nodes']:
    if n['id'] in summaries:
        n['summary'] = summaries[n['id']]
saved = g if updated == g else save_graph(vault, 'source', SID, updated, g['revision'])
mf['graph_revision'] = saved['revision']
nm = {n['id']: n for n in saved['nodes']}
selected = set(mf['focus_node_ids'])
focused = copy.deepcopy(saved)
focused['title'] = '《纵横天下》全书重点线索探索图'
focused['nodes'] = [n for n in saved['nodes'] if n['id'] in selected]
focused['edges'] = [e for e in saved['edges'] if e['from'] in selected and e['to'] in selected]
focused['threads'] = [t for t in saved['threads'] if t['id'].startswith('editorial-')]
profile_by_node = {}
for aid, p in inp['core_profiles'].items():
    for nid in p['map_nodes']:
        profile_by_node.setdefault(nid, []).append((aid, mf['profile_assets'][aid]))
for node in focused['nodes']:
    if node['id'] in profile_by_node:
        node['characters'] = [p['asset_id'] for _, p in profile_by_node[node['id']]]
render_graph(focused, OUT / 'map')
for thread in focused['threads']:
    part = copy.deepcopy(focused)
    members = set(thread['node_ids'])
    event_nodes = [copy.deepcopy(nm[nid]) for nid in thread['node_ids']]
    root_id = 'editorial-display-root'
    for n in event_nodes:
        # 这是一层线内浏览目录，不是新增的情节因果。
        n['parent_id'] = root_id
        if n['id'] in profile_by_node:
            n['characters'] = [p['asset_id'] for _, p in profile_by_node[n['id']]]
    part['title'] = thread['title']
    part['nodes'] = [{'id': root_id, 'parent_id': None, 'kind': 'story', 'title': thread['title'], 'summary': '单线浏览目录；实线关系按各自标签解释，目录归属不等于因果。', 'claim_kind': 'synthesis'}] + event_nodes
    part['edges'] = [e for e in focused['edges'] if e['from'] in members and e['to'] in members]
    part['threads'] = [copy.deepcopy(thread)]
    part['threads'][0]['edge_ids'] = [e['id'] for e in part['edges']]
    render_graph(part, OUT / 'lines' / thread['id'])

chapters = {c['chapter_id']: c for r in sources[SID]['revisions'] if r['revision'] == mf['source_revision'] for c in r['chapters']}
register = []
count = 0
for node in saved['nodes']:
    nid = node['id']
    if nid not in selected or node.get('kind') not in {'event','scene'}:
        continue
    count += 1
    register += ['', f'<a id="event-{nid}"></a>', '### ' + node['title'], '', node.get('summary', '')]
    people = profile_by_node.get(nid, [])
    if people:
        register += ['', '人物：' + ' · '.join(f"[{p['name']}](characters/{aid}.md)" for aid, p in people)]
    related = [e for e in saved['edges'] if e['id'].startswith('editorial-') and nid in (e['from'], e['to'])]
    if related:
        register += ['', '跨卷或后续联系：', '']
        for edge in related:
            other = edge['to'] if edge['from'] == nid else edge['from']
            label = {'cause':'因果','setup':'铺垫','payoff':'回收','reveal':'揭示','echo':'呼应'}[edge['kind']]
            register.append(f"- **{label}**：[{nm[other]['title']}](#event-{other})。{edge['label']}。{edge['summary']}")
    register += ['', '<details>', '<summary>章节依据</summary>', '', '| 章节 | 全文行号 |', '|---|---|']
    seen = set()
    for ev in node.get('evidence', []):
        key = (ev['chapter_id'],ev.get('start_line'),ev.get('end_line'))
        if key in seen:
            continue
        seen.add(key)
        ch = chapters[ev['chapter_id']]
        register.append(f"| {ch['title']}（{ev['chapter_id']}） | {ev.get('start_line',ch['start_line'])}—{ev.get('end_line',ch['end_line'])} |")
    register += ['', '</details>', '']
map_path = OUT / 'map.md'
intro = map_path.read_text(encoding='utf-8').split('<!-- event-register:start -->')[0]
map_path.write_text(intro + '<!-- event-register:start -->\n' + '\n'.join(register) + '\n<!-- event-register:end -->\n', encoding='utf-8')
mf['event_register_count'] = count
(OUT / 'editorial-manifest.json').write_text(json.dumps(mf, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps({'graph_revision': saved['revision'], 'event_register_count': count, 'empty_event_summaries': [n['id'] for n in focused['nodes'] if n.get('kind') in {'scene','event'} and not n.get('summary')], 'map_character_links': sum(len(p) for p in profile_by_node.values())}, ensure_ascii=False))
