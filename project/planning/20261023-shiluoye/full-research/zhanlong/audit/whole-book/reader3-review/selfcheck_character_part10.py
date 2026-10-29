from character_arc_common import *
p=A/'reader3-character-arcs-part10.json';m=p.with_suffix('.md');b=p.read_bytes();mb=m.read_bytes();x=json.loads(b);r=x['characters'][2]
old=r['key_decisions'];new=old.replace('剑锋寒斩首','问剑、剑锋寒左右合斩');assert old!=new;r['key_decisions']=new
(P/'character-part10-selfcheck-before.json').write_bytes(b);(P/'character-part10-selfcheck-before.md').write_bytes(mb);dump(p,x);m.write_bytes(mb.decode('utf-8').replace(old,new).encode('utf-8'))
dump(P/'character-part10-selfcheck-delta.json',{'reason':'交primary前定向原文1381 L99312—39实读，明确问剑与剑锋寒共同斩首，不能漏一个行动者；仅一个字段。','before_sha256':hashlib.sha256(b).hexdigest(),'after_sha256':sha(p),'md_after_sha256':sha(m),'delta':[{'path':'/characters/2/key_decisions','before':old,'after':new}]})
v=P/'character-arcs-part10-validation.json';r=json.loads(v.read_text(encoding='utf-8'));r.update(sha256=sha(p),md_sha256=sha(m));dump(v,r);st=P/'character-arc-reader-state.json';s=json.loads(st.read_text(encoding='utf-8'));s['groups'][-1]=r;dump(st,s);print(json.dumps(r,ensure_ascii=False))
