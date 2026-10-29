"""只检索已签终评中的措辞，保候选ID与来源；不生成终评。"""
from pathlib import Path
import json,sys
B=Path(__file__).parent/'zhanlong'
P=json.loads((B/'primary-audit-review-progress.json').read_text(encoding='utf-8'))
terms=sys.argv[1:];assert terms
sys.stdout.reconfigure(encoding='utf-8')
for batch in P['batches']:
    path=B/'audit/whole-book'/batch['path']
    for row in json.loads(path.read_text(encoding='utf-8')):
        text=' '.join(str(row.get(k,'')) for k in ['rationale','title','audit_domain'])
        if any(t in text for t in terms):
            print(json.dumps(dict(path=batch['path'],candidate_id=row['candidate_id'],
                status=row['status'],title=row.get('title'),rationale=row['rationale']),ensure_ascii=False))
