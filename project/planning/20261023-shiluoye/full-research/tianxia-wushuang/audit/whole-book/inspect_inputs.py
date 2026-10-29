"""只读核对审计输入及前书四包schema；不读取新小说正文。"""
import json,pathlib,hashlib,sys
sys.stdout.reconfigure(encoding='utf-8');H=pathlib.Path(__file__).resolve().parent;B=H.parents[1];W=H.parents[2];R=H.parents[5]
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
if len(sys.argv)>1 and sys.argv[1]=='schema':
 old=W/'zongheng-tianxia/vol08'
 for file,key in [('character-arc-audit-draft.json','characters'),('end-state-audit-draft.json','findings'),('historical-question-pool.json','candidates'),('local-question-pool.json','candidates')]:
  d=read(old/file);print(file,list(d));print(json.dumps(d[key][0],ensure_ascii=False))
else:
 for v in range(1,9):
  formal=R/f'writing-vault/library/reports/tianxia-wushuang/vol{v:02d}-analysis.json';a=formal if formal.exists() else B/f'vol{v:02d}/analysis.json'
  graph=formal.with_name(f'vol{v:02d}-graph.json') if formal.exists() else B/f'vol{v:02d}/graph.json'
  review=B/f'review-vol{v:02d}.json';state=B/f'vol{v:02d}/reader-state.json'
  if not a.exists():print('V',v,'PENDING');continue
  d=read(a);g=read(graph)
  print(json.dumps(dict(volume=v,status='formal-library' if formal.exists() else 'reviewed-stage' if review.exists() else 'under-review-stage',analysis=a.relative_to(R).as_posix(),keys=list(d),dimensions={k:len(val if isinstance(val,list) else val.get('observations',[])) for k,val in d['dimensions'].items()},threads=len(g['threads']),questions=len(d.get('open_questions',[])),reader=read(state).get('reader') if state.exists() else None),ensure_ascii=False))
  for key in ['open_questions','unresolved_questions','unresolved_and_anomalies','unresolved','local_historical_questions']:
   if key in d:
    x=d[key];print(key,'type',type(x).__name__,'count',len(x),'example',json.dumps(x[0] if isinstance(x,list) and x else x,ensure_ascii=False)[:1800])
