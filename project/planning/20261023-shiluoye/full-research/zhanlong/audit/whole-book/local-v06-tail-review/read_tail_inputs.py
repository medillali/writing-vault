import pathlib,json,sys
sys.stdout.reconfigure(encoding='utf-8');Q=pathlib.Path(__file__).resolve().parent;A=Q.parent;B=A.parents[1];ROOT=B.parents[3];F=ROOT/'writing-vault/library/reports/zhanlong'
mode=sys.argv[1]
if mode in ('candidates','candidate-text'):
 off,count=map(int,sys.argv[2:]);pool=json.loads((A/'local-question-pool.json').read_text(encoding='utf-8'));rows=[x for x in pool['candidates'] if x['volume']==6][200:399]
 for i,c in enumerate(rows[off:off+count],off):
  obj=dict(assigned_offset=i,original_volume_offset=i+200,**c) if mode=='candidates' else dict(assigned_offset=i,candidate_id=c['candidate_id'],title=c['title'],original_record=c['original_record'],original_evidence=c['original_evidence'])
  print(json.dumps(obj,ensure_ascii=False))
 print('END_ASSIGNED_CANDIDATES',off,min(off+count,len(rows)),len(rows))
elif mode=='search':
 terms=sys.argv[2:]
 for v in range(1,7):
  f=F/f'vol{v:02d}-chapter-notes.jsonl'
  for line in f.read_text(encoding='utf-8').splitlines():
   x=json.loads(line)
   hits=[t for t in terms if t in line]
   if hits:print(x['chapter_id'],x['title'],'命中',','.join(hits))
 print('END_SEARCH_ONLY_NOT_FULL_READING')
elif mode=='notes':
 ids={int(n) for n in sys.argv[2:]}
 for v in range(1,7):
  f=F/f'vol{v:02d}-chapter-notes.jsonl'
  for line in f.read_text(encoding='utf-8').splitlines():
   if line.strip():
    x=json.loads(line)
    if int(x['chapter_id'].split('-')[1]) in ids:print('BEGIN_DERIVED',f.name,x['chapter_id']);print(json.dumps(x,ensure_ascii=False));print('END_DERIVED',x['chapter_id'])
