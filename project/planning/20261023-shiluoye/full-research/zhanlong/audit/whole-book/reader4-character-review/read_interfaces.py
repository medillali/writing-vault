import sys,json,hashlib
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parents[7]
A=Path(__file__).resolve().parent.parent
F=ROOT/'writing-vault/library/reports/zhanlong'
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def out(x): print(json.dumps(x,ensure_ascii=False,indent=2))
r=read(A/'character-arc-entity-roster-proposal.json')
ASSIGNED=([x for x in r['entities'] if x['proposed_owner']=='reader4_external_players']+
 [{'name':x,'proposed_owner':'reader4_external_players','stage_cards':[]} for x in r['supplementary_entities_for_source_check']['reader4_external_players']]+
 [x for x in r['entities'] if x['proposed_owner']=='reader3_npc'][-20:])
def compact(x): print(json.dumps(x,ensure_ascii=False,separators=(',',':')))
def keys(v):
 an=read(F/f'vol{v:02}-analysis.json')
 return {k:an[k] for k in ['stage_characters','major_character_states','character_states'] if k in an}
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x): p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if sys.argv[1]=='init':
 pins={str(p.relative_to(ROOT)).replace('\\','/'):sha(p) for v in range(1,7) for p in [F/f'vol{v:02}-{z}' for z in ['cards.json','analysis.json','handoff.md']]}
 pp=list((F/'audit').glob('priority*.json'))+[F/'vol02-primary-corrections.json',F/'vol03-note-corrections.json',A/'priority-corrections-delta.json']
 pins.update({str(p.relative_to(ROOT)).replace('\\','/'):sha(p) for p in pp if p.exists()})
 write(Path(__file__).parent/'input-receipt.json',{'status':'input-pinned-not-reading-complete','actual_reviewer':'/root/zongheng_vol04_full','formal_input_sha256':pins,'roster_sha256':sha(A/'character-arc-entity-roster-proposal.json'),'assignment_count':len(ASSIGNED),'assignment':ASSIGNED})
 compact({'assigned':[(i+1,x['name'],len(x['stage_cards'])) for i,x in enumerate(ASSIGNED)],'priority_files':[(str(p.relative_to(ROOT)),sha(p)) for p in pp if p.exists()]})
 for v in range(1,7):
  s=keys(v);compact({'volume':v,'states_structure':{k: str(type(t)) for k,t in s.items()},'state_keys':{k:list(t[0]) if isinstance(t,list) and t else list(t)[:3] for k,t in s.items()}})
elif sys.argv[1]=='entity':
 for i in range(int(sys.argv[2])-1,int(sys.argv[3])):
  e=ASSIGNED[i];print('ENTITY-BEGIN',i+1,e['name']);compact(e)
  for m in e['stage_cards']:
   v=m['volume'];cs=read(F/f'vol{v:02}-cards.json');c=cs[m['index']-1]
   assert c['origin_key']==m['origin_key'],(m,c.get('origin_key'))
   compact({'volume':v,'card':{k:z for k,z in c.items() if k in ['title','origin_key','asset_id','content']},'evidence_common':{'source_id':c['evidence'][0]['source_id'],'revision':c['evidence'][0]['revision']},'evidence':[{k:z for k,z in ref.items() if k not in ['source_id','revision']} for ref in c['evidence']]})
   for k,t in keys(v).items():
    arr=t if isinstance(t,list) else list(t.values())
    matches=[x for x in arr if isinstance(x,dict) and (x.get('origin_key')==m['origin_key'] or x.get('name')==m['title'] or x.get('name')==e['name'] or x.get('title')==m['title'])]
    for x in matches:
     se=x.get('evidence',[])
     compact({'volume':v,'state_field':k,'state':{a:b for a,b in x.items() if a!='evidence'},'state_evidence': 'identical-to-card-evidence' if se==c['evidence'] else se})
  print('ENTITY-END',i+1)
elif sys.argv[1]=='priority':
 p=ROOT/sys.argv[2];d=read(p);out(d)
