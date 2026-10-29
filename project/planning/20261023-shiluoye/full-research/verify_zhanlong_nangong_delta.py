"""主审对已批准单对象纠正独立重放；不新增正文阅读。"""
from pathlib import Path
import json, hashlib
B=Path(__file__).parent/'zhanlong/audit/whole-book'
D=B/'local-v02-v05-review'
p=json.loads((D/'nangong-membership-and-sword-growth-proposal.json').read_text(encoding='utf-8'))['changes'][0]
before=json.loads((D/'history/batch003-before-nangong-membership.json').read_text(encoding='utf-8'))
now=json.loads((D/'adjudications-local-v02-batch003.json').read_text(encoding='utf-8'))
assert hashlib.sha256((D/'history/batch003-before-nangong-membership.json').read_bytes()).hexdigest()==p['input_sha256']
assert len(before)==len(now)==20
idx=[i for i,x in enumerate(before) if x['candidate_id']==p['candidate_id']]
assert len(idx)==1 and before[idx[0]]==p['before']
before[idx[0]]=p['after']
assert before==now
print(json.dumps(dict(exact_only_approved_object=True,after=p['after'],sha256=hashlib.sha256((D/'adjudications-local-v02-batch003.json').read_bytes()).hexdigest()),ensure_ascii=False,indent=2))
