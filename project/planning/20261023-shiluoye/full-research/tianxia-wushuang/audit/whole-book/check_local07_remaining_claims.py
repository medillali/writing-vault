import json,pathlib,sys
sys.stdout.reconfigure(encoding='utf-8')
H=pathlib.Path(__file__).resolve().parent
for n in map(int,sys.argv[1:] or range(1,6)):
 for x in json.loads((H/f'adjudications-local-v07-part{n:02}.json').read_text(encoding='utf-8')):
  if x['status']!='answered':print(n,x['candidate_id'],x['status'],x['rationale'])
