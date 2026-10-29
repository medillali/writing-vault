"""只核本目录真实阅读状态，避免恢复后重复或虚增。"""
import json
from pathlib import Path
p=Path(__file__).resolve().parent
s=json.loads((p/'reader-state.json').read_text(encoding='utf-8'))
n=[json.loads(x) for x in (p/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines()]
assert s['read_chapter_ids']==[r['chapter_id'] for r in n]
print({k:s[k] for k in ['read_raw_fragments','read_body_units','next_chapter_id','truncated_pending']})
print('notes',len(n),n[-1]['chapter_id'])
