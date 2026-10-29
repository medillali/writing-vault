"""逐集校验、生成审查入口并提交私人库；原文不进入Git。"""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
from persist import ROOT,HERE,SID,CH,DIMS,SOURCE,check_report
sys.path.insert(0,str(ROOT/'distill-novels/scripts'))
from fictionlib.vault import Vault

GH=Path.home()/'Tools/gh/bin/gh.exe'
ENV={**os.environ,'GIT_TERMINAL_PROMPT':'0','GH_PROMPT_DISABLED':'1'}

def command(args,cwd=None):
    r=subprocess.run([str(x) for x in args],cwd=cwd,env=ENV,capture_output=True,text=True,encoding='utf-8',errors='replace')
    if r.returncode:raise RuntimeError(r.stderr or r.stdout)
    return r.stdout

def git(*args):
    repo=ROOT/'writing-vault'
    return command(['git','-c',f'safe.directory={repo.as_posix()}','-c','http.sslBackend=openssl',
                    '-c','credential.helper=','-c',f'credential.helper=!{GH.as_posix()} auth git-credential',
                    '-c','user.name=Codex','-c','user.email=codex@local.invalid',*args],repo)

def main(n,push):
    if n>=15:
        from verify_cross_retention import verify
        print(json.dumps(verify()))
    v=Vault(ROOT/'writing-vault')
    folder=v.root/'library/reports/super-skeleton'
    reports=[json.loads(p.read_text(encoding='utf-8')) for p in sorted(folder.glob('vol[0-9][0-9].json'))]
    assert [r['volume'] for r in reports]==list(range(1,n+1))
    for report in reports:check_report(report)
    checkpoint=v.get_checkpoint('run-deep-super-skeleton-20261022')
    done=[c for r in reports for c in r['chapter_ids']]
    assert checkpoint['completed_chapters']==done
    assert set(checkpoint['pending_chapters'])==set(CH)-set(done)
    assert len(done)==len(set(done))
    status=v.validate()
    graph=json.loads((v.root/'library/sources'/SID/'plot-graph.json').read_text(encoding='utf-8'))
    assert graph['coverage'][0]['chapter_ids']==done
    assert graph['coverage'][0]['complete']==(n==18)
    script=HERE/'build_review.py'
    if not script.exists():raise ValueError('审查页生成器尚未就绪，不发布无入口的批次')
    print(command([sys.executable,'-X','utf8',script]))
    html=(v.root/'library/views/超级骷髅兵全书审查.html').read_text(encoding='utf-8')
    assert 'private-sources' not in html, '审查页不得包含本机原文路径'
    raw=Path(SOURCE['normalized_path']).read_text(encoding='utf-8')
    assert not any(line[:200] in html for line in raw.splitlines() if len(line)>=200), '审查页包含长原文段落'
    # 随研究主档保存生成器，备份恢复后无需依赖临时工作目录。
    (folder/'rebuild_review.py').write_text(script.read_text(encoding='utf-8'),encoding='utf-8')
    audit=folder/'audit'
    audit.mkdir(exist_ok=True)
    for review in HERE.glob('review-[0-9][0-9].md'):
        if int(review.stem[-2:])<=n:
            (audit/review.name).write_text(review.read_text(encoding='utf-8'),encoding='utf-8')
    if n>=8:
        for name in ['cross-audit-01-06.md','early-reconciliation.md','early-reconciliation.json']:
            if (HERE/name).exists():(audit/name).write_text((HERE/name).read_text(encoding='utf-8'),encoding='utf-8')
    (folder/'cross-input.json').write_text((HERE/'cross-input.json').read_text(encoding='utf-8'),encoding='utf-8')
    assert git('branch','--show-current').strip()=='main'
    assert git('remote','get-url','origin').strip()=='https://github.com/medillali/writing-vault.git'
    git('add','library','history','exchanges/runs/run-deep-super-skeleton-20261022.json')
    names=git('diff','--cached','--name-only','-z').split('\0')
    assert all(not name or name.startswith(('library/','history/','exchanges/runs/')) for name in names)
    git('diff','--cached','--check')
    if any(names):print(git('commit','-m',f'research: complete Super Skeleton volume {n:02d} nine-dimension draft').splitlines()[0])
    sha=git('rev-parse','HEAD').strip()
    if push:
        meta=json.loads(command([GH,'api','repos/medillali/writing-vault']))
        assert meta['private'] and meta['owner']['login']=='medillali'
        git('push','origin','main')
        remote=json.loads(command([GH,'api','repos/medillali/writing-vault/commits/main']))['sha']
        assert remote==sha
    result={'volume':n,'completed_segments':len(done),'validation':status,'head':sha,'pushed':push}
    (HERE/f'publish-{n:02d}.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    with (HERE/'progress.md').open('a',encoding='utf-8') as f:f.write(f'\n- 第{n}集：正式入库与检查通过，Git {sha}，已推送={push}。')
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('volume',type=int);p.add_argument('--push',action='store_true');a=p.parse_args();main(a.volume,a.push)
