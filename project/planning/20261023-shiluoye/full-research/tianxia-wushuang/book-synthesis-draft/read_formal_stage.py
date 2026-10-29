import json,sys,hashlib
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');P=Path(__file__).parent;ROOT=P.parents[4];v=int(sys.argv[1]);p=ROOT/'writing-vault/library/reports/tianxia-wushuang'/f'vol{v:02d}-analysis.json';a=json.loads(p.read_text(encoding='utf-8'))
print(json.dumps(dict(path=p.as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),reader=a.get('reader')),ensure_ascii=False))
for d in sys.argv[2:]:
 print('BEGIN FORMAL',v,d)
 for i,o in enumerate(a['dimensions'][d]):
  result={k:x for k,x in o.items() if k!='evidence'};result['index_zero_based']=i;result['evidence_chapters']=list(dict.fromkeys(e['chapter_id'] for e in o['evidence']))
  print(json.dumps(result,ensure_ascii=False))
 print('END FORMAL',v,d)
