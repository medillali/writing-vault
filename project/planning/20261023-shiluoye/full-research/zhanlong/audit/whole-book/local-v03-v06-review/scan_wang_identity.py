from pathlib import Path
import json,hashlib,sys,re
sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent;A=H.parent;R=Path('C:/Users/Administrator/Documents/ChatGPT/Novel');B=A.parents[1];F=R/'writing-vault/library/reports/zhanlong';L=R/'writing-vault/library';sid='src-20f2d16e3d1b472fa4b230ab0e1770c9'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
paths=[]
for v in range(1,7):
 paths += [p for p in (B/f'vol{v:02d}').glob('*') if p.suffix in ['.json','.jsonl','.md','.py']]
 paths += [p for p in F.glob(f'vol{v:02d}-*') if p.suffix in ['.json','.jsonl','.md']]
for p in (L/'characters').glob('*.json'):
 if sid in p.read_text(encoding='utf-8-sig'):paths.append(p)
paths += [L/'views'/f'{p.stem}.md' for p in paths[:] if p.parent==L/'characters' and (L/'views'/f'{p.stem}.md').exists()]
paths += list(A.glob('character-arcs-part*.json'))+list(A.glob('character-arcs-part*.md'))
hits=[]
def wanted(x,context=''):
 return ('王翦' in x and any(t in x for t in ['王将','秦雨','若雨'])) or ('王翦' in context and any(t in x for t in ['王将','秦雨','若雨','表白','一分领袖']))
def walk(x,keys,p,context=''):
 if isinstance(x,dict):
  context=x.get('title',x.get('name',context))
  for k,y in x.items():walk(y,keys+[k],p,context)
 elif isinstance(x,list):
  for i,y in enumerate(x):walk(y,keys+[i],p,context)
 elif isinstance(x,str) and wanted(x,context):hits.append(dict(path=p.relative_to(R).as_posix(),sha256=sha(p),field_path=keys,context=context,value=x))
for p in dict.fromkeys(paths):
 if p.suffix=='.json':walk(json.loads(p.read_text(encoding='utf-8-sig')),[],p)
 elif p.suffix=='.jsonl':
  for i,line in enumerate(p.read_text(encoding='utf-8-sig').splitlines()):
   if line.strip():walk(json.loads(line),['jsonl',i],p)
 else:
  for i,line in enumerate(p.read_text(encoding='utf-8-sig').splitlines(),1):
   if wanted(line):hits.append(dict(path=p.relative_to(R).as_posix(),sha256=sha(p),field_path=['line',i],value=line))
poolhits=[]
for file in ['local-question-pool.json','historical-question-pool.json']:
 p=A/file;d=json.loads(p.read_text(encoding='utf-8'));rows=d.get('candidates',d.get('questions',[]))
 for c in rows:
  t=c.get('terminal_assessment') or {};s=t.get('rationale','')
  if wanted(s) or ('王翦' in c.get('title','') and any(k in s for k in ['秦雨','若雨','王将'])):poolhits.append(dict(pool=file,pool_sha256=sha(p),candidate_id=c.get('candidate_id'),title=c.get('title'),terminal_assessment=t))
out=dict(status='finite_scan_candidates_for_manual_adjudication_not_auto_corrections',current_material_hits=hits,pool_terminal_hits=poolhits,scope='stage六卷当前根/正式六卷当前根/SID人物canon+对应view/我方已交人物；已合池只看terminal不改原题。搜索命中不是错误断言，也不是原文覆盖。')
p=A/'wangjiang-wangjian-identity-scan.json';p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('CURRENT_FIELDS '+str(len(hits))+' POOL_TERMINALS '+str(len(poolhits)))
for i,h in enumerate(hits):print(json.dumps(dict(index=i,**h),ensure_ascii=False,separators=(',',':')))
print('POOL')
for h in poolhits:print(json.dumps(dict(pool=h['pool'],candidate_id=h['candidate_id'],title=h['title'],rationale=h['terminal_assessment'].get('rationale')),ensure_ascii=False,separators=(',',':')))
