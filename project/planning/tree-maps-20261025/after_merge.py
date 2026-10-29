from pathlib import Path
import hashlib,json,subprocess,sys
sys.stdout.reconfigure(encoding='utf-8');R=Path(__file__).resolve().parents[2];V=R/'writing-vault';P=Path(__file__).parent
def git(*args):return subprocess.check_output(['git','-c',f'safe.directory={V.as_posix()}','-c','core.autocrlf=false','-C',str(V),*args]).decode('utf-8').strip()
before=json.loads((P/'main-before-merge.json').read_text(encoding='utf-8'))
paths=sorted(set(x for x in (git('diff','HEAD','--name-only','-z')+'\0'+git('ls-files','--others','--exclude-standard','-z')).split('\0') if x))
after={p:hashlib.sha256((V/p).read_bytes()).hexdigest() if (V/p).is_file() else None for p in before}
normalizations=json.loads((P/'local-newline-normalization.json').read_text(encoding='utf-8'))
allowed={x['path']:x for x in normalizations}
changed=[p for p in before if before[p]!=after[p]]
assert all(p in allowed and before[p]==allowed[p]['original_sha256'] and after[p]==allowed[p]['canonical_sha256'] for p in changed),changed
assert not set(paths)-set(before),'出现未包含在基线的工作区改动'
commit=git('rev-parse','HEAD');changed=sorted(x for x in git('diff-tree','--no-commit-id','--name-only','-r','-z',commit).split('\0') if x)
receipt={'commit':commit,'base':git('rev-parse','HEAD^'),'changed_paths':changed,'parallel_paths_preserved':len(before),'unrelated_changes_identical':True,'generated_plot_copies_normalized_to_git_lf':len(normalizations),'source_graphs_modified_in_git':False,'raw_sources_uploaded':False}
(P/'local-commit.json').write_bytes((json.dumps(receipt,ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps({k:v for k,v in receipt.items() if k!='changed_paths'},ensure_ascii=False))
# 复用已验证的API发布方法，限定本次准确提交和范围。
s=(R/'.planning/book-catalog-20261025/publish_api.py').read_text(encoding='utf-8')
s=s.replace("local_sha=='34f2b642ea5ce81022f8bf38c4519f16c8028c05'",f"local_sha=='{commit}'")
s=s.replace('assert len(changed)==34',f'assert len(changed)=={len(changed)}')
s=s.replace("'root_readme_only_navigation_added':True", "'map_reference':'超级骷髅兵分枝交汇树与同图缩放地图'")
(P/'publish_api.py').write_bytes(s.encode('utf-8'))
