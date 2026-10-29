import pathlib,json
base=pathlib.Path(__file__).resolve().parent
src=json.loads((base.parent/'zongheng-tianxia/source.json').read_text(encoding='utf-8-sig'))
notes=json.loads((base/'notes-data.json').read_text(encoding='utf-8'))
chapters=src['chapters']
records=[]
for number,summary in sorted(notes.items(),key=lambda x:int(x[0])):
    c=chapters[int(number)]
    records.append({'chapter_id':c['chapter_id'],'title':c['title'],'start_line':c['start_line'],'end_line':c['end_line'],'full_text_read':True,'fact_summary':summary})
payload={'source_id':src['source_id'],'revision':src['revision'],'reading_method':'模型逐章全文读取并分析','coverage_complete':False,'complete_book':False,'fully_read_chapter_count':len(records),'chapters':records}
(base/'read-log.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
header=['# 《网游之纵横天下》卷二连续阅读笔记','','目标范围：正文第50—100章。模型逐章全文读取并分析，索引不计阅读；本笔记仅列实际全文已读章节。','', '继承第49章状态：巫师之心未完成；追星弓失去必中且全力量命中风险待看；旧弓待卖；法杖5000现金已兑现；复活预言同人2小时仅能受益一次。旧年龄、职业、货币、错名等疑点无证据时保留。','']
for c in records:header.append('- '+c['chapter_id']+' '+c['title']+' L'+str(c['start_line'])+'—'+str(c['end_line'])+'：'+c['fact_summary'])
(base/'reading-notes.md').write_text('\n'.join(header)+'\n',encoding='utf-8')
print('saved_read_chapters',len(records))
