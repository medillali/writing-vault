"""只同步已授权的地图阅读成果到既有私有资料库。"""
import sys
sys.dont_write_bytecode=True
import json
from verify_plot_images import ROOT,VAULT,REPORT,GH,command,git
from verify_map import verify,BASE
verify()
assert git('branch','--show-current').strip()=='codex/full-map-viewer'
assert not git('diff','--cached','--name-only').strip(),'存在其他任务暂存的文件'
git('fetch','origin','main')
assert git('rev-parse','origin/main').strip()==BASE,'远程发生其他更新，先整合再继续'
git('add','--','README.md','library/reports/super-skeleton')
names=git('diff','--cached','--name-only','-z').split('\0')
assert all(not p or p=='README.md' or p.startswith('library/reports/super-skeleton/') for p in names)
assert not any('/whole-book/' in p or '/plot/images/' in p for p in names)
git('diff','--cached','--check')
git('commit','-m','新增整图地图阅读器并优化Codex与GitHub看图入口')
head=git('rev-parse','HEAD').strip()
git('switch','main');git('merge','--ff-only','codex/full-map-viewer')
git('push','origin','main')
remote=json.loads(command([GH,'api','repos/medillali/writing-vault/commits/main']))['sha']
assert remote==head
tree=json.loads(command([GH,'api',f'repos/medillali/writing-vault/git/trees/{head}?recursive=1']))
assert not tree['truncated']
actual={x['path']:x['sha'] for x in tree['tree'] if x['type']=='blob'}
expected={}
for row in git('ls-tree','-r','-z','HEAD').split('\0'):
    if row:
        info,name=row.split('\t',1);expected[name]=info.split()[2]
assert actual==expected
assert not git('diff','HEAD','--','README.md','library/reports/super-skeleton').strip()
result={'commit':head,'remote_main':remote,'private_repository':'medillali/writing-vault','remote_blobs_match':len(actual),
        'map_changes_committed':True,'unrelated_work_preserved':git('status','--porcelain').splitlines(),
        'reader_entry':'https://github.com/medillali/writing-vault/blob/main/library/reports/super-skeleton/reading/plot/map.md',
        'public_website_deployed':False,'physical_phone_verified':False}
(ROOT/'distill-novels/work/full_distill/map-sync-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
