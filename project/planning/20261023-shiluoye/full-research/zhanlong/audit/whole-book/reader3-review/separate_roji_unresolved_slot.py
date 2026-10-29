from character_arc_common import *
p=A/'reader3-character-arcs-part08.json';m=p.with_suffix('.md');b=p.read_bytes();bm=m.read_bytes();x=json.loads(b)
assert x['characters'][0]['audit_id']=='character-arc-r3-046'
slot=x['characters'].pop(0);x['unresolved_roster_names']=[slot];x['confirmed_character_count']=6;x['unresolved_roster_name_count']=1
(P/'character-part08-before-separate-unresolved.json').write_bytes(b);(P/'character-part08-before-separate-unresolved.md').write_bytes(bm)
dump(p,x);text=bm.decode('utf-8').replace('## character-arc-r3-046 罗戟','## 未决名词槽 character-arc-r3-046 罗戟（不计确认人物）');m.write_bytes(text.encode('utf-8'))
dump(P/'character-part08-separate-unresolved-delta.json',{'reason':'primary明确无源候选独立未决名词，不放确认characters；原槽判断逐值不变。','before_sha256':hashlib.sha256(b).hexdigest(),'after_sha256':sha(p),'moved_audit_id':slot['audit_id'],'from':'/characters/0','to':'/unresolved_roster_names/0','confirmed_characters':6,'unresolved_names':1})
v=P/'character-arcs-part08-validation.json';r=json.loads(v.read_text(encoding='utf-8'));r.update(sha256=sha(p),md_sha256=sha(m),characters=6,unresolved_names=1);dump(v,r)
st=P/'character-arc-reader-state.json';s=json.loads(st.read_text(encoding='utf-8'));s['groups'][-1]=r;dump(st,s);print(json.dumps(r,ensure_ascii=False))
