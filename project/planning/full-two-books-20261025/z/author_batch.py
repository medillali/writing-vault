from pathlib import Path
import json,sys
P=Path(__file__).parent; books=json.loads((P.parent/'sources.json').read_text(encoding='utf-8'))['z']
q=Path(sys.argv[1]); a=json.loads(q.read_text(encoding='utf-8'))
def ev(ordinal,lo,hi):return {'chapter_id':books['units'][ordinal-1]['unit_id'],'start_line':lo,'end_line':hi}
out={'source_key':'z','source_id':books['source_id'],'source_revision':books['revision'],'unit_start':a['units'][0][0],'unit_end':a['units'][-1][0],'label':a['label'],'units':[],'dimensions':{},'characters':[],'scenes':[],'patterns':[],'threads':[],'questions':[]}
for n,event,change,lo,hi in a['units']:
 m=books['units'][n-1];out['units'].append({'ordinal':n,'unit_id':m['unit_id'],'title':m['title'],'events':[event],'state_changes':[change] if change else [],'open_questions':[],'evidence':[ev(n,lo,hi)]})
for dim,claims in a['dimensions'].items():out['dimensions'][dim]=[{'claim':c,'kind':k,'evidence':[ev(n,lo,hi)]} for c,k,n,lo,hi in claims]
for kind in ['characters','scenes','patterns','threads','questions']:
 for row in a.get(kind,[]):
  for field in ['evidence','setup_evidence','resolution_evidence']:
   if field in row:row[field]=[ev(*e) for e in row[field]]
  out[kind].append(row)
target=P/a['file'];target.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(target.name, len(out['units']), 'units')
