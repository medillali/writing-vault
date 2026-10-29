import json,hashlib
from pathlib import Path
P=Path(__file__).parent
load=lambda p:json.loads(p.read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
q=P/'adjudications-local-note-v03-part05.json'
assert sha(q)=='a2db25290034b618c7ce26b8f97a169fa14452d5907c8f08d384d88b86dc626f'
old=load(q);new=[r for r in load(P/'adjudications-local-note-v03.json') if 168<=r['original_index']<216]
diff=[(a,b) for a,b in zip(old,new) if a!=b]
assert len(old)==len(new)==93 and len(diff)==1
a,b=diff[0];assert a['candidate_id']==b['candidate_id']=='v03-local-notes-unresolved-175-01'
assert a['original_record']==b['original_record'] and a['status']==b['status']=='answered'
s=P/'primary-before';s.mkdir(exist_ok=True)
(s/'v03-part05-before-anchor-175.json').write_bytes(q.read_bytes())
q.write_text(json.dumps(new,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
d={'reason':'root完整复核342/370后指定：千幻+雷厉→千冰在370；342是龙岩火球+诛刃→斩龙。仅更正175-01理由和后证定位。','candidate_id':a['candidate_id'],'before':a,'after':b,'unchanged_other_rows':92,'new_part_sha256':sha(q)}
p=P/'primary-delta-v03-part05.json';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'part_sha256':sha(q),'delta_sha256':sha(p),'before_path':str(s/'v03-part05-before-anchor-175.json')},ensure_ascii=False))
