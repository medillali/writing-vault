"""压缩重复定位和标签，仅供逐项主审派生稿；绝非正文阅读证明。"""
import json,sys
from pathlib import Path
book,vol,part=sys.argv[1],int(sys.argv[2]),sys.argv[3];d=Path(__file__).parent/book/f'vol{vol:02d}'
def rd(n):return json.loads((d/n).read_text(encoding='utf-8'))
def short(v):
 if isinstance(v,list):return [short(x) for x in v]
 if isinstance(v,dict):
  if {'source_id','revision','chapter_id'}.issubset(v):return v['chapter_id']
  return {k:short(x) for k,x in v.items() if k not in ['source_id','revision','review_status','user_notes','favorite','tags','scope','character_origin_keys']}
 if isinstance(v,str) and '/full-20261025/' in v:return v.split('/full-20261025/',1)[1]
 return v
if part=='dimensions':
 data=rd('analysis.json')['dimensions'];out={}
 for k,rows in data.items():
  out[k]=[]
  for r in rows:
   x={}
   for f,v in r.items():
    if f=='evidence':x[f]=list(dict.fromkeys(e['chapter_id'] for e in v))
    elif isinstance(v,dict) and 'text' in v:x[f]=v['text']
    else:x[f]=v
   out[k].append(x)
 data=out
elif part.startswith('cards:'):
 typ=part.split(':')[1];data=rd('cards.json');data=data.get('cards',[]) if isinstance(data,dict) else data;data=[c for c in data if c['asset_type']==typ]
 data=[dict(origin_key=c['origin_key'],title=c['title'],content=c['content'],evidence=list(dict.fromkeys(e['chapter_id'] for e in c['evidence']))) for c in data]
elif part.startswith('analysis:'):data=rd('analysis.json')[part.split(':')[1]]
elif part.startswith('graph:'):data=rd('graph.json')[part.split(':')[1]]
else:raise ValueError(part)
if len(sys.argv)>4:
 if isinstance(data,dict):data={k:data[k] for k in sys.argv[4:]}
 else:data=data[int(sys.argv[4]):int(sys.argv[5]) if len(sys.argv)>5 else None]
sys.stdout.reconfigure(encoding='utf-8');print(json.dumps(short(data),ensure_ascii=False,separators=(',',':')))
