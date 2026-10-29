import copy,hashlib,json
from audit_evidence import H,render_characters
p=H/'character-arcs-part02.json';raw=p.read_bytes();assert hashlib.sha256(raw).hexdigest()=='c08516e592fe83c82984270fdf7d5590f5eed9ca140789456f81b89c99243394'
a=json.loads(raw);b=copy.deepcopy(a)
for x in b['characters']:
 if x['audit_id']=='character-arc-18':x['key_decisions']=x['key_decisions'].replace('825为唯一哥哥离古入烛','837为唯一哥哥离古入烛')
 if x['audit_id']=='character-arc-29':x['key_decisions']=x['key_decisions'].replace('早争第三城/夺资源','早争领地/夺资源')
assert sum(x!=y for x,y in zip(a['characters'],b['characters']))==2
(H/'reviewed-batches'/'character-arcs-part02-before-stage-locator-delta.json').write_bytes(raw)
p.write_text(json.dumps(b,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');sha=hashlib.sha256(p.read_bytes()).hexdigest()
deltas=[dict(audit_id=x['audit_id'],before=x,after=y) for x,y in zip(a['characters'],b['characters']) if x!=y]
(H/'character02-stage-locator-delta.json').write_text(json.dumps(dict(before_sha256=hashlib.sha256(raw).hexdigest(),after_sha256=sha,unchanged_other_characters=16,deltas=deltas,name_check='孙青青保原名；本代理BEGIN-END全文读0042，L4077本人自介；另全文读1082明确该章梦境不作唯一姓名来源。'),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
render_characters('character-arcs-part02.md',b['characters'],b['title']);print(sha)
