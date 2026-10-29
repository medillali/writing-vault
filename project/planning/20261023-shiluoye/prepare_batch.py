import pathlib,sys,json,hashlib,re,collections
sys.stdout.reconfigure(encoding='utf-8')
root=pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0,str(root/'distill-novels/scripts'))
from prepare_sources import prepare
from fictionlib.vault import Vault
inputs=[pathlib.Path('E:/chromedownload')/n for n in ['《网游之天下无双》（校对版全本）作者：失落叶.txt','《网游之纵横天下》（校对版全本）作者：失落叶 (1).txt','《斩龙》（校对版全本）作者：失落叶.txt']]
out=root/'writing-vault/private-sources/normalized'
m=prepare(inputs,out)
print('prepared',len(m['sources']),flush=True)
v=Vault(root/'writing-vault')
print('import',v.import_sources(m),flush=True)
audit=[]
for p in inputs:
    data=p.read_bytes(); t=data.decode('gb18030').replace('\r\n','\n').replace('\r','\n'); rev=hashlib.sha256(t.encode()).hexdigest()
    s=next(s for s in m['sources'] if s['revision']==rev)
    chapters=s['chapters']; nums=[]
    for c in chapters:
        n=re.search(r'第\s*(\d+)\s*章',c['title'])
        if n: nums.append(int(n[1]))
    item={'input_path':str(p),'file_sha256':hashlib.sha256(data).hexdigest(),'source_id':s['source_id'],'revision':rev,'title':s['title'],'characters':len(t),'indexed_segments':len(chapters),'normalized_sha256_verified':hashlib.sha256(pathlib.Path(s['normalized_path']).read_bytes()).hexdigest()==rev,'detected_encoding':'gb18030','numeric_chapters':len(nums),'duplicate_numbers':[n for n,c in collections.Counter(nums).items() if c>1],'missing_numbers':sorted(set(range(1,max(nums)+1))-set(nums)) if nums else [],'preamble_segments':[c['chapter_id'] for c in chapters if c['title']=='章前内容']}
    audit.append(item)
    print(json.dumps(item,ensure_ascii=False),flush=True)
    print('first',chapters[:3],'last',chapters[-2:],flush=True)
    slug={'网游之天下无双':'tianxia-wushuang','网游之纵横天下':'zongheng-tianxia','斩龙':'zhanlong'}
    key=next(k for k in slug if k in s['title'])
    work=root/'.planning/20261023-shiluoye'/slug[key];work.mkdir(exist_ok=True)
    (work/'source.json').write_text(json.dumps(s,ensure_ascii=False,indent=2),encoding='utf-8')
(root/'.planning/20261023-shiluoye/source-audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
