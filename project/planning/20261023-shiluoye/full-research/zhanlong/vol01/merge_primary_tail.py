"""合并已逐项派生读完的primary笔记，原行字节不改；不生成文学事实。"""
from pathlib import Path
import json,hashlib,collections
from datetime import datetime,timezone
P=Path(__file__).parent;T=P.parent/'primary-vol01-tail'
load=lambda p:json.loads(p.read_text(encoding='utf-8'))
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert not (P/'merge-receipt.json').exists(),'already merged'
for name in ('chapter-notes.jsonl','read-log.json','reader-state.json'):
 (P/('prefix-'+name)).write_bytes((P/name).read_bytes())
raw_prefix=(P/'prefix-chapter-notes.jsonl').read_bytes();raw_tail=(T/'chapter-notes.jsonl').read_bytes()
prefix=[json.loads(s) for s in raw_prefix.decode('utf-8').splitlines() if s.strip()]
tail=[json.loads(s) for s in raw_tail.decode('utf-8').splitlines() if s.strip()]
assert len(prefix)==150 and len(tail)==100
assert [r['chapter_id'] for r in prefix]==[f'ch-{i:04d}' for i in range(2,152)]
assert [r['chapter_id'] for r in tail]==[f'ch-{i:04d}' for i in range(152,252)]
assert all(r['reader']=='primary' for r in tail)
assert all(r['full_text_read'] and all(k in r for k in ('facts','inferences','state_changes','unresolved')) for r in prefix+tail)
source=load(P.parent/'source.json');spec=next(v for v in source['volumes'] if v['volume']==1)
ids=[r['chapter_id'] for r in prefix+tail];expected=[s['chapter_id'] for u in spec['units'] for s in u['segments']]
assert ids==expected and len(set(ids))==250
chapters={r['chapter_id']:r for r in source['chapters']}
for r in prefix+tail:assert (r['start_line'],r['end_line'])==(chapters[r['chapter_id']]['start_line'],chapters[r['chapter_id']]['end_line'])
merged=raw_prefix+(b'' if raw_prefix.endswith(b'\n') else b'\n')+raw_tail
(P/'chapter-notes.jsonl').write_bytes(merged)
assert (P/'chapter-notes.jsonl').read_bytes().endswith(raw_tail)
now=datetime.now(timezone.utc).isoformat()
attribution={'source_id':source['source_id'],'revision':source['revision'],'volume':1,'method':'两读者分工全文实读；卷负责人随后完整派生读取primary尾100条四栏，不计自己原文覆盖。','readers':[{'reader':'/root/zongheng_vol03_full','raw_range':[2,151],'raw_fragments':150,'body_units':148,'mode':'original-full-text'},{'reader':'primary','raw_range':[152,251],'raw_fragments':100,'body_units':100,'mode':'original-full-text'}],
 'derived_note_reading':{'reader':'/root/zongheng_vol03_full','source':str(T/'chapter-notes.jsonl'),'source_sha256':sha(T/'chapter-notes.jsonl'),'notes':100,'ranges':[[152,161],[162,181],[182,201],[202,221],[222,241],[242,251]],'all_four_fields_read':True,'handoff_read':True,'read_at':now,'encoding_repair':'首152—161输出编码不明，已以-X utf8重新全文显示并完整读；不把乱码算已读。'},'review_status':'draft'}
save(P/'reading-attribution.json',attribution)
state=load(P/'prefix-reader-state.json');state.update(reader='split-reading: agent3 + primary',read_chapter_ids=ids,read_raw_fragments=250,read_body_units=248,next_chapter_id=None,current_chapter_id=None,complete=True,status='full-volume-split-read-artifacts-in-progress',reading_attribution='reading-attribution.json',pending_truncations=[],current_state={'volume_end':'251红草夹击仍进行/简首折跃未死/矿权未结；秦王醒魂100%仍半品不能穿，南宫决9采/妹灵9铸未正式入斩龙。','protagonist':'64新三转龙域守夜者、神虎已孵实练且241曾死/后又战；来源具体装备状态以尾笔记。','organizations':'斩龙200实建/201二级满300/245报三级972，倾浅副/李牧长老；林东仍英雄冢。','boundaries':'NPC冉闵实复生守谷/罗林仅誓忠；云辰交卷后灵体消散，卡尔流霜争议未消；改造体幕后未知。'})
save(P/'reader-state.json',state)
logs=load(P/'prefix-read-log.json')['chapters']+load(T/'read-log.json')['chapters']
assert [r['chapter_id'] for r in logs]==ids
save(P/'read-log.json',{'source_id':source['source_id'],'revision':source['revision'],'volume':1,'chapters':logs,'complete_book':False,'complete_volume':True,'raw_fragments':250,'body_units':248,'method':attribution['method'],'reading_attribution':'reading-attribution.json','unresolved_truncations':[]})
receipt={'source_id':source['source_id'],'revision':source['revision'],'volume':1,'merged_at':now,'coverage':{'raw_fragments':250,'body_units':248,'no_overlap':True,'no_gap':True,'expected_source_segments_match':True},'inputs':{str(P/'prefix-chapter-notes.jsonl'):sha(P/'prefix-chapter-notes.jsonl'),str(T/'chapter-notes.jsonl'):sha(T/'chapter-notes.jsonl')},'primary_rows_byte_preserved':True,'tail_suffix_identical':True,'canonical_sha256':sha(P/'chapter-notes.jsonl'),'reader_counts':dict(collections.Counter(r['reader'] for r in prefix+tail)),'derived_notes_reading':attribution['derived_note_reading']}
save(P/'merge-receipt.json',receipt)
print(json.dumps(receipt,ensure_ascii=False,indent=2))
