from pathlib import Path
import subprocess,json,hashlib,sys
R=Path(__file__).resolve().parents[2];V=R/'.verify/two-books';OUT=V/'library/reports/two-books-20261023'
def git(*args):
    p=subprocess.run(['git','-c',f'safe.directory={V.as_posix()}','-c','http.sslBackend=openssl','-C',str(V),*args],text=True,encoding='utf-8',capture_output=True)
    if p.returncode:raise RuntimeError(p.stderr+p.stdout)
    return p.stdout.strip()
mode=sys.argv[1]
if mode=='publish':
    assert not git('diff','--name-only')
    names=sorted(set(git('ls-files','--others','--exclude-standard').splitlines()+git('diff','--cached','--name-only').splitlines()))
    allowed={'AGENTS.md','START-HERE.md','CONTENT-GUIDE.md','RESEARCH-QUEUE.md'}
    for f in names:
        assert f in allowed or f.startswith(('templates/','exchanges/runs/run-two-books-','exchanges/runs/run-zeidan-legacy-','exchanges/outbox/','library/reports/two-books-20261023/','library/characters/chr-twobooks-','library/scenes/scn-twobooks-','library/patterns/pat-twobooks-','library/sources/src-abe49798d224463fb60416f1286fd23f','library/sources/src-dd0554907f2942feb3162689dbad167f')),f
        assert not f.endswith('.txt') and not f.startswith('private-sources/')
    assert git('check-ignore','private-sources/normalized/manifest.json')
    spec=R/'.planning/two-books-20261023/git-pathspec.bin'
    spec.write_bytes(b'\0'.join(f.encode('utf-8') for f in names)+b'\0')
    git('add',f'--pathspec-from-file={spec}','--pathspec-file-nul')
    print('STAGED',len(names),'files',flush=True)
    git('diff','--cached','--check')
    author=git('log','-1','--format=%an%n%ae').splitlines()
    assert len(author)==2 and '@' in author[1]
    print(git('-c',f'user.name={author[0]}','-c',f'user.email={author[1]}','commit','-m','保存双书试蒸馏、贼胆旧研究与长期内容管理入口').splitlines()[0],flush=True)
    print(git('push','origin','HEAD:main'),flush=True)
elif mode=='receipt':
    sha=git('rev-parse','HEAD')
    def api(path):
        p=subprocess.run(['gh','api',path],text=True,encoding='utf-8',capture_output=True,check=True)
        return json.loads(p.stdout)
    repo=api('repos/medillali/writing-vault');assert repo['private'] is True
    remote=api('repos/medillali/writing-vault/git/ref/heads/main')['object']['sha'];assert sha==remote
    tree=api(f'repos/medillali/writing-vault/git/trees/{sha}?recursive=1');assert not tree['truncated']
    remote_files={e['path']:e['sha'] for e in tree['tree'] if e['type']=='blob'}
    local={}
    for rec in git('ls-tree','-r',sha).splitlines():
        meta,path=rec.split('\t',1);local[path]=meta.split()[2]
    # Git默认转义非ASCII路径，使用-z再次取得逐字路径。
    raw=git('ls-tree','-rz',sha)
    local={rec.split('\t',1)[1]:rec.split('\t',1)[0].split()[2] for rec in raw.split('\0') if rec}
    assert local==remote_files
    added=git('diff','--name-only','--diff-filter=A','ca64b73379d524a28b12db1047c9ef016a758305',sha).splitlines()
    result={'valid':True,'repository':'medillali/writing-vault','private':True,'branch':'main','content_commit':sha,'remote_commit_matches':True,'tree_blob_count':len(local),'all_tree_blobs_match':True,'added_paths':len(added),'raw_sources_uploaded':False,'verification':'GitHub API读取main提交与递归树，逐文件比较Git blob SHA。'}
    (R/'.planning/two-books-20261023/remote-latest.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if not (OUT/'validation/remote-content.json').exists():(OUT/'validation/remote-content.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False),flush=True)
else:raise SystemExit(mode)
