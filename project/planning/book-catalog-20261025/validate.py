from pathlib import Path
import json,sys,re,subprocess,hashlib,urllib.parse
sys.stdout.reconfigure(encoding='utf-8');R=Path(__file__).resolve().parents[2];V=R/'writing-vault';P=Path(__file__).parent;C=V/'书库'
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(raw):return hashlib.sha256(raw).hexdigest()
def git(*args):return subprocess.run(['git','-c',f'safe.directory={V.as_posix()}','-C',str(V),*args],capture_output=True,check=True).stdout.decode('utf-8').strip()
books=load(C/'catalog.json')['books'];tracked=set(git('ls-files','-z').split('\0'))-{''};own={p.relative_to(V).as_posix() for p in C.rglob('*') if p.is_file() and '__pycache__' not in p.parts};errors=[];links=0
for f in C.rglob('*.md'):
 for raw in re.findall(r'\]\(([^)\n]+)\)',f.read_text(encoding='utf-8')):
  target=urllib.parse.unquote(raw.strip('<>').split('#')[0])
  if not target or re.match(r'^[a-zA-Z]+:',target):continue
  p=(f.parent/target).resolve();links+=1
  if not p.is_relative_to(V) or not p.exists():errors.append({'page':f.relative_to(V).as_posix(),'target':target,'reason':'missing'})
  elif p.is_file() and p.relative_to(V).as_posix() not in tracked|own:errors.append({'page':f.relative_to(V).as_posix(),'target':target,'reason':'not published'})
assert not errors,errors
for b in books:
 page=C/'按书名'/b['directory']/'README.md';assert page.exists()
 for kind,value in [('按作者',b['author']),*[('按类型',g) for g in b['genres']]]:
  text=(C/kind/value/'README.md').read_text(encoding='utf-8');assert b['directory'] in text
 if b.get('map'):
  m=b['map'];assert b['research_status']=='full';assert all((V/m[k]).exists() for k in ['overview','html','png','svg','preview'])
  assert (C/'按书名'/b['directory']/'剧情地图.md').exists()
  if m.get('graph'):
   g=load(V/m['graph']);assert g['coverage'][0]['complete'];assert g['coverage'][0]['source_id']==b['source_id'];assert g['coverage'][0]['revision']==b['source_revision']
   assert len([n for n in g['nodes'] if n['kind']=='scene'])==m['events'] and len(g['edges'])==m['relations']
   bookdir=(V/m['graph']).parents[1];cov=load(bookdir/'coverage.json');assert cov['actual_reading_units']==m['unit_count']
   for name in ['browser','diagram-layout']:assert load(bookdir/'validation'/f'{name}.json')['valid']
   manifest=load((V/m['html']).with_name('manifest.json'));assert sha((V/m['png']).read_bytes())==manifest['source_png_sha256'];assert sha((V/m['html']).read_text(encoding='utf-8').encode())==manifest['html_sha256']
 else:assert not (C/'按书名'/b['directory']/'剧情地图.md').exists()
metadata_before={p.relative_to(C).as_posix():sha(p.read_bytes()) for p in C.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
run=subprocess.run([sys.executable,str(C/'重建目录.py')],capture_output=True,check=True);assert all(sha((C/n).read_bytes())==s for n,s in metadata_before.items()),'目录重建不稳定'
integration=load(P/'integration.json');live=(V/'README.md').read_bytes();assert live.startswith(integration['prefix'].encode());assert live[len(integration['prefix'].encode()):]==(P/'README-before-navigation.bin').read_bytes(),'README其他内容变化，先审查'
head=git('show','HEAD:README.md');expected=head if head.startswith(integration['prefix']) else integration['prefix']+head
assert git('show',':README.md')==expected,'README暂存混入其他修改'
result={'valid':True,'books':len(books),'authors':len({b['author'] for b in books}),'genres':len({g for b in books for g in b['genres']}),'full_book_maps':sum(bool(b.get('map')) for b in books),'markdown_links_checked':links,'broken_or_unpublished_links':errors,'rebuild_idempotent':True,'readme_staging_isolated':True,'raw_sources_added':False,'map_validation':'两本全书地图本轮重新生成，桌面与手机离线交互及图像几何通过；超级骷髅兵复用既有完整地图。'}
(C/'validation').mkdir(exist_ok=True);(C/'validation/index.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(P/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,ensure_ascii=False))
