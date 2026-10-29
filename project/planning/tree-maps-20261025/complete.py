from pathlib import Path
import json,subprocess
R=Path(__file__).resolve().parents[2];P=Path(__file__).parent;V=R/'writing-vault';W=(R/'.verify/tree-maps-20261025').resolve()
receipt=json.loads((P/'remote-verification.json').read_text(encoding='utf-8'))
def git(v,*args):return subprocess.check_output(['git','-c',f'safe.directory={v.as_posix()}','-C',str(v),*args]).decode('utf-8').strip()
assert receipt['valid'] and receipt['all_tree_blobs_match']
assert git(V,'rev-parse','HEAD')==receipt['remote_head']==git(V,'rev-parse','refs/remotes/origin/main')
p=P/'task_plan.md';s=p.read_text(encoding='utf-8').replace('- [ ] 更新本地/Git书目入口，限定提交并远程回读。','- [x] 更新本地/Git书目入口，限定提交并远程回读。');p.write_bytes(s.encode('utf-8'))
with (P/'progress.md').open('a',encoding='utf-8') as out:out.write('\n本轮完成：新版树图与地图已在真实资料库/main，提交'+receipt['remote_head']+'；私有远程4145个文件对象全树回读一致。原书名/作者/类型导航已更新。真实手机手势与文学、审美判断仍待用户审阅。\n')
# 只清理由本轮创建、已合入且无改动的临时工作树；路径明确限定在.verify内。
assert W==R/'.verify/tree-maps-20261025' and W.is_relative_to((R/'.verify').resolve())
assert git(W,'rev-parse','HEAD')==receipt['remote_head']
assert not git(W,'status','--porcelain')
ignored=[p for p in git(W,'ls-files','--others','--ignored','--exclude-standard','-z').split('\0') if p]
assert all('/__pycache__/' in p and p.endswith('.pyc') for p in ignored),ignored
subprocess.run(['git','-c',f'safe.directory={V.as_posix()}','-C',str(V),'worktree','remove',str(W)],check=True,capture_output=True)
print(json.dumps({'remote_verified':True,'commit':receipt['remote_head'],'temporary_worktree_removed':not W.exists(),'primary_workspace':str(V)},ensure_ascii=False))
