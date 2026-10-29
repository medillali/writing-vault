"""按primary要求只补提案continuity03的两章事实/推断证据。"""
import json,hashlib,copy
from pathlib import Path
P=Path(__file__).parent;Q=P/'continuity-proposal'
f=Q/'before-after.json';before=f.read_bytes();x=json.loads(before);old=copy.deepcopy(x)
assert not (Q/'before-after.v1.json').exists()
(Q/'before-after.v1.json').write_bytes(before)
(Q/'before-after.v1.md').write_bytes((Q/'before-after.md').read_bytes())
row=x['changes'][2]['after'];base=row['evidence'][0]
for field,kind in [('evidence','fact'),('interpretation_evidence','inference')]:
 for raw,a,b in [(946,70737,70805),(956,71391,71462)]:
  assert not any(e['chapter_id']==f'ch-{raw:04d}' for e in row[field])
  row[field].append({'source_id':base['source_id'],'revision':base['revision'],'chapter_id':f'ch-{raw:04d}','start_line':a,'end_line':b,'claim_kind':kind})
for i,c in enumerate(x['changes']):
 if i!=2:assert c==old['changes'][i]
 else:
  o=copy.deepcopy(c)
  for field in ['evidence','interpretation_evidence']:o['after'][field]=o['after'][field][:-2]
  assert o==old['changes'][i]
f.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
m=Q/'before-after.md';m.write_text(m.read_text(encoding='utf-8')+'\n## primary要求的证据增量\n\n仅continuity03 after补证据：ch-0946 L70737—70805、ch-0956 L71391—71462；evidence两条fact，interpretation_evidence两条inference；SID/rev不变。其他文本/旧证/旧核心均未改。\n',encoding='utf-8')
print(json.dumps({'proposal_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'md_sha256':hashlib.sha256(m.read_bytes()).hexdigest(),'core_unchanged':hashlib.sha256((P/'analysis.json').read_bytes()).hexdigest()==x['analysis_before_sha256']},ensure_ascii=False))
