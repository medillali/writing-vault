"""审计用定向原文片段读取，单独登记，不虚增整章全文覆盖。"""
import sys,json,hashlib,datetime
from pathlib import Path
P=Path(__file__).parent;W=P.parents[6]
f=W/'writing-vault/private-sources/normalized/sources/src-20f2d16e3d1b472fa4b230ab0e1770c9/61ab0b114c76446fda554abfafdac8c432cd88afaba7c2541f4473a3902134e3.txt'
lo,hi=map(int,sys.argv[1:3]);assert 0<lo<=hi and hi-lo<160
lines=f.read_text(encoding='utf-8').splitlines();x='\n'.join(f'L{i} {lines[i-1]}' for i in range(lo,hi+1))
print(f'BEGIN TARGETED EXCERPT {lo}—{hi}');print(x);print('END TARGETED EXCERPT')
with (P/'targeted-source-access.jsonl').open('a',encoding='utf-8') as o:o.write(json.dumps({'reviewer':'/root/zongheng_vol03_full','at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'start_line':lo,'end_line':hi,'kind':'targeted-excerpt-not-new-full-chapter','excerpt_sha256':hashlib.sha256(x.encode()).hexdigest()},ensure_ascii=False)+'\n')
