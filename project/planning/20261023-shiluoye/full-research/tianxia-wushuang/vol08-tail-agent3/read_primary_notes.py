"""逐条完整显示primary前段原始笔记，不把派生阅读计作正文亲读。"""
import json,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
P=Path(__file__).parent;V=P.parent/'vol08'
N=[json.loads(x) for x in (V/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
start,end=map(int,sys.argv[1:3]);assert 1505<=start<=end<=1572 and end-start<8
for n in N:
 i=int(n['chapter_id'][3:])
 if start<=i<=end:
  print('BEGIN_PRIMARY_NOTE',n['chapter_id']);print(json.dumps(n,ensure_ascii=False));print('END_PRIMARY_NOTE',n['chapter_id'])
