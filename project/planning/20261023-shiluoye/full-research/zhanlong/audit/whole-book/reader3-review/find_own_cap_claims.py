from common import A
import json
for p in sorted(A.glob('adjudications-local-v04-batch*.json')):
 for r in json.loads(p.read_text(encoding='utf-8')):
  t=r['rationale']
  if ('万' in t) and any(x in t for x in ['批示','建制申请','建制审批','军批','军团二十万','上限不等申请','上限批','申请军团']):
   print(p.name,r['candidate_id'],t)
