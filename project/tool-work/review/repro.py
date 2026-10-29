import sys
from pathlib import Path
sys.path[:0] = [str(Path(__file__).resolve().parents[2] / 'scripts'), str(Path(__file__).resolve().parents[2] / 'tests')]
from support import VaultCase
from test_graph import graph_sample
from fictionlib.exchange import export_bundle, import_changes, backup, restore
from fictionlib.graph import save_graph, graph_path, render_graph
from fictionlib.storage import read_json, json_text
from html.parser import HTMLParser

t = VaultCase()
t.setUp()
try:
    v=t.vault
    a=v.put_asset(t.card())
    v.put_asset({'asset_id':a['asset_id'],'title':'version 2'},1)
    b=v.put_asset(t.card(asset_type='pattern',scope='reusable-pattern',title='derived',derived_from=[{'asset_id':a['asset_id'],'revision':1}]))
    bundle=export_bundle(v,t.root/'export')
    print('Export assets:',[(x['asset_id'],x['revision']) for x in bundle['assets']])
    try: print('Unmodified template:',import_changes(v,read_json(t.root/'export/changes-template.json')))
    except ValueError as e: print('Unmodified template rejected:',str(e))
    p=v.create_project('Unrelated private project')
    g=save_graph(v,'project',p['project_id'],graph_sample())
    scoped=export_bundle(v,t.root/'scoped',asset_ids=[b['asset_id']])
    print('Unrelated graphs in --asset bundle:',[x['owner'] for x in scoped['graphs']])
    graphfile=v.root/graph_path('project',p['project_id'])
    g['edges'][0]['to']='missing'
    graphfile.write_text(json_text(g),encoding='utf-8')
    print('Dangling graph validate:',v.validate())
    backup(v,t.root/'broken.zip')
    print('Dangling graph restore:',restore(t.root/'broken.zip',t.root/'restored'))
    data=graph_sample()
    data['nodes'][0]['title']='@@DATA@@'
    data['nodes'][1]['title']=' onmouseover=alert(1) '
    render_graph(data,t.root/'view')
    class P(HTMLParser):
        def handle_starttag(self,tag,attrs):
            bad=[x for x in attrs if x[0].startswith('on')]
            if bad: print('ACTIVE EVENT ATTR:',tag,bad)
    P().feed((t.root/'view/index.html').read_text(encoding='utf-8'))
finally:
    t.doCleanups()
