import pathlib,json,hashlib,sys
sys.stdout.reconfigure(encoding='utf-8');H=pathlib.Path(__file__).resolve().parent
for dn in ['history-v01-v04-review','local-v01-v04-review','notes-v01-v03-review']:
 p=H/dn
 if not p.exists():continue
 for f in sorted(p.rglob('*.json')):
  d=json.loads(f.read_text(encoding='utf-8'))
  rows=d if isinstance(d,list) else next((v for k,v in d.items() if k in ['adjudications','candidates','judgments'] and isinstance(v,list)),[])
  print(str(f.relative_to(H)),len(rows),hashlib.sha256(f.read_bytes()).hexdigest())
  if rows:print('FIRST_KEYS',list(rows[0]),'FIRST',json.dumps(rows[0],ensure_ascii=False)[:4500])
