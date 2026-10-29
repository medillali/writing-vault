from pathlib import Path
import json,hashlib,sys
R=Path(__file__).resolve().parents[2];V=R/'writing-vault';P=Path(__file__).parent
m=json.loads((V/'private-sources/normalized/manifest.json').read_text(encoding='utf-8'))
all_units=json.loads((V/'library/reports/collection/reading-units.json').read_text(encoding='utf-8'))
books={}
for key,sid in [('z','src-2d8a13f33737429da512e5cc9e839712'),('l','src-359a2bd5a60747038b12a7ba483a5f80')]:
 s=next(s for s in m['sources'] if s['source_id']==sid)
 textpath=Path(s['normalized_path']);body=textpath.read_text(encoding='utf-8')
 assert hashlib.sha256(body.encode()).hexdigest()==s['revision']
 units=[u for u in all_units[sid]['units'] if u['kind'] in ['body','prologue']]
 books[key]={'source_id':sid,'revision':s['revision'],'title':s['title'],'normalized_path':str(textpath),'characters':len(body),'units':units,'chapters':s['chapters'],'index_corrections':all_units[sid].get('index_corrections',[])}
 print(key,sid,s['title'],len(body),'chars',len(s['chapters']),'segments',len(units),'reading units', 'first',units[0]['title'],'last',units[-1]['title'])
(P/'sources.json').write_text(json.dumps(books,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
