from pathlib import Path
import json,subprocess,sys,hashlib
sys.stdout.reconfigure(encoding='utf-8');R=Path(__file__).resolve().parents[2];V=R/'writing-vault';P=Path(__file__).parent
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def git(*args,raw=False):
 p=subprocess.run(['git','-c',f'safe.directory={V.as_posix()}','-c','http.sslBackend=openssl','-C',str(V),*args],capture_output=True,check=True)
 return p.stdout if raw else p.stdout.decode('utf-8').strip()
def api(path):return json.loads(subprocess.run(['gh','api',path],capture_output=True,text=True,encoding='utf-8',check=True).stdout)
assert load(P/'validation.json')['valid'];assert git('branch','--show-current')=='main';assert api('repos/medillali/writing-vault')['private']
assert git('remote','get-url','origin').lower().removesuffix('.git').endswith('medillali/writing-vault')
names={p.relative_to(V).as_posix() for p in (V/'书库').rglob('*') if p.is_file() and '__pycache__' not in p.parts}|{'START-HERE.md','AGENTS.md'}
map_prefix='library/reports/two-books-full-20261025/'
map_changes=set(git('diff','--name-only','-z','--',map_prefix).split('\0'))-{''}
assert all('/plot/' in n or '/validation/' in n for n in map_changes),map_changes
names|=map_changes;allowed=names|{'README.md'}
staged=set(git('diff','--cached','--name-only','-z').split('\0'))-{''};assert staged=={'README.md'},staged
integration=load(P/'integration.json');assert git('show',':README.md')==integration['prefix']+git('show','HEAD:README.md')
live=(V/'README.md').read_bytes();assert live[len(integration['prefix'].encode()):]==(P/'README-before-navigation.bin').read_bytes()
assert all(not n.startswith('private-sources/') and not n.endswith('.txt') for n in names)
spec=P/'paths.bin';spec.write_bytes(b'\0'.join(n.encode('utf-8') for n in sorted(names))+b'\0');git('add',f'--pathspec-from-file={spec}','--pathspec-file-nul')
staged=set(git('diff','--cached','--name-only','-z').split('\0'))-{''};assert staged<=allowed;git('diff','--cached','--check')
identity=git('log','-1','--format=%an%n%ae').splitlines();git('-c',f'user.name={identity[0]}','-c',f'user.email={identity[1]}','commit','-m','按书名作者类型建立书库目录，集中全书剧情地图入口')
commit=git('rev-parse','HEAD');print('提交',commit,'本批文件',len(staged),flush=True);git('push','origin','HEAD:main')
ref=api('repos/medillali/writing-vault/git/ref/heads/main')['object']['sha'];assert ref==commit
tree=api(f'repos/medillali/writing-vault/git/trees/{commit}?recursive=1');assert not tree['truncated'];remote={x['path']:x['sha'] for x in tree['tree'] if x['type']=='blob'}
local={row.split('\t',1)[1]:row.split('\t',1)[0].split()[2] for row in git('ls-tree','-rz',commit).split('\0') if row};assert remote==local
assert not (set(git('diff','--name-only','-z').split('\0'))-{''}) & names
assert not git('diff','--cached','--name-only')
receipt={'valid':True,'private_repository':'medillali/writing-vault','commit':commit,'remote_head':ref,'all_tree_blobs_match':True,'tree_blobs':len(local),'committed_paths':sorted(staged),'root_readme_only_navigation_added':True,'unrelated_research_staged':False,'book_count':8,'author_count':3,'genre_count':2,'full_book_map_count':3,'raw_sources_uploaded':False}
(P/'remote-verification.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in receipt.items() if k!='committed_paths'},ensure_ascii=False))
