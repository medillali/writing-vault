import json,pathlib,re,sys
sys.stdout.reconfigure(encoding='utf-8')
b=pathlib.Path(__file__).parent
s=json.loads((b/'source.json').read_text(encoding='utf-8-sig'))
rows=[]
for line in (b/'reading-notes.md').read_text(encoding='utf-8').splitlines():
 m=re.match(r'- 第(\d+)章 (ch-\d+) (\d+)—(\d+)：(.*)',line)
 if not m: continue
 n,cid,start,end,summary=m.groups()
 c=next(c for c in s['chapters'] if c['chapter_id']==cid)
 assert int(start)==c['start_line'] and int(end)==c['end_line']
 rows.append({'chapter_id':cid,'original_chapter_number':int(n),'title':c['title'],'start_line':int(start),'end_line':int(end),'fact_summary':summary,'full_text_read':True,'reading_method':'模型逐章全文读取并分析','reread_after_truncation':int(n)==17})
out={'source_id':s['source_id'],'revision':s['revision'],'scope':'卷一连续正文阅读','complete_book':False,'chapters':rows,'read_chapter_count':len(rows),'next_chapter_id':f'ch-{len(rows)+2:04d}'}
(b/'read-log.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('saved',len(rows),'full chapters')
