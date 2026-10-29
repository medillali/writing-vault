from revision import revise
from common import P,dump,sha
import json
p=json.loads((P/'wetland-three-items-proposal.json').read_text(encoding='utf-8'))
for x in p['proposals']:
 n=int(x['batch_file'].split('batch')[1].split('.')[0]);a=x['after']
 revise(1,n,x['candidate_id'],'wetland-approved',{k:a[k] for k in x['changed_fields']},'root已逐项批准proposal，追加318/319实游后证，原明日日历保留；其余19逐值不动。')
ds=[json.loads((P/f'batch{n:03d}-wetland-approved-delta.json').read_text(encoding='utf-8')) for n in [10,11,12]]
f=P/'wetland-approved-combined-delta.json';dump(f,{'approved_proposal_sha256':sha(P/'wetland-three-items-proposal.json'),'deltas':ds});print(f.name,sha(f))
