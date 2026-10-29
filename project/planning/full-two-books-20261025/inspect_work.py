from pathlib import Path
import json,subprocess,sys
R=Path(__file__).resolve().parents[2]; P=Path(__file__).parent; V=R/'.verify/two-books'
mode=sys.argv[1]
if mode=='files':
 for folder in ['distill-novels/scripts/fictionlib','.planning/two-books-20261023']:
  print(folder)
  for f in sorted((R/folder).glob('*')):
   if f.is_file():print(f.name)
elif mode=='defs':
 for f in (R/'distill-novels/scripts/fictionlib').glob('*.py'):
  for i,l in enumerate(f.read_text(encoding='utf-8').splitlines(),1):
   if any(v in l for v in ['def put_asset','def save_graph','def _validate_locked','def _sources','def validate','def add_','def render','def graph_']):print(f.name,i,l)
elif mode=='git':
 for folder in ['.verify/two-books','writing-vault']:
  root=R/folder; print(folder)
  x=subprocess.run(['git','-c',f'safe.directory={root.as_posix()}','-C',str(root),'status','--short','--branch'],capture_output=True,text=True,encoding='utf-8',check=True)
  print(x.stdout[:6000])
elif mode=='progress':
 for d in ['z','z-b','l-a','l-b','z-c','z-d']:
  batches=[]
  for f in sorted((P/d).glob('batch-*.json')):
   b=json.loads(f.read_text(encoding='utf-8'));batches.append([b['unit_start'],b['unit_end']])
  print(d,batches)
