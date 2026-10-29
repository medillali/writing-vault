import json,re,pathlib,sys
sys.stdout.reconfigure(encoding='utf-8')
b=pathlib.Path(__file__).resolve().parent
s=json.loads((b.parent/'source.json').read_text(encoding='utf-8'))
n=[json.loads(x) for x in (b/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines()]
if len(sys.argv)>1:
 a,z=map(int,sys.argv[1:3])
 for x in n:
  k=int(x['chapter_id'].split('-')[1])
  if a<=k<=z: print(x['chapter_id'],x['title'])
else:
 v=next(x for x in s['volumes'] if x['volume']==6)
 print({k:v[k] for k in v if k!='units'})
 print('units',len(v['units']),'segments',sum(len(x['segments']) for x in v['units']))
 print('first',n[0]['title'],'last',n[-1]['title'])
 for u in v['units']:
  if len(u['segments'])>1:print('merged',u)
