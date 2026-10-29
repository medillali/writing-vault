import json,copy,hashlib
from audit_evidence import H,render_characters
x=json.loads((H/'character-qingkong-first-person-proposal.json').read_text(encoding='utf-8'));p=H/x['path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==x['input_sha256']
before=json.loads(p.read_text(encoding='utf-8'));after=copy.deepcopy(before);i=next(i for i,r in enumerate(after['characters']) if r['audit_id']==x['audit_id']);assert after['characters'][i]==x['before'];after['characters'][i]=x['after'];assert all(a==b for n,(a,b) in enumerate(zip(before['characters'],after['characters'])) if n!=i)
(H/'reviewed-batches/character-arcs-part02-before-qingkong-first-person.json').write_bytes(p.read_bytes());p.write_text(json.dumps(after,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');render_characters(p.with_suffix('.md').name,after['characters'],after['title'])
x.update(status='applied_after_primary_semantic_approval',after_sha256=hashlib.sha256(p.read_bytes()).hexdigest());(H/'character-qingkong-first-person-delta.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(x['after_sha256'])
