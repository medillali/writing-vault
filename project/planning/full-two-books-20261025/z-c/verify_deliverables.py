from save_batch import *
sys=__import__('sys');sys.stdout.reconfigure(encoding='utf-8')
bs=[json.loads(x.read_text(encoding='utf-8')) for x in sorted(P.glob('batch-*.json'))]
ords=[u['ordinal'] for b in bs for u in b['units']]
assert ords==list(range(321,371))
dims={'worldbuilding','characters','plot','style','narrative','dialogue','pacing','themes','continuity'}
for b in bs:
 assert set(b['dimensions'])==dims
 assert all(b['dimensions'][k] and all(x['evidence'] for x in b['dimensions'][k]) for k in dims)
 assert len(b['scenes'])>=3 and len(b['patterns'])>=2
 assert all(u['evidence'] and u['events'] for u in b['units'])
q={q['key'] for b in bs for q in b['questions']}
m=json.loads((P/'terminal-question-map.json').read_text(encoding='utf-8'))['items']
assert q=={x['key'] for x in m} and len(m)==len(q)
idx={u['unit_id']:u for u in BOOK['units']};count=0
def check(v):
 global count
 if isinstance(v,dict):
  if {'chapter_id','start_line','end_line'}<=v.keys():
   u=idx[v['chapter_id']];assert u['start_line']<=v['start_line']<=v['end_line']<=u['end_line'];count+=1
  for x in v.values():check(x)
 elif isinstance(v,list):
  for x in v:check(x)
for f in P.glob('*.json'):check(json.loads(f.read_text(encoding='utf-8')))
r={'source_key':'z','scope':'321..370','unit_count':len(ords),'gaps':[],'batch_count':len(bs),'dimensions_per_batch':9,'scenes':sum(len(b['scenes']) for b in bs),'patterns':sum(len(b['patterns']) for b in bs),'unique_questions':len(q),'question_map_complete':True,'evidence_boundary_errors':0,'checked_evidence_objects':count,'limitations':'自动验证证明结构与证据章界，实际全文阅读由逐段研究过程负责，不推导解释质量或用户风格认可。'}
(P/'validation-report.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(r,ensure_ascii=False))
