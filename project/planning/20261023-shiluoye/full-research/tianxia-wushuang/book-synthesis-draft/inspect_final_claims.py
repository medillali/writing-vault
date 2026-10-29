import json,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');P=Path(__file__).parent
a=json.loads((P.parent/'book-synthesis-draft.json').read_text(encoding='utf-8'))
for d in sys.argv[1:]:
 print('BEGIN',d)
 for r in a['dimensions'][d]:print(json.dumps({k:r[k] for k in ['id','title','fact_summary','claim','late_stage_result']},ensure_ascii=False))
 print('END',d)
