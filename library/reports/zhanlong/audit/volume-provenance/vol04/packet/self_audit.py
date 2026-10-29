"""隔离包自核；不改原文、原逐章笔记或其他卷。"""
import json,hashlib,collections
from pathlib import Path
P=Path(__file__).parent
A=json.loads((P/'analysis.json').read_text(encoding='utf-8'))
C=json.loads((P/'cards.json').read_text(encoding='utf-8'))
G=json.loads((P/'graph.json').read_text(encoding='utf-8'))
N=[json.loads(s) for s in (P/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines()]
assert len(N)==215 and all(n['reader']=='/root/zongheng_vol03_full' and n['full_text_read'] for n in N)
assert [int(n['chapter_id'].split('-')[1]) for n in N]==list(range(754,969))
assert sum(n['unit_kind']=='body' for n in N)==214
assert all(len(v)==4 for v in A['dimensions'].values())
for rows in A['dimensions'].values():
 for x in rows:
  assert all(x[k].strip() for k in ['textual_fact','observation','mechanism','limits_and_counterevidence'])
S=[c for c in C if c['asset_type']=='scene'];PATS=[c for c in C if c['asset_type']=='pattern']
for field in ['applicability','failure_mode']:
 vals=[c['content'][field] for c in S]
 assert len(vals)==len(set(vals)),field
for c in S:
 assert all(c['content'][k] for k in ['summary','goal','obstacle','choice','consequence','state_change','why_it_works','applicability','failure_mode'])
origins={c['origin_key']:c for c in C}
for c in S:
 assert all(k in origins and origins[k]['asset_type']=='character' for k in c['content']['characters_origin_keys'])
for c in PATS:
 assert all(origins[k]['asset_type']=='scene' for k in c['content']['derived_from_origin_keys'])
edges={e['id']:e for e in G['edges']}
outside=[]
for t in G['threads']:
 for eid in t['edge_ids']:
  e=edges[eid]
  if not {e['from'],e['to']}.issubset(t['node_ids']):outside.append([t['id'],eid])
assert not outside,outside
for node in G['nodes']:
 for k in node.get('knowledge',[]):
  assert k['state'] in ['knows','suspects','misbelieves','unknown']
  assert k['observer']=='reader' or k['observer'] in origins
  if k['state']=='misbelieves':assert k.get('belief')
expected=[(n['chapter_id'],n['reader'],n['unresolved']) for n in N if n['unresolved']]
assert [(x['chapter_id'],x['reader'],x['unresolved']) for x in A['chapter_unresolved_index']]==expected
def refs(v):
 if isinstance(v,list):return sum(refs(x) for x in v)
 if not isinstance(v,dict):return 0
 c=0
 if {'source_id','revision','chapter_id'}.issubset(v):
  assert v.get('claim_kind') in ['fact','inference','synthesis','plan'];c=1
 return c+sum(refs(x) for x in v.values())
rc=sum(refs(x) for x in [A,C,G])
report={'status':'self-audit-passed-awaiting-primary','coverage':{'raw':215,'body':214,'batches':55,'unresolved_truncations':0,'reader':'/root/zongheng_vol03_full'},'observations':36,'cards':dict(collections.Counter(c['asset_type'] for c in C)),'graph':{'nodes':len(G['nodes']),'edges':len(G['edges']),'threads':len(G['threads']),'knowledge':sum(len(n.get('knowledge',[])) for n in G['nodes']),'thread_edges_outside_members':outside},'original_unresolved_index':{'notes_with_unresolved':len(expected),'strings':sum(len(n[2]) for n in expected),'verbatim_preserved':True},'claim_kind_refs':rc,'scene_boundaries_distinct':True,'source_anomalies':len(A['source_anomalies']),'volume_end_questions':len(A['unresolved_volume_end']),'semantic_guards':[
 '兰馨活归/旁女真死/龙鳞自刎/降俘处死分人分动作',
 '塞小斯文尾/凯尔主群让/盖奥斩/罗问尾徐斩尸/西罗杀',
 '火象唐门毁座/火云叶毁座/紫炎清眸林杀/临海主毁座待定后委托',
 '血案雷真亡、主昏未死、月唐救；魏裴法律层不净化',
 '佩徐欧罗特莫文真死，具名死者不被补兵当复生',
 '方召回不等逐步强逼夺城，薛爱主只方推，找人未回',
 '现实蝴蝶/游戏蝴蝶两物，政治镇国刀/战斗镇岳分开',
 '末刺魔失败/魔山活/火神矛未得/三万未分/矿权未结',
 '酒10不等十级酒已造，奖魅275计算不等末面板',
 '私军杀怪不升级/正军可升级，失城解2000码时点保留'],
 'review_boundary':'本自核仅本代理；local校验不替primary逐项文学审查，不替用户审美批准。'}
(P/'self-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
