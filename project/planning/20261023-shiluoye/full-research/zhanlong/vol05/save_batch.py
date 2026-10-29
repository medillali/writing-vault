"""只持久化本代理逐片原文完整读完后的手写四栏笔记，不生成阅读事实。"""
import json,pathlib,sys,datetime,hashlib
V=pathlib.Path(__file__).resolve().parent;B=V.parent
s=json.loads((B/'source.json').read_text(encoding='utf-8'));assert s['source_id']=='src-20f2d16e3d1b472fa4b230ab0e1770c9';assert s['revision']=='61ab0b114c76446fda554abfafdac8c432cd88afaba7c2541f4473a3902134e3'
v=next(x for x in s['volumes'] if x['volume']==5);units={seg['chapter_id']:u for u in v['units'] for seg in u['segments']};canonical={c['chapter_id']:c for c in s['chapters']};scope=list(units)
payload=json.loads((V/sys.argv[1]).read_text(encoding='utf-8'));p=V/'chapter-notes.jsonl';old=[json.loads(x) for x in p.read_text(encoding='utf-8').splitlines() if x] if p.exists() else [];old_ids=[x['chapter_id'] for x in old];new=[]
for note in payload['chapters']:
 cid=note['chapter_id'];assert cid in units and cid not in old_ids and cid not in [x['chapter_id'] for x in new];assert note['full_text_read'] is True
 c=canonical[cid];assert (note['start_line'],note['end_line'])==(c['start_line'],c['end_line']);assert all(isinstance(note[k],list) for k in ['facts','inferences','state_changes','unresolved'])
 row=dict(source_id=s['source_id'],revision=s['revision'],reader='/root/zongheng_vol04_full',volume=5,read_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),unit_id=units[cid]['unit_id'],unit_kind=units[cid]['kind'],**note);row['title']=c['title'];new.append(row)
rows=old+new;ids=[x['chapter_id'] for x in rows];assert ids==scope[:len(ids)]
p.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows),encoding='utf-8')
def write(name,x):(V/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
body={x['unit_id'] for x in rows if x['unit_kind']=='body'};next_id=scope[len(ids)] if len(ids)<len(scope) else None
write('reader-state.json',dict(source_id=s['source_id'],revision=s['revision'],volume=5,reader='/root/zongheng_vol04_full',status='reading' if next_id else 'read_complete_research_pending',read_chapter_ids=ids,indexed_segments_read=len(ids),body_units_read=len(body),assigned_segments=len(scope),assigned_body_units=v['body_units'],next_chapter_id=next_id,truncated_pending=[],current_stage=payload['stage_state'],complete_book=False,complete_volume=next_id is None,notes_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),ownership='本卷逐章原文实读归属本代理；其他卷派生阅读不算个人原文全文。'))
write('read-log.json',dict(source_id=s['source_id'],revision=s['revision'],volume=5,reader='/root/zongheng_vol04_full',complete_book=False,complete_volume=next_id is None,method='read_chapters.py每1—2片BEGIN-END实际全文，截断补读；每2—4片手写四栏持久化。',chapters=[dict(chapter_id=x['chapter_id'],start_line=x['start_line'],end_line=x['end_line'],full_text_read=True,reader=x['reader'],unit_id=x['unit_id'],unit_kind=x['unit_kind']) for x in rows],indexed_segments_read=len(ids),body_units_read=len(body),truncated_pending=[],anomalies=[]))
print(json.dumps(dict(saved=len(new),segments=len(ids),body_units=len(body),next=next_id),ensure_ascii=False))
