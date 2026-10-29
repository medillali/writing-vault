import json,hashlib
from pathlib import Path
P=Path(__file__).parent;load=lambda p:json.loads(p.read_text(encoding='utf-8'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
p=P/'adjudications-local-note-v03-part09.json'
assert sha(p)=='0db53bcf242023b5653f4c8147451dced559a742cbeb8f2f4efc3f4c4ab44860'
s=P/'primary-before';baseline=s/'v03-part09-before-blue-contract-328.json'
assert sha(baseline)=='c63956d6c8288629948efd8581cc17fccd0b44f1cce916010a2b1bffbd0c22d0'
old=load(baseline);new=[r for r in load(P/'adjudications-local-note-v03.json') if 324<=r['original_index']<360]
diff=[(a,b) for a,b in zip(old,new) if a!=b];assert len(old)==len(new)==81 and len(diff)==1
a,b=diff[0];assert a['candidate_id']==b['candidate_id']=='v03-local-notes-unresolved-328-02'
assert a['status']==b['status']=='partial' and a['original_record']==b['original_record']
p.write_text(json.dumps(new,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
d={'reason':'root指定并已完整复核857四栏：蓝星在857新项目已正式签约；旧581协议是否同份/细则未全仍分层，不可全书笼统说蓝星未签。','candidate_id':a['candidate_id'],'before':a,'after':b,'other_rows_unchanged':80,'new_part_sha256':sha(p)}
q=P/'primary-delta-v03-part09.json';q.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'part_sha256':sha(p),'delta_sha256':sha(q)},ensure_ascii=False))
