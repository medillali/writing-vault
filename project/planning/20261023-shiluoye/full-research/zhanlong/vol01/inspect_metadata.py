import json,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
P=Path(__file__).parent;B=P.parent
W=next(p for p in P.parents if (p/'writing-vault').exists())
source=json.loads((B/'source.json').read_text(encoding='utf-8'))
print('SOURCE_KEYS',list(source))
print('SOURCE_META',json.dumps({k:v for k,v in source.items() if k not in ['chapters','volumes']},ensure_ascii=False))
print('RAW_COUNT',len(source['chapters']))
for v in source['volumes']:
 if v.get('volume') in [1,4] or v.get('number') in [1,4]:
  print('VOLUME',json.dumps({k:x for k,x in v.items() if k!='units'},ensure_ascii=False))
  units=v['units'];print('UNIT_COUNT',len(units))
  print('FIRST_UNITS',json.dumps(units[:3],ensure_ascii=False))
  print('LAST_UNITS',json.dumps(units[-2:],ensure_ascii=False))
  print('SPECIAL_UNITS',json.dumps([u for u in units if len(u.get('segments',[]))!=1 or u.get('kind') not in [None,'body']],ensure_ascii=False))
ru=json.loads((W/'writing-vault/library/reports/collection/reading-units.json').read_text(encoding='utf-8'))
print('READING_UNITS_KEYS',list(ru))
entry=ru[source['source_id']]
print('READING_ENTRY_META',json.dumps({k:v for k,v in entry.items() if k!='units'},ensure_ascii=False))
print('READING_SPECIAL_ASSIGNED',json.dumps([u for u in entry.get('units',[]) if (2<=int(u['unit_id'][3:])<=251 or 754<=int(u['unit_id'][3:])<=968) and (len(u.get('segment_ids',[]))!=1 or u.get('kind')!='body')],ensure_ascii=False))
