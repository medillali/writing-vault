"""仅复制本批独占路径，检查其他工作指纹，再限定暂存和远程读回。"""
from pathlib import Path
import sys,json,hashlib,subprocess,zipfile,shutil
sys.stdout.reconfigure(encoding='utf-8')
R=Path(__file__).resolve().parents[2];P=Path(__file__).parent;V=R/'.verify/two-books';L=R/'writing-vault';REL='library/reports/two-books-full-20261025';O=V/REL
sys.path.insert(0,str(R/'distill-novels/scripts'))
from fictionlib.vault import Vault
from fictionlib.storage import locked,digest
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def dump(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def git(root,*args,raw=False):
 p=subprocess.run(['git','-c',f'safe.directory={root.as_posix()}','-c','http.sslBackend=openssl','-C',str(root),*args],capture_output=True,check=True)
 return p.stdout if raw else p.stdout.decode('utf-8').strip()
class Cached(Vault):
 def _sources(self):
  if not hasattr(self,'cache'):self.cache=super()._sources()
  return self.cache
def preserved():
 before=load(P/'concurrent-preservation.json')['fingerprints'] if (P/'concurrent-preservation.json').exists() else load(P/'baseline-dirty.json');bad=[]
 for rel,sha in before.items():
  if not (L/rel).exists() or hashlib.sha256((L/rel).read_bytes()).hexdigest()!=sha:bad.append(rel)
 assert not bad,('其他任务已有文件指纹变化，先审计，不覆盖',bad)
 return len(before)
def selected():
 names={p.relative_to(V).as_posix() for p in O.rglob('*') if p.is_file()}
 names|={'AGENTS.md','START-HERE.md','CONTENT-GUIDE.md'}
 for book in ['zeidan','leveling']:
  for a in load(O/book/'asset-manifest.json'):
   folder={'character':'characters','scene':'scenes','pattern':'patterns'}[a['type']];aid=a['asset_id'];names|={f'library/{folder}/{aid}.json',f'library/views/{aid}.md'}
   names|={p.relative_to(V).as_posix() for p in (V/f'history/assets/{aid}').glob('*.json')}
 for a in load(O/'shared-asset-manifest.json'):
  aid=a['asset_id'];names|={f'library/patterns/{aid}.json',f'library/views/{aid}.md'}
  names|={p.relative_to(V).as_posix() for p in (V/f'history/assets/{aid}').glob('*.json')}
 for s in load(P/'sources.json').values():
  rel=f'library/sources/{s["source_id"]}/plot-graph.json';names.add(rel);gid=load(V/rel)['graph_id']
  names|={p.relative_to(V).as_posix() for p in (V/f'history/graphs/{gid}').glob('*.json')}
 for k in ['z','l']:names.add(f'exchanges/runs/run-full-two-books-20261025-{k}.json')
 return names
def commit_names(names,message):
 remote=git(L,'remote','get-url','origin').lower().removesuffix('.git')
 assert 'github.com' in remote and remote.endswith('medillali/writing-vault'),remote
 private=subprocess.run(['gh','api','repos/medillali/writing-vault','--jq','.private'],capture_output=True,text=True,check=True).stdout.strip();assert private=='true'
 existing=set(git(L,'diff','--cached','--name-only','-z').split('\0'))-{''}
 assert existing<=names,'有其他暂存内容，不能混入本次提交'
 assert git(L,'branch','--show-current')=='main'
 assert all(not n.startswith('private-sources/') and not n.lower().endswith('.txt') for n in names)
 spec=P/'full-pathspec.bin';spec.write_bytes(b'\0'.join(n.encode('utf-8') for n in sorted(names))+b'\0')
 git(L,'add',f'--pathspec-from-file={spec}','--pathspec-file-nul');staged=set(git(L,'diff','--cached','--name-only','-z').split('\0'))-{''};assert staged and staged<=names
 git(L,'diff','--cached','--check');author=git(L,'log','-1','--format=%an%n%ae').splitlines()
 git(L,'-c',f'user.name={author[0]}','-c',f'user.email={author[1]}','commit','-m',message)
 sha=git(L,'rev-parse','HEAD');print('提交',sha,'本批文件',len(staged),flush=True);git(L,'push','origin','HEAD:main');return sha
def remote_receipt(sha):
 def api(path):return json.loads(subprocess.run(['gh','api',path],capture_output=True,text=True,encoding='utf-8',check=True).stdout)
 repo=api('repos/medillali/writing-vault');assert repo['private']
 head=api('repos/medillali/writing-vault/git/ref/heads/main')['object']['sha']
 if head!=sha:assert api(f'repos/medillali/writing-vault/compare/{sha}...{head}')['status'] in ['ahead','identical']
 tree=api(f'repos/medillali/writing-vault/git/trees/{sha}?recursive=1');assert not tree['truncated'];remote={x['path']:x['sha'] for x in tree['tree'] if x['type']=='blob'}
 local={s.split('\t',1)[1]:s.split('\t',1)[0].split()[2] for s in git(L,'ls-tree','-rz',sha).split('\0') if s};assert local==remote
 return {'valid':True,'repository':'medillali/writing-vault','private':True,'branch':'main','content_commit':sha,'remote_head':head,'remote_contains_commit':True,'tree_blob_count':len(local),'all_tree_blobs_match':True,'raw_sources_uploaded':False}
mode=sys.argv[1]
if mode=='copy':
 preserved();names=selected();tracked=set(git(L,'ls-files','-z').split('\0'))-{''};changes=[]
 for rel in names:
  src=V/rel;dst=L/rel;assert src.is_file(),rel;assert dst.resolve().is_relative_to(L.resolve())
  if dst.exists() and dst.read_bytes()!=src.read_bytes():
   if rel in tracked:assert dst.read_bytes()==git(L,'show','HEAD:'+rel,raw=True),f'本次目标已有未提交修改：{rel}'
   else:raise AssertionError('本次新路径与既有未跟踪文件冲突：'+rel)
  if not dst.exists() or dst.read_bytes()!=src.read_bytes():changes.append(rel)
 vault=Cached(L)
 with locked(L):
  for rel in changes:
   dst=L/rel;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes((V/rel).read_bytes())
  result=vault._validate_locked();assert result['valid'];assert digest(vault.cache)==digest(Vault._sources(vault))
 preserved();dump(P/'owned-paths.json',sorted(names));result.update({'selected_files':len(names),'copied_files':len(changes),'preserved_modified_files':len(load(P/'baseline-dirty.json')),'unrelated_paths_written':0});dump(O/'validation/live-integration.json',result);dump(L/REL/'validation/live-integration.json',result);print(json.dumps(result,ensure_ascii=False))
elif mode=='publish':
 preserved();names=set(load(P/'owned-paths.json'))|{REL+'/validation/live-integration.json'};sha=commit_names(names,'完整蒸馏贼胆与练级专家，保存逐章九维、终态账与离线地图');dump(P/'content-commit.json',{'commit':sha});result=remote_receipt(sha);dump(P/'remote-content.json',result);print(json.dumps(result,ensure_ascii=False))
elif mode=='backup':
 sha=load(P/'content-commit.json')['commit'];base=R/'backups/full-two-books-20261025';base.mkdir(parents=True,exist_ok=True);zpath=base/f'writing-vault-{sha[:12]}.zip';git(L,'-c','core.autocrlf=false','-c','core.eol=lf','archive','--format=zip',f'--output={zpath}',sha)
 expected={s.split('\t',1)[1]:s.split('\t',1)[0].split()[2] for s in git(L,'ls-tree','-rz',sha).split('\0') if s};restore=R/'.verify'/f'full-two-books-restore-{sha[:12]}'
 assert restore.resolve().is_relative_to((R/'.verify').resolve())
 if restore.exists():assert not any(restore.iterdir()),'已有非空恢复目录，不能覆盖'
 restore.mkdir(exist_ok=True)
 with zipfile.ZipFile(zpath) as archive:
  assert set(archive.namelist())-{n for n in archive.namelist() if n.endswith('/')}==set(expected)
  for name,hash_ in expected.items():
   raw=archive.read(name);assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==hash_
   target=(restore/name).resolve();assert target.is_relative_to(restore.resolve());target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
 vault=Cached(restore)
 with locked(restore):result=vault._validate_locked();assert result['valid'];assert digest(vault.cache)==digest(Vault._sources(vault))
 # 两本原文与规范化文本分开备份；不进入资料库Git快照。
 rawzip=base/'two-originals-and-normalized-private.zip';metadata=load(P/'sources.json');entries={};sourceinfo={}
 for k,s in metadata.items():
  pattern='*贼胆*.txt' if k=='z' else '*网游之练级专家*.txt';candidates=list(Path('E:/chromedownload').glob(pattern));assert len(candidates)==1
  rawpath=candidates[0];normpath=Path(s['normalized_path']);norm=normpath.read_bytes();assert hashlib.sha256(norm).hexdigest()==s['revision']
  entries['originals/'+rawpath.name]=rawpath.read_bytes();entries['normalized/'+k+'.txt']=norm;sourceinfo[k]={'source_id':s['source_id'],'revision':s['revision'],'raw_sha256':hashlib.sha256(rawpath.read_bytes()).hexdigest()}
 with zipfile.ZipFile(rawzip,'w',compression=zipfile.ZIP_DEFLATED) as archive:
  for n,raw in entries.items():archive.writestr(n,raw)
  archive.writestr('source-identities.json',json.dumps(sourceinfo,ensure_ascii=False,indent=2).encode())
 with zipfile.ZipFile(rawzip) as archive:
  for name,raw in entries.items():assert archive.read(name)==raw
 receipt={'valid':True,'content_commit':sha,'snapshot':'已提交资料库快照；不含其他任务未提交改动','archive':zpath.name,'archive_sha256':hashlib.sha256(zpath.read_bytes()).hexdigest(),'git_blobs_verified':len(expected),'restored_library':result,'raw_sources_archive':rawzip.name,'raw_sources_sha256':hashlib.sha256(rawzip.read_bytes()).hexdigest(),'raw_files_verified':len(entries),'raw_sources_uploaded':False,'remote':load(P/'remote-content.json')}
 dump(base/'backup-receipt.json',receipt);dump(O/'validation/save-and-restore.json',receipt);dump(L/REL/'validation/save-and-restore.json',receipt);dump(P/'backup-result.json',receipt);print(json.dumps(receipt,ensure_ascii=False))
elif mode=='receipt':
 names={REL+'/validation/save-and-restore.json'};sha=commit_names(names,'记录双书全量成果的远程回读与备份恢复验收');result=remote_receipt(sha);dump(P/'remote-final.json',result);preserved();print(json.dumps(result,ensure_ascii=False))
else:raise SystemExit(mode)
