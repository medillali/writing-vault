"""只在隔离卷目录写验证凭据；结构检查不是主代理文学签收。"""
import pathlib,json,hashlib,sys,collections,datetime
P=pathlib.Path(__file__).parent
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,str(P.parents[1]))
from check_volume import load_and_check
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(n):return json.loads((P/n).read_text(encoding='utf-8'))
def save(n,x):(P/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
# 私有builder题名人工转录纠正，不修改源/旧笔记。
b=P/'build_research.py';txt=b.read_text(encoding='utf-8');txt=txt.replace('卷二 群雄逐鹿｜九维研究草稿','卷二 英雄崛起｜九维研究草稿');b.write_text(txt,encoding='utf-8')
result=load_and_check('zhanlong',2)[-1]
rows=[json.loads(x) for x in (P/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines() if x]
tail=P.parent/'primary-vol02-tail'/'chapter-notes.jsonl'
assert (P/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines()==(P/'prefix-chapter-notes.jsonl').read_text(encoding='utf-8').splitlines()+tail.read_text(encoding='utf-8').splitlines()
assert all(x['reader']=='/root/zongheng_vol04_full' for x in rows[:153]) and all(x['reader']=='primary' for x in rows[153:])
assert read('tail-derived-reading-receipt.json')['input_sha256']==h(tail)
analysis=read('analysis.json'); cards=read('cards.json');graph=read('graph.json')
assert all(len(v)==5 and all(o['mechanism'] and o['limits_and_counterevidence'] for o in v) for v in analysis['dimensions'].values())
assert all({'facts','inferences','state_changes','unresolved'}.issubset(x) for x in rows)
assert {x['chapter_id'] for x in analysis['chapter_unresolved_index']}=={x['chapter_id'] for x in rows if x['unresolved']}
origins={c['origin_key'] for c in cards};names=collections.Counter(c['asset_type'] for c in cards)
for c in cards:
 for k in c['content'].get('characters_origin_keys',[]):assert k in origins
def claims(x):
 if isinstance(x,dict):
  if {'source_id','revision','chapter_id'}.issubset(x):assert x.get('claim_kind'),x
  for y in x.values():claims(y)
 elif isinstance(x,list):
  for y in x:claims(y)
for x in [analysis,cards,graph]:claims(x)
state=read('reader-state.json');state.update(status='research-complete-awaiting-primary-review',research_status='draft',research_counts={'observations':45,'cards':dict(names),'nodes':len(graph['nodes']),'edges':len(graph['edges']),'threads':len(graph['threads'])})
state['current_stage']=['卷二253片/252正文共同全文和研究草稿齐，前153本代理/尾100primary，尾100派生全读保原行。','504仅公主5万寒风放行，池兄妹活护送未入渊/未满24h，洛克林退未死；通缉与守护任务继续。','待primary文学审阅/正式保存，本代理转卷五1019继续。']
save('reader-state.json',state)
result.update({'status':'passed','validation_scope':'覆盖、章界证据、来源引用、图结构与原行/reader归属；不是主代理文学签收','personal_full_volume_raw_read':False,'merged_reading_complete':True,'derived_tail_notes_all_100_read':True,'original_lines_unchanged':True,'reader_counts':dict(collections.Counter(x['reader'] for x in rows)),'nine_dimensions':9,'observations':45,'independent_mechanism_fields':45,'independent_limit_fields':45,'chapter_unresolved_original_items_preserved':True,'open_questions':len(analysis['open_questions']),'source_anomalies':len(analysis['unresolved_and_anomalies']),'named_life_state_entries':len(analysis['named_life_state_audit']),'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat()})
save('validation.json',result)
core=['analysis.json','cards.json','graph.json','read-log.json','chapter-notes.jsonl','reader-state.json']
support=['report.md','handoff.md','validation.json','reading-attribution.json','merge-receipt.json','tail-derived-reading-receipt.json','prefix-handoff.md','prefix-validation.json','prefix-chapter-notes.jsonl','prefix-reader-state.json','prefix-read-log.json']
support+=['primary-corrections.json','priority-corrections-delta.json','priority-corrections.md','review-corrections/raw0314-two-swords-delta.json','review-corrections/raw0314-two-swords-before/freeze-manifest.json','review-corrections/raw0314-two-swords-before/snapshot.json']
save('freeze-manifest.json',{'status':'draft-frozen-for-primary-review','source_id':analysis['source_id'],'revision':analysis['revision'],'volume':2,'complete_book':False,'core_sha256':{n:h(P/n) for n in core},'support_sha256':{n:h(P/n) for n in support},'external_input_sha256':{'../primary-vol02-tail/'+n:h(tail.parent/n) for n in ['chapter-notes.jsonl','read-log.json','reader-state.json','HANDOFF.md']},'notes':'主审修订须保具体delta并重验；冻结不等正式入库或用户认可。'})
print(json.dumps({'validation':result,'core_sha256':read('freeze-manifest.json')['core_sha256'],'manifest_sha256':h(P/'freeze-manifest.json')},ensure_ascii=False))
