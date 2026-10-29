"""按primary完整审阅意见精准改三边类型与一处矿工补证，不重生全稿。"""
from pathlib import Path
import json,copy
D=Path(__file__).resolve().parent
def read(n):return json.loads((D/n).read_text(encoding='utf-8'))
def write(n,x):(D/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
graph=read('graph.json')
ids=['e-geometry-training-feit-cost','e-siege-wall-mirror-counter','e-sealing-contract-beastking-rebirth']
changes=[]
for eid in ids:
    edge=next(x for x in graph['edges'] if x['id']==eid)
    assert edge['kind']=='cause'
    edge['kind']='setup'
    changes.append(dict(edge_id=eid,before='cause',after='setup'))
write('graph.json',graph)
analysis=read('analysis.json')
entry=next(x for x in analysis['dimensions']['characters'] if x['id']=='v04-distributed-work')
prototype=entry['fact']['evidence'][0]
added=[]
for target,kind in [(entry['fact'],'fact'),(entry['inference'],'inference'),(entry['mechanism'],'synthesis'),(entry,'synthesis')]:
    assert not any(x['chapter_id']=='ch-0699' and x['start_line']==58857 for x in target['evidence'])
    evidence=copy.deepcopy(prototype)
    evidence.update(chapter_id='ch-0699',start_line=58857,end_line=58857,claim_kind=kind)
    target['evidence'].append(evidence);added.append(evidence)
write('analysis.json',analysis)
path=D/'handoff.md'
text=path.read_text(encoding='utf-8')
assert '主审定向修订说明' not in text
text+='\n## 主审定向修订说明\n\n三条仅承接前置条件的图边已由cause收窄为setup：训练→菲特、攻墙→明镜对策、封印石交易→王战。训练没有直接导致死亡，采购也不证明引出了Boss；其余图字段及阅读笔记未重生。人物九维distributed-work补raw0699 L58857月光石实际采瑟银矿证据，原控制与分红定位保留。raw0725—0726范围的心如日月系统击杀已保留，不以早期存活阶段覆盖终稿。\n'
path.write_text(text,encoding='utf-8')
write('primary-delta-applied.json',dict(status='primary_requested_delta_applied',reviewer_request='primary',
    graph_edge_changes=changes,observation_id='v04-distributed-work',added_evidence=added,
    unchanged_reading_records=True,regenerated_other_fields=False,
    note='raw0725—0726范围的心如日月击杀已在成稿保留；此delta未改其事实。'))
print(json.dumps(dict(edges=changes,evidence_added=len(added),status='applied'),ensure_ascii=False))
