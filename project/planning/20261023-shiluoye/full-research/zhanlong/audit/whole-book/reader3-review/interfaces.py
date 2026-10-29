"""只读冻结池/正式派生材料；本代理隔离目录保存收据和阅读进度。"""
import json,sys,hashlib
from pathlib import Path
P=Path(__file__).parent;A=P.parent;B=A.parent.parent;W=B.parent;ROOT=W.parents[2]
POOL=json.loads((A/'local-question-pool.json').read_text(encoding='utf-8'))
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
if sys.argv[1]=='receipt':
 files=[A/'WORKFLOW.md',A/'local-question-pool.json',A/'historical-question-pool.json',B/'source.json',ROOT/'writing-vault/library/reports/collection/reading-units.json']
 for i in range(1,7):
  for name in ['analysis.json','cards.json','graph.json','read-log.json','handoff.md']:
   p=ROOT/f'writing-vault/library/reports/zhanlong/vol{i:02d}-{name}'
   if p.exists():files.append(p)
 for p in [ROOT/'writing-vault/library/reports/zhanlong/vol02-primary-corrections.json',B/'primary-focused-rereads.json']:
  if p.exists():files.append(p)
 receipt={'status':'inputs-fixed-before-adjudication','reviewer':'/root/zongheng_vol03_full','scope':{'volume1':467,'volume4':373,'total':840},'local_candidates_total':len(POOL['candidates']),'pending_inputs':POOL['pending_inputs'],'inputs':[{'path':str(p.relative_to(ROOT)).replace('\\','/'),'sha256':sha(p),'bytes':p.stat().st_size} for p in files if p.exists()],'original_reading_attribution':'本代理亲读卷1前150片并完整派生读primary尾100四栏，卷4全部215片亲读；其余卷终点后证依据最终正式派生材料和必要定向原文，不冒个人全书重读。','progress':{'v01_next_onebased_offset':1,'v04_next_onebased_offset':1,'completed_candidate_ids':[]}}
  # 不覆盖既有收据。
 f=P/'input-receipt.json';assert not f.exists();f.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(receipt,ensure_ascii=False))
elif sys.argv[1]=='candidates':
 v,lo,hi=map(int,sys.argv[2:5]);cs=[c for c in POOL['candidates'] if c['volume']==v]
 seen=set()
 for ix,c in enumerate(cs[lo-1:hi],lo):
  print('\nCANDIDATE',ix,c['candidate_id'],'TITLE',c['title'])
  key=(c['original_field'],c['original_index'])
  if key not in seen:
   print('ORIGINAL',c['original_path'],c['original_field'],c['original_index'],json.dumps(c['original_record'],ensure_ascii=False));seen.add(key)
  print('EVIDENCE',json.dumps(c['original_evidence'],ensure_ascii=False))
elif sys.argv[1]=='note':
 lo,hi=map(int,sys.argv[2:4])
 for v in range(1,7):
  p=B/f'vol{v:02d}/chapter-notes.jsonl'
  if not p.exists():continue
  for s in p.read_text(encoding='utf-8').splitlines():
   n=json.loads(s);num=int(n['chapter_id'].split('-')[1])
   if lo<=num<=hi:print(json.dumps(n,ensure_ascii=False))
elif sys.argv[1]=='line':
 n=int(sys.argv[2]);src=load(B/'source.json');print(json.dumps([c for c in src['chapters'] if c['start_line']<=n<=c['end_line']],ensure_ascii=False))
elif sys.argv[1]=='record':
 v=int(sys.argv[2]);field=sys.argv[3];ix=int(sys.argv[4]);p=ROOT/f'writing-vault/library/reports/zhanlong/vol{v:02d}-analysis.json';print(json.dumps(load(p)[field][ix],ensure_ascii=False,indent=2))
elif sys.argv[1]=='find':
 terms=sys.argv[2:]
 for v in range(1,7):
  p=ROOT/f'writing-vault/library/reports/zhanlong/vol{v:02d}-analysis.json'
  x=load(p)
  def leaves(x,path=''):
   if isinstance(x,dict):
    for k,vv in x.items():leaves(vv,path+'/'+k)
   elif isinstance(x,list):
    for i,vv in enumerate(x):leaves(vv,path+'/'+str(i))
   elif isinstance(x,str) and any(z in x for z in terms):print(f'V{v}',path,x)
  leaves(x)
elif sys.argv[1]=='search':
 terms=sys.argv[2:]
 for v in range(1,7):
  for typ in ['analysis','cards']:
   p=ROOT/f'writing-vault/library/reports/zhanlong/vol{v:02d}-{typ}.json'
   if not p.exists():continue
   x=load(p)
   def walk(x,path=''):
    if isinstance(x,dict):
     if any(isinstance(t,str) and any(z in t for z in terms) for t in x.values()):print(str(p.relative_to(ROOT)),path,json.dumps(x,ensure_ascii=False))
     else:
      for k,vv in x.items():walk(vv,path+'/'+k)
    elif isinstance(x,list):
     for i,vv in enumerate(x):walk(vv,path+'/'+str(i))
   walk(x)
