"""全部本地验收完成后保存最终审查成果，并核对私人远程提交。"""
import json
from check_and_publish import ROOT,HERE,GH,command,git,SOURCE

def main():
    vault=ROOT/'writing-vault'
    for name in ['fullbook-verification.json','live-18-qa.json','review-package.json','delivery-backup-verification.json']:
        assert (HERE/name).exists(),name
    assert json.loads((HERE/'review-package.json').read_text(encoding='utf-8'))['browser_check']=='passed'
    assert json.loads((HERE/'delivery-backup-verification.json').read_text(encoding='utf-8'))['all_archived_files_identical_to_delivery'] is True
    assert git('branch','--show-current').strip()=='main'
    assert git('remote','get-url','origin').strip()=='https://github.com/medillali/writing-vault.git'
    html=(vault/'library/views/超级骷髅兵全书审查.html').read_text(encoding='utf-8')
    assert 'private-sources' not in html
    from pathlib import Path
    raw=Path(SOURCE['normalized_path']).read_text(encoding='utf-8')
    assert not any(line[:200] in html for line in raw.splitlines() if len(line)>=200)
    git('add','README.md','library','history','exchanges/runs/run-deep-super-skeleton-20261022.json')
    names=[n for n in git('diff','--cached','--name-only','-z').split('\0') if n]
    assert names and all(n=='README.md' or n.startswith(('library/','history/','exchanges/runs/')) for n in names)
    git('diff','--cached','--check')
    print(git('commit','-m','research: finalize Super Skeleton whole-book audits and offline review').splitlines()[0])
    meta=json.loads(command([GH,'api','repos/medillali/writing-vault']))
    assert meta['private'] is True and meta['owner']['login']=='medillali'
    git('push','origin','main')
    sha=git('rev-parse','HEAD').strip()
    assert json.loads(command([GH,'api','repos/medillali/writing-vault/commits/main']))['sha']==sha
    assert not git('status','--porcelain').strip()
    result={'head':sha,'pushed':True,'private':True,'files_in_final_commit':len(names),'clean':True}
    (HERE/'publish-final.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
