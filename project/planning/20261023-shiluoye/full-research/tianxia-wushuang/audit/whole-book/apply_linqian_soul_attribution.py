import json,hashlib,copy
from audit_evidence import H,render_characters
proposal=json.loads((H/'character-linqian-soul-attribution-proposal.json').read_text(encoding='utf-8'))
results=[]
for change in proposal['changes']:
 p=H/change['path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==change['input_sha256']
 before=json.loads(p.read_text(encoding='utf-8'));after=copy.deepcopy(before)
 ix=next(i for i,x in enumerate(after['characters']) if x['audit_id']==change['audit_id'])
 assert after['characters'][ix]==change['before'];after['characters'][ix]=change['after']
 (H/'reviewed-batches'/f'{p.stem}-before-linqian-soul-attribution.json').write_bytes(p.read_bytes())
 p.write_text(json.dumps(after,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 render_characters(p.with_suffix('.md').name,after['characters'],after['title'])
 assert all(a==b for i,(a,b) in enumerate(zip(before['characters'],after['characters'])) if i!=ix)
 results.append(dict(path=change['path'],audit_id=change['audit_id'],before_sha256=change['input_sha256'],after_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),changed_fields=change['changed_fields'],before=change['before'],after=change['after']))
out=dict(status='applied_after_primary_semantic_approval',approval='root消息批准逐值proposal，仅69/88相应字段，不等用户审美批准。',changes=results)
(H/'character-linqian-soul-attribution-delta.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print([(x['path'],x['after_sha256']) for x in results])
