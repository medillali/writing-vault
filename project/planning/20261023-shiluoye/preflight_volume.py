"""入库前只读检查完整阅读日志、卡片证据、派生引用及图结构。"""
import pathlib,json,sys,copy,uuid,functools,collections
sys.stdout.reconfigure(encoding='utf-8')
root=pathlib.Path(__file__).resolve().parents[2];sys.path.insert(0,str(root/'distill-novels/scripts'))
from fictionlib.vault import Vault
from fictionlib.graph import validate_graph
vol=int(sys.argv[1]) if len(sys.argv)>1 else 1
work=root/'.planning/20261023-shiluoye'/('zongheng-tianxia' if vol==1 else f'zongheng-tianxia-vol{vol:02d}')
def read(p):return json.loads(p.read_text(encoding='utf-8'))
src=read(root/'.planning/20261023-shiluoye/zongheng-tianxia/source.json');sid=src['source_id'];rev=src['revision']
analysis=read(work/'analysis.json');cards=read(work/'cards.json');cards=cards.get('cards') if isinstance(cards,dict) else cards
graph=read(work/'graph.json');log=read(work/'read-log.json')
start,end={1:(2,50),2:(51,101)}[vol];expected={f'ch-{n:04d}' for n in range(start,end+1)}
assert set(analysis['read_chapter_ids'])==expected and len(analysis['read_chapter_ids'])==len(expected)
assert set(c['chapter_id'] for c in log['chapters'])==expected and len(log['chapters'])==len(expected)
chapters={c['chapter_id']:c for c in src['chapters']}
for c in log['chapters']:
    assert c['full_text_read'] is True
    assert (c['start_line'],c['end_line'])==(chapters[c['chapter_id']]['start_line'],chapters[c['chapter_id']]['end_line'])
assert log['complete_book'] is False
assert len(set(c['origin_key'] for c in cards))==len(cards)
origin={c['origin_key']:c.get('asset_id') or {'character':'chr','scene':'scn','pattern':'pat'}[c['asset_type']]+'-'+uuid.uuid5(uuid.NAMESPACE_URL,c['origin_key']).hex for c in cards}
overlay={origin[c['origin_key']]:c for c in cards}
v=Vault(root/'writing-vault');v._source=functools.lru_cache(maxsize=None)(v._source)
original_get=v._get_asset
v._get_asset=lambda aid,revision=None:overlay[aid] if aid in overlay else original_get(aid,revision)
evidence_count=0
def check_evidence(data):
    global evidence_count
    if isinstance(data,list):
        for item in data:check_evidence(item)
    elif isinstance(data,dict):
        if {'source_id','revision','chapter_id'}.issubset(data):
            assert data['source_id']==sid and data['revision']==rev and data['chapter_id'] in expected,data
            v.validate_evidence([data]);evidence_count+=1
        for val in data.values():check_evidence(val)
for c in cards:
    assert c['content']['summary'] and c['evidence']
    assert {'作者:失落叶','作品:网游之纵横天下'}.issubset(c['tags'])
    assert c.get('review_status','draft')=='draft' and not c.get('user_notes') and not c.get('favorite',False)
    for key in c['content'].get('derived_from_origin_keys',[]):assert key in origin,key
    if c['asset_type']=='pattern':assert c['scope']=='reusable-pattern'
    else:assert c['scope']=='source-analysis'
check_evidence(cards);check_evidence(graph);check_evidence(analysis)
def replace_refs(data):
    if isinstance(data,dict):return {k:replace_refs(val) for k,val in data.items()}
    if isinstance(data,list):return [replace_refs(val) for val in data]
    if isinstance(data,str) and data in origin:return origin[data]
    return data
graph=replace_refs(graph)
assert all(c['source_id']==sid and c['revision']==rev and c['complete'] is False for c in graph['coverage'])
assert {cid for c in graph['coverage'] for cid in c['chapter_ids']}==expected
graph['owner']={'kind':'source','id':sid}
validate_graph(graph,v)
print(json.dumps({'volume':vol,'read_chapters':len(expected),'cards':dict(collections.Counter(c['asset_type'] for c in cards)),'evidence_ranges_checked':evidence_count,'nodes':len(graph['nodes']),'edges':len(graph['edges']),'threads':len(graph['threads']),'preflight':'passed'},ensure_ascii=False))
