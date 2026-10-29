"""只读正式资料库，校验本批证据和草稿结构；结果仅写本批目录。"""
import copy
import json
import sys
from collections import Counter
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[2]
sys.path.insert(0, str(ROOT / 'distill-novels/scripts'))
from fictionlib.vault import Vault, ASSET_FIELDS
from fictionlib.graph import validate_graph

source = json.loads((BASE.parent/'zongheng-tianxia/source.json').read_text(encoding='utf-8-sig'))
lookup = {c['chapter_id']:c for c in source['chapters']}
read_ids = [source['chapters'][i]['chapter_id'] for i in range(50,101)]
data = {name:json.loads((BASE/name).read_text(encoding='utf-8')) for name in ('cards.json','analysis.json','graph.json','read-log.json')}
log = data['read-log.json']
assert log['fully_read_chapter_count']==51
assert log['complete_book'] is False
assert [c['chapter_id'] for c in log['chapters']]==read_ids
for c in log['chapters']:
    assert c['full_text_read'] is True
    assert c['start_line']==lookup[c['chapter_id']]['start_line']
    assert c['end_line']==lookup[c['chapter_id']]['end_line']
assert data['analysis.json']['read_chapter_ids']==read_ids
assert set(data['analysis.json']['dimensions'])=={'worldbuilding','characters','plot','style','narrative','dialogue','pacing','themes','continuity'}
evidence_count = 0
def walk(obj):
    global evidence_count
    if isinstance(obj,dict):
        if {'source_id','revision','chapter_id','claim_kind'}<=set(obj):
            assert obj['source_id']==source['source_id'] and obj['revision']==source['revision']
            assert obj['chapter_id'] in read_ids
            c=lookup[obj['chapter_id']]
            assert c['start_line']<=obj['start_line']<=obj['end_line']<=c['end_line']
            assert obj['claim_kind'] in {'fact','inference','synthesis','plan'}
            evidence_count+=1
        for v in obj.values(): walk(v)
    elif isinstance(obj,list):
        for v in obj:walk(v)
walk(data)

cards=data['cards.json']
keys={c['origin_key']:c for c in cards}
assert len(keys)==len(cards)
counts=Counter(c['asset_type'] for c in cards)
assert counts['character']>=6 and counts['scene']>=6 and counts['pattern']>=4
vault=Vault(ROOT/'writing-vault')
for c in cards:
    assert set(c)<=ASSET_FIELDS
    assert c['review_status']=='draft' and c['user_notes']=='' and c['favorite'] is False
    assert c['origin_key'].startswith(source['source_id']+'/vol02-20261023/')
    assert {'作者:失落叶','作品:网游之纵横天下'}<=set(c['tags'])
    vault._validate_asset(copy.deepcopy(c))
    if c['asset_type']=='pattern':
        refs=c['content']['derived_from_origin_keys']
        assert refs and all(keys[k]['asset_type']=='scene' for k in refs)
graph=data['graph.json']
validate_graph(graph,vault)
assert len(graph['coverage'])==1 and graph['coverage'][0]['complete'] is False
assert graph['coverage'][0]['chapter_ids']==read_ids
for n in graph['nodes']:
    if n.get('asset_origin_key'):assert keys[n['asset_origin_key']]['asset_type']=='scene'
    for k in n.get('character_origin_keys',[]):assert keys[k]['asset_type']=='character'

result={'valid':True,'fully_read_chapters':51,'range':'ch-0051—ch-0101 / L3567—6700',
 'counts':dict(counts),'graph_nodes':len(graph['nodes']),'graph_edges':len(graph['edges']),
 'evidence_references_checked_including_repeated':evidence_count,
 'checks':['JSON读取','九维键','连续51章与全文标记','来源修订/章节/行号边界','官方卡片验证器只读检查','官方图验证器只读检查','卡片稳定键唯一与标签','机制到场景引用','图卡片origin_key引用','全书complete=false','用户字段draft且未填评价'],
 'limits':['边界和结构验证不等于文学解释正确','不计入未读第101章后的原文','未运行正式入库、生成视图、提交或推送']}
(BASE/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
