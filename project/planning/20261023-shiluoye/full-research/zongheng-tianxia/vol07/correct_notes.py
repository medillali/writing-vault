import json,pathlib
p=pathlib.Path(__file__).parent
for name in ['batch-936-939.json','chapter-notes.jsonl']:
 f=p/name
 rows=json.loads(f.read_text(encoding='utf-8')) if name.endswith('.json') else [json.loads(x) for x in f.read_text(encoding='utf-8').splitlines()]
 for r in rows:
  if r.get('index')==939 or r.get('chapter_id')=='ch-0939':
   r['unresolved'][0]='各装最低强化成本合计7100点，与7427额度可兼容；永恒具体失败次数未列，不自行列精确耗分或余数。此前笔记把永恒最低成本误算5900已纠为3100，不是源文矛盾。'
  if r.get('chapter_id')=='ch-0919':
   r['facts']=[x.replace('半时?原不到半分钟','不到半分钟') for x in r['facts']]
 f.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n' if name.endswith('.json') else ''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows),encoding='utf-8')
