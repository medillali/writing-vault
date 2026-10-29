"""分卷研究的入库前定位/覆盖/引用检查，不替代文学审查。"""
import pathlib,json,sys,functools,uuid,copy,collections
ROOT=pathlib.Path(__file__).resolve().parents[3];WORK=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'distill-novels/scripts'))
from fictionlib.vault import Vault
from fictionlib.graph import validate_graph
def read(path):return json.loads(path.read_text(encoding='utf-8'))
def rewrite(value,mapping):
    if isinstance(value,dict):return {k:rewrite(v,mapping) for k,v in value.items()}
    if isinstance(value,list):return [rewrite(v,mapping) for v in value]
    return mapping.get(value,value) if isinstance(value,str) else value
def load_and_check(book,volume):
    source=read(WORK/book/'source.json');sid=source['source_id'];rev=source['revision']
    spec=next(v for v in source['volumes'] if v['volume']==volume);directory=WORK/book/f'vol{volume:02d}'
    analysis=read(directory/'analysis.json');cards=read(directory/'cards.json');cards=cards['cards'] if isinstance(cards,dict) else cards
    graph=read(directory/'graph.json');log=read(directory/'read-log.json')
    expected={c['chapter_id'] for u in spec['units'] for c in u['segments']};chapters={c['chapter_id']:c for c in source['chapters']}
    assert analysis['source_id']==sid and analysis['revision']==rev
    assert log['source_id']==sid and log['revision']==rev
    assert set(analysis['read_chapter_ids'])==expected and len(analysis['read_chapter_ids'])==len(expected)
    assert set(c['chapter_id'] for c in log['chapters'])==expected and len(log['chapters'])==len(expected)
    assert log['complete_book'] is False
    for c in log['chapters']:
        original=chapters[c['chapter_id']]
        assert c['full_text_read'] is True and (c['start_line'],c['end_line'])==(original['start_line'],original['end_line'])
    notes=[json.loads(line) for line in (directory/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines() if line.strip()]
    assert len(notes)==len(expected) and {c['chapter_id'] for c in notes}==expected
    assert all(c['full_text_read'] is True for c in notes)
    state=read(directory/'reader-state.json')
    assert state['source_id']==sid and state['revision']==rev
    assert set(state.get('completed_chapter_ids',state.get('read_chapter_ids',[])))==expected
    assert not state.get('pending_chapter_ids')
    assert all(not state.get(k) for k in ['unresolved_truncations','pending_truncations','truncated_pending'])
    required={'worldbuilding','characters','plot','style','narrative','dialogue','pacing','themes','continuity'}
    assert required.issubset(analysis['dimensions'])
    for dimension in required:
        entries=analysis['dimensions'][dimension]
        if isinstance(entries,dict):entries=entries.get('observations',[])
        assert len(entries)>=3,(dimension,len(entries))
    assert cards and len({c['origin_key'] for c in cards})==len(cards)
    mapping={c['origin_key']:c.get('asset_id') or {'character':'chr','scene':'scn','pattern':'pat'}[c['asset_type']]+'-'+uuid.uuid5(uuid.NAMESPACE_URL,c['origin_key']).hex for c in cards}
    overlay={mapping[c['origin_key']]:c for c in cards}
    vault=Vault(ROOT/'writing-vault');vault._source=functools.lru_cache(maxsize=None)(vault._source)
    original_get=vault._get_asset;vault._get_asset=lambda aid,revision=None:overlay[aid] if aid in overlay else original_get(aid,revision)
    evidence_count=0
    def evidence_check(value):
        nonlocal evidence_count
        if isinstance(value,list):
            for item in value:evidence_check(item)
        elif isinstance(value,dict):
            if {'source_id','revision','chapter_id'}.issubset(value):
                assert value['source_id']==sid and value['revision']==rev and value['chapter_id'] in expected,value
                vault.validate_evidence([value]);evidence_count+=1
            for child in value.values():evidence_check(child)
    for card in cards:
        assert card['origin_key'].startswith(sid+f'/full-20261025/vol{volume:02d}/')
        assert card['content']['summary'] and card['evidence']
        assert {'作者:失落叶','作品:'+{'zongheng-tianxia':'网游之纵横天下','tianxia-wushuang':'网游之天下无双','zhanlong':'斩龙'}[book]}.issubset(card['tags'])
        assert card.get('review_status','draft')=='draft' and not card.get('user_notes') and not card.get('favorite',False)
        assert card['scope']==('reusable-pattern' if card['asset_type']=='pattern' else 'source-analysis')
        for origin in card['content'].get('derived_from_origin_keys',[]):assert origin in mapping and overlay[mapping[origin]]['asset_type']!='pattern'
    for content in [analysis,cards,graph]:evidence_check(content)
    graph=rewrite(copy.deepcopy(graph),mapping);graph['owner']={'kind':'source','id':sid}
    for node in graph['nodes']:
        if 'character_origin_keys' in node:node['characters']=node.pop('character_origin_keys')
        if 'asset_origin_key' in node:node['asset_id']=node.pop('asset_origin_key')
    assert {cid for c in graph['coverage'] for cid in c['chapter_ids']}==expected
    assert all(c['source_id']==sid and c['revision']==rev and c['complete'] is False for c in graph['coverage'])
    validate_graph(graph,vault)
    counts=dict(collections.Counter(c['asset_type'] for c in cards))
    assert counts.get('character',0)>=8 and counts.get('scene',0)>=12 and counts.get('pattern',0)>=6,counts
    result={'book':book,'volume':volume,'indexed_segments_read':len(expected),'body_units_read':spec['body_units'],'cards':counts,'evidence_references_checked':evidence_count,'nodes':len(graph['nodes']),'edges':len(graph['edges']),'threads':len(graph['threads']),'preflight':'passed'}
    return source,spec,directory,analysis,cards,graph,mapping,result
if __name__=='__main__':
    sys.stdout.reconfigure(encoding='utf-8');print(json.dumps(load_and_check(sys.argv[1],int(sys.argv[2]))[-1],ensure_ascii=False))
