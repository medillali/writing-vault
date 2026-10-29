"""分块展示原文及全局行号；输出日志只证明展示范围，不代替阅读判断。"""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).parent
SOURCE_ID = 'src-9ff09c395734410b856f77c77a652834'
manifest = json.loads((ROOT/'writing-vault/private-sources/normalized/manifest.json').read_text(encoding='utf-8'))
source = next(s for s in manifest['sources'] if s['source_id'] == SOURCE_ID)
raw = Path(source['normalized_path']).read_bytes()
assert hashlib.sha256(raw).hexdigest() == source['revision']
text = raw.decode('utf-8')
lines = text.splitlines(keepends=True)
heads = [c for c in source['chapters'] if '集 ' in c['title'] and c['title'].startswith('第')]
volumes=[]
for i, head in enumerate(heads):
    end = heads[i+1]['start_offset'] if i+1<len(heads) else len(text)
    chapters=[c for c in source['chapters'] if head['start_offset']<=c['start_offset']<end]
    start_line=1 if i==0 else head['start_line']
    end_line=chapters[-1]['end_line']
    chunks=[]
    start=start_line
    count=0
    for n in range(start_line,end_line+1):
        size=len(lines[n-1])
        if count and count+size>9000:
            chunks.append({'part':len(chunks)+1,'start_line':start,'end_line':n-1,'characters':count})
            start=n;count=0
        count+=size
    if count: chunks.append({'part':len(chunks)+1,'start_line':start,'end_line':end_line,'characters':count})
    volumes.append({'volume':i+1,'title':head['title'],'chapters':chapters,'chunks':chunks})

p=argparse.ArgumentParser()
p.add_argument('--volume',type=int)
p.add_argument('--part',type=int)
p.add_argument('--lines',nargs=2,type=int)
p.add_argument('--inventory',action='store_true')
a=p.parse_args()
if a.inventory:
    print(json.dumps({'source_id':SOURCE_ID,'revision':source['revision'],'volumes':volumes},ensure_ascii=False,indent=2))
elif a.lines:
    start,end=a.lines
    assert 1<=start<=end<=len(lines)
    assert sum(len(x) for x in lines[start-1:end])<=16000
    for n in range(start,end+1): print(f'{n}: {lines[n-1].rstrip()}')
else:
    volume=volumes[a.volume-1]
    if not a.part:
        print(json.dumps(volume,ensure_ascii=False,indent=2))
    else:
        chunk=volume['chunks'][a.part-1]
        print(json.dumps({'source_id':SOURCE_ID,'revision':source['revision'],'volume':a.volume,**chunk},ensure_ascii=False))
        for n in range(chunk['start_line'],chunk['end_line']+1): print(f'{n}: {lines[n-1].rstrip()}')
        print(f"END_VOLUME_{a.volume}_PART_{a.part}")
