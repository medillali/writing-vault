from pathlib import Path
import json
P=Path(__file__).parent
p=P/'z_b04.py';s=p.read_text(encoding='utf-8');assert "'aliases':['龙岩之哥尚待后续明示对应']" in s;p.write_text(s.replace("'aliases':['龙岩之哥尚待后续明示对应']","'aliases':[]"),encoding='utf-8')
p=P/'z-b/batch-04.json';d=json.loads(p.read_text(encoding='utf-8'))
for c in d['characters']:
 if c['key']=='snail':assert c['aliases']==['龙岩之哥尚待后续明示对应'];c['aliases']=[]
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
