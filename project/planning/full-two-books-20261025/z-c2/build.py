from pathlib import Path
import json
ROOT=Path(__file__).parent
BOOK=json.loads((ROOT.parent/'sources.json').read_text(encoding='utf-8'))['z']
def ev(n,a=None,b=None):
 u=BOOK['units'][n-1]
 return {'chapter_id':u['unit_id'],'start_line':a or u['start_line'],'end_line':b or u['end_line']}
def refs(rows):return [ev(*x) if isinstance(x,list) else x for x in rows]
def save(number,start,end,label,rows,dimensions,characters,scenes,patterns,threads,questions):
 units=[]
 for n,events,changes,qs,a,b in rows:
  u=BOOK['units'][n-1]
  units.append(dict(ordinal=n,unit_id=u['unit_id'],title=u['title'],events=events,state_changes=changes,open_questions=qs,evidence=[ev(n,a,b)]))
 dims={k:[dict(claim=x[0],kind=x[1],evidence=refs(x[2:])) for x in v] for k,v in dimensions.items()}
 for group in [characters,scenes,patterns,threads]:
  for c in group:c['evidence']=refs(c.get('evidence',[]))
 for c in questions:
  c['setup_evidence']=refs(c.get('setup_evidence',[]));c['resolution_evidence']=refs(c.get('resolution_evidence',[]))
 d=dict(source_key='z',source_id=BOOK['source_id'],unit_start=start,unit_end=end,label=label,units=units,dimensions=dims,characters=characters,scenes=scenes,patterns=patterns,threads=threads,questions=questions)
 assert [x['ordinal'] for x in units]==list(range(start,end+1))
 assert set(dims)==set('worldbuilding characters plot style narrative dialogue pacing themes continuity'.split())
 (ROOT/f'batch-{number:02d}.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
