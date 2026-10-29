import pathlib,json,sys
sys.stdout.reconfigure(encoding='utf-8')
p=pathlib.Path('C:/Users/Administrator/Documents/ChatGPT/Chinese Novel/books/zeidan')
print('FILES',[(x.name,x.is_dir()) for x in p.iterdir()])
for n in ['coverage.json','validation.json','entities.json','scenes.json','threads.json','chapter-notes.jsonl']:
    q=p/'distillation'/n
    if n.endswith('jsonl'):
        lines=q.read_text(encoding='utf-8').splitlines(); print(n,len(lines),lines[:2]); continue
    j=json.loads(q.read_text(encoding='utf-8')); print(n, type(j).__name__,len(j)); print(json.dumps(j if n in ['coverage.json','validation.json'] else (j[:2] if isinstance(j,list) else {k:(v[:1] if isinstance(v,list) else v) for k,v in j.items()}),ensure_ascii=False)[:14000])
