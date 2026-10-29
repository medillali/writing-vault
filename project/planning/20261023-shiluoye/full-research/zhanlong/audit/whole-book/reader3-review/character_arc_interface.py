"""按已授权名单输出人物卡全部语义与原证据；检索只定位，不代人物终评。"""
from synthesis_common import *
import sys, re
A=P.parent
ROSTER_PATH=A/'character-arc-entity-roster-proposal.json'
ROSTER=json.loads(ROSTER_PATH.read_text(encoding='utf-8'))
NPC=[e for e in ROSTER['entities'] if e['proposed_owner']=='reader3_npc']
assert len(NPC)==60 and NPC[39]['name']=='云飘飘' and NPC[40]['name']=='火狮榛'
SCOPE=NPC[:40]+[{'name':n,'stage_cards':[],'source_check_required':True} for n in ROSTER['supplementary_entities_for_source_check']['reader3_npc']]
assert len(SCOPE)==64
def cards(v):return json.loads((F/f'vol{v:02d}-cards.json').read_text(encoding='utf-8'))
def all_states(v):
 a=json.loads((F/f'vol{v:02d}-analysis.json').read_text(encoding='utf-8'))
 return a.get('major_character_states',a.get('stage_characters',a.get('character_states',[])))
def locator_compact(x):
 if isinstance(x,list):
  if x and isinstance(x[0],dict) and 'chapter_id' in x[0]:return [f"{e.get('chapter_id')} L{e.get('start_line')}-{e.get('end_line')} {e.get('claim_kind','')}" for e in x]
  return [locator_compact(y) for y in x]
 if isinstance(x,dict):return {k:locator_compact(y) for k,y in x.items()}
 return x
def getcard(stage):
 cs=cards(stage['volume']);c=cs[stage['index']-1];assert c['title']==stage['title'],(stage,c['title'])
 return c
if sys.argv[1]=='scope':
 for i,e in enumerate(SCOPE,1):print(i,json.dumps(e,ensure_ascii=False))
elif sys.argv[1]=='sample':
 print('CARD',json.dumps(getcard(SCOPE[0]['stage_cards'][0]),ensure_ascii=False,indent=2))
 for v in [1,4,6]:
  st=all_states(v);print('STATE',v,type(st).__name__,json.dumps(st[:2] if isinstance(st,list) else dict(list(st.items())[:2]),ensure_ascii=False,indent=2))
elif sys.argv[1]=='read':
 lo,hi=map(int,sys.argv[2:4]);assert hi-lo<8
 for i in range(lo,hi+1):
  e=SCOPE[i-1];print('BEGIN ENTITY',i,e['name'])
  for st in e['stage_cards']:
   c=getcard(st);print('FULL CONTENT AND ALL EVIDENCE',st['volume'],json.dumps(locator_compact({k:c.get(k) for k in ['asset_id','origin_key','title','content','evidence','user_notes']}),ensure_ascii=False))
  print('END ENTITY',i,e['name'])
elif sys.argv[1]=='state-search':
 for v in range(1,7):
  st=all_states(v);items=list(st.values()) if isinstance(st,dict) else st
  for i,x in enumerate(items):
   if any(n in json.dumps(x,ensure_ascii=False) for n in sys.argv[2:]):print('STATE',v,i+1,json.dumps(locator_compact(x),ensure_ascii=False))
elif sys.argv[1]=='handoff-search':
 for v in range(1,7):
  p=F/f'vol{v:02d}-handoff.md'
  for i,line in enumerate(p.read_text(encoding='utf-8').splitlines(),1):
   if any(n in line for n in sys.argv[2:]):print('HANDOFF',v,i,line)
elif sys.argv[1]=='keys':
 for v in range(1,7):
  a=json.loads((F/f'vol{v:02d}-analysis.json').read_text(encoding='utf-8'));print(v,list(a))
elif sys.argv[1]=='existing-schema':
 a=json.loads((A/'character-arcs-part01.json').read_text(encoding='utf-8'));print(list(a));print(json.dumps({k:v for k,v in a.items() if k not in ['characters','formal_input_sha256']},ensure_ascii=False));print(json.dumps(a.get('characters',[None])[0],ensure_ascii=False))
elif sys.argv[1]=='note-hits':
 for v in range(1,7):
  rows=[json.loads(x) for x in (F/f'vol{v:02d}-chapter-notes.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
  hits=[int(x['chapter_id'][3:]) for x in rows if any(n in json.dumps(x,ensure_ascii=False) for n in sys.argv[2:])]
  print(v,hits)
elif sys.argv[1]=='notes':
 wanted=set(map(int,sys.argv[2:]))
 for v in range(1,7):
  for line in (F/f'vol{v:02d}-chapter-notes.jsonl').read_text(encoding='utf-8').splitlines():
   x=json.loads(line)
   if int(x['chapter_id'][3:]) in wanted:print('FULL NOTE',v,json.dumps(x,ensure_ascii=False))
elif sys.argv[1]=='state-for':
 lo,hi=map(int,sys.argv[2:4]);origins={st['origin_key'] for e in SCOPE[lo-1:hi] for st in e['stage_cards']}
 for v in range(1,7):
  st=all_states(v);items=list(st.values()) if isinstance(st,dict) else st
  for i,x in enumerate(items):
   if isinstance(x,dict) and x.get('origin_key') in origins:print('FULL MATCHED STATE',v,i+1,json.dumps(locator_compact(x),ensure_ascii=False))
