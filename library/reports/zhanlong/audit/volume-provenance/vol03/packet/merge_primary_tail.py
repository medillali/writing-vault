"""只拼接实际读者的原行，并记录主代理完整派生接读；不生成阅读内容。"""
import pathlib,json,hashlib,collections,sys
P=pathlib.Path(__file__).parent;T=P.parent/'primary-vol03-tail'
sys.stdout.reconfigure(encoding='utf-8')
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(n,x):(P/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
S=read(P.parent/'source.json');spec=next(v for v in S['volumes'] if v['volume']==3)
ids=[s['chapter_id'] for u in spec['units'] for s in u['segments']]
prefix=P/'prefix-chapter-notes.jsonl';tail=T/'chapter-notes.jsonl'
assert sha(prefix)=='3e7818ff524689dc23e4f1bb9551685922463b663535b329e617f37312f64ad1'
assert sha(P/'prefix-reader-state.json')=='d33a189ac3bfe6b95b6a07c626ad948e0493e522028db6a15d273c548d212f0e'
receipt=read(P/'primary-prefix-derived-reading-progress.json')
assert receipt['complete_prefix_derived_reading'] and len(receipt['read_chapter_ids'])==149
pa=[json.loads(x) for x in prefix.read_text(encoding='utf-8').splitlines() if x]
ta=[json.loads(x) for x in tail.read_text(encoding='utf-8').splitlines() if x]
assert len(pa)==149 and len(ta)==100 and [x['chapter_id'] for x in pa+ta]==ids
assert all(x['reader']=='zongheng_vol05_full' for x in pa) and all(x['reader']=='primary' for x in ta)
assert all(x['full_text_read'] is True for x in pa+ta)
(P/'chapter-notes.jsonl').write_bytes(prefix.read_bytes().rstrip(b'\r\n')+b'\n'+tail.read_bytes().rstrip(b'\r\n')+b'\n')
assert (P/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines()==prefix.read_text(encoding='utf-8').splitlines()+tail.read_text(encoding='utf-8').splitlines()
pl=read(P/'prefix-read-log.json');tl=read(T/'read-log.json')
save('read-log.json',{'source_id':S['source_id'],'revision':S['revision'],'volume':3,'complete_volume':True,'complete_book':False,'indexed_segments_read':249,'body_units_read':248,'chapters':pl['chapters']+tl['chapters'],'method':'前149片zongheng_vol05_full逐片实际全文，后100片primary逐片实际全文；主代理另完整派生接读前149条四栏，不冒称个人整卷原文阅读。','truncated_pending':[],'anomalies':[]})
save('reader-state.json',{'source_id':S['source_id'],'revision':S['revision'],'volume':3,'status':'full-volume-reading-complete-research-in-progress','read_chapter_ids':ids,'indexed_segments_read':249,'body_units_read':248,'complete_volume':True,'complete_book':False,'next_chapter_id':None,'truncated_pending':[],'notes_sha256':sha(P/'chapter-notes.jsonl'),'assembler':'primary','personal_full_volume_raw_read':False,'prefix_notes_derived_read_complete':True})
save('reading-attribution.json',{'source_id':S['source_id'],'revision':S['revision'],'volume':3,'total_raw_segments':249,'total_body_units':248,'complete_volume':True,'complete_book':False,'assembler':'primary','personal_full_volume_claim':False,'readers':[{'reader':'zongheng_vol05_full','range':'raw0505—0653','raw_segments':149,'body_units':148,'primary_input':'prefix-chapter-notes.jsonl','sha256':sha(prefix)},{'reader':'primary','range':'raw0654—0753','raw_segments':100,'body_units':100,'primary_input':'../primary-vol03-tail/chapter-notes.jsonl','sha256':sha(tail)}],'derived_input_receipt':'primary-prefix-derived-reading-progress.json'})
save('merge-receipt.json',{'status':'passed','raw_segments':249,'body_units':248,'prefix_original_lines_unchanged':True,'tail_original_lines_unchanged':True,'reader_fields_unchanged':True,'prefix_derived_all_149_read':True,'reader_counts':dict(collections.Counter(n['reader'] for n in pa+ta)),'inputs_sha256':{'prefix-chapter-notes.jsonl':sha(prefix),'primary-prefix-derived-reading-progress.json':sha(P/'primary-prefix-derived-reading-progress.json'),'../primary-vol03-tail/chapter-notes.jsonl':sha(tail),'../primary-vol03-tail/HANDOFF.md':sha(T/'HANDOFF.md')},'merged_notes_sha256':sha(P/'chapter-notes.jsonl')})
print(json.dumps({'raw':249,'body':248,'readers':dict(collections.Counter(n['reader'] for n in pa+ta)),'prefix_derived_complete':True},ensure_ascii=False))
