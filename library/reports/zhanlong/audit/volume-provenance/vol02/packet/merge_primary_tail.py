"""把两位实际读者的原始笔记原行拼接，保留前段快照，不生成正文阅读。"""
import pathlib,json,hashlib,datetime
P=pathlib.Path(__file__).parent; T=P.parent/'primary-vol02-tail'
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def save(n,x):(P/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
S=read(P.parent/'source.json');spec=next(v for v in S['volumes'] if v['volume']==2)
ids=[s['chapter_id'] for u in spec['units'] for s in u['segments']]
for n in ['chapter-notes.jsonl','reader-state.json','read-log.json']:
 q=P/('prefix-'+n)
 if not q.exists():q.write_bytes((P/n).read_bytes())
prefix=P/'prefix-chapter-notes.jsonl'; tail=T/'chapter-notes.jsonl'
pa=[json.loads(x) for x in prefix.read_text(encoding='utf-8').splitlines() if x];ta=[json.loads(x) for x in tail.read_text(encoding='utf-8').splitlines() if x]
assert len(pa)==153 and len(ta)==100
assert all(x['reader']=='/root/zongheng_vol04_full' for x in pa)
assert all(x['reader']=='primary' for x in ta)
assert [x['chapter_id'] for x in pa+ta]==ids
assert all(x['full_text_read'] for x in pa+ta)
# 本代理已按0:8至94:100十三批完整读取全部四栏，无截断；不是原文重读。
receipt={'source_id':S['source_id'],'revision':S['revision'],'status':'derived-notes-completely-read','derived_reader':'/root/zongheng_vol04_full','original_reader':'primary','chapter_ids':[x['chapter_id'] for x in ta],'count':100,'method':'read_tail_notes.py按0:8、8:16、16:24、24:32、32:40、40:48、48:56、56:64、64:72、72:80、80:88、88:94、94:100完整输出，逐条读四栏；首次乱码0:8修stdout后全文重读，不算原文亲读。','input_sha256':h(tail),'read_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'raw_text_personally_read':False}
save('tail-derived-reading-receipt.json',receipt)
out=prefix.read_bytes().rstrip(b'\r\n')+b'\n'+tail.read_bytes().rstrip(b'\r\n')+b'\n';(P/'chapter-notes.jsonl').write_bytes(out)
assert (P/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines()==prefix.read_text(encoding='utf-8').splitlines()+tail.read_text(encoding='utf-8').splitlines()
pl=read(P/'prefix-read-log.json');tl=read(T/'read-log.json')
log={'source_id':S['source_id'],'revision':S['revision'],'volume':2,'complete_volume':True,'complete_book':False,'indexed_segments_read':253,'body_units_read':252,'chapters':pl['chapters']+tl['chapters'],'method':'两读者各自逐片BEGIN-END全文；前段153片本代理、后100片primary。原笔记原行拼接，本代理完整读取尾段四栏派生。','truncated_pending':[],'anomalies':[]}
save('read-log.json',log)
save('reading-attribution.json',{'source_id':S['source_id'],'revision':S['revision'],'volume':2,'total_raw_segments':253,'total_body_units':252,'complete_volume':True,'complete_book':False,'readers':[{'reader':'/root/zongheng_vol04_full','range':'raw0252—0404','raw_segments':153,'body_units':152,'primary_input':'prefix-chapter-notes.jsonl','sha256':h(prefix)},{'reader':'primary','range':'raw0405—0504','raw_segments':100,'body_units':100,'primary_input':'../primary-vol02-tail/chapter-notes.jsonl','sha256':h(tail)}],'assembler':'/root/zongheng_vol04_full','tail_derived_receipt':'tail-derived-reading-receipt.json','personal_full_volume_claim':False})
save('reader-state.json',{'source_id':S['source_id'],'revision':S['revision'],'volume':2,'status':'full-volume-reading-complete-research-in-progress','read_chapter_ids':ids,'indexed_segments_read':253,'body_units_read':252,'complete_volume':True,'complete_book':False,'complete_personal_prefix':True,'personal_raw_range':'raw0252—0404','tail_raw_reader':'primary','tail_notes_derived_read_complete':True,'next_chapter_id':None,'truncated_pending':[],'notes_sha256':h(P/'chapter-notes.jsonl'),'current_stage':['504止公主率五万寒风实际放行、兄妹活逃仍未入青麟渊/24h未结。','池阳历史经记忆晶/石尸/灵念明示；秦蒙死亡已证而凶手未明，主御气巅峰/电弧剑实得未验证破阳炎。','九维/卡图/report/handoff待写，完整覆盖不等文学主审或全书已完。']})
save('merge-receipt.json',{'status':'passed','raw_segments':253,'body_units':252,'prefix_original_lines_unchanged':True,'tail_original_lines_unchanged':True,'reader_fields_unchanged':True,'tail_derived_all_100_read':True,'inputs_sha256':{'prefix-chapter-notes.jsonl':h(prefix),'../primary-vol02-tail/chapter-notes.jsonl':h(tail),'../primary-vol02-tail/read-log.json':h(T/'read-log.json'),'../primary-vol02-tail/reader-state.json':h(T/'reader-state.json'),'../primary-vol02-tail/HANDOFF.md':h(T/'HANDOFF.md')},'merged_notes_sha256':h(P/'chapter-notes.jsonl')})
print(json.dumps({'merged':len(ids),'body':252,'notes_sha256':h(P/'chapter-notes.jsonl')},ensure_ascii=False))
