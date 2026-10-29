import json,pathlib,sys
sys.stdout.reconfigure(encoding='utf-8');H=pathlib.Path(__file__).resolve().parent;source=json.loads((H.parents[1]/'source.json').read_text(encoding='utf-8'));lines=pathlib.Path(source['normalized_path']).read_text(encoding='utf-8').splitlines()
for term in sys.argv[1:] or ['公孙谷','王诩']:
 hits=[]
 for i,line in enumerate(lines,1):
  if term in line:
   c=next(c for c in source['chapters'] if c['start_line']<=i<=c['end_line']);hits.append(dict(chapter_id=c['chapter_id'],line=i,text=line))
 print(term,len(hits));print(json.dumps(hits[:10],ensure_ascii=False))
