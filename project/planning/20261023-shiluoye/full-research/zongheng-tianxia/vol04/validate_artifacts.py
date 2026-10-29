import json,hashlib
from pathlib import Path
from collections import Counter
r=Path(__file__).parent
s=json.loads((r.parent/'source.json').read_text(encoding='utf-8'))
v=next(v for v in s['volumes'] if v['volume']==4)
segs=[x for u in v['units'] for x in u['segments']]
expected=[x['chapter_id'] for x in segs]
chap={x['chapter_id']:x for x in s['chapters']}
files={name:json.loads((r/name).read_text(encoding='utf-8')) for name in ['read-log.json','reader-state.json','analysis.json','cards.json','graph.json']}
ns=[json.loads(x) for x in (r/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines()]
assert [x['chapter_id'] for x in ns]==expected
assert [x['chapter_id'] for x in files['read-log.json']['chapters']]==expected
assert files['reader-state.json']['read_chapter_ids']==files['analysis.json']['read_chapter_ids']==expected
assert len(expected)==178 and len(set(expected))==178
for n in ns:
    q=chap[n['chapter_id']]
    assert n['full_text_read'] and (n['start_line'],n['end_line'])==(q['start_line'],q['end_line'])
    assert n['facts'] and all(k in n for k in ['inferences','state_changes','unresolved'])
assert files['read-log.json']['complete_volume'] and not files['read-log.json']['complete_book']
assert not files['reader-state.json']['truncated_pending'] and files['reader-state.json']['next_chapter_id'] is None
evidence_count=0
def walk(o):
    global evidence_count
    if isinstance(o,dict):
        if 'evidence' in o:
            assert isinstance(o['evidence'],list) and o['evidence']
            for e in o['evidence']:
                assert all(k in e for k in ['source_id','revision','chapter_id','start_line','end_line','claim_kind'])
                assert e['source_id']==s['source_id'] and e['revision']==s['revision']
                assert e['chapter_id'] in expected
                c=chap[e['chapter_id']]
                assert c['start_line']<=e['start_line']<=e['end_line']<=c['end_line']
                assert e['claim_kind'] in ['fact','inference','synthesis','plan']
                evidence_count+=1
        for z in o.values():walk(z)
    elif isinstance(o,list):
        for z in o:walk(z)
for o in files.values():walk(o)
a=files['analysis.json'];cards=files['cards.json'];g=files['graph.json']
assert len(a['dimensions'])==9 and all(len(x)>=3 for x in a['dimensions'].values())
assert all('fact' in x and 'inference' in x for xs in a['dimensions'].values() for x in xs)
keys={x['origin_key']:x for x in cards};assert len(keys)==len(cards)
for c in cards:
    assert c['origin_key'].startswith(s['source_id']+'/full-20261025/vol04/')
    assert c['review_status']=='draft' and c['favorite'] is False and c['user_notes']==''
    assert c['content']['summary'] and '作者:失落叶' in c['tags'] and '作品:网游之纵横天下' in c['tags']
    if c['asset_type']=='pattern':
        assert c['scope']=='reusable-pattern'
        assert all(keys[k]['asset_type']=='scene' for k in c['content']['derived_from_origin_keys'])
        assert all(k in c['content'] for k in ['causal_steps','applicability','failure_mode','originality_transform'])
    else:assert c['scope']=='source-analysis'
    if c['asset_type']=='scene':assert all(k in c['content'] for k in ['goal','obstacle','choice','consequence','state_change','why_it_works','applicability','failure_mode'])
counts=Counter(c['asset_type'] for c in cards);assert counts['character']>=8 and counts['scene']>=12 and counts['pattern']>=6
nodes={x['id']:x for x in g['nodes']};edges={x['id']:x for x in g['edges']}
assert len(nodes)==len(g['nodes']) and len(edges)==len(g['edges'])
roots=[n for n in nodes.values() if n['parent_id'] is None];assert len(roots)==1 and roots[0]['kind']=='story'
for n in nodes.values():
    seen=set();p=n['id']
    while p is not None:
        assert p in nodes and p not in seen
        seen.add(p);p=nodes[p]['parent_id']
    if n['kind']=='scene':
        assert n['asset_origin_key'] in keys and keys[n['asset_origin_key']]['asset_type']=='scene'
        assert any(int(e['chapter_id'][3:])==n['narrative_order'] for e in n['evidence'])
        assert all(keys[k]['asset_type']=='character' for k in n['characters'])
    for k in n.get('knowledge',[]):
        assert k['observer']=='reader' or k['observer'] in keys
        assert k['state'] in ['unknown','suspects','knows','misbelieves']
for e in edges.values():
    assert e['from'] in nodes and e['to'] in nodes
    assert e['kind'] in ['cause','setup','reveal','misdirection','reversal','echo','payoff']
for t in g['threads']:
    assert t['status'] in ['open','partial','resolved','abandoned','unknown']
    assert t['kind'] in ['main','subplot','hidden']
    assert all(k in nodes for k in t['node_ids']) and all(k in edges for k in t['edge_ids'])
    assert all(edges[k]['from'] in t['node_ids'] and edges[k]['to'] in t['node_ids'] for k in t['edge_ids'])
    if t['status']=='resolved':assert t.get('resolution_note') and t['evidence']
assert g['coverage'][0]['chapter_ids']==expected and g['coverage'][0]['complete'] is False
assert next(t for t in g['threads'] if t['id']=='v04-thread-guild')['status']!='resolved'
for name in ['report.md','handoff.md']:assert (r/name).stat().st_size>1000
result=dict(status='passed-structural-checks',review_status='draft',source_id=s['source_id'],revision=s['revision'],volume=4,body_units=178,index_segments=178,full_text_read=178,complete_volume=True,complete_book=False,truncated_pending=[],dimensions={k:len(v) for k,v in a['dimensions'].items()},cards=dict(counts),graph=dict(nodes=len(nodes),edges=len(edges),threads=len(g['threads']),knowledge_entries=sum(len(n.get('knowledge',[])) for n in nodes.values())),evidence_locators_checked=evidence_count,checks=['read-log/notes/state/analysis/graph精确连续同覆盖','每个evidence源修订/章内行号/claim_kind齐全','九维事实与解释分开','卡片origin_key唯一且机制引用本批场景','树单根无环，边线程端点有效，枚举合法，主线未误标resolved','narrative_order对准主事件章且有本节点证据','图事件asset_origin_key可映射本批场景，人物/知识observer可映射本批人物','全部draft无用户收藏审美写入'],limitations=['结构校验不证明文学解释正确或用户认可。','本阅读者卷三前史待主代理衔接，卷五结算未倒灌。'],artifacts={name:dict(bytes=(r/name).stat().st_size,sha256=hashlib.sha256((r/name).read_bytes()).hexdigest()) for name in ['chapter-notes.jsonl','read-log.json','analysis.json','cards.json','graph.json','report.md','handoff.md']})
(r/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:result[k] for k in ['status','body_units','cards','graph','evidence_locators_checked']},ensure_ascii=False))
