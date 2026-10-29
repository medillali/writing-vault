"""将模型已实际完整读过的人工四栏批次持久化；不生成文学判断。"""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,sys
sys.stdout.reconfigure(encoding='utf-8')
HERE=Path(__file__).resolve().parent
src=json.loads((HERE.parent/'source.json').read_text(encoding='utf-8-sig'))
volume=int(HERE.name[3:])
units=next(v['units'] for v in src['volumes'] if v['volume']==volume)
chapter_by_id={c['chapter_id']:c for c in src['chapters']}
assigned=[seg for u in units for seg in u['segment_ids']]
unit_for_segment={seg:u for u in units for seg in u['segment_ids']}
batch_path=HERE/sys.argv[1]
batch=json.loads(batch_path.read_text(encoding='utf-8-sig'))
notes_path=HERE/'chapter-notes.jsonl'
old=[json.loads(s) for s in notes_path.read_text(encoding='utf-8-sig').splitlines()] if notes_path.exists() else []
assert len({r['chapter_id'] for r in old})==len(old)
assert [r['chapter_id'] for r in old]==assigned[:len(old)]
new=[]
for r in batch['chapters']:
    assert r.pop('begin_end_verified',False) is True
    assert r.pop('full_text_read',False) is True
    cid=r['chapter_id']
    assert int(cid[3:])<=653,'primary-vol03-tail负责654—753，当前读者不可越界'
    assert cid==assigned[len(old)+len(new)],(cid,'not next contiguous assigned fragment')
    assert all(k in r and isinstance(r[k],list) for k in ['facts','inferences','state_changes','unresolved'])
    c=chapter_by_id[cid]; u=unit_for_segment[cid]
    new.append(dict(source_id=src['source_id'],revision=src['revision'],volume=volume,
                    reader='zongheng_vol05_full',read_at=datetime.now(timezone.utc).isoformat(),
                    chapter_id=cid,title=c['title'],start_line=c['start_line'],end_line=c['end_line'],
                    full_text_read=True,unit_id=u['unit_id'],unit_kind=u['kind'],**{k:v for k,v in r.items() if k!='chapter_id'}))
all_notes=old+new
notes_path.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in all_notes),encoding='utf-8')
seen=[r['chapter_id'] for r in all_notes]
body_seen={unit_for_segment[c]['unit_id'] for c in seen if unit_for_segment[c]['kind']=='body'}
state=dict(source_id=src['source_id'],revision=src['revision'],volume=volume,
    reader='zongheng_vol05_full',status='reading' if len(seen)<len(assigned) else 'full_text_read_artifacts_pending',
    assigned_chapter_ids=assigned,read_chapter_ids=seen,read_raw_fragments=len(seen),
    read_body_units=len(body_seen),assigned_raw_fragments=len(assigned),
    assigned_body_units=sum(u['kind']=='body' for u in units),
    next_chapter_id=assigned[len(seen)] if len(seen)<len(assigned) else None,
    active_chapter_id=None,truncated_pending=[],complete_book=False,
    full_assigned_volume_text_read=len(seen)==len(assigned),
    reader_assigned_prefix_end='ch-0653',tail_reader='primary',tail_directory='../primary-vol03-tail',
    last_stage_state=batch['stage_state'],last_batch=batch_path.name,
    last_batch_sha256=hashlib.sha256(batch_path.read_bytes()).hexdigest(),
    reading_boundary='本卷原文实际阅读，不冒前卷/后卷原文已读；facts明确说话者/行动者，研究常规边界不机械生成unresolved。')
(HERE/'reader-state.json').write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
log_path=HERE/'read-log.json'
log=json.loads(log_path.read_text(encoding='utf-8')) if log_path.exists() else dict(source_id=src['source_id'],revision=src['revision'],volume=volume,reader='zongheng_vol05_full',complete_book=False,method='read_chapters.py每次1—2片实际BEGIN—END；人工四栏后每2—4片持久化。',batches=[])
log['chapters']=[{k:r[k] for k in ['chapter_id','title','start_line','end_line','full_text_read','unit_id','unit_kind','reader']} for r in all_notes]
log['batches'].append(dict(batch=batch_path.name,chapter_ids=[r['chapter_id'] for r in new],begin_end_verified=True,truncated_pending=[],batch_sha256=state['last_batch_sha256']))
log['truncated_pending']=[];log['full_assigned_volume_text_read']=state['full_assigned_volume_text_read']
log_path.write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:state[k] for k in ['volume','read_raw_fragments','read_body_units','next_chapter_id','truncated_pending']},ensure_ascii=False))
