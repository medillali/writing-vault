"""只提交双书修图和书库入口，快进合入主工作区并核对并行研究未变。"""
from pathlib import Path
import hashlib,json,subprocess,sys
sys.stdout.reconfigure(encoding='utf-8')
R=Path(__file__).resolve().parents[2];W=R/'.verify/tree-maps-20261025';V=R/'writing-vault';P=Path(__file__).parent
BASE='34f2b642ea5ce81022f8bf38c4519f16c8028c05'
def git(v,*args,raw=False):
 cmd=['git','-c',f'safe.directory={v.as_posix()}','-c','core.autocrlf=false','-c','core.quotepath=false','-C',str(v),*args]
 x=subprocess.run(cmd,capture_output=True,check=True).stdout
 return x if raw else x.decode('utf-8').strip()
def files(v):
 tracked=[x for x in git(v,'diff','HEAD','--name-only','-z').split('\0') if x]
 untracked=[x for x in git(v,'ls-files','--others','--exclude-standard','-z').split('\0') if x]
 return sorted(set(tracked+untracked))
def snapshot(v):
 return {p:hashlib.sha256((v/p).read_bytes()).hexdigest() if (v/p).is_file() else None for p in files(v)}
assert git(W,'branch','--show-current')=='codex/two-book-tree-maps'
assert git(V,'branch','--show-current')=='main'
assert git(W,'rev-parse','HEAD')==git(V,'rev-parse','HEAD')==BASE
assert not git(V,'diff','--cached','--name-only'),'主工作区已有暂存改动，不能混入'
paths=files(W);assert paths and all(p.startswith(('library/reports/two-books-full-20261025/','书库/')) for p in paths)
assert not any('__pycache__' in p or p.endswith('.pyc') or '/private-sources/' in p for p in paths)
assert not any(p.endswith('/plot/graph.json') for p in paths)
before=snapshot(V);assert not set(before)&set(paths),('当前并行研究与修图文件重叠',sorted(set(before)&set(paths)))
(P/'main-before-merge.json').write_bytes((json.dumps(before,ensure_ascii=False,indent=2)+'\n').encode())
git(W,'add','--',*paths)
staged=sorted(x for x in git(W,'diff','--cached','--name-only','-z').split('\0') if x);assert staged==paths
print('限定暂存路径',len(paths),'；并行研究保留',len(before),'个路径',flush=True)
git(W,'-c','user.name=Codex','-c','user.email=codex@local.invalid','commit','-m','按超级骷髅兵形式重做双书剧情树与离线缩放地图')
commit=git(W,'rev-parse','HEAD');git(V,'merge','--ff-only','codex/two-book-tree-maps')
assert git(V,'rev-parse','HEAD')==commit
after=snapshot(V);assert after==before,'并行研究有变化，需检查是否来自其他任务；未推送'
receipt={'commit':commit,'base':BASE,'changed_paths':paths,'parallel_paths_preserved':len(before),'unrelated_changes_identical':True,'source_graphs_modified':False,'raw_sources_uploaded':False}
(P/'local-commit.json').write_bytes((json.dumps(receipt,ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps({k:v for k,v in receipt.items() if k!='changed_paths'},ensure_ascii=False))
