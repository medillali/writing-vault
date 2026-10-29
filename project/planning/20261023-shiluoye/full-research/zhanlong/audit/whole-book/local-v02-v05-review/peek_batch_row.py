from save_manual_batch import P,read
import sys,json
sys.stdout.reconfigure(encoding='utf-8')
b=int(sys.argv[1]);term=sys.argv[2]
for x in read(P/f'adjudications-local-v02-batch{b:03d}.json'):
    if term in x['candidate_id']:print(json.dumps(x,ensure_ascii=False,indent=2))
