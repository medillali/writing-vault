import json,pathlib,sys
HERE=pathlib.Path(__file__).resolve().parent
sys.stdout.reconfigure(encoding='utf-8')
notes=[json.loads(l) for l in (HERE/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines()]
if sys.argv[1]=='schema':
 g=json.loads((HERE.parents[1]/'zongheng-tianxia/vol08/graph.json').read_text(encoding='utf-8'))
 print(json.dumps({'node':g['nodes'][9],'edge':g['edges'][0],'thread':g['threads'][0]},ensure_ascii=False,indent=2))
else:
 a,b=map(int,sys.argv[1:3])
 for n in notes:
  if a<=int(n['chapter_id'][3:])<=b:
   print(n['chapter_id'],n['title'],f"L{n['start_line']}-{n['end_line']}")
   for k in ['facts','inferences','unresolved']:
    print(k+': '+'；'.join(n[k]))
