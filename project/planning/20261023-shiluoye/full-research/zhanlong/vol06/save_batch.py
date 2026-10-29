"""仅保存模型已逐片BEGIN—END实际读过的人工四栏；不生成文学判断。"""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,sys
sys.stdout.reconfigure(encoding='utf-8')
HERE=Path(__file__).resolve().parent
src=json.loads((HERE.parent/'source.json').read_text(encoding='utf-8-sig'))
units=next(v['units'] for v in src['volumes'] if v['volume']==6)
by_id={c['chapter_id']:c for c in src['chapters']}
assigned=[seg for u in units for seg in u['segment_ids']]
unit_for={seg:u for u in units for seg in u['segment_ids']}
assert assigned==[f'ch-{n:04d}' for n in range(1180,1387)]
path=HERE/sys.argv[1];batch=json.loads(path.read_text(encoding='utf-8-sig'))
notes_path=HERE/'chapter-notes.jsonl'
old=[json.loads(x) for x in notes_path.read_text(encoding='utf-8-sig').splitlines()] if notes_path.exists() else []
assert [r['chapter_id'] for r in old]==assigned[:len(old)]
new=[]
for row in batch['chapters']:
    assert row.pop('begin_end_verified',False) is True and row.pop('full_text_read',False) is True
    cid=row['chapter_id'];assert cid==assigned[len(old)+len(new)]
    assert all(k in row and isinstance(row[k],list) for k in ['facts','inferences','state_changes','unresolved'])
    c=by_id[cid];u=unit_for[cid]
    new.append(dict(source_id=src['source_id'],revision=src['revision'],volume=6,reader='zongheng_vol05_full',
                    read_at=datetime.now(timezone.utc).isoformat(),chapter_id=cid,title=c['title'],
                    start_line=c['start_line'],end_line=c['end_line'],full_text_read=True,
                    unit_id=u['unit_id'],unit_kind=u['kind'],**{k:v for k,v in row.items() if k!='chapter_id'}))
all_notes=old+new
notes_path.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in all_notes),encoding='utf-8')
seen=[r['chapter_id'] for r in all_notes];body={unit_for[c]['unit_id'] for c in seen if unit_for[c]['kind']=='body'}
state=dict(source_id=src['source_id'],revision=src['revision'],volume=6,reader='zongheng_vol05_full',
 status='reading' if len(seen)<len(assigned) else 'full_text_read_artifacts_pending',
 assigned_chapter_ids=assigned,read_chapter_ids=seen,read_raw_fragments=len(seen),read_body_units=len(body),
 assigned_raw_fragments=207,assigned_body_units=206,next_chapter_id=assigned[len(seen)] if len(seen)<207 else None,
 active_chapter_id=None,truncated_pending=[],complete_book=False,full_assigned_volume_text_read=len(seen)==207,
 last_stage_state=batch['stage_state'],last_batch=path.name,last_batch_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
 reading_boundary='本人实际读本卷原文，卷4/5及卷3尾未读原文，当前回述保渠道，不倒灌其他作品；事实/推断/计划分层。')
(HERE/'reader-state.json').write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
log_path=HERE/'read-log.json'
log=json.loads(log_path.read_text(encoding='utf-8')) if log_path.exists() else dict(source_id=src['source_id'],revision=src['revision'],volume=6,reader='zongheng_vol05_full',complete_book=False,method='read_chapters.py每1—2片全文BEGIN—END；人工四栏每2—4片保存。',batches=[])
log['chapters']=[{k:r[k] for k in ['chapter_id','title','start_line','end_line','full_text_read','unit_id','unit_kind','reader']} for r in all_notes]
log['batches'].append(dict(batch=path.name,chapter_ids=[r['chapter_id'] for r in new],begin_end_verified=True,truncated_pending=[],batch_sha256=state['last_batch_sha256']))
log['truncated_pending']=[];log['full_assigned_volume_text_read']=state['full_assigned_volume_text_read']
log_path.write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:state[k] for k in ['volume','read_raw_fragments','read_body_units','next_chapter_id','truncated_pending']},ensure_ascii=False))
