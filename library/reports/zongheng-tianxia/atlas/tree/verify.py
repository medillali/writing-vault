"""验证事件唯一性、完整关系、方向性质、源图不变及实际PNG产物。"""
from pathlib import Path
from collections import Counter
import hashlib
import json
import xml.etree.ElementTree as ET
from PIL import Image

HERE=Path(__file__).resolve().parent
VAULT=HERE.parents[4]
SID='src-2a13958390274509b2af019f6b12d981'
source=VAULT/'library/sources'/SID/'plot-graph.json'
g=json.loads(source.read_text(encoding='utf-8'))
m=json.loads((HERE/'manifest.json').read_text(encoding='utf-8'))
b=json.loads((HERE/'browser-check.json').read_text(encoding='utf-8'))
events=[n for n in g['nodes'] if n['kind'] in ['event','scene']]
groups=[n for n in g['nodes'] if n['kind'] not in ['event','scene']]
whole=[t for t in g['threads'] if t['id'].startswith('editorial-')]
assert hashlib.sha256(source.read_bytes()).hexdigest()==m['graph_sha256']
assert g['revision']==m['graph_revision']==13
assert set(m['events'])=={n['id'] for n in events}
assert len(m['events'])==len(set(m['events']))==260
assert {n['id'] for n in groups}=={n['id'] for n in m['removed_group_nodes']}
assert set(m['events'])|{n['id'] for n in groups}=={n['id'] for n in g['nodes']}
assert {n['id']:n for n in m['source_snapshots']['events']}=={n['id']:n for n in events}
assert m['source_snapshots']['edges']==g['edges']
assert m['source_snapshots']['whole_book_threads']==whole
assert m['states']=={'partial':4,'resolved':3}
svg=ET.fromstring((HERE/'tree.svg').read_text(encoding='utf-8'))
drawn={k:[e for e in svg.iter() if e.get('data-kind')==k] for k in ['event','edge','thread','annotation','reading-order']}
assert Counter(e.get('id') for e in drawn['event'])==Counter(n['id'] for n in events)
assert Counter(e.get('id') for e in drawn['edge'])==Counter(e['id'] for e in g['edges'])
assert Counter(e.get('id') for e in drawn['thread'])==Counter(t['id'] for t in whole)
assert Counter(e.get('id') for e in drawn['reading-order'])==Counter(e['id'] for e in m['reading_guide']['edges'])
assert len(m['reading_guide']['node_ids'])==31 and len(drawn['reading-order'])==30
assert m['reading_guide']['acyclic'] is True
for d in drawn['reading-order']:
    assert d.get('data-relation')=='reading-order'
    assert d.get('data-from') in m['events'] and d.get('data-to') in m['events']
    assert all(p.get('marker-end') is None for p in d if p.tag.endswith('path'))
strict=json.loads((HERE/'semantic-only-manifest.json').read_text(encoding='utf-8'))
assert m['graph_sha256']==strict['graph_sha256']
assert all(m[k]==strict[k] for k in ['roots','forks','junctions'])
byid={e.get('id'):e for e in drawn['edge']}
for e in g['edges']:
    d=byid[e['id']]
    assert d.get('data-from')==e['from'] and d.get('data-to')==e['to']
    assert d.get('data-relation')==e['kind']
    paths=[p for p in d if p.tag.endswith('path') and p.get('stroke')!='transparent']
    assert paths
    assert all(p.get('stroke-dasharray')==('' if e['kind']=='cause' else '2 11' if e['kind']=='echo' else '11 8') for p in paths)
assert len({e.get('id') for e in svg.iter() if e.get('id')})==sum(1 for e in svg.iter() if e.get('id'))
assert all(e['from'] in m['events'] and e['to'] in m['events'] for e in g['edges'])
html=(HERE/'index.html').read_text(encoding='utf-8')
assert '超级骷髅兵' not in html
assert 'src-9ff09c395734410b856f77c77a652834' not in html
assert SID in html and "viewKey='novel-tree-'+data.meta.source_id+'-v3'" in html
assert '/* VIEWER_CSS */' not in html and '/* VIEWER_JS */' not in html
assert '/* TREE_DATA */' not in html and '<!-- TREE_SVG -->' not in html
assert 'decodeURIComponent(location.hash.slice(1))' in html
images={}
for name in b['images']:
    with Image.open(HERE/name) as im:
        im.verify()
    with Image.open(HERE/name) as im:
        images[name]={'width':im.width,'height':im.height,'bytes':(HERE/name).stat().st_size}
assert images['tree.png']['width']==m['width'] and images['tree.png']['height']==m['height']
assert b['text_overflow']==b['node_overlap']==b['edges_through_unrelated_nodes']==b['external_requests']==b['javascript_errors']==0
result={'source_id':SID,'source_graph_revision':g['revision'],'source_graph_sha256':m['graph_sha256'],'source_graph_unchanged':True,'original_nodes':330,'drawn_unique_events':260,'event_kind_counts':dict(Counter(n['kind'] for n in events)),'retained_semantic_edges':len(g['edges']),'original_non_editorial_edges':sum(not e['id'].startswith('editorial-') for e in g['edges']),'editorial_edges':sum(e['id'].startswith('editorial-') for e in g['edges']),'retained_edge_kinds':dict(Counter(e['kind'] for e in g['edges'])),'semantic_edges_added':0,'edge_directions_and_kinds_unchanged':True,'dangling_edges':0,'duplicate_event_ids':0,'removed_group_nodes':len(groups),'removed_group_kinds':dict(Counter(n['kind'] for n in groups)),'removed_group_ids':[n['id'] for n in groups],'parent_hierarchy_edges_drawn':0,'whole_book_threads':7,'whole_book_states':m['states'],'hidden_identity_states':{t['id']:t['status'] for t in whole if t['kind']=='hidden'},'roots':len(m['roots']),'forks':len(m['forks']),'junctions':len(m['junctions']),'junction_count_excludes_echo':True,'images':images,'browser_verified':True,'literary_interpretation_user_approved':False,'remote_publish_performed':False}
result.update({'reading_guide_nodes':31,'display_reading_order_links':30,'reading_order_counted_as_semantic_edges':False,'reading_order_affects_roots_forks_junctions':False,'reading_order_is_acyclic':True,'semantic_only_snapshot_retained':True})
(HERE/'integrity-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:result[k] for k in ['drawn_unique_events','retained_semantic_edges','removed_group_nodes','dangling_edges','duplicate_event_ids','source_graph_unchanged']},ensure_ascii=False))
