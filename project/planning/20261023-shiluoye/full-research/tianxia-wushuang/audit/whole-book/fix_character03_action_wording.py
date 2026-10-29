import copy,hashlib,json
from audit_evidence import H,render_characters
p=H/'character-arcs-part03.json';raw=p.read_bytes();assert hashlib.sha256(raw).hexdigest()=='a9477bf0f4e259b0532d5658e01cabfdd01b9926604a8092fdad0d60988c8270'
a=json.loads(raw);b=copy.deepcopy(a)
for x in b['characters']:
 if x['audit_id']=='character-arc-33':x['key_decisions']=x['key_decisions'].replace('1380切磋败伪主并付赌款','1380切磋败给伪装陆后付赌款')
 if x['audit_id']=='character-arc-32':x['evidence_boundaries']=x['evidence_boundaries'].replace('1371被强吻者周小萌','1371遭强吻企图者周小萌')
assert sum(x!=y for x,y in zip(a['characters'],b['characters']))==2
(H/'reviewed-batches'/'character-arcs-part03-before-action-wording-delta.json').write_bytes(raw)
p.write_text(json.dumps(b,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');sha=hashlib.sha256(p.read_bytes()).hexdigest()
(H/'character03-action-wording-delta.json').write_text(json.dumps(dict(before_sha256=hashlib.sha256(raw).hexdigest(),after_sha256=sha,unchanged_other_characters=14,deltas=[dict(audit_id=x['audit_id'],before=x,after=y) for x,y in zip(a['characters'],b['characters']) if x!=y],source_check='本代理BEGIN-END全文复读1380，L109662—109668陆赢、十万款到、切磋无损。'),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
render_characters('character-arcs-part03.md',b['characters'],b['title']);print(sha)
