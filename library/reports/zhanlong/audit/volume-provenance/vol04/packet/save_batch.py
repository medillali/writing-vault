"""仅保存模型实际读完并手写的本卷笔记，不自动读取正文或生成文学结论。"""
import json,sys,hashlib
from datetime import datetime,timezone
from pathlib import Path
P=Path(__file__).parent;B=P.parent;source=json.loads((B/'source.json').read_text(encoding='utf-8'))
volume=int(P.name[-2:]);spec=next(v for v in source['volumes'] if v['volume']==volume)
expected=[s['chapter_id'] for u in spec['units'] for s in u['segments']]
chapters={c['chapter_id']:c for c in source['chapters']};units={s['chapter_id']:u for u in spec['units'] for s in u['segments']}
load=lambda p:json.loads(p.read_text(encoding='utf-8'))
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
payload_path=P/sys.argv[1];payload=load(payload_path)
assert 1<=len(payload['notes'])<=4
np=P/'chapter-notes.jsonl';old=[json.loads(s) for s in np.read_text(encoding='utf-8').splitlines() if s.strip()] if np.exists() else []
ids=[r['chapter_id'] for r in old];newids=[r['chapter_id'] for r in payload['notes']]
assert newids==expected[len(ids):len(ids)+len(newids)],('not next expected segment',newids,expected[len(ids):len(ids)+4])
assert payload['complete_begin_end_verified'] is True and payload.get('unresolved_truncations',[])==[]
now=datetime.now(timezone.utc).isoformat();new=[]
for r in payload['notes']:
 c=chapters[r['chapter_id']];u=units[r['chapter_id']]
 assert all(k in r and isinstance(r[k],list) for k in ['facts','inferences','state_changes','unresolved'])
 n={'source_id':source['source_id'],'revision':source['revision'],'volume':volume,'reader':'/root/zongheng_vol03_full','read_at':now,
 'chapter_id':c['chapter_id'],'title':c['title'],'start_line':c['start_line'],'end_line':c['end_line'],'unit_id':u['unit_id'],'unit_kind':u['kind'],'printed_numbers':u['printed_numbers'],'full_text_read':True,
 **{k:r[k] for k in ['facts','inferences','state_changes','unresolved']}}
 new.append(n)
allrows=old+new;np.write_text(''.join(json.dumps(n,ensure_ascii=False)+'\n' for n in allrows),encoding='utf-8');readids=[r['chapter_id'] for r in allrows]
body_complete=sum(u['kind']=='body' and all(s['chapter_id'] in readids for s in u['segments']) for u in spec['units'])
complete=readids==expected
state={'source_id':source['source_id'],'revision':source['revision'],'volume':volume,'reader':'/root/zongheng_vol03_full','read_chapter_ids':readids,
 'read_raw_fragments':len(readids),'expected_raw_fragments':len(expected),'read_body_units':body_complete,'expected_body_units':spec['body_units'],
 'next_chapter_id':expected[len(readids)] if not complete else None,'current_chapter_id':None,'pending_truncations':[],'complete':complete,
 'last_batch':payload_path.name,'current_state':payload.get('current_state',{}),'status':'reading' if not complete else 'full-volume-read-artifacts-pending'}
save(P/'reader-state.json',state)
log={'source_id':source['source_id'],'revision':source['revision'],'volume':volume,'reader':'/root/zongheng_vol03_full','chapters':[{k:r[k] for k in ['chapter_id','start_line','end_line','full_text_read','unit_id','unit_kind','reader']} for r in allrows],
 'complete_book':False,'complete_volume':complete,'method':'每次1—2原索引片段逐行全文输出，逐次确认BEGIN/END无截断；2—4片即时手写四栏笔记。raw片段与合并正文单元分别计数。',
 'raw_fragments':len(readids),'body_units':body_complete,'source_sha256':source['revision'],'unresolved_truncations':[]}
save(P/'read-log.json',log)
print(json.dumps({'volume':volume,'raw_fragments':len(readids),'body_units':body_complete,'next':state['next_chapter_id'],'complete':complete},ensure_ascii=False))
