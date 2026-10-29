import copy,hashlib,json
from audit_evidence import H,evidence,render_characters
p=H/'character-arcs-part02.json';raw=p.read_bytes();assert hashlib.sha256(raw).hexdigest()=='60b48eb91dcbdc7a4a117fa2c870a00526246aa2f53376b1e5b85ed1928c92f1'
a=json.loads(raw);b=copy.deepcopy(a);x=next(x for x in b['characters'] if x['name']=='月光石');x['key_decisions']=x['key_decisions'].replace('回古继续法核','1413原文明述重回古剑、继续法核');x['evidence']=evidence([int(e['chapter_id'][3:]) for e in x['evidence']]+[1413])
(H/'reviewed-batches'/'character-arcs-part02-before-explicit-return.json').write_bytes(raw)
p.write_text(json.dumps(b,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');sha=hashlib.sha256(p.read_bytes()).hexdigest();render_characters('character-arcs-part02.md',b['characters'],b['title'])
(H/'character02-moon-return-delta.json').write_text(json.dumps(dict(before_sha256=hashlib.sha256(raw).hexdigest(),after_sha256=sha,audit_id=x['audit_id'],added_explicit_return_chapter='ch-1413',unchanged_other_characters=17),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(sha)
