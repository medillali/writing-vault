"""核对新版阅读产物、证据与保护边界；不代替用户文学评价。"""
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote

P = Path(__file__).resolve().parent
R = P.parents[2]
V = R / 'writing-vault'
O = V / 'library/reports/zongheng-tianxia/atlas'
sys.path.insert(0, str(R / 'distill-novels/scripts'))
from fictionlib.vault import Vault

def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))

manifest = read(O / 'editorial-manifest.json')
tree = read(O / 'tree/manifest.json')
pre = read(P / 'profiles-preflight.json')
merged = read(P / 'profiles-merged.json')['profiles']
v = Vault(V)
sources = {s['source_id']: s for s in v.sources()}
fallback = v._source
v._source = lambda sid: sources[sid] if sid in sources else fallback(sid)
assets = {a['asset_id']: a for a in v.search(asset_type='character')}
assert len(manifest['profile_assets']) == len(merged) == 47
assert sum(len(p['acts']) for p in merged) == 158
assert len({x['asset_id'] for x in manifest['profile_assets'].values()}) == 47
for key, record in manifest['profile_assets'].items():
    a = assets[record['asset_id']]
    v._validate_asset(a)
    assert a['revision'] == record['revision']
    assert a['content']['档案版本'] == 2
    assert a['origin_key'].endswith('/editorial-person/' + key)
    assert (V / 'history/assets' / a['asset_id'] / '1.json').is_file()
    assert {k: a[k] for k in ['user_notes', 'favorite', 'review_status']} == pre['owned_fields'][a['asset_id']]
    body = (O / 'characters' / (key + '.md')).read_text(encoding='utf-8')
    for section in ['身份与生活位置', '重要物品与资源', '性格怎样体现在行动中', '成为现在这个人以前', '心理与世界观', '贯通全书的经历', '重要关系怎样变化', '隐藏信息与知情范围', '从这个人物研究创作', '仍需保留的空缺与分歧']:
        assert '## ' + section in body, (key, section)
    assert '```json' not in body
    assert all(n in tree['events'] for n in record['map_nodes'])

for name, expected in pre['protected_hashes'].items():
    assert hashlib.sha256((V / name).read_bytes()).hexdigest() == expected, name
assert hashlib.sha256((V / 'private-sources/normalized/sources' / manifest['source_id'] / (manifest['source_revision'] + '.txt')).read_bytes()).hexdigest() == manifest['source_revision']
assert len(tree['events']) == len(set(tree['events'])) == 260
assert len(tree['edges']) == 227
assert len(tree['reading_guide']['node_ids']) == 31
assert len(tree['reading_guide']['edges']) == 30
assert tree['states'] == {'partial': 4, 'resolved': 3}
assert read(O / 'tree/integrity-check.json')['source_graph_unchanged'] is True
browser = read(O / 'tree/browser-check.json')
assert all(browser[k] == 0 for k in ['text_overflow', 'node_overlap', 'edges_through_unrelated_nodes', 'external_requests', 'javascript_errors'])
assert '```mermaid' not in (O / 'map.md').read_text(encoding='utf-8')
assert '(tree/index.html)' in (O / 'map.md').read_text(encoding='utf-8')

links, missing = 0, []
documents = list(O.rglob('*.md')) + [V / 'START-HERE.md', O.parent.parent / 'collection/内容审阅.md']
for doc in documents:
    body = doc.read_text(encoding='utf-8')
    for target in re.findall(r'\]\((<[^>]+>|[^)]+)\)', body):
        target = target.strip('<>')
        if re.match(r'^[A-Za-z][A-Za-z0-9+.-]*:', target):
            continue
        filename, _, anchor = target.partition('#')
        destination = (doc.parent / unquote(filename)).resolve() if filename else doc
        links += 1
        if not destination.is_file():
            missing.append((str(doc.relative_to(V)), target))
        elif anchor:
            if destination == (O / 'tree/index.html').resolve():
                if anchor not in tree['events']:
                    missing.append((str(doc.relative_to(V)), target))
            elif anchor.startswith('event-') or destination == (O / 'map.md').resolve():
                if f'id="{anchor}"' not in destination.read_text(encoding='utf-8'):
                    missing.append((str(doc.relative_to(V)), target))
assert not missing, missing
people = read(O / 'tree/character-links.json')
for nid, rows in people.items():
    assert nid in tree['events']
    for row in rows:
        assert (O / 'tree' / row['href']).resolve().is_file()

bykey = {p['audit_id']: p for p in merged}
assert '炼狱' in bykey['character-arc-45']['acts'][-1]['outcome']
assert '他一方面' not in bykey['character-arc-23']['psychology']['complexity']
assert '求' in bykey['character-arc-40']['acts'][-1]['development']
audit = read(O.parent / 'audit/whole-book/character-arc-audit-draft.json')
assert '已天域' in next(x for x in audit['characters'] if x['audit_id'] == 'character-arc-45')['terminal_state']
report = {'checked_at_utc': datetime.now(timezone.utc).isoformat(), 'content_version': 2, 'scope': '纵横天下样板；其他作品本轮重整未完成', 'unique_person_dossiers': 47, 'continuous_character_acts': 158, 'unique_event_cards': 260, 'semantic_relations': 227, 'separate_reading_guide': {'nodes': 31, 'links': 30}, 'local_links_checked': links, 'missing_links': missing, 'event_to_profile_links': sum(len(x) for x in people.values()), 'formal_graph_unchanged': True, 'source_and_checkpoints_unchanged': True, 'user_fields_preserved': True, 'old_profile_revision_retained': True, 'known_corrections_checked': ['勇敢的心炼狱天域', '大巫师女性指代', '林香先求助后亲自发声'], 'literary_approval': False, 'remote_push_performed': False}
(O / 'verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
