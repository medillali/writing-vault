"""提取主审所要求纠正的全部字段；只读，不代替语义审阅。"""
import json, sys
from pathlib import Path
d=Path(__file__).parent/'tianxia-wushuang/vol07'
cards=json.loads((d/'cards.json').read_text(encoding='utf-8'))
graph=json.loads((d/'graph.json').read_text(encoding='utf-8'))
def short(v):
 if isinstance(v,list): return [short(x) for x in v]
 if isinstance(v,dict):
  if {'source_id','revision','chapter_id'}.issubset(v):return v['chapter_id']
  return {k:short(x) for k,x in v.items() if k not in ['source_id','revision','tags','scope','user_notes','favorite','review_status','character_origin_keys','derived_from_origin_keys']}
 return v
names={'character':['moon','tiger','lv','luanyue','xiaomeng','li','lei','feiyin','he','xin','lubu','unnamedrider','yuelu'], 'scene':['duel','copper','challenge','supplies','soul','fall','thunder']}
if sys.argv[1]=='cards':
 data=[dict(origin_key=c['origin_key'],title=c['title'],content=c['content']) for c in cards if c['origin_key'].split('/')[-1] in names.get(c['asset_type'],[])]
else:
 data=[x for x in graph['nodes'] if x['id'] in ['v07-renew','v07-sulun','v07-challenge','v07-supplies','v07-soul','v07-fall','v07-thunder']]
if len(sys.argv)>2:data=data[int(sys.argv[2]):int(sys.argv[3])]
sys.stdout.reconfigure(encoding='utf-8');print(json.dumps(short(data),ensure_ascii=False,separators=(',',':')))
