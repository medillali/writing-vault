from pathlib import Path
import json,re,sys
sys.stdout.reconfigure(encoding='utf-8')
P=Path(__file__).parent;R=P.parent
S=json.loads((R/'sources.json').read_text(encoding='utf-8'))['z'];idx={u['unit_id']:u for u in S['units']}
inv=json.loads((P/'integration-inventory.json').read_text(encoding='utf-8'))
evcount=0;errors=[];checks=[]
def scan(x,p):
 global evcount
 if isinstance(x,dict):
  if {'chapter_id','start_line','end_line'}<=x.keys():
   evcount+=1;u=idx.get(x['chapter_id'])
   if not u or not u['start_line']<=x['start_line']<=x['end_line']<=u['end_line']:errors.append({'path':p,'evidence':x,'unit_bounds':u})
  for k,v in x.items():scan(v,p+'.'+k)
 elif isinstance(x,list):
  for n,v in enumerate(x):scan(v,p+f'[{n}]')
names=['book-synthesis.json','ending-audit.json','terminal-question-map.json','causal-relations.json','characters-final.json','threads.json','identity-links.json']
for name in names:
 f=P/name
 if not f.exists():
  draft=P/(f.stem+'.draft.json');provisional=P/(f.stem+'.provisional.json')
  f=draft if draft.exists() else provisional
 if not f.exists():continue
 d=json.loads(f.read_text(encoding='utf-8'));scan(d,f.name);checks.append(f.name)
 if name=='terminal-question-map.json':
  keys=[x['key'] for x in d['items']]
  if set(keys)!=set(inv['questions']):errors.append({'question_key_missing':sorted(set(inv['questions'])-set(keys)),'extra':sorted(set(keys)-set(inv['questions']))})
  if len(keys)!=len(set(keys)):errors.append({'question_duplicates':True})
  for q in d['items']:
   if not q.get('evidence'):errors.append({'empty_question_evidence':q['key']})
   if q['final_status'] not in {'resolved','partial','open','unknown','abandoned'}:errors.append({'invalid_status':q})
 if name=='causal-relations.json':
  scenes=set()
  for folder in ['z','z-b','z-c','z-c2','z-d']:
   for b in (R/folder).glob('batch-*.json'):
    scenes.update(x['key'] for x in json.loads(b.read_text(encoding='utf-8'))['scenes'])
  for row in d['items']:
   for k in ['from_scene_key','to_scene_key']:
    if row[k] not in scenes:errors.append({'missing_scene_key':row[k]})
  if not 12<=len(d['items'])<=20:errors.append({'causal_count':len(d['items'])})
 if name=='book-synthesis.json':
  expected={'worldbuilding','characters','plot','style','narrative','dialogue','pacing','themes','continuity'}
  if set(d['dimensions'])!=expected or not all(d['dimensions'].values()):errors.append({'dimension_coverage':False})
markdown_refs=0
for name in ['book-synthesis.md','ending-audit.md']:
 f=P/name
 if not f.exists():continue
 for chapter,a,b in re.findall(r'(ch-\d+):L(\d+)(?:[–-](\d+))?',f.read_text(encoding='utf-8')):
  markdown_refs+=1;u=idx.get(chapter);a=int(a);b=int(b or a)
  if not u or not u['start_line']<=a<=b<=u['end_line']:errors.append({'markdown_evidence':name,'chapter_id':chapter,'start_line':a,'end_line':b})
out={'checked_files':checks,'evidence_count':evcount,'markdown_reference_count':markdown_refs,'errors':errors,'interpretation_limit':'范围/键/结构校验不等于解释质量或用户偏好认可；实际阅读全文覆盖以各分工正文阅读和批次证据共同说明。'}
(P/'final-validation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('checked',len(checks),'evidence',evcount,'markdown_refs',markdown_refs,'errors',len(errors))
for e in errors:print(json.dumps(e,ensure_ascii=False))
