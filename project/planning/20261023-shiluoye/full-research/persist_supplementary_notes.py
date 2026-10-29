"""把已读书首补充笔记和阅读者归属复制到正式报告，原书首不重复计正文。"""
import json,hashlib,sys
from pathlib import Path
BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[2]
book=sys.argv[1];stage=BASE/book;dest=ROOT/'writing-vault/library/reports'/book
dest.mkdir(parents=True,exist_ok=True)
records=[]
for name in ['supplementary-read-log.json','supplementary-reading-notes.md']:
 path=stage/name
 if not path.exists():continue
 data=path.read_bytes();(dest/name).write_bytes(data)
 records.append(dict(file=name,sha256=hashlib.sha256(data).hexdigest()))
(dest/'supplementary-note-receipt.json').write_text(json.dumps(dict(book=book,files=records,note='只复制已有实读补充资料；不新增或重复计正文覆盖。'),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(records,ensure_ascii=False))
