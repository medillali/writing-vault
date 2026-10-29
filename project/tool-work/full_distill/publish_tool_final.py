"""只保存已复核的图可读性修复，推送既有私人工具库并独立克隆核验。"""
import json
from check_and_publish import ROOT,HERE,GH,command

def main():
    repo=ROOT/'distill-novels'
    target=ROOT/'.verify/t18'
    assert not target.exists()
    prefix=['git','-c',f'safe.directory={repo.as_posix()}','-c','http.sslBackend=openssl',
            '-c','credential.helper=','-c',f'credential.helper=!{GH.as_posix()} auth git-credential',
            '-c','user.name=Codex','-c','user.email=codex@local.invalid']
    def git(*args):return command(prefix+list(args),repo)
    assert git('branch','--show-current').strip()=='codex/persistent-fiction-library'
    assert git('remote','get-url','personal').strip()=='https://github.com/medillali/distill-novels.git'
    assert not git('diff','--cached','--name-only').strip()
    names=['scripts/fictionlib/viewer.html','tests/browser_smoke.cjs','tests/browser_readability.cjs','tests/render_readability_fixture.py']
    git('add',*names)
    assert set(x for x in git('diff','--cached','--name-only','-z').split('\0') if x)==set(names)
    git('diff','--cached','--check')
    meta=json.loads(command([GH,'api','repos/medillali/distill-novels']))
    assert meta['private'] is True and meta['owner']['login']=='medillali'
    print(git('commit','-m','fix: keep large plot graphs readable when filtering').splitlines()[0])
    git('push','personal','HEAD:main')
    sha=git('rev-parse','HEAD').strip()
    assert json.loads(command([GH,'api','repos/medillali/distill-novels/commits/main']))['sha']==sha
    assert not git('diff','--name-only','HEAD').strip()
    command(prefix+['clone','--quiet','https://github.com/medillali/distill-novels.git',target],ROOT)
    def cloned(*args):return command(['git','-c',f'safe.directory={target.as_posix()}',*args],target)
    assert cloned('rev-parse','HEAD').strip()==sha
    paths=[p for p in git('ls-files','-z').split('\0') if p]
    assert set(paths)==set(p for p in cloned('ls-files','-z').split('\0') if p)
    endings=[]
    for name in paths:
        assert not name.startswith(('private-sources/','work/'))
        a=(repo/name).read_bytes();b=(target/name).read_bytes()
        if a!=b:
            assert a.replace(b'\r\n',b'\n')==b.replace(b'\r\n',b'\n'),name
            endings.append(name)
    result={'remote_private':True,'commit':sha,'tracked_files_verified':len(paths),
            'byte_identical_files':len(paths)-len(endings),'line_ending_only_differences':endings,
            'original_text_absent':True,'clone':str(target),'tracked_changes_clean':True}
    (HERE/'tool-final-verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
