"""实际阅读必要派生接口的分组输出，保全文本，证据定位以章节ID简写。"""
import json,pathlib,sys
sys.stdout.reconfigure(encoding='utf-8');H=pathlib.Path(__file__).resolve().parent;R=H.parents[5]
v=int(sys.argv[1]);mode=sys.argv[2];lo=int(sys.argv[3]) if len(sys.argv)>3 else 0;hi=int(sys.argv[4]) if len(sys.argv)>4 else 9999
p=R/f'writing-vault/library/reports/tianxia-wushuang/vol{v:02d}-analysis.json';a=json.loads(p.read_text(encoding='utf-8'))
def clean(x):
 if isinstance(x,dict):
  return {k:([e.get('chapter_id') for e in val] if k=='evidence' else clean(val)) for k,val in x.items() if k not in ['source_id','revision','origin_key','asset_id']}
 if isinstance(x,list):return [clean(val) for val in x]
 return x
if mode=='states':
 field=next(k for k in ['major_character_states','character_states','characters'] if k in a)
 rows=a[field]
 if isinstance(rows,dict):rows=[dict(identity=k,state=val) for k,val in rows.items()]
 print('FIELD',field)
elif mode=='history':
 pool=json.loads((H/'historical-question-pool.json').read_text(encoding='utf-8'));rows=[x for x in pool['candidates'] if x['volume']==v]
elif mode in ['local','localcompact']:
 pool=json.loads((H/'local-question-pool.json').read_text(encoding='utf-8'));rows=[x for x in pool['candidates'] if x['volume']==v]
elif mode=='notes':
 B=H.parents[1];rows=[json.loads(l) for l in (B/f'vol{v:02d}/chapter-notes.jsonl').read_text(encoding='utf-8').splitlines() if l.strip()]
else:raise ValueError(mode)
last_group=None
for i,x in enumerate(rows):
 if lo<=i<hi:
  if mode=='localcompact':
   group=(x['original_field'],x['original_index'])
   if group!=last_group:
    print('ORIGINAL',json.dumps(clean(x['original_record']),ensure_ascii=False));last_group=group
   out=dict(candidate_id=x['candidate_id'],title=x['title'],chapters=[e['chapter_id'] for e in x['original_evidence']])
  elif mode in ['history','local']:
   record=clean(x['original_record'])
   if isinstance(record,dict):record={k:val for k,val in record.items() if k not in ['node_ids','edge_ids','resolution_evidence']}
   out=dict(candidate_id=x['candidate_id'],title=x['title'],original_stage_status=x.get('original_stage_status'),original_record=record,original_evidence=[e['chapter_id'] for e in x['original_evidence']])
  else:out=clean(x)
  print(i,json.dumps(out,ensure_ascii=False))
print('END_INTERFACE',v,mode,lo,min(hi,len(rows)),'TOTAL',len(rows))
