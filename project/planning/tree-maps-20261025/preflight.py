from pathlib import Path
import hashlib,json,re,subprocess,sys
sys.stdout.reconfigure(encoding='utf-8')
V=Path('.verify/tree-maps-20261025').resolve();O=V/'library/reports/two-books-full-20261025'
def git(*args):return subprocess.check_output(['git','-c',f'safe.directory={V.as_posix()}','-c','core.quotepath=false','-C',str(V),*args]).decode('utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads((V/'书库/generated-files.json').read_text(encoding='utf-8'))
assert all(sha(V/'书库'/p)==h for p,h in manifest['files'].items())
catalog=json.loads((V/'书库/catalog.json').read_text(encoding='utf-8'))
for b in catalog['books']:
 if b['title'] not in ('贼胆','网游之练级专家'):continue
 m=b['map'];d=json.loads((V/m['topology']).read_text(encoding='utf-8'))
 assert m['reader'].endswith('/whole-book/index.html') and m['events']==len(d['nodes'])
 assert m['relations']==sum(e['kind']!='sequence' for e in d['edges'])
changed=[p for p in git('diff','--name-only','-z').split('\0') if p]
assert all(p.startswith(('library/reports/two-books-full-20261025/','书库/')) for p in changed)
assert not any(p.endswith('/plot/graph.json') for p in changed),'原图不能因展示改变'
fail=[];count=0
paths=[O/'TREE-MAPS-ACCEPTANCE.md',O/'README.md',*[O/f/'README.md' for f in ('zeidan','leveling')],*[O/f/'plot/README.md' for f in ('zeidan','leveling')],*[V/'书库/按书名'/b['directory']/'剧情地图.md' for b in catalog['books'] if b['title'] in ('贼胆','网游之练级专家')]]
for p in paths:
 for target in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
  if target.startswith(('http:','https:','#')):continue
  count+=1;q=(p.parent/target.split('#')[0]).resolve()
  if not q.exists():fail.append((str(p),target))
assert not fail,fail
print(json.dumps({'generated_pages':len(manifest['files']),'checked_local_links':count,'changed_tracked_paths':len(changed),'source_graphs_unchanged':True,'catalog_view_counts_match':True},ensure_ascii=False))
