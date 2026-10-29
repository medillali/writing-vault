from pathlib import Path
import json,sys
sys.stdout.reconfigure(encoding='utf-8')
P=Path(__file__).parent
s=json.loads((P.parent/'sources.json').read_text(encoding='utf-8'))['z']
bs=[json.loads(f.read_text(encoding='utf-8')) for f in sorted(P.glob('batch-*.json'))]
idx={u['unit_id']:u for u in s['units']}
errors=[]; evidence_count=0
def visit(x,path):
 global evidence_count
 if isinstance(x,dict):
  if {'chapter_id','start_line','end_line'}<=x.keys():
   evidence_count+=1
   u=idx.get(x['chapter_id'])
   if not u or not u['start_line']<=x['start_line']<=x['end_line']<=u['end_line']:
    errors.append({'path':path,'evidence':x,'source':u})
  for k,v in x.items():visit(v,path+'.'+k)
 elif isinstance(x,list):
  for i,v in enumerate(x):visit(v,path+f'[{i}]')
for b in bs:
 assert set(b['dimensions'])==set('worldbuilding characters plot style narrative dialogue pacing themes continuity'.split())
 assert all(b['dimensions'].values())
 visit(b,b['label'])
ordinals=[u['ordinal'] for b in bs for u in b['units']]
assert ordinals==list(range(1,233))
result={'actual_model_read_units':232,'range':[1,232],'batch_count':len(bs),'evidence_count':evidence_count,'evidence_errors':errors,'scope':'前半分工，非全书终点','checks':['JSON可解析','单元1..232连续且无重复','每阶段九维非空','每证据章节及行号界内']}
(P/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
