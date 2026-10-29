import json,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');B=Path(__file__).parents[3];d=json.loads((B/'source.json').read_text(encoding='utf-8'));lines=Path(d['normalized_path']).read_text(encoding='utf-8').splitlines()
ids={f'ch-{int(x):04d}' for x in sys.argv[1:]};assert len(ids)<=4
for c in d['chapters']:
 if c['chapter_id'] in ids:
  print('BEGIN FULL',c['chapter_id'],c['title'],c['start_line'],c['end_line'])
  for i in range(c['start_line'],c['end_line']+1):print(f'L{i} {lines[i-1]}')
  print('END FULL',c['chapter_id'])
