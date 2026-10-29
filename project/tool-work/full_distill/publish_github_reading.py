"""限定提交阅读副本，并读回远程树核对Git对象。"""
import json
from check_and_publish import ROOT,HERE,GH,command,git

v=ROOT/'writing-vault'
assert git('branch','--show-current').strip()=='main'
assert git('remote','get-url','origin').strip()=='https://github.com/medillali/writing-vault.git'
assert not git('diff','--cached','--name-only').strip()
proof=json.loads((HERE/'github-reading-verification.json').read_text(encoding='utf-8'))
assert proof['card_content_preserved']==226 and proof['local_links_checked']>4000
meta=json.loads(command([GH,'api','repos/medillali/writing-vault']))
assert meta['private'] is True and meta['owner']['login']=='medillali'
validation=v/'library/reports/super-skeleton/validation/github-reading.json'
validation.write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
paths=['README.md','library/reports/super-skeleton/README.md','library/reports/super-skeleton/rebuild_github_reading.py',
       'library/reports/super-skeleton/reading','library/reports/super-skeleton/validation/github-reading.json']
git('add',*paths)
names=[n for n in git('diff','--cached','--name-only','-z').split('\0') if n]
assert all(n in paths or n.startswith('library/reports/super-skeleton/reading/') for n in names)
git('diff','--cached','--check')
print(git('commit','-m','docs: lead readable cards with summaries and Chinese fields').splitlines()[0],flush=True)
git('push','origin','main')
sha=git('rev-parse','HEAD').strip()
assert json.loads(command([GH,'api','repos/medillali/writing-vault/commits/main']))['sha']==sha
tree=json.loads(command([GH,'api',f'repos/medillali/writing-vault/git/trees/{sha}?recursive=1']))
assert not tree['truncated']
remote={x['path']:x['sha'] for x in tree['tree'] if x['type']=='blob'}
tracked={}
for row in git('ls-files','--stage','-z').split('\0'):
    if not row:continue
    attrs,name=row.split('\t',1)
    tracked[name]=attrs.split()[1]
assert remote==tracked
assert not git('status','--porcelain').strip()
result={'private':True,'commit':sha,'changed_files':len(names),'remote_git_blobs_verified':len(remote),'clean':True,
        'reading_url':'https://github.com/medillali/writing-vault/blob/main/library/reports/super-skeleton/reading/README.md'}
(HERE/'github-reading-published.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
