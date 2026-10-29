"""只保存本代理实际完整读完并手写的笔记；不生成阅读事实或文学判断。"""
import json,pathlib,sys,datetime,hashlib
V=pathlib.Path(__file__).resolve().parent;B=V.parent;R=V.parents[4]
s=json.loads((B/'source.json').read_text(encoding='utf-8'));assert s['source_id']=='src-20f2d16e3d1b472fa4b230ab0e1770c9';assert s['revision']=='61ab0b114c76446fda554abfafdac8c432cd88afaba7c2541f4473a3902134e3'
volume=2;v=next(v for v in s['volumes'] if v['volume']==volume);units={seg['chapter_id']:u for u in v['units'] for seg in u['segments']};canonical={c['chapter_id']:c for c in s['chapters']};scope=list(units)
payload=json.loads((V/sys.argv[1]).read_text(encoding='utf-8'));old=[];p=V/'chapter-notes.jsonl'
if p.exists():old=[json.loads(l) for l in p.read_text(encoding='utf-8').splitlines() if l.strip()]
old_ids=[x['chapter_id'] for x in old];new=[]
for note in payload['chapters']:
 cid=note['chapter_id'];assert cid in units and int(cid[3:])<=404 and cid not in old_ids and cid not in [x['chapter_id'] for x in new];assert note['full_text_read'] is True
 c=canonical[cid];assert note['start_line']==c['start_line'] and note['end_line']==c['end_line'];assert all(isinstance(note[k],list) for k in ['facts','inferences','state_changes','unresolved'])
 row=dict(source_id=s['source_id'],revision=s['revision'],reader='/root/zongheng_vol04_full',volume=volume,read_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),unit_id=units[cid]['unit_id'],unit_kind=units[cid]['kind'],**note);row['title']=c['title'];new.append(row)
rows=old+new;ids=[x['chapter_id'] for x in rows];assert ids==scope[:len(ids)],'仅准连续真实已读片段。'
p.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows),encoding='utf-8')
def write(name,x):(V/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
body_units={x['unit_id'] for x in rows if x['unit_kind']=='body'}
next_id=scope[len(ids)] if len(ids)<153 else None
write('reader-state.json',dict(source_id=s['source_id'],revision=s['revision'],volume=volume,reader='/root/zongheng_vol04_full',status='reading_personal_prefix' if next_id else 'personal_prefix_read_pending_primary_tail',read_chapter_ids=ids,indexed_segments_read=len(ids),body_units_read=len(body_units),assigned_segments=len(scope),assigned_body_units=v['body_units'],personal_assigned_segments=153,personal_assigned_body_units=152,personal_stop_chapter_id='ch-0404',primary_tail_scope='ch-0405—ch-0504',next_chapter_id=next_id,truncated_pending=[],current_stage=payload['stage_state'],complete_book=False,complete_volume=False,complete_personal_prefix=next_id is None,notes_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),ownership='本代理原文实读仅raw252—404前段；raw405—504由root独占，未合齐前全卷不完整。前卷研究不计本人亲读。'))
write('read-log.json',dict(source_id=s['source_id'],revision=s['revision'],volume=volume,reader='/root/zongheng_vol04_full',complete_book=False,complete_volume=False,complete_personal_prefix=next_id is None,personal_stop_chapter_id='ch-0404',method='read_chapters.py按1—2片BEGIN-END实际全文读取；手写本批四栏笔记，每2—4片持久化。',chapters=[dict(chapter_id=x['chapter_id'],start_line=x['start_line'],end_line=x['end_line'],full_text_read=True,unit_id=x['unit_id'],unit_kind=x['unit_kind']) for x in rows],indexed_segments_read=len(ids),body_units_read=len(body_units),truncated_pending=[],anomalies=[]))
print(json.dumps(dict(saved=len(new),segments=len(ids),body_units=len(body_units),next=next_id),ensure_ascii=False))
