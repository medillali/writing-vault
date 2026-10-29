from pathlib import Path
import subprocess,json
R=Path(__file__).resolve().parents[2];V=R/'.verify/two-books'
def git(*args):
 p=subprocess.run(['git','-c',f'safe.directory={V.as_posix()}','-C',str(V),*args],text=True,encoding='utf-8',capture_output=True)
 if p.returncode:raise RuntimeError(p.stderr+p.stdout)
 return p.stdout.strip()
assert git('branch','--show-current')=='codex/two-book-distillation'
assert git('check-ignore','private-sources/normalized/manifest.json')
git('add','-A');git('diff','--cached','--check')
author=git('log','-1','--format=%an%n%ae').splitlines()
print(git('-c',f'user.name={author[0]}','-c',f'user.email={author[1]}','commit','-m','对齐长期库来源身份并保存验证与整合记录').splitlines()[0])
assert not git('status','--porcelain')
print('隔离工作分支已保存；正式交付在长期库main。')
