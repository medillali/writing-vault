"""把本轮完整人物稿写入既有主档，保留人工字段与旧版本。"""
import copy
import hashlib
import json
import re
import sys
from pathlib import Path

PLAN = Path(__file__).resolve().parent
ROOT = PLAN.parents[2]
VAULT = ROOT / 'writing-vault'
OUT = VAULT / 'library/reports/zongheng-tianxia/atlas'
SID = 'src-2a13958390274509b2af019f6b12d981'
REV = '2c541951301de981c755ebf4001bf3ec909d1e7d44314e14fa8af51751849a52'
sys.path.insert(0, str(ROOT / 'distill-novels/scripts'))
from fictionlib.vault import Vault

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def write(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def collect_evidence(obj):
    result = []
    if isinstance(obj, dict):
        if {'source_id', 'revision', 'chapter_id'} <= obj.keys():
            result.append({k: v for k, v in obj.items() if k in {'source_id', 'revision', 'chapter_id', 'start_line', 'end_line', 'claim_kind'}})
        else:
            for value in obj.values():
                result.extend(collect_evidence(value))
    elif isinstance(obj, list):
        for value in obj:
            result.extend(collect_evidence(value))
    return result

def unique(items):
    result, seen = [], set()
    for item in items:
        key = json.dumps(item, sort_keys=True, ensure_ascii=False)
        if key not in seen:
            seen.add(key)
            result.append(item)
    return result

audits = {x['audit_id']: x for x in read(OUT.parent / 'audit/whole-book/character-arc-audit-draft.json')['characters']}
graph_path = VAULT / 'library/sources' / SID / 'plot-graph.json'
graph = read(graph_path)
events = {n['id']: n for n in graph['nodes'] if n['kind'] in {'scene', 'event'}}
old_input = read(PLAN.parent / 'zongheng-editorial-input.json')
old_manifest = read(OUT / 'editorial-manifest.json')
inputs = ['profiles-core.json', 'profiles-npc.json', 'profiles-support-input.json', 'profiles-support-npc-input.json', 'profiles-support-allies-a-input.json', 'profiles-support-allies-b-input.json']
profiles = [p for file in inputs for p in read(PLAN / file)['profiles']]
assert len(profiles) == 47 and len({p['audit_id'] for p in profiles}) == 47
assert {p['audit_id'] for p in profiles} == set(audits) - {'character-arc-29'}

for p in profiles:
    for field in ['identity', 'possessions', 'personality', 'background', 'psychology', 'acts', 'relationships', 'knowledge', 'memories', 'craft', 'limits', 'summary']:
        assert field in p, (p['audit_id'], field)
    assert len(p['acts']) >= 2
    assert all({'context', 'development', 'outcome'} <= a.keys() for a in p['acts'])
    p['name'] = audits[p['audit_id']]['name']
    # 本轮主代理定点回读的初见衣着和转述渠道，补入准确定位。
    extra = {'character-arc-34': ('ch-0006', 245, 245), 'character-arc-35': ('ch-0006', 244, 244), 'character-arc-36': ('ch-0006', 241, 243), 'character-arc-39': ('ch-0022', 1556, 1583)}
    p['evidence'] = unique(collect_evidence(p) + collect_evidence(audits[p['audit_id']]))
    if p['audit_id'] in extra:
        cid, start, end = extra[p['audit_id']]
        p['evidence'].append({'source_id': SID, 'revision': REV, 'chapter_id': cid, 'start_line': start, 'end_line': end, 'claim_kind': 'fact'})
    p['interpretation_status'] = '来源人物研究；事件与身份保留证据，性格、心理、分幕与创作方法为研究综合，待用户取舍。'
    p['method'] = '整合既有八卷阅读、全书审计与本轮定点复核；不是声明本轮重新逐章通读。'

write(PLAN / 'profiles-support.json', {'profiles': [p for p in profiles if p['audit_id'] not in {x['audit_id'] for x in read(PLAN / 'profiles-core.json')['profiles'] + read(PLAN / 'profiles-npc.json')['profiles']}]})
write(PLAN / 'profiles-merged.json', {'source_id': SID, 'source_revision': REV, 'profiles': profiles})

vault = Vault(VAULT)
source_table = {s['source_id']: s for s in vault.sources()}
original_source = vault._source
vault._source = lambda sid: source_table[sid] if sid in source_table else original_source(sid)
source = source_table[SID]
chapters = {c['chapter_id']: c for r in source['revisions'] if r['revision'] == REV for c in r['chapters']}
existing = {a['asset_id']: a for a in vault.search(asset_type='character')}
for p in profiles:
    vault.validate_evidence(p['evidence'])
    aid = old_manifest['profile_assets'][p['audit_id']]['asset_id']
    assert aid in existing and existing[aid]['origin_key'] == SID + '/editorial-person/' + p['audit_id']

normalized = VAULT / 'private-sources/normalized/sources' / SID / (REV + '.txt')
protected_files = [graph_path, normalized] + sorted((VAULT / 'exchanges/runs').glob('*.json'))
protected_hashes = {str(p.relative_to(VAULT)): digest(p) for p in protected_files}
preflight = {'profiles': len(profiles), 'acts': sum(len(p['acts']) for p in profiles), 'evidence_locations': sum(len(p['evidence']) for p in profiles), 'source_id': SID, 'graph_revision': graph['revision'], 'protected_hashes': protected_hashes, 'owned_fields': {a['asset_id']: {k: a[k] for k in ['user_notes', 'favorite', 'review_status']} for p in profiles for a in [existing[old_manifest['profile_assets'][p['audit_id']]['asset_id']]]}}
write(PLAN / 'profiles-preflight.json', preflight)
if '--apply' not in sys.argv:
    print(json.dumps({k: preflight[k] for k in ['profiles', 'acts', 'evidence_locations', 'graph_revision']}, ensure_ascii=False))
    sys.exit(0)

labels = {'name': '姓名与称谓', 'age': '年龄与时点', 'position': '身份与社会位置', 'residence': '住处与活动范围', 'family': '家庭与亲缘', 'income': '生计与资源', 'core': '基本位置', 'succession': '师承与传承', 'terminal': '最后可靠状态', 'first_impression': '初见印象', 'hair_eyes_body': '发式、眼睛与身体', 'change': '外在变化', 'strengths': '优势与美德', 'flaws': '缺陷与张力', 'habits': '习惯与小动作', 'agenda': '目标与世界观', 'trauma': '旧伤与防卫', 'complexity': '内在冲突'}

def text_of(x):
    if isinstance(x, str):
        return x
    if isinstance(x, dict):
        return x.get('text') or x.get('analysis') or ''
    return ''

def paragraphs(value, custom=None):
    if isinstance(value, str):
        return [value, '']
    if isinstance(value, dict) and 'text' in value:
        return [text_of(value), '']
    if isinstance(value, dict):
        return [part for key, item in value.items() if key != 'evidence' for part in [f"**{(custom or labels).get(key, key)}。** {text_of(item)}", ''] if text_of(item)]
    result = []
    for item in value:
        if isinstance(item, str):
            result.extend([item, ''])
        else:
            name = item.get('item') or item.get('name') or ''
            result.extend([(f'**{name}。** ' if name else '') + text_of(item), ''])
    return result

aliases = {p['audit_id']: p['name'].split('／') for p in profiles}
aliases['character-arc-01'] += ['书生', '呆子']
aliases['character-arc-04'] += ['紫韵儿']
aliases['character-arc-14'] += ['尘埃']
aliases['character-arc-15'] += ['很萌']
aliases['character-arc-16'] += ['随风']
aliases['character-arc-36'] += ['去年夏天']
aliases['character-arc-44'] += ['魔方']
aliases['character-arc-47'] += ['花火']

def matching_person(name):
    return next((key for key, names in aliases.items() if name in names), None)

# 匹配只生成“此章有关”的查阅链接，不据同章出现推断因果、感情或共同知情。
manual_events = {
    'character-arc-12': ['v8-v08-wsl', 'v8-v08-beastcity'],
    'character-arc-17': ['v7-v07-split', 'v8-v08-after'],
    'character-arc-23': ['v8-v08-sacrifice'],
    'character-arc-24': ['v4-v04-kallen', 'v8-v08-kallen'],
    'character-arc-26': ['v5-v05-scene-dwarf'],
    'character-arc-31': ['v4-v04-cemetery'],
    'character-arc-35': ['v8-v08-after'],
    'character-arc-36': ['v6-v06-scene-snow-rescue', 'v8-v08-after'],
    'character-arc-37': ['v7-v07-redtrauma', 'v7-v07-recruit'],
    'character-arc-40': ['v8-v08-family'],
    'character-arc-42': ['v6-v06-scene-moon-rise'],
    'character-arc-43': ['v6-v06-scene-moon-rise', 'v7-v07-redtrauma'],
    'character-arc-45': ['v6-v06-scene-weapon-pact', 'v6-v06-scene-world-final', 'v7-v07-manhunt'],
    'character-arc-46': ['v6-v06-scene-recruit-council', 'v7-v07-dragonrace'],
    'character-arc-47': ['v6-v06-scene-recruit-council', 'v7-v07-dal'],
    'character-arc-48': ['v7-v07-s4', 'v7-v07-manhunt', 'v8-v08-after'],
}
profile_events, event_people = {}, {}
for p in profiles:
    key = p['audit_id']
    chosen = list(old_input['core_profiles'].get(key, {}).get('map_nodes', [])) + manual_events.get(key, [])
    assert all(n in events for n in chosen)
    evchap = {e['chapter_id'] for e in p['evidence']}
    names = aliases[key]
    for nid, n in events.items():
        desc = n['title'] + n.get('summary', '')
        if any(name in desc for name in names if len(name) >= 2) and evchap & {e['chapter_id'] for e in n.get('evidence', [])}:
            chosen.append(nid)
    profile_events[key] = list(dict.fromkeys(chosen))
    for nid in profile_events[key]:
        event_people.setdefault(nid, []).append({'name': p['name'], 'href': '../characters/' + key + '.md'})

saved = {}
for p in sorted(profiles, key=lambda p: p['audit_id']):
    key = p['audit_id']
    current = existing[old_manifest['profile_assets'][key]['asset_id']]
    record = {k: copy.deepcopy(current[k]) for k in ['asset_id', 'asset_type', 'scope', 'origin_key', 'tags', 'user_notes', 'favorite', 'review_status']}
    record['title'] = p['name'] + '｜完整人物档案'
    record['tags'] = list(dict.fromkeys(record['tags'] + ['完整人物档案:v2']))
    record['content'] = {'summary': p['summary'], '人物': p['name'], '档案版本': 2, '上游人物审计': key, '相关剧情事件': profile_events[key], '完整人物档案': {k: v for k, v in p.items() if k not in {'evidence', 'summary'}}, '结局与最后可靠状态': audits[key]['terminal_state'], '原文事实与研究解释': p['interpretation_status']}
    record['evidence'] = p['evidence']
    saved[key] = vault.put_asset(record, base_revision=current['revision'], generated=True)
    print(key, saved[key]['revision'], flush=True)

for p in sorted(profiles, key=lambda p: p['audit_id']):
    key, a = p['audit_id'], saved[p['audit_id']]
    lines = ['# ' + p['name'], '', '[人物库](../characters.md) · [全书树图](../tree/index.html) · [剧情地图说明](../map.md)', '', p['summary'], '', '## 身份与生活位置', '']
    lines += paragraphs(p['identity'])
    if p.get('appearance'):
        lines += ['## 外貌与他人印象', ''] + paragraphs(p['appearance'])
    lines += ['## 重要物品与资源', ''] + paragraphs(p['possessions'])
    lines += ['## 性格怎样体现在行动中', '', '以下性格与心理是依据行为作的研究解释；具体经历与人物原话见文末依据。', ''] + paragraphs(p['personality'], {**labels, 'core': '核心倾向'})
    lines += ['## 成为现在这个人以前', '', p['background'], '', '## 心理与世界观', ''] + paragraphs(p['psychology'])
    lines += ['## 贯通全书的经历', '', '按改变目标、关系或处境的转折分幕。幕内连贯叙述，不把每次升级另拆为一张卡。', '']
    for i, act in enumerate(p['acts'], 1):
        title = act['title'] if re.match(r'第.+幕', act['title']) else f"第{i}幕：{act['title']}"
        lines += ['### ' + title, '']
        if act.get('range'):
            lines += [act['range'], '']
        lines += [act['context'], '', act['development'], '', act['outcome'], '']
    lines += ['## 重要关系怎样变化', '']
    for rel in p['relationships']:
        target = matching_person(rel['person'])
        name = f"[{rel['person']}]({target}.md)" if target else rel['person']
        lines += ['**' + name + '。** ' + rel['analysis'], '']
    lines += ['## 隐藏信息与知情范围', ''] + paragraphs(p['knowledge'])
    if p['memories']:
        lines += ['## 留下长期影响的经历', ''] + paragraphs(p['memories'])
    lines += ['## 从这个人物研究创作', '', p['craft'], '', '## 仍需保留的空缺与分歧', '', p['limits'], '']
    if profile_events[key]:
        lines += ['## 回到剧情树', '', '下列链接定位同一张全书大图；表示相关事件查阅，不单凭共同出现推断关系。', '']
        lines += [f"- [{events[n]['title']}](../tree/index.html#{n})" for n in profile_events[key]] + ['']
    lines += ['<details>', '<summary>原文定位、研究来源与版本</summary>', '', p['method'], '', '| 原章标题与阅读单元 | 全文行号 |', '|---|---|']
    spans = unique([{k: e[k] for k in ['chapter_id', 'start_line', 'end_line']} for e in a['evidence']])
    for e in sorted(spans, key=lambda e: (e['start_line'], e['end_line'])):
        lines += [f"| {chapters[e['chapter_id']]['title']}（{e['chapter_id']}） | {e['start_line']}—{e['end_line']} |"]
    lines += ['', f"[版本主档](../../../../characters/{a['asset_id']}.json) · [全书人物审计](../../audit/whole-book/character-arc-audit-draft.md)", '', f"来源修订：`{REV}`；人物主档第{a['revision']}版。正文中的分幕、目标与方法是研究综合，非原著新增事实。", '', '</details>', '', '## 你的取舍', '', a['user_notes'] or '尚未填写；本稿没有代替你确认喜欢或不喜欢。', '']
    (OUT / 'characters' / (key + '.md')).write_text('\n'.join(lines), encoding='utf-8')
    alias = ['# ' + p['name'], '', p['summary'], '', f"[完整人物档案](../reports/zongheng-tianxia/atlas/characters/{key}.md) · [全书树图](../reports/zongheng-tianxia/atlas/tree/index.html)", '', f"主档版本：{a['revision']}。原阶段卡保留，当前阅读副本以完整档案为入口。", '']
    (VAULT / 'library/views' / (a['asset_id'] + '.md')).write_text('\n'.join(alias), encoding='utf-8')

groups = [ ('核心人物', list(range(1, 7))), ('龙域、王国与亡灵线', [7,8,9,10,18,20,21,22,23,24,25,26,27,28,30]), ('组织、盟友与竞争者', [11,12,13,14,15,16,17,32,37,38,39,40,41,42,43,44,45,46,47,48]), ('现实生活与工作室', [19,31,33,34,35,36]) ]
bykey = {p['audit_id']: p for p in profiles}
index = ['# 《纵横天下》完整人物库', '', '[全书树图](tree/index.html) · [剧情地图](map.md) · [创作研究](craft.md)', '', '人物按一人一份完整档案整理。核心人物展开连续的人生阶段；重要配角按材料详略处理，串联身份、性格、心理、行动、关系与终点。外貌、年龄或创伤缺证时保留空缺，不补造设定。', '', '事实与研究解释分开；人物原文定位折叠在每份档案末尾。龙神等未完成实体辨析的称号不强行合为一个人。', '']
for title, numbers in groups:
    index += ['## ' + title, '', '| 人物 | 贯通阅读的重点 |', '|---|---|']
    for num in numbers:
        key = f'character-arc-{num:02}'
        p = bykey[key]
        index += [f"| [{p['name']}](characters/{key}.md) | {p['summary']} |"]
    index += ['']
pending = audits['character-arc-29']
index += ['## 身份待考：龙神称号与实体', '', pending['key_decisions'], '', pending['evidence_boundaries'], '', '此项仍是待辨析记录，不计入47位独立人物档案。', '']
(OUT / 'characters.md').write_text('\n'.join(index), encoding='utf-8')
write(OUT / 'tree/character-links.json', event_people)

manifest = copy.deepcopy(old_manifest)
manifest.update({'content_version': 2, 'editorial_status': '按用户树图与完整档案要求返工；本地完成，文学判断待审阅', 'tree_entry': 'tree/index.html', 'profile_count': 47, 'act_count': preflight['acts']})
for key, a in saved.items():
    manifest['profile_assets'][key] = {'asset_id': a['asset_id'], 'revision': a['revision'], 'name': bykey[key]['name'], 'deep_creative_analysis': True, 'profile_version': 2, 'acts': len(bykey[key]['acts']), 'map_nodes': profile_events[key]}
write(OUT / 'editorial-manifest.json', manifest)

after_hashes = {str(p.relative_to(VAULT)): digest(p) for p in protected_files}
assert protected_hashes == after_hashes, '来源、正式图或阅读检查点意外改变'
assert all(preflight['owned_fields'][a['asset_id']] == {k: a[k] for k in ['user_notes', 'favorite', 'review_status']} for a in saved.values())
receipt = {'version': 2, 'source_id': SID, 'graph_revision': graph['revision'], 'profiles_updated': len(saved), 'acts': preflight['acts'], 'input_files': inputs, 'formal_graph_unchanged': True, 'source_and_reading_checkpoints_unchanged': True, 'user_fields_preserved': True, 'event_profile_links': sum(len(x) for x in event_people.values()), 'linked_events': len(event_people), 'profiles_with_event_links': sum(bool(x) for x in profile_events.values()), 'pending_identity': 'character-arc-29', 'publication': 'local-only; no commit or push', 'literary_acceptance': '待用户审阅'}
write(OUT / 'content-reorganization-receipt.json', receipt)
print(json.dumps(receipt, ensure_ascii=False), flush=True)
