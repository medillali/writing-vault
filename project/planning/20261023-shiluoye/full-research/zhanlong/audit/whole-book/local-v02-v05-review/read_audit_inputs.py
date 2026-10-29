"""候选与派生证据阅读入口；只输出原记录，不产生终点评语。"""
import pathlib,json,sys
sys.stdout.reconfigure(encoding='utf-8');P=pathlib.Path(__file__).resolve().parent;A=P.parent;B=A.parents[1];ROOT=B.parents[3];F=ROOT/'writing-vault/library/reports/zhanlong'
mode=sys.argv[1]
if mode=='candidates':
 vol,offset,count=map(int,sys.argv[2:]);pool=json.loads((A/'local-question-pool.json').read_text(encoding='utf-8'));rows=[x for x in pool['candidates'] if x['volume']==vol]
 for i,c in enumerate(rows[offset:offset+count],offset):print(json.dumps(dict(offset=i,candidate_id=c['candidate_id'],volume=vol,title=c['title'],original_field=c['original_field'],original_index=c['original_index'],atomic_index=c['atomic_index'],original_record=c['original_record']),ensure_ascii=False))
 print('END_CANDIDATES',vol,offset,min(offset+count,len(rows)),len(rows))
elif mode=='notes':
 ids={int(n) for n in sys.argv[2:]}
 for vol in range(1,7):
  file=F/f'vol{vol:02d}-chapter-notes.jsonl'
  for line in file.read_text(encoding='utf-8').splitlines():
   if not line.strip():continue
   n=json.loads(line)
   if int(n['chapter_id'].split('-')[1]) in ids:print('BEGIN_DERIVED',file.name,n['chapter_id']);print(json.dumps(n,ensure_ascii=False));print('END_DERIVED',n['chapter_id'])
elif mode=='locate':
 terms=sys.argv[2:]
 for vol in range(1,7):
  for line in (F/f'vol{vol:02d}-chapter-notes.jsonl').read_text(encoding='utf-8').splitlines():
   if line.strip() and any(t in line for t in terms):
    n=json.loads(line);print(n['chapter_id'],n.get('title',''),','.join(t for t in terms if t in line))
else:raise ValueError(mode)
