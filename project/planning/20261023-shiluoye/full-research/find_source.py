"""在指定章内查证定位；匹配不能代替完整阅读。"""
import pathlib,json,sys
root=pathlib.Path(__file__).resolve().parent
book,term,start,end=sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4])
source=json.loads((root/book/'source.json').read_text(encoding='utf-8'))
lines=pathlib.Path(source['normalized_path']).read_text(encoding='utf-8').splitlines()
sys.stdout.reconfigure(encoding='utf-8')
for c in source['chapters']:
    if start<=int(c['chapter_id'].split('-')[1])<=end:
        for n in range(c['start_line'],c['end_line']+1):
            if term in lines[n-1]:print(c['chapter_id']+' '+c['title']+f' L{n}: '+lines[n-1])
