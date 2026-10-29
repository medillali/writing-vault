"""本轮阅读深化、链接与只读来源保护检查。"""
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote

P=Path(__file__).resolve().parent
R=P.parents[2]
V=R/'writing-vault'
O=V/'library/reports/zongheng-tianxia/atlas'
T=O/'tree'
SID='src-2a13958390274509b2af019f6b12d981'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
report_path=T/'reading-check.json'
report_path.write_text('{"status":"checking"}\n',encoding='utf-8')
baseline=read(P/'protected-baseline.json')
for name,expected in baseline.items():
    assert hashlib.sha256((R/name).read_bytes()).hexdigest()==expected,name
g=read(V/'library/sources'/SID/'plot-graph.json')
nodes={n['id']:n for n in g['nodes']}
m=read(T/'manifest.json')
narrative=read(T/'reading-guide.json')
assert narrative['source_id']==SID and narrative['graph_revision']==g['revision']==13
assert len(narrative['entries'])==51
assert all(id in narrative['entries'] for id in m['reading_guide']['node_ids'])
sys.path.insert(0,str(R/'distill-novels/scripts'))
from fictionlib.vault import Vault
vault=Vault(V)
sources={s['source_id']:s for s in vault.sources()}
fallback=vault._source
vault._source=lambda sid:sources[sid] if sid in sources else fallback(sid)
for id,n in narrative['entries'].items():
    assert nodes[id]['kind'] in {'event','scene'}
    assert all(isinstance(n[k],str) and n[k].strip() for k in ['title','stage','situation','action','consequence'])
    assert n['evidence']==nodes[id]['evidence']
    vault.validate_evidence(n['evidence'])
    assert all(other in m['events'] for other in n['branch_ids'])
revision=read(O/'editorial-manifest.json')['source_revision']
assert hashlib.sha256((V/'private-sources/normalized/sources'/SID/(revision+'.txt')).read_bytes()).hexdigest()==revision
assert len(m['events'])==260 and len(m['edges'])==227
assert len(m['reading_guide']['node_ids'])==31 and len(m['reading_guide']['edges'])==30
assert read(T/'integrity-check.json')['source_graph_unchanged']
browser=read(P/'viewer-check.json')
assert browser['passed']==13 and browser['failed']==0
assert not browser['javascript_errors'] and not browser['external_requests']
layout=read(T/'browser-check.json')
assert all(layout[k]==0 for k in ['text_overflow','node_overlap','edges_through_unrelated_nodes','external_requests','javascript_errors'])

valid_fragments=set(m['events'])|{t['id'] for t in g['threads']}|set(m['edges'])|{e['id'] for e in m['reading_guide']['edges']}
missing=[]
checked=0
for doc in O.rglob('*.md'):
    for target in re.findall(r'\]\((<[^>]+>|[^)]+)\)',doc.read_text(encoding='utf-8')):
        target=target.strip('<>')
        if re.match(r'^[A-Za-z][A-Za-z0-9+.-]*:',target):continue
        filename,_,anchor=target.partition('#')
        destination=(doc.parent/unquote(filename)).resolve() if filename else doc
        checked+=1
        if not destination.is_file():missing.append((str(doc.relative_to(V)),target))
        elif anchor:
            if destination==(T/'index.html').resolve():
                if anchor not in valid_fragments:missing.append((str(doc.relative_to(V)),target))
            elif anchor.startswith('event-') or destination==(O/'map.md').resolve():
                if f'id="{anchor}"' not in destination.read_text(encoding='utf-8'):missing.append((str(doc.relative_to(V)),target))
assert not missing,missing
report={'status':'valid','checked_at_utc':datetime.now(timezone.utc).isoformat(),'map_reading_version':3,'unique_events':260,'semantic_relations':227,'reading_order_is_separate':True,'main_reading_steps':31,'explained_events':51,'other_events_use_existing_summaries':209,'viewer_checks_passed':13,'layout_overflow_overlap_crossings':0,'local_links_checked':checked,'missing_links':missing,'protected_files_unchanged':len(baseline),'original_source_unchanged':True,'formal_graph_unchanged':True,'all_character_master_files_unchanged':True,'reading_checkpoint_unchanged':True,'narrative_evidence_matches_formal_events':True,'source_id':SID,'literary_approval':False,'remote_push_performed':False}
report_path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
