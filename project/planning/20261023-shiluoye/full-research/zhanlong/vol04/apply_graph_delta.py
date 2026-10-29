"""primary批准：只修一条后用边的目标、标签及三条证据。"""
import json,copy,hashlib
from pathlib import Path
P=Path(__file__).parent;D=P/'primary-delta'
f=P/'graph.json';raw=f.read_bytes();G=json.loads(raw);O=copy.deepcopy(G)
b=D/'graph.before-equipment-edge.json';assert not b.exists();b.write_bytes(raw)
e=next(e for e in G['edges'] if e['id']=='e-equipmentshield');before=copy.deepcopy(e)
assert e['from']=='s-deer' and e['to']=='s-serin' and e['kind']=='payoff'
e['to']='s-riverwar';e['label']='761英雄盔实戴，778/781免晕在敌控中实际验证；不是持有即全程无伤。'
base=e['evidence'][0]
e['evidence']=[{'source_id':base['source_id'],'revision':base['revision'],'chapter_id':f'ch-{n:04d}','start_line':a,'end_line':b,'claim_kind':'inference'} for n,a,b in [(761,59291,59410),(778,60429,60480),(781,60584,60649)]]
test=copy.deepcopy(G);i=next(i for i,x in enumerate(test['edges']) if x['id']==e['id']);test['edges'][i]=before
assert test==O
f.write_text(json.dumps(G,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
r={'status':'applied-primary-approved','scope':'仅e-equipmentshield目标/label/evidence；from/kind/其他边/全部线程及其他值不动','before':before,'after':e,'before_sha256':hashlib.sha256(raw).hexdigest(),'after_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'basis':'primary 2026-10-26 同意精准修订及三段定位'}
(D/'equipment-edge-delta.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(D/'delta.md').write_text((D/'delta.md').read_text(encoding='utf-8')+'\n后续独立第7处经primary批准：e-equipmentshield由deer→serin改deer→riverwar，改标签/证据761/778/781。其他图值/全部线程不动。独立before与delta见graph.before-equipment-edge.json及equipment-edge-delta.json；先前receipt的graph unchanged指此独立修订前阶段。\n',encoding='utf-8')
print(json.dumps({'graph_after_sha256':r['after_sha256'],'delta_sha256':hashlib.sha256((D/'equipment-edge-delta.json').read_bytes()).hexdigest()},ensure_ascii=False))
