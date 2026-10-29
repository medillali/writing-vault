"""核对已审四栏笔记中的逐章未决被完整原样保留于索引。"""
from pathlib import Path
import json
B=Path(__file__).parent/'tianxia-wushuang/vol06'
notes=[json.loads(x) for x in (B/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
a=json.loads((B/'analysis.json').read_text(encoding='utf-8'));rows=a['chapter_unresolved_index']
assert len(rows)==len(notes)==235
index={r['chapter_id']:r for r in rows}
for note in notes:assert index[note['chapter_id']]['items']==note['unresolved'],note['chapter_id']
print('235 chapter unresolved entries exactly match all previously read chapter notes')
