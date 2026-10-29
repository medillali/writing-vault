from pathlib import Path
import sys,json,hashlib,zipfile,subprocess
R=Path(__file__).resolve().parents[2];L=R/'writing-vault';P=R/'.planning/two-books-20261023';V=R/'.verify/two-books';O=L/'library/reports/two-books-20261023'
sys.path.insert(0,str(R/'distill-novels/scripts'))
from fictionlib.vault import Vault
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def dump(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
class Cached(Vault):
 def _sources(self):
  if not hasattr(self,'cache'):self.cache=super()._sources()
  return self.cache
sha=read(P/'remote-latest.json')['content_commit'];prefix=['git','-c',f'safe.directory={L.as_posix()}','-c','core.autocrlf=false','-C',str(L)]
zpath=R/f'backups/writing-vault-two-books-canonical-exact-{sha[:7]}.zip';restore=R/'.verify/two-books-canonical-exact-restore'
assert not zpath.exists() and not restore.exists()
subprocess.run(prefix+['archive','--format=zip','-o',str(zpath),sha],check=True,capture_output=True)
tree=subprocess.run(prefix+['ls-tree','-rz',sha],check=True,capture_output=True).stdout.decode('utf-8')
expected={rec.split('\t',1)[1]:rec.split('\t',1)[0].split()[2] for rec in tree.split('\0') if rec}
with zipfile.ZipFile(zpath) as z:
 assert z.testzip() is None
 actual={n for n in z.namelist() if not n.endswith('/')};assert actual==set(expected)
 for name in sorted(actual):
  dest=restore/name;assert dest.resolve().is_relative_to(restore.resolve())
  data=z.read(name);assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==expected[name],name
  dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
validation=Cached(restore).validate();assert validation['valid'] and validation['assets']==565 and validation['sources']==6
rawzip=R/'backups/two-books-canonical-originals-20261023.zip';assert not rawzip.exists()
coverage=read(O/'coverage.json')['sources']
with zipfile.ZipFile(rawzip,'w',zipfile.ZIP_DEFLATED) as z:
 for s in coverage.values():
  source=next(Path('E:/chromedownload').glob(f"*{s['title']}*.txt"));data=source.read_bytes();assert hashlib.sha256(data).hexdigest()==s['raw_sha256']
  z.writestr(s['source_id']+'.txt',data)
 z.writestr('SOURCE-HASHES.json',json.dumps(coverage,ensure_ascii=False,indent=2))
with zipfile.ZipFile(rawzip) as z:
 assert z.testzip() is None
 for s in coverage.values():assert hashlib.sha256(z.read(s['source_id']+'.txt')).hexdigest()==s['raw_sha256']
result={'valid':True,'content_commit':sha,'archive':zpath.relative_to(R).as_posix(),'sha256':hashlib.sha256(zpath.read_bytes()).hexdigest(),'files':len(expected),'all_git_blob_hashes_match':True,'restored_validation':validation,'raw_archive':rawzip.relative_to(R).as_posix(),'raw_original_hashes_match':True,'originals_uploaded':False,'note':'从已经远程回读的Git内容提交生成，恢复到新目录，逐文件核对Git blob身份并重新执行完整资料校验。最终远程回执文档另随下一次提交保存。'}
dump(P/'canonical-backup.json',result)
for base in [L,V]:
 report=base/'library/reports/two-books-20261023'
 dump(report/'validation/canonical-backup-restore.json',result);dump(report/'validation/remote-content.json',read(P/'remote-latest.json'))
 p=report/'acceptance.md';s=p.read_text(encoding='utf-8')
 s=s.replace('待最终远程回读','已提交并远程核验（8d0cb62）').replace('1058处卡片证据','1174处卡片证据')
 s=s.replace('2152文件逐一恢复匹配，全库验证通过','最终Git快照2190文件恢复匹配，全库验证通过')
 s+='\n## 最终交付核验\n\n内容提交 `'+sha+'` 已推送私有仓库 `medillali/writing-vault` 的 `main`，并通过GitHub API读回核对全部2190个文件的Git blob身份，见[远程回执](validation/remote-content.json)。\n\n身份统一后的[最终备份恢复](validation/canonical-backup-restore.json)以该Git提交生成，2190文件逐一匹配；恢复库565卡、6来源、6图通过。旧2152文件快照仅为历史恢复点。真实共享库另外存在并行任务新建的两部来源，整合时[本地核验](validation/live-integration.json)为565卡、8来源、6图；没有覆盖其他任务资料。\n\n实际检索已能命中本批“奖励保留尚未兑现的部分”机制卡。后续接续《练级专家》第13章；研究卡仍待人工审阅，原创试用未开始。\n'
 p.write_text(s,encoding='utf-8')
print(json.dumps(result,ensure_ascii=False),flush=True)
