"""尾段独立阅读记录；commit只接受本代理已经完整读过的真实笔记。"""
import json,sys
from pathlib import Path
from datetime import datetime,timezone
sys.stdout.reconfigure(encoding='utf-8')
P=Path(__file__).parent;B=P.parent;S=json.loads((B/'source.json').read_text(encoding='utf-8'))
SPEC=next(x for x in S['volumes'] if x['volume']==8)
CH={x['chapter_id']:x for x in S['chapters']}
ASSIGNED=[f'ch-{i:04d}' for i in range(1573,1610)]
UNITS={s['chapter_id']:u for u in SPEC['units'] for s in u['segments']}
assert all(cid in UNITS for cid in ASSIGNED)
READER='/root/zongheng_vol03_full'
def W(n,v):(P/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def save(records):
 done=[x['chapter_id'] for x in records];assert done==ASSIGNED[:len(done)]
 complete=done==ASSIGNED;now=datetime.now(timezone.utc).isoformat()
 base=dict(source_id=S['source_id'],revision=S['revision'],volume=8,reader=READER,assigned_chapter_ids=ASSIGNED,read_chapter_ids=done,completed_chapter_ids=done,pending_chapter_ids=ASSIGNED[len(done):],next_chapter_id=next((x for x in ASSIGNED if x not in done),None),pending_truncations=[],unresolved_truncations=[],complete_assigned_tail=complete,complete_volume=False,complete_book=False,metadata_only=False,reading_authorized=True,status='assigned_tail_read_complete' if complete else 'reading_assigned_tail',updated_at=now,reading_attribution='本代理仅实读末卷raw1573—1609尾段；raw1505—1572由primary独立负责，不在本日志冒领。')
 W('reader-state.json',base)
 W('read-log.json',dict(source_id=S['source_id'],revision=S['revision'],volume=8,reader=READER,assigned_segment_count=37,indexed_segments_read=len(done),complete_assigned_tail=complete,complete_volume=False,complete_book=False,method='逐片全文输出核BEGIN/END，无截断才保存full_text_read；每2—4片即时事实/推断/状态/疑点笔记。',chapters=[{k:x[k] for k in ['chapter_id','title','start_line','end_line','reader','unit_id','full_text_read']} for x in records]))
 (P/'chapter-notes.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in records),encoding='utf-8')
 print(json.dumps(dict(read_segments=len(done),assigned=37,next=base['next_chapter_id'],complete_assigned_tail=complete),ensure_ascii=False))
if sys.argv[1]=='init':
 assert not (P/'chapter-notes.jsonl').exists()
 save([])
 print(json.dumps(dict(first={k:CH[ASSIGNED[0]][k] for k in ['chapter_id','title','start_line','end_line']},last={k:CH[ASSIGNED[-1]][k] for k in ['chapter_id','title','start_line','end_line']},source_id=S['source_id'],revision=S['revision']),ensure_ascii=False))
elif sys.argv[1]=='commit':
 records=[json.loads(x) for x in (P/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
 batch=json.loads(Path(sys.argv[2]).read_text(encoding='utf-8'));assert 1<=len(batch)<=4
 for row in batch:
  row=dict(row);cid=row['chapter_id'];assert cid==ASSIGNED[len(records)]
  assert row.pop('model_full_text_read') is True
  assert all(isinstance(row[k],list) for k in ['facts','inferences','state_changes','unresolved'])
  ch=CH[cid];u=UNITS[cid]
  records.append(dict(**row,source_id=S['source_id'],revision=S['revision'],reader=READER,title=ch['title'],start_line=ch['start_line'],end_line=ch['end_line'],unit_id=u.get('unit_id',u.get('chapter_id')),full_text_read=True))
 save(records)