elif sys.argv[1]=='prioritysemantic':
 p=ROOT/sys.argv[2];d=read(p);compact({k:v for k,v in d.items() if k not in ['affected_fields','evidence']});seen={}
 for x in d.get('affected_fields',[]):
  k=json.dumps([x.get('before'),x.get('after'),x.get('issue_id')],ensure_ascii=False)
  if k not in seen:seen[k]={'before':x.get('before'),'after':x.get('after'),'issue_id':x.get('issue_id'),'evidence':x.get('evidence'),'paths':[]}
  seen[k]['paths'].append([x.get('path'),x.get('field_path')])
 for x in seen.values():compact(x)
elif sys.argv[1]=='handoff':
 for v in range(int(sys.argv[2]),int(sys.argv[3])+1):
  print('HANDOFF-BEGIN',v);print((F/f'vol{v:02}-handoff.md').read_text(encoding='utf-8-sig'));print('HANDOFF-END',v)
elif sys.argv[1]=='findnotes':
 terms=sys.argv[2].strip('"').split('|')
 for v in range(1,7):
  rows=[json.loads(s) for s in (F/f'vol{v:02}-chapter-notes.jsonl').read_text(encoding='utf-8-sig').splitlines() if s.strip()]
  hit=[x for x in rows if any(t in json.dumps(x,ensure_ascii=False) for t in terms)]
  compact({'volume':v,'hits':[(x.get('chapter_id'),x.get('title'),[t for t in terms if t in json.dumps(x,ensure_ascii=False)]) for x in hit]})
elif sys.argv[1]=='notes':
 ids={f'ch-{int(x):04}' for x in sys.argv[2].split(',')}
 for v in range(1,7):
  for s in (F/f'vol{v:02}-chapter-notes.jsonl').read_text(encoding='utf-8-sig').splitlines():
   x=json.loads(s)
   if x.get('chapter_id') in ids:compact({'volume':v,'note':x})
elif sys.argv[1] in ['rawsearch','rawfirst']:
 source=read(A.parents[1]/'source.json');lines=Path(source['normalized_path']).read_text(encoding='utf-8-sig').splitlines();chapters=source['chapters']
 for term in sys.argv[2].strip('"').split('|'):
  hits=[i+1 for i,x in enumerate(lines) if term in x]; tail=hits[-int(sys.argv[3]):] if sys.argv[1]=='rawsearch' else hits[:int(sys.argv[3])]
  compact({'term':term,'occurrence_lines':len(hits),'last':[(next(c['chapter_id'] for c in chapters if c['start_line']<=i<=c['end_line']),i,lines[i-1]) for i in tail]})
elif sys.argv[1]=='rawrange':
 source=read(A.parents[1]/'source.json');lines=Path(source['normalized_path']).read_text(encoding='utf-8-sig').splitlines();a=int(sys.argv[2]);b=int(sys.argv[3]);print('LIMITED-EXCERPT-BEGIN',a,b);print('\n'.join(f'L{i}: {lines[i-1]}' for i in range(a,b+1)));print('LIMITED-EXCERPT-END')
elif sys.argv[1]=='roster':
 out({k:v for k,v in r.items() if k!='entities'})
 out([x for x in r['entities'] if x['proposed_owner']=='reader4_external_players'])
 out([x for x in r['entities'] if x['proposed_owner']=='reader3_npc'][-20:])
elif sys.argv[1]=='schema':
 s=read(A/'character-arcs-part01.json');out({k:v for k,v in s.items() if k!='characters'});out(s['characters'][0])
elif sys.argv[1]=='text':
 p=ROOT/sys.argv[2];lines=p.read_text(encoding='utf-8-sig').splitlines();start=int(sys.argv[3]);end=int(sys.argv[4]);print('\n'.join(f'{i+1}: {x}' for i,x in enumerate(lines) if start<=i+1<=end))
elif sys.argv[1]=='inspect':
 for v in range(1,7):
  c=read(F/f'vol{v:02}-cards.json');an=read(F/f'vol{v:02}-analysis.json');out({'volume':v,'cards_type':str(type(c)),'cards_keys':list(c) if isinstance(c,dict) else None,'analysis_keys':list(an),'state_first':an.get('major_character_states',[])[:1]})
