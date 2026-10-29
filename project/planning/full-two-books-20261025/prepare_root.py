from pathlib import Path
import subprocess,json,hashlib
R=Path(__file__).resolve().parents[2];V=R/'.verify/two-books';L=R/'writing-vault';P=Path(__file__).parent
def git(root,*args):
 p=subprocess.run(['git','-c',f'safe.directory={root.as_posix()}','-C',str(root),*args],capture_output=True,text=True,encoding='utf-8',check=True);return p.stdout.strip()
assert not git(V,'status','--porcelain')
author=git(V,'log','-1','--format=%an%n%ae').splitlines()
print(git(V,'-c',f'user.name={author[0]}','-c',f'user.email={author[1]}','merge','--no-edit','origin/main').splitlines()[0])
if git(V,'branch','--show-current')!='codex/two-book-full-distillation':git(V,'branch','-m','codex/two-book-full-distillation')
dirty=git(L,'ls-files','-m','-z').split('\0')
finger={name:hashlib.sha256((L/name).read_bytes()).hexdigest() for name in dirty if name and (L/name).is_file()}
(P/'baseline-dirty.json').write_text(json.dumps(finger,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(P/'baseline.json').write_text(json.dumps({'live_head':git(L,'rev-parse','HEAD'),'worktree_head':git(V,'rev-parse','HEAD'),'worktree':str(V),'branch':git(V,'branch','--show-current'),'existing_modified_tracked_files':len(finger)},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Existing isolated worktree reused; modified live files recorded:',len(finger))
