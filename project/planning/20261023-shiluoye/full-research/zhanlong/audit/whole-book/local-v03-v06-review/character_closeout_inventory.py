"""只读清点自辖旧卡与新条目，不生成文学结论。"""
from pathlib import Path
import json,sys
sys.stdout.reconfigure(encoding='utf-8')
A=Path(__file__).resolve().parent.parent
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
d=load(A/'character-arc-entity-roster-proposal.json')
for i,e in enumerate(d['entities']):
 if e['proposed_owner']=='zongheng_vol05_full_main_and_reality':
  print(json.dumps(dict(roster_index=i,name=e['name'],audit_id=e.get('audit_id'),stage_cards=e['stage_cards']),ensure_ascii=False,separators=(',',':')))
print('SUPPLEMENT_KEYS',list(d.keys()))
for p in sorted(A.glob('character-arcs-part[0-9][0-9].json')):
 rows=load(p)['characters'];print(p.name,[(x['audit_id'],x['name'],x.get('entity_type')) for x in rows])
