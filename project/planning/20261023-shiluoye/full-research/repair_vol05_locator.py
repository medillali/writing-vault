"""依据主代理逐章回读及精确查证修正单处定位，不改研究范围。"""
import pathlib,json
root=pathlib.Path(__file__).resolve().parent
directory=root/'zongheng-tianxia/vol05'
source=json.loads((root/'zongheng-tianxia/source.json').read_text(encoding='utf-8'))
path=directory/'analysis.json';data=json.loads(path.read_text(encoding='utf-8'))
issue=next(x for x in data['unresolved_and_anomalies'] if x['id']=='first-soul')
assert issue['evidence'][0]['chapter_id']=='ch-0478'
chapter=next(c for c in source['chapters'] if c['chapter_id']=='ch-0479')
issue['evidence'][0].update(chapter_id='ch-0479',start_line=chapter['start_line'],end_line=chapter['end_line'])
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
path=directory/'handoff.md';text=path.read_text(encoding='utf-8')
text=text.replace('（原477、527）','（原478、527）')
path.write_text(text,encoding='utf-8')
print('first-soul: ch-0478 -> ch-0479 L49414—49535; handoff原478')
