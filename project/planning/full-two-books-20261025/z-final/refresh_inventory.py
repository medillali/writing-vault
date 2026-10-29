from pathlib import Path
import json,sys
sys.stdout.reconfigure(encoding='utf-8')
P=Path(__file__).parent;R=P.parent
s=json.loads((R/'sources.json').read_text(encoding='utf-8'))['z'];idx={u['unit_id']:u for u in s['units']}
units=[];qs={};ths={};chars={};batches=[];errors=[];evcount=0
def inspect(x,path):
 global evcount
 if isinstance(x,dict):
  if {'chapter_id','start_line','end_line'}<=x.keys():
   evcount+=1;u=idx.get(x['chapter_id'])
   if not u or not u['start_line']<=x['start_line']<=x['end_line']<=u['end_line']:errors.append({'path':path,'evidence':x,'source':u})
  for k,v in x.items():inspect(v,path+'.'+k)
 elif isinstance(x,list):
  for i,v in enumerate(x):inspect(v,path+f'[{i}]')
for d in ['z','z-b','z-c','z-c2','z-d']:
 for f in sorted((R/d).glob('batch-*.json')):
  b=json.loads(f.read_text(encoding='utf-8'));bp=str(f.relative_to(R));batches.append({'path':bp,'start':b['unit_start'],'end':b['unit_end']});units.extend(u['ordinal'] for u in b['units']);inspect(b,bp)
  for q in b['questions']:qs.setdefault(q['key'],[]).append({'batch':bp,'through':b['unit_end'],**q})
  for t in b['threads']:ths.setdefault(t['key'],[]).append({'batch':bp,'through':b['unit_end'],**t})
  for c in b['characters']:
   k='zhao-lanxin' if c['name']=='赵岚馨' else c['key']
   chars.setdefault(k,[]).append({'batch':bp,'through':b['unit_end'],**c,'key':k})
coverage={'source_key':'z','batches':batches,'unit_count':len(units),'unique_unit_count':len(set(units)),'missing_units':[n for n in range(1,464) if n not in units],'duplicate_units':sorted({n for n in units if units.count(n)>1}),'evidence_count':evcount,'evidence_errors':errors,'claim':'原文实际阅读由各分工承担；本目录二次综合不新增原文阅读计数。'}
for name,data in [('integration-inventory.json',{'questions':qs,'threads':ths,'characters':chars}),('integration-validation.json',coverage)]:
 (P/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('units',len(units),'missing',len(coverage['missing_units']),'questions',len(qs),'threads',len(ths),'evidence_errors',len(errors))
for e in errors:print(json.dumps(e,ensure_ascii=False))
