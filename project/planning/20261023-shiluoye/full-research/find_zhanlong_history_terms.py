"""只查本次主审历史判断的给定词，供跨批一致性检查。"""
from pathlib import Path
import json,re,sys
sys.stdout.reconfigure(encoding='utf-8')
A=Path(__file__).parent/'zhanlong/audit/whole-book'
pool={r['candidate_id']:r for r in json.loads((A/'historical-question-pool.json').read_text(encoding='utf-8'))['candidates']}
for p in sorted(A.glob('adjudications-history-v*-batch*.json')):
 for row in json.loads(p.read_text(encoding='utf-8')):
  if re.search('洛阳|北辰|林被问剑',row['rationale']):
   print(p.name,json.dumps(dict(original=pool[row['candidate_id']],judgment={k:row[k] for k in ['candidate_id','status','rationale','later_chapters']}),ensure_ascii=False))
