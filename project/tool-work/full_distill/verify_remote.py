"""从私人远程重新克隆，并对照最终本地研究主档。"""
import hashlib
import json
from pathlib import Path
import sys
from check_and_publish import ROOT,HERE,GH,command,git
from fictionlib.vault import Vault

def main():
    original=ROOT/'writing-vault'
    target=ROOT/'.verify/c18'
    assert not target.exists(), '使用新的短路径，避免覆盖既有验收副本'
    sha=git('rev-parse','HEAD').strip()
    assert not git('status','--porcelain').strip(), '正式库必须先提交完成'
    meta=json.loads(command([GH,'api','repos/medillali/writing-vault']))
    assert meta['private'] is True and meta['owner']['login']=='medillali'
    remote=json.loads(command([GH,'api','repos/medillali/writing-vault/commits/main']))['sha']
    assert remote==sha
    prefix=['git','-c','http.sslBackend=openssl','-c','credential.helper=',
            '-c',f'credential.helper=!{GH.as_posix()} auth git-credential']
    command(prefix+['clone','--quiet','https://github.com/medillali/writing-vault.git',target])
    def clone_git(*args):
        return command(['git','-c',f'safe.directory={target.as_posix()}',*args],target)
    assert clone_git('rev-parse','HEAD').strip()==sha
    print('Private remote cloned; commit matches local '+sha,flush=True)
    paths=[s for s in git('ls-files','-z').split('\0') if s]
    assert set(paths)==set(s for s in clone_git('ls-files','-z').split('\0') if s)
    endings=[]
    for name in paths:
        assert not name.startswith('private-sources/')
        a=(original/name).read_bytes();b=(target/name).read_bytes()
        if a!=b:
            assert a.replace(b'\r\n',b'\n')==b.replace(b'\r\n',b'\n'),name
            endings.append(name)
    print(f'Verified {len(paths)} tracked files; {len(endings)} differ only in Windows line endings. Validating restored vault.',flush=True)
    local_vault=Vault(original)
    clone=Vault(target)
    status=clone.validate()
    print('Fresh remote clone vault validation passed.',flush=True)
    assert {a['asset_id']:a for a in clone.search()}=={a['asset_id']:a for a in local_vault.search()}
    assert not (target/'private-sources').exists()
    script=target/'library/reports/super-skeleton/rebuild_review.py'
    command([sys.executable,'-X','utf8',script],target)
    page='library/views/超级骷髅兵全书审查.html'
    assert (target/page).read_bytes()==(original/page).read_bytes()
    result={'remote_private':True,'commit':sha,'tracked_files_verified':len(paths),
            'byte_identical_files':len(paths)-len(endings),'line_ending_only_differences':endings,
            'vault':status,'original_text_absent':True,'independent_html_rebuild_identical':True,
            'clone':str(target),'review_html_sha256':hashlib.sha256((target/page).read_bytes()).hexdigest()}
    (HERE/'remote-fullbook-verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
