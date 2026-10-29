"""只读核验个人前段真实笔记、源章界及状态；不是整卷文学验收。"""
import pathlib,json,hashlib
V=pathlib.Path(__file__).resolve().parent
s=json.loads((V.parent/'source.json').read_text(encoding='utf-8'))
rows=[json.loads(x) for x in (V/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines() if x]
state=json.loads((V/'reader-state.json').read_text(encoding='utf-8'));log=json.loads((V/'read-log.json').read_text(encoding='utf-8'))
expected=[f'ch-{i:04d}' for i in range(252,405)];canon={x['chapter_id']:x for x in s['chapters']}
assert [x['chapter_id'] for x in rows]==expected==state['read_chapter_ids']
assert len(rows)==153 and len({x['unit_id'] for x in rows if x['unit_kind']=='body'})==152
for x in rows:
 c=canon[x['chapter_id']]
 assert x['full_text_read'] is True and x['reader']=='/root/zongheng_vol04_full'
 assert x['source_id']==s['source_id'] and x['revision']==s['revision']
 assert (x['start_line'],x['end_line'])==(c['start_line'],c['end_line'])
 assert all(isinstance(x[k],list) for k in ['facts','inferences','state_changes','unresolved'])
assert state['complete_personal_prefix'] and not state['complete_volume'] and state['next_chapter_id'] is None
assert not log['complete_volume'] and not state['truncated_pending']
assert [x['chapter_id'] for x in log['chapters']]==expected
files=['chapter-notes.jsonl','reader-state.json','read-log.json','reading-scope.json','prefix-handoff.md']
out={'status':'passed_personal_prefix_only','source_id':s['source_id'],'revision':s['revision'],'reader':'/root/zongheng_vol04_full','indexed_segments':153,'body_units':152,'range':['ch-0252','ch-0404'],'primary_tail':['ch-0405','ch-0504'],'primary_tail_read_by_this_reader':False,'complete_volume':False,'truncated_pending':[],'checks':['连续实际逐片笔记与read-log一致','源身份及章界逐项一致','全四栏/归属存在','state仅个人前段完成，全卷false'],'sha256':{f:hashlib.sha256((V/f).read_bytes()).hexdigest() for f in files}}
(V/'prefix-validation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out,ensure_ascii=False))
