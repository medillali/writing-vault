import json,hashlib,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
P=Path(__file__).parent;B=P.parent;ROOT=P.parents[4]
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
if len(sys.argv)>1 and sys.argv[1]=='schema':
 x=read(B.parent/'zongheng-tianxia'/'book-synthesis-draft.json')
 print(json.dumps(dict(keys=list(x),sample_row=next(iter(x['dimensions'].values()))[0],validation=x['validation']),ensure_ascii=False,indent=2));raise SystemExit
if len(sys.argv)>1 and sys.argv[1]=='formal-diff':
 out=[]
 for v in range(1,9):
  p=B/f'vol{v:02d}'/'analysis.json';f=ROOT/'writing-vault'/'library'/'reports'/'tianxia-wushuang'/f'vol{v:02d}-analysis.json'
  if p.exists() and f.exists():
   a=read(p);b=read(f);diff=[]
   for d,rows in a['dimensions'].items():
    for i,row in enumerate(rows):
     if row!=b['dimensions'][d][i]:diff.append(dict(dimension=d,index=i,stage=row,formal=b['dimensions'][d][i]))
   out.append(dict(volume=v,dimensions_equal=not diff,differences=diff))
 print(json.dumps(out,ensure_ascii=False,indent=2));raise SystemExit
old=read(P/'basis-snapshot.json');results=[]
for v in range(1,9):
 p=B/f'vol{v:02d}';a=p/'analysis.json';s=p/'reader-state.json';f=ROOT/'writing-vault'/'library'/'reports'/'tianxia-wushuang'/f'vol{v:02d}-analysis.json'
 previous=next((x for x in old['materials'] if x['volume']==v),None)
 row=dict(volume=v,package_ready=all((p/x).is_file() for x in ['analysis.json','cards.json','graph.json','report.md','handoff.md','validation.json']),stage_analysis_sha256=sha(a) if a.is_file() else None,formal_analysis_exists=f.is_file(),formal_analysis_sha256=sha(f) if f.is_file() else None,old_analysis_unchanged=(sha(a)==previous['sha256']) if a.is_file() and previous else None)
 if s.is_file():st=read(s);row.update(complete_volume=st.get('complete_volume'),next=st.get('next_chapter_id'),reader=st.get('reader'))
 results.append(row)
print(json.dumps(results,ensure_ascii=False,indent=2))
