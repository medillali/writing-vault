from common import A,P,dump,sha
import json
result={'purpose':'仅检索定位后人工复核，不算新增全文阅读；不修改两池/历史判断','inputs':[],'own_twenty_mentions':[],'history_twenty_mentions':[]}
for p in sorted(A.glob('adjudications-local-v04-batch*.json')):
 result['inputs'].append({'path':str(p),'sha256':sha(p)})
 for r in json.loads(p.read_text(encoding='utf-8')):
  t=r['rationale']
  if '20万' in t or '二十万' in t:
   result['own_twenty_mentions'].append({'file':p.name,'candidate_id':r['candidate_id'],'rationale':t})
hp=A/'historical-question-pool.json';result['inputs'].append({'path':str(hp),'sha256':sha(hp)})
h=json.loads(hp.read_text(encoding='utf-8'))
for r in h['candidates']:
 t=json.dumps(r,ensure_ascii=False)
 if ('20万' in t or '二十万' in t) and any(x in t for x in ['御林','军团','军批','统兵']):
  result['history_twenty_mentions'].append({'candidate_id':r['candidate_id'],'record':r})
result['manual_conclusion']='当前需改的终点批示错漏仅016/017/018四项，已单独proposal并root批准；其余提及个人上限/实际军数/首批训练/别会人数不改。历史只定位供root核，不修改历史评语。'
dump(P/'cap-global-scan-receipt.json',result)
print('OWN',len(result['own_twenty_mentions']))
for x in result['own_twenty_mentions']:print(x['file'],x['candidate_id'],x['rationale'])
print('HISTORY',len(result['history_twenty_mentions']))
for x in result['history_twenty_mentions']:print(json.dumps(x,ensure_ascii=False))
