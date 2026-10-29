"""为跨书比较重读已发表综合的文学语义；证据与上游记录只折叠显示，不创建阅读状态。"""
import json, pathlib, sys
sys.stdout.reconfigure(encoding='utf-8')
path=pathlib.Path(sys.argv[1])
data=json.loads(path.read_text(encoding='utf-8'))
for dimension in sys.argv[2].split(','):
    for row in data['dimensions'][dimension]:
        result={k:v for k,v in row.items() if k not in ['supporting_observations','evidence']}
        result['dimension']=dimension
        result['upstream_observations']=len(row.get('supporting_observations',[]))
        result['evidence_chapters']=list(dict.fromkeys(e['chapter_id'] for e in row.get('evidence',[])))
        result['published_source_path']=path.as_posix()
        print(json.dumps(result,ensure_ascii=False,separators=(',',':')))
