"""只读定位当前主档卡片中的相关身份字段；不将关键词命中当事实判断。"""
from pathlib import Path
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
root=Path(__file__).resolve().parents[3]
sid='src-d8926e2a35f04bcf8139cff0ea516bbd'
def walk(x,p=''):
    if isinstance(x,dict):
        for k,v in x.items():yield from walk(v,p+'/'+k)
    elif isinstance(x,list):
        for i,v in enumerate(x):yield from walk(v,p+'/'+str(i))
    elif isinstance(x,str) and ('谁与争锋' in x or '谁中165' in x):yield p,x
count=0
for folder in ['characters','scenes','patterns']:
    for path in sorted((root/'writing-vault/library'/folder).glob('*.json')):
        obj=json.loads(path.read_text(encoding='utf-8'))
        if not any(e.get('source_id')==sid for e in obj.get('evidence',[])):continue
        hits=list(walk(obj))
        if hits:
            count+=len(hits)
            print(json.dumps({'file':path.relative_to(root).as_posix(),'title':obj.get('title'),'matches':hits},ensure_ascii=False))
print(json.dumps({'matched_fields':count,'read_only':True}))
