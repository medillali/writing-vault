"""只读核对研究产物和正式库；仅将结果写回分配的规划目录。"""
import copy
import hashlib
import json
import pathlib
import sys

sys.stdout.reconfigure(encoding='utf-8')
B = pathlib.Path(__file__).resolve().parent
ROOT = B.parents[2]
sys.path.insert(0, str(ROOT / 'distill-novels/scripts'))
from fictionlib.vault import Vault
from fictionlib.graph import validate_graph

S = json.loads((B/'source.json').read_text(encoding='utf-8-sig'))
A = json.loads((B/'analysis.json').read_text(encoding='utf-8'))
C = json.loads((B/'cards.json').read_text(encoding='utf-8'))
G = json.loads((B/'graph.json').read_text(encoding='utf-8'))
L = json.loads((B/'read-log.json').read_text(encoding='utf-8'))
vault = Vault(ROOT/'writing-vault')
expected = [f'ch-{n+1:04d}' for n in range(1,50)]
assert A['read_chapter_ids'] == expected
assert [x['chapter_id'] for x in L['chapters']] == expected
assert A['source_id'] == L['source_id'] == S['source_id']
assert A['revision'] == L['revision'] == S['revision']
assert L['read_chapter_count'] == len(L['chapters']) == 49
assert A['scope']['volume_read_complete'] and not A['scope']['whole_book_complete']
assert not L['complete_book']
for n, row in enumerate(L['chapters'], 1):
    original = S['chapters'][n]
    assert row['original_chapter_number'] == n
    for key in ['chapter_id', 'title', 'start_line', 'end_line']:
        assert row[key] == original[key], (n, key)
    assert row['full_text_read'] is True
    assert row['reading_method'] == '模型逐章全文读取并分析'
    assert row['fact_summary'].strip()
assert L['chapters'][16]['reread_after_truncation'] is True
assert A['next_reading']['start_chapter_id'] == L['next_chapter_id'] == 'ch-0051'
assert set(A['dimensions']) == {'worldbuilding','characters','plot','style','narrative','dialogue','pacing','themes','continuity'}
assert sum(len(d['observations']) for d in A['dimensions'].values()) == 36
assert all(d['evidence_limits'] for d in A['dimensions'].values())

origins = {c['origin_key']: c for c in C}
assert len(origins) == len(C)
prefix = S['source_id'] + '/standard-20261023/'
scene_required = {'goal','obstacle','choice','consequence','state_change','why_it_works','applicability','failure_mode'}
for c in C:
    validation_copy = copy.deepcopy(c)
    validation_copy.setdefault('derived_from', [])
    vault._validate_asset(validation_copy)
    assert c['origin_key'].startswith(prefix)
    assert {'作者:失落叶','作品:网游之纵横天下'}.issubset(c['tags'])
    assert c['scope'] != 'original-project'
    assert c['review_status'] == 'draft' and c['user_notes'] == ''
    if c['asset_type'] == 'scene':
        assert scene_required.issubset(c['content'])
    if c['asset_type'] == 'character':
        assert c['content']['aliases'] and c['content']['phase_scope']['chapter_ids'] == expected
    if c['asset_type'] == 'pattern':
        assert c['scope'] == 'reusable-pattern'
        refs = c['content']['derived_from_origin_keys']
        assert refs
        assert all(ref in origins and origins[ref]['asset_type'] == 'scene' for ref in refs)
assert origins[prefix+'pattern-identity-layers']['content']['derived_from_origin_keys'] == [prefix+'scene-identity']
assert A['characters'] == [c for c in C if c['asset_type']=='character']
assert A['scenes'] == [c for c in C if c['asset_type']=='scene']
assert A['reusable_patterns'] == [c for c in C if c['asset_type']=='pattern']

evidence_counts = {'lists': 0, 'entries': 0}
def check_nested(value):
    if isinstance(value, dict):
        for key, child in value.items():
            if key == 'evidence':
                vault.validate_evidence(child)
                evidence_counts['lists'] += 1
                evidence_counts['entries'] += len(child)
                for entry in child:
                    assert entry['source_id'] == S['source_id']
                    assert entry['revision'] == S['revision']
                    assert entry['chapter_id'] in expected
                    assert entry['claim_kind'] != 'plan'
            else:
                check_nested(child)
    elif isinstance(value, list):
        for child in value: check_nested(child)
for item in [A,C,G]: check_nested(item)
assert validate_graph(G, vault)
assert A['threads'] == G['threads']
assert len(G['coverage']) == 1
assert G['coverage'][0] == {'source_id':S['source_id'],'revision':S['revision'],'chapter_ids':expected,'complete':False}
grave = next(t for t in G['threads'] if t['id']=='grave')
assert grave['status']=='partial' and '未击杀' in grave['resolution_note']
old = json.loads((ROOT/'writing-vault/library/sources'/S['source_id']/'plot-graph.json').read_text(encoding='utf-8'))
assert {n['id'] for n in old['nodes']}.issubset(n['id'] for n in G['nodes'])
assert {e['id'] for e in old['edges']}.issubset(e['id'] for e in G['edges'])

files = ['analysis.json','cards.json','graph.json','read-log.json','report.md']
file_checks = []
for name in files:
    data = (B/name).read_bytes()
    assert data
    text = data.decode('utf-8')
    assert '人工研究草稿' not in text and '人工分析' not in text
    file_checks.append({'file':name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
result = {
    'status':'passed',
    'method':'只读调用 fictionlib.validate_graph、Vault._validate_asset 副本验证和递归 evidence 检查；未入库',
    'source_id':S['source_id'],'revision':S['revision'],
    'full_chapters':49,'dimension_observations':36,
    'cards':{kind:sum(c['asset_type']==kind for c in C) for kind in ['character','scene','pattern']},
    'graph':{'nodes':len(G['nodes']),'edges':len(G['edges']),'threads':len(G['threads']),'source_complete':False},
    'nested_evidence':evidence_counts,
    'checks':['连续49章和原索引标题/行范围一致','第17章补读记录保留','九维证据和限制字段存在','29张卡schema通过','稳定origin_key唯一','6机制派生场景存在','分析副本与卡片/图相同','图树、关系、线成员、旧人物引用和覆盖验证通过','所有递归证据位于已读修订范围','全书未完成标记一致'],
    'limits':['不把schema/范围校验当作解释正确或用户审美认可','正式derived_from版本引用由主代理入库时转换','未读取卷二及后文'],
    'files':file_checks
}
(B/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
