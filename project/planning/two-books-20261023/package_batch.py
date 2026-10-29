from pathlib import Path
import sys,json,hashlib,shutil,zipfile
R=Path(__file__).resolve().parents[2];V=R/'.verify/two-books';OUT=V/'library/reports/two-books-20261023';B=R/'backups'
sys.path.insert(0,str(R/'distill-novels/scripts'))
from fictionlib.vault import Vault
from fictionlib.exchange import export_bundle
class ReadSnapshotVault(Vault):
    def _sources(self):
        if not hasattr(self,'source_snapshot'):self.source_snapshot=super()._sources()
        return self.source_snapshot
def dump(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
v=ReadSnapshotVault(V)
out=OUT/'handoff'
if not out.exists():
    ids=[x['asset_id'] for x in json.loads((OUT/'batch-assets.json').read_text(encoding='utf-8')) if x['type']=='pattern']
    result=export_bundle(v,out,ids,None,100000)
    print('HANDOFF',json.dumps({k:x for k,x in result.items() if k!='context'},ensure_ascii=False)[:1000],flush=True)
# 为两份原文件留本机独立副本，Git仍忽略此目录。
coverage=json.loads((OUT/'coverage.json').read_text(encoding='utf-8'))
for k,s in coverage['sources'].items():
    raw=next(Path('E:/chromedownload').glob(f"*{s['title']}*.txt"))
    dest=V/f"private-sources/originals/{s['source_id']}.txt";dest.parent.mkdir(parents=True,exist_ok=True)
    if dest.exists():assert hashlib.sha256(dest.read_bytes()).hexdigest()==s['raw_sha256']
    else:shutil.copy2(raw,dest)
    assert hashlib.sha256(dest.read_bytes()).hexdigest()==s['raw_sha256']
rawzip=B/'two-books-originals-20261023.zip'
if not rawzip.exists():
    with zipfile.ZipFile(rawzip,'w',zipfile.ZIP_DEFLATED) as z:
        for p in (V/'private-sources/originals').glob('*.txt'):z.write(p,p.name)
        z.writestr('SOURCE-HASHES.json',json.dumps(coverage['sources'],ensure_ascii=False,indent=2))
with zipfile.ZipFile(rawzip) as z:
    assert z.testzip() is None
    for s in coverage['sources'].values():assert hashlib.sha256(z.read(f"{s['source_id']}.txt")).hexdigest()==s['raw_sha256']
print('RAW_BACKUP_VERIFIED',flush=True)
# 完整本地研究快照覆盖指南和模板；排除原文、Git、锁和缓存。
zip_path=B/'writing-vault-two-books-20261023.zip'
restore=R/'.verify/tbr'
assert not zip_path.exists() and not restore.exists(), '备份和恢复必须使用新路径，不能覆盖旧文件。'
files={}
for p in V.rglob('*'):
    if not p.is_file():continue
    rel=p.relative_to(V).as_posix()
    if rel.split('/')[0] in {'.git','.lock','.journal.json','.cache','private-sources'} or rel.endswith('.local.json'):continue
    assert not p.is_symlink()
    files[rel]=hashlib.sha256(p.read_bytes()).hexdigest()
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
    for rel in sorted(files):z.write(V/rel,rel)
    z.writestr('SNAPSHOT-HASHES.json',json.dumps(files,ensure_ascii=False,indent=2))
restore.mkdir(parents=True)
with zipfile.ZipFile(zip_path) as z:
    assert z.testzip() is None
    for rel,sha in files.items():
        dest=restore/rel
        assert dest.resolve().is_relative_to(restore.resolve())
        data=z.read(rel);assert hashlib.sha256(data).hexdigest()==sha
        dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
rv=ReadSnapshotVault(restore)
check=rv.validate()
assert check['valid'] and check['assets']==565 and check['sources']==6
result={'valid':True,'snapshot_file':'backups/'+zip_path.name,'snapshot_sha256':hashlib.sha256(zip_path.read_bytes()).hexdigest(),'snapshot_files':len(files),'all_file_hashes_match':True,'restored_library':check,'raw_backup':'backups/'+rawzip.name,'raw_source_hashes_match':True,'original_text_in_research_archive':False,'note':'完整研究快照使用ZIP逐文件哈希恢复，含根目录指南与模板；全库检查沿用原规则并缓存来源只读索引。后续验收与远程回执可能晚于本快照，以Git为最终版本。'}
dump(OUT/'validation/backup-restore.json',result)
print(json.dumps(result,ensure_ascii=False),flush=True)
