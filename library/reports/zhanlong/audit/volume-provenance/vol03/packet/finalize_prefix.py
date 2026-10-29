"""记录本人已实际读完的前缀交接，不将待合尾段伪称整卷完成。"""
from pathlib import Path
import json,hashlib
from datetime import datetime,timezone
HERE=Path(__file__).resolve().parent
state=json.loads((HERE/'reader-state.json').read_text(encoding='utf-8'))
notes=[json.loads(x) for x in (HERE/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines()]
expected=[f'ch-{n:04d}' for n in range(505,654)]
assert state['read_chapter_ids']==expected==[r['chapter_id'] for r in notes]
assert len(notes)==149 and sum(r['unit_kind']=='body' for r in notes)==148
assert all(r['reader']=='zongheng_vol05_full' and r['full_text_read'] for r in notes)
assert not state['truncated_pending']
state.update(status='prefix_full_text_read_tail_pending',reader_assigned_prefix_complete=True,
             next_chapter_id='ch-0654',next_chapter_for_this_reader=None,
             full_assigned_volume_text_read=False,complete_book=False,
             prefix_handoff='prefix-handoff.md')
(HERE/'reader-state.json').write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
files=['chapter-notes.jsonl','reader-state.json','read-log.json','note-corrections.json','prefix-handoff.md']
receipt=dict(status='prefix_checkpoint_verified_not_complete_volume',checked_at=datetime.now(timezone.utc).isoformat(),
 source_id=state['source_id'],revision=state['revision'],volume=3,
 actual_reader='zongheng_vol05_full',raw_range=[505,653],raw_fragments=149,body_units=148,
 all_begin_end_verified=True,truncated_pending=[],tail_reader='primary',tail_range=[654,753],
 next_for_this_reader={'volume':6,'raw':1180},
 file_sha256={f:hashlib.sha256((HERE/f).read_bytes()).hexdigest() for f in files},
 limits=['本回执只证149片前缀阅读与持久化一致，不证整卷249片完成。','文学分析/卡/图将在完整读primary尾笔记并保归属后构建，当前未伪填。'])
(HERE/'prefix-validation.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(receipt,ensure_ascii=False,indent=2))
