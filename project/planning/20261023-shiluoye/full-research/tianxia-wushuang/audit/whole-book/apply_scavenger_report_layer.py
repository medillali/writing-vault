import json,copy,hashlib
from audit_evidence import H,render_characters
x=json.loads((H/'character-scavenger-report-layer-proposal.json').read_text(encoding='utf-8'));results=[]
for c in x['changes']:
 p=H/c['path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==c['input_sha256'];before=json.loads(p.read_text(encoding='utf-8'));after=copy.deepcopy(before);i=next(i for i,r in enumerate(after['characters']) if r['audit_id']==c['audit_id']);assert after['characters'][i]==c['before'];after['characters'][i]=c['after']
 assert all(a==b for n,(a,b) in enumerate(zip(before['characters'],after['characters'])) if n!=i)
 (H/'reviewed-batches'/f'{p.stem}-before-scavenger-report-layer.json').write_bytes(p.read_bytes());p.write_text(json.dumps(after,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');render_characters(p.with_suffix('.md').name,after['characters'],after['title'])
 results.append(dict(c,after_sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
x.update(status='applied_after_primary_semantic_approval',changes=results)
(H/'character-scavenger-report-layer-delta.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print([(r['path'],r['after_sha256']) for r in results])
