"""只列王戒回复范围相关原派生串，供逐字段人工提案。"""
from pathlib import Path
import hashlib,json,sys
sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent; BOOK=H.parent.parents[1];ROOT=BOOK.parents[3];F=ROOT/'writing-vault/library/reports/zhanlong'
def walk(x,path=()):
    if isinstance(x,dict):
        for k,v in x.items():yield from walk(v,path+(k,))
    elif isinstance(x,list):
        for i,v in enumerate(x):yield from walk(v,path+(i,))
    elif isinstance(x,str) and (('王戒' in x or '王者领域' in x or 'L42957' in x or '自身秒回' in x) and any(k in x for k in ['回','治','差','争议'])):
        yield dict(path=list(path),value=x)
files=sorted(F.glob('vol03-*'))+[BOOK/'vol03/chapter-notes.jsonl',BOOK/'vol03-prefix/chapter-notes.jsonl']
for p in files:
    if not p.is_file():continue
    if p.suffix=='.json':
        hits=list(walk(json.loads(p.read_text(encoding='utf-8'))))
        if hits:print(json.dumps(dict(file=p.relative_to(ROOT).as_posix(),hits=hits),ensure_ascii=False))
    elif p.suffix=='.jsonl':
        for i,line in enumerate(p.read_text(encoding='utf-8').splitlines()):
            row=json.loads(line);hits=list(walk(row))
            if hits:print(json.dumps(dict(file=p.relative_to(ROOT).as_posix(),jsonl_index=i,chapter_id=row['chapter_id'],reader=row.get('reader'),hits=hits),ensure_ascii=False))
