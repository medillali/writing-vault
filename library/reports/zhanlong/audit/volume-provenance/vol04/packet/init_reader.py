"""只初始化本卷元数据和真实空检查点，不读取正文。"""
import json,sys,hashlib
from pathlib import Path
P=Path(__file__).parent;B=P.parent
S=json.loads((B/'source.json').read_text(encoding='utf-8'));V=next(v for v in S['volumes'] if v['volume']==4)
ROOT=next(p for p in P.parents if (p/'writing-vault').exists())
RU=ROOT/'writing-vault/library/reports/collection/reading-units.json'
R=json.loads(RU.read_text(encoding='utf-8'))[S['source_id']]
expected=[s['chapter_id'] for u in V['units'] for s in u['segments']]
assert expected==[f'ch-{i:04d}' for i in range(754,969)]
mapped=[u for u in R['units'] if any(s in expected for s in u['segment_ids'])]
assert [s for u in mapped for s in u['segment_ids']]==expected
assert sum(u['kind']=='body' for u in mapped)==214
assert not (P/'reader-state.json').exists(),'不覆盖真实检查点'
def save(name,x):(P/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
save('metadata-check.json',{'source_id':S['source_id'],'revision':S['revision'],'volume':4,'expected_raw_fragments':len(expected),'expected_body_units':214,'first':expected[0],'last':expected[-1],'reading_units_sha256':hashlib.sha256(RU.read_bytes()).hexdigest(),'special_units':[u for u in mapped if u['kind']!='body' or len(u['segment_ids'])!=1],'source_spec_match':True,'predecessor_boundary':'本代理只读卷一，卷二三前态暂缺；从本卷起点保阶段边界，必要时读已交正式接口另记派生归属，不猜前态。'})
save('reader-state.json',{'source_id':S['source_id'],'revision':S['revision'],'volume':4,'reader':'/root/zongheng_vol03_full','read_chapter_ids':[],'read_raw_fragments':0,'expected_raw_fragments':215,'read_body_units':0,'expected_body_units':214,'next_chapter_id':expected[0],'pending_truncations':[],'complete':False,'status':'reading','current_state':{'boundary':'尚未读取卷四正文；不据目录预填事实。'}})
save('read-log.json',{'source_id':S['source_id'],'revision':S['revision'],'volume':4,'reader':'/root/zongheng_vol03_full','chapters':[],'complete_book':False,'complete_volume':False,'raw_fragments':0,'body_units':0,'unresolved_truncations':[]})
(P/'chapter-notes.jsonl').write_text('',encoding='utf-8')
print(json.dumps({'raw':len(expected),'body':214,'special':[u for u in mapped if u['kind']!='body' or len(u['segment_ids'])!=1]},ensure_ascii=False))
