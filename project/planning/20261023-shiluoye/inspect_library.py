import json, pathlib, sys
sys.stdout.reconfigure(encoding='utf-8')
root = pathlib.Path(__file__).resolve().parents[2]
vault = root / 'writing-vault'
manifest = json.loads((vault/'private-sources/normalized/manifest.json').read_text(encoding='utf-8'))
print('SOURCES')
for s in manifest['sources']:
    print(json.dumps({k:s.get(k) for k in ['source_id','title','filename','revision','characters','normalized_path']}, ensure_ascii=False))
    print('chapters',len(s['chapters']), 'first',s['chapters'][:3], 'last',s['chapters'][-2:])
print('LIBRARY DIRS', [p.name for p in (vault/'library').iterdir()])
print('CHECKPOINTS')
for p in (vault/'exchanges/runs').glob('*.json'):
    j=json.loads(p.read_text(encoding='utf-8'))
    print(p.name, json.dumps({k:v for k,v in j.items() if k not in ['completed_chapters','pending_chapters']},ensure_ascii=False), 'completed',len(j.get('completed_chapters',[])), 'pending',len(j.get('pending_chapters',[])))
print('INPUTS')
for pattern in ['*网游之天下无双*','*网游之纵横天下*','*斩龙*']:
    for p in pathlib.Path('E:/chromedownload').glob(pattern):
        b=p.read_bytes()
        enc=[]
        for e in ['utf-8-sig','gb18030']:
            try:
                t=b.decode(e); enc.append((e,len(t)))
            except UnicodeError: pass
        print(str(p),len(b),enc)
print('LEGACY')
legacy=pathlib.Path('C:/Users/Administrator/Documents/ChatGPT/Chinese Novel/books/zeidan/distillation')
print('legacy_exists',legacy.exists())
if legacy.exists(): print([p.name for p in legacy.iterdir()])
