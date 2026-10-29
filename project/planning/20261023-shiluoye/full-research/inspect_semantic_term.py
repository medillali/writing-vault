"""定向检查研究措辞和它所在条目的证据章，不替代原文阅读。"""
import json,sys
from pathlib import Path
data=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'));term=sys.argv[2]
sys.stdout.reconfigure(encoding='utf-8')
def walk(x,path='',context=None):
 if isinstance(x,dict):
  context=x if 'evidence' in x else context
  for k,v in x.items():walk(v,path+'/'+k,context)
 elif isinstance(x,list):
  for i,v in enumerate(x):walk(v,path+'/'+str(i),context)
 elif isinstance(x,str) and term in x:
  ev=(context or {}).get('evidence',[])
  print(json.dumps({'path':path,'text':x,'chapters':sorted({e['chapter_id'] for e in ev if isinstance(e,dict) and 'chapter_id' in e})},ensure_ascii=False))
walk(data)
