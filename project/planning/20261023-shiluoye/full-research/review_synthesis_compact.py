"""主审全部文学语义，折叠重复的继承证据数组（结构核验另计）。"""
import json,sys
from pathlib import Path
B=Path(__file__).parent;data=json.loads((B/sys.argv[1]/'book-synthesis-draft.json').read_text(encoding='utf-8'))
sys.stdout.reconfigure(encoding='utf-8')
for dim in sys.argv[2].split(','):
 for row in data['dimensions'][dim]:
  result={k:v for k,v in row.items() if k not in ['supporting_observations','evidence','review_status','literary_choice']}
  result['support_volumes']=sorted({o['volume'] for o in row['supporting_observations']})
  result['references']=len(row.get('evidence',[]))
  print(json.dumps(dict(dimension=dim,**result),ensure_ascii=False,separators=(',',':')))
