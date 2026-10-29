"""仅合并已完成的分工阅读，保留primary和尾段原件及逐条读者归属。"""
import json,hashlib,sys
from pathlib import Path
from datetime import datetime,timezone
sys.stdout.reconfigure(encoding='utf-8')
P=Path(__file__).parent;T=P.parent/'vol08-tail-agent3';B=P.parent
R=lambda p:json.loads(p.read_text(encoding='utf-8'))
S=R(B/'source.json');SP=next(v for v in S['volumes'] if v['volume']==8);CH={c['chapter_id']:c for c in S['chapters']}
UNITS={s['chapter_id']:u for u in SP['units'] for s in u['segments']};expected=[s['chapter_id'] for u in SP['units'] for s in u['segments']]
snapshot=P/'primary-original';snapshot.mkdir(exist_ok=True)
for n in ['chapter-notes.jsonl','reader-state.json']:
 target=snapshot/n
 if not target.exists():target.write_bytes((P/n).read_bytes())
primary=[json.loads(x) for x in (snapshot/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
tail=[json.loads(x) for x in (T/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
assert [x['chapter_id'] for x in primary]==[f'ch-{i:04d}' for i in range(1505,1573)]
assert [x['chapter_id'] for x in tail]==[f'ch-{i:04d}' for i in range(1573,1610)]
assert R(T/'reader-state.json')['complete_assigned_tail'] and R(T/'primary-material-state.json')['complete']
N=[]
for row in primary+tail:
 row=dict(row);cid=row['chapter_id'];ch=CH[cid];u=UNITS[cid]
 assert row['full_text_read'] and (row['start_line'],row['end_line'])==(ch['start_line'],ch['end_line'])
 assert row['reader']==('primary' if int(cid[3:])<=1572 else '/root/zongheng_vol03_full')
 row.update(source_id=S['source_id'],revision=S['revision'],unit_id=u.get('unit_id',u.get('chapter_id')))
 N.append(row)
assert [n['chapter_id'] for n in N]==expected and len(N)==105 and SP['body_units']==104
def W(n,v):(P/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(P/'chapter-notes.jsonl').write_text(''.join(json.dumps(n,ensure_ascii=False)+'\n' for n in N),encoding='utf-8')
attribution=[dict(reader='primary',start_chapter_id='ch-1505',end_chapter_id='ch-1572',segments=68,body_units=67,original_notes_path=(snapshot/'chapter-notes.jsonl').resolve().as_posix()),dict(reader='/root/zongheng_vol03_full',start_chapter_id='ch-1573',end_chapter_id='ch-1609',segments=37,body_units=37,original_notes_path=(T/'chapter-notes.jsonl').resolve().as_posix())]
state=R(snapshot/'reader-state.json')
state.update(source_id=S['source_id'],revision=S['revision'],volume=8,reader='primary + /root/zongheng_vol03_full',reading_attribution=attribution,read_chapter_ids=expected,completed_chapter_ids=expected,completed_count=105,completed_body_units=104,next_chapter_id=None,pending_chapter_ids=[],pending_truncations=[],unresolved_truncations=[],complete_volume=True,complete_book=False,metadata_only=False,reading_authorized=True,status='volume_read_complete_research_in_progress',synthesizer='/root/zongheng_vol03_full',note='105片/104正文由两位真实读者分工全文覆盖，综合者完整阅读primary68条逐章笔记；不冒称一人亲读全卷。',updated_at=datetime.now(timezone.utc).isoformat())
W('reader-state.json',state)
W('read-log.json',dict(source_id=S['source_id'],revision=S['revision'],volume=8,reader=state['reader'],reading_attribution=attribution,complete_volume=True,complete_book=False,indexed_segments_read=105,body_units_read=104,chapters=[{k:n[k] for k in ['chapter_id','title','start_line','end_line','reader','unit_id','full_text_read']} for n in N],method='primary实际全文读1505—1572；agent3实际全文读1573—1609；各自逐批持久化/补齐截断后合并，原件保留，未用摘要替代正文阅读。',unit_anomalies=[dict(chapter_id='ch-1505',type='volume_header',count_as_body=False)],synthesis_material_read=dict(primary_original_notes=68,complete=True,log=(T/'primary-material-state.json').resolve().as_posix())))
if (P/'assignment.json').exists():
 a=R(P/'assignment.json');a.update(status='volume_read_complete_research_in_progress',reading_authorized=True,reader=state['reader'],reading_attribution=attribution);W('assignment.json',a)
W('reader-merge-validation.json',dict(status='coverage_and_attribution_passed',source_id=S['source_id'],revision=S['revision'],segments=105,body_units=104,overlap=0,gaps=0,reading_attribution=attribution,original_sha256={str(p.resolve().as_posix()):hashlib.sha256(p.read_bytes()).hexdigest() for p in [snapshot/'chapter-notes.jsonl',snapshot/'reader-state.json',T/'chapter-notes.jsonl',T/'reader-state.json']},complete_volume=True,complete_book=False))
print(json.dumps(dict(segments=len(N),body_units=104,primary=68,agent3=37,overlap=0,gaps=0),ensure_ascii=False))
