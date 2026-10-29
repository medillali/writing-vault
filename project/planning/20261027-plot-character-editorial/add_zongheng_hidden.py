"""把已核对的身份暗线接入主图；先有人物判断，再有后证。"""
import copy
import json
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'distill-novels/scripts'))
from fictionlib.vault import Vault
from fictionlib.graph import save_graph, validate_graph
V=ROOT/'writing-vault'
SID='src-2a13958390274509b2af019f6b12d981'
O=V/'library/reports/zongheng-tianxia/atlas'
mf=json.loads((O/'editorial-manifest.json').read_text(encoding='utf-8'))
g=json.loads((V/'library/sources'/SID/'plot-graph.json').read_text(encoding='utf-8'))
old=copy.deepcopy(g)
nm={n['id']:n for n in g['nodes']}
revision=mf['source_revision']
nid='editorial-mentor-missing'
node={'id':nid,'parent_id':'v7-v07-root','kind':'scene','narrative_order':915,'title':'冰兰的旧师之谜：死亡判断与缺尸疑点并存','summary':'冰兰依据传承判断明宇已死，却仍感觉其气息；当年的六具尸骸不包含明宇与亚兰。她请书生查寒冰结界，判断、希望与可见证据不能合成一个已经证实的死亡事实。','claim_kind':'fact','evidence':[{'source_id':SID,'revision':revision,'chapter_id':'ch-0915','start_line':102358,'end_line':102370,'claim_kind':'fact'}],'characters':[mf['profile_assets'][k]['asset_id'] for k in ['character-arc-01','character-arc-07']]}
g['nodes']=[n for n in g['nodes'] if n['id']!=nid]
position=next(i for i,n in enumerate(g['nodes']) if n['id']=='v7-v07-aryan')
g['nodes'].insert(position,node)
nm[nid]=node
new_edges=[
 {'id':'editorial-annie-identity','from':'v4-v04-linkforge','to':'v5-v05-scene-annie-reversal','kind':'reveal','label':'被当作已死的旧女王，后来以霜之剑刃和菲雅姐姐的身份出现','summary':'林克握住记忆权杖误认安妮归来；后来的战场身份揭露更新了主角对于安妮命运的认识，却不会使此前的误认变成真人重逢。','claim_kind':'inference','evidence':[{'source_id':SID,'revision':revision,'chapter_id':'ch-0401','start_line':39621,'end_line':39662,'claim_kind':'fact'},{'source_id':SID,'revision':revision,'chapter_id':'ch-0529','start_line':55196,'end_line':55206,'claim_kind':'fact'}]},
 {'id':'editorial-mentor-identity','from':nid,'to':'v8-v08-bloodroar','kind':'reveal','label':'失踪旧师现身，先前的死亡判断被后证更新','summary':'缺尸与气息形成调查疑点，后来明宇现身并以月哀重创冰兰；不能在两端之间补造一次没有被展示的先死亡后复活过程。','claim_kind':'inference','evidence':node['evidence']+nm['v8-v08-bloodroar']['evidence']}
]
for e in new_edges:
    g['edges']=[x for x in g['edges'] if x['id']!=e['id']]+[e]
threads=[
 {'id':'editorial-hidden-annie','title':'安妮身份：旧女王、敌军领袖与保护妹妹的行动','kind':'hidden','status':'resolved','node_ids':['v4-v04-linkforge','v5-v05-scene-annie-reversal','v8-v08-capture','v8-v08-cleanse'],'edge_ids':['editorial-annie-identity'],'resolution_note':'身份与控制处境得到揭露及净化后证；不将其等同林克真人重逢或过去后果被取消。'},
 {'id':'editorial-hidden-mentor','title':'明宇身份：传承死亡判断、缺尸疑点与现身','kind':'hidden','status':'resolved','node_ids':[nid,'v7-v07-aryan','v8-v08-bloodroar','v8-v08-endbattle'],'edge_ids':['editorial-mentor-identity'],'resolution_note':'现身和终战寂灭分别更新身份与存死；早期人物判死仍保原认知。'}
]
for t in threads:
    g['threads']=[x for x in g['threads'] if x['id']!=t['id']]+[t]
vault=Vault(V)
sources={s['source_id']:s for s in vault.sources()}
fallback=vault._source
vault._source=lambda sid: sources[sid] if sid in sources else fallback(sid)
validate_graph(g,vault)
saved=save_graph(vault,'source',SID,g,old['revision'])
mf['graph_revision']=saved['revision']
mf['bridge_ids']=sorted(set(mf['bridge_ids'])|{e['id'] for e in new_edges})
mf['focus_node_ids']=sorted(set(mf['focus_node_ids'])|{nid})
(O/'editorial-manifest.json').write_text(json.dumps(mf,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'graph_revision':saved['revision'],'identity_threads_added':2,'relations_added':2,'targeted_identity_evidence_verified':True},ensure_ascii=False))
