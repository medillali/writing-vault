from common import B,P,ROOT,sha,dump
import json
paths=list((B/'vol04').glob('*'))+list((ROOT/'writing-vault/library/reports/zhanlong').glob('vol04-*'))
hits=[];scanned=[]
def walk(v,p=''):
 if isinstance(v,dict):
  for k,w in v.items():yield from walk(w,p+'/'+str(k))
 elif isinstance(v,list):
  for i,w in enumerate(v):yield from walk(w,p+'/'+str(i))
 elif isinstance(v,str):yield p,v
for f in paths:
 if not f.is_file() or f.suffix not in ['.json','.jsonl','.md']:continue
 scanned.append({'path':str(f.relative_to(ROOT)).replace('\\','/'),'sha256':sha(f)})
 if f.suffix=='.json':
  try:ls=list(walk(json.loads(f.read_text(encoding='utf-8'))))
  except Exception:continue
 elif f.suffix=='.jsonl':
  ls=[]
  for i,s in enumerate(f.read_text(encoding='utf-8').splitlines()):
   if s.strip():ls+=list(walk(json.loads(s),f'/jsonl/{i}'))
 else:ls=[(f'/line/{i}',s) for i,s in enumerate(f.read_text(encoding='utf-8').splitlines(),1)]
 for field,s in ls:
  if '乘风' in s and ('27' in s or '自冲' in s or '语差' in s):
   x={'path':str(f.relative_to(ROOT)).replace('\\','/'),'sha256':sha(f),'field':field,'value':s};hits.append(x);print(json.dumps(x,ensure_ascii=False))
dump(P/'wind-fields-scan.json',{'scanned_documents':scanned,'hits':hits,'read_only':True})
