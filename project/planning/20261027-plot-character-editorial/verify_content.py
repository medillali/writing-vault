"""内容层的范围、互链、证据与保护核查；不替代文学判断。"""
import hashlib
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'distill-novels/scripts'))
from fictionlib.vault import Vault
from fictionlib.graph import validate_graph
V=ROOT/'writing-vault'
O=V/'library/reports/zongheng-tianxia/atlas'
SID='src-2a13958390274509b2af019f6b12d981'
manifest=json.loads((O/'editorial-manifest.json').read_text(encoding='utf-8'))
before=json.loads(Path(__file__).with_name('graph-before.json').read_text(encoding='utf-8'))
graph=json.loads((V/'library/sources'/SID/'plot-graph.json').read_text(encoding='utf-8'))
vault=Vault(V)
sources={s['source_id']:s for s in vault.sources()}
fallback=vault._source
vault._source=lambda sid:sources[sid] if sid in sources else fallback(sid)
validate_graph(graph,vault)
node_map={n['id']:n for n in graph['nodes']}
assert set(n['id'] for n in before['nodes']).issubset(node_map)
edge_map={e['id']:e for e in graph['edges']}
assert all(edge_map[e['id']]==e for e in before['edges'])
assert graph['coverage']==before['coverage']
threads=[t for t in graph['threads'] if t['id'].startswith('editorial-')]
assert len(threads)==7
assert {t['kind'] for t in threads}=={'main','subplot','hidden'}
relations=[e for e in graph['edges'] if e['id'].startswith('editorial-')]
assert len(relations)==18
assert all(len({e['chapter_id'] for e in rel['evidence']})>=2 for rel in relations)

def branch(nid):
    n=node_map[nid]
    while n.get('parent_id') and node_map[n['parent_id']].get('parent_id'):
        n=node_map[n['parent_id']]
    return n['id']
cross=[e for e in relations if branch(e['from'])!=branch(e['to'])]
assets={a['asset_id']:a for a in vault.search(asset_type='character')}
for key,p in manifest['profile_assets'].items():
    a=assets[p['asset_id']]
    vault._validate_asset(a)
    assert a['revision']==p['revision']
    assert a['review_status']=='draft' and not a['favorite']
    body=(O/'characters'/f'{key}.md').read_text(encoding='utf-8')
    assert '结局与最后可靠状态' in body and '仍不能确定的事' in body
    if p['deep_creative_analysis']:
        assert '真正改变人物的选择' in body and '从这条人物线研究创作' in body
assert len(manifest['profile_assets'])==47
assert len(manifest['pending_subjects'])==1
assert len({p['asset_id'] for p in manifest['profile_assets'].values()})==47

missing=[]
checked_links=0
for doc in O.rglob('*.md'):
    text=doc.read_text(encoding='utf-8')
    for target in re.findall(r'\]\(([^)]+)\)',text):
        if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',target):
            continue
        target=target.strip('<>')
        filename,_,anchor=target.partition('#')
        destination=(doc.parent/unquote(filename)).resolve() if filename else doc
        checked_links+=1
        if not destination.is_file():
            missing.append({'from':str(doc.relative_to(V)),'target':target})
        elif anchor and destination.name=='map.md':
            content=destination.read_text(encoding='utf-8')
            if f'id="{anchor}"' not in content:
                missing.append({'from':str(doc.relative_to(V)),'anchor':target})
assert not missing, missing
map_text=(O/'map.md').read_text(encoding='utf-8')
registered=set(re.findall(r'<a id="event-([^"]+)"',map_text))
needed=set(n for p in manifest['profile_assets'].values() for n in assets[p['asset_id']]['content']['相关剧情事件'])
needed.update(n for e in relations for n in [e['from'],e['to']])
assert needed.issubset(registered)
assert len(registered)==manifest['event_register_count']==73
assert all(node_map[nid].get('summary') for nid in registered)
for thread in threads:
    html=O/'lines'/thread['id']/'index.html'
    content=html.read_text(encoding='utf-8')
    assert thread['title'] in content
    assert not re.search(r'<script[^>]+src=',content)
source_file=ROOT/'writing-vault/private-sources/normalized/sources'/SID/(manifest['source_revision']+'.txt')
assert hashlib.sha256(source_file.read_bytes()).hexdigest()==manifest['source_revision']
report={'checked_at_utc':datetime.now(timezone.utc).isoformat(),'scope':'纵横天下第一套内容重整；不代表其余书本轮已完成或用户认可文学解释','graph_revision':graph['revision'],'original_node_ids_retained':len(before['nodes']),'original_edges_unchanged':len(before['edges']),'added_or_expanded_events':len(graph['nodes'])-len(before['nodes']),'relations':len(relations),'cross_volume_relations':len(cross),'relation_kinds':dict(Counter(e['kind'] for e in relations)),'whole_book_threads':len(threads),'identity_hidden_threads':sum(t['kind']=='hidden' for t in threads),'person_dossiers':47,'focused_creative_profiles':13,'unresolved_identity_groups':1,'event_register':len(registered),'local_links_checked':checked_links,'missing_links':0,'original_source_hash_unchanged':True,'coverage_checkpoint_unchanged':True,'automatic_literary_approval':False,'git_push_performed':False}
(O/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
