import json,sys
from pathlib import Path

p = Path('writing-vault/library/reports/two-books-full-20261025/zeidan')
g=json.loads((p/'plot/graph.json').read_text(encoding='utf-8'))
mode=sys.argv[1]
if mode=='notes-shape':
    q=json.loads((p/'chapter-notes.json').read_text(encoding='utf-8')); print(type(q).__name__);print(str(q)[:4000])
elif mode=='questions':
    q=json.loads((p/'terminal-question-map.json').read_text(encoding='utf-8'))
    for x in q['items']: print(x['key'], x['final_status'], x['answer'])
elif mode=='relations':
    for e in g['edges']:
        if e['from'].startswith('event-') and e['to'].startswith('event-'):
            print(e['from'],e['to'],e['kind'],e.get('label'), e.get('summary',''))
elif mode=='shape':
    for n in g['nodes']:
        if n.get('kind')=='scene':
            print(json.dumps(n,ensure_ascii=False));break
elif mode=='scenes':
    ns=[n for n in g['nodes'] if n.get('kind')=='scene']
    print(len(ns))
    for i,n in enumerate(ns,1):
        if len(sys.argv)>2 and not int(sys.argv[2])<=i<=int(sys.argv[3]):continue
        print(i,n['id'],n['title'],'|',n['summary'],'|',str(n['mechanism']),'|',[(e['chapter_id'],e['start_line'],e['end_line']) for e in n['evidence']])
else:
    print((p/mode).read_text(encoding='utf-8'))
