from pathlib import Path
import json, sys, hashlib
ROOT=Path(__file__).resolve().parents[2]
V=ROOT/'.verify/two-books'
M=json.loads((V/'private-sources/normalized/manifest.json').read_text(encoding='utf-8'))
if len(sys.argv)>1:
    word=sys.argv[1]; lo=int(sys.argv[2]); hi=int(sys.argv[3])
    s=next(s for s in M['sources'] if word in s['title'])
    lines=Path(s['normalized_path']).read_text(encoding='utf-8').splitlines()
    for c in s['chapters'][lo-1:hi]:
        print('\nCHAPTER',c['chapter_id'],c['title'])
        for n in range(c['start_line'],c['end_line']+1):
            print(f'{n}: {lines[n-1]}')
else:
    for s in M['sources']:
        print(json.dumps({k:s.get(k) for k in ['source_id','title','revision','encoding','warnings','normalized_path']},ensure_ascii=False))
        print('COUNT',len(s['chapters']),'FIRST',[(c['chapter_id'],c['title']) for c in s['chapters'][:14]],'LAST',s['chapters'][-1]['title'])
    old=ROOT.parent/'Chinese Novel/books/zeidan'
    for name in ['manifest.json','distillation/entities.json','distillation/scenes.json','distillation/threads.json','distillation/chapter-notes.jsonl']:
        text=(old/name).read_text(encoding='utf-8')
        print('SCHEMA',name,text[:6500])
    for p in Path('E:/chromedownload').glob('*贼胆*.txt'):
        print('RAW_SHA',hashlib.sha256(p.read_bytes()).hexdigest())
