import pathlib,sys,json,hashlib
sys.stdout.reconfigure(encoding='utf-8')
root=pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0,str(root/'distill-novels/scripts'))
from prepare_sources import prepare
from fictionlib.vault import Vault
paths=[pathlib.Path('E:/chromedownload')/n for n in ['《贼胆》（校对版全本）作者：发飙的蜗牛.txt','《网游之练级专家》（校对版全本）作者：发飙的蜗牛.txt']]
m=prepare(paths,root/'writing-vault/private-sources/normalized')
print(Vault(root/'writing-vault').import_sources(m))
old=root.parent/'Chinese Novel/books/zeidan'
om=json.loads((old/'manifest.json').read_text(encoding='utf-8'))
raw=paths[0].read_bytes()
assert hashlib.sha256(raw).hexdigest()==om['source']['sha256']
t=raw.decode('gb18030').replace('\r\n','\n').replace('\r','\n')
rev=hashlib.sha256(t.encode()).hexdigest()
s=next(s for s in m['sources'] if s['revision']==rev)
lookup={c['start_line']:c for c in s['chapters']}
mapping=[]
for c in om['chapters']:
    nc=lookup[c['line_start']]
    assert nc['end_line']==c['line_end'],(c,nc)
    assert nc['title']==c['title'],(c,nc)
    mapping.append({'legacy_sequence':c['sequence'],'legacy_chapter_id':c['id'],'chapter_id':nc['chapter_id'],'title':nc['title'],'start_line':nc['start_line'],'end_line':nc['end_line']})
work=root/'.planning/20261023-shiluoye/zeidan';work.mkdir(exist_ok=True)
(work/'source.json').write_text(json.dumps(s,ensure_ascii=False,indent=2),encoding='utf-8')
(work/'chapter-map.json').write_text(json.dumps(mapping,ensure_ascii=False,indent=2),encoding='utf-8')
print('zeidan',s['source_id'],'mapped',len(mapping),'segments',len(s['chapters']))
for s in m['sources']:
    if '练级专家' in s['title']:print(s['title'],s['source_id'],len(s['chapters']))
