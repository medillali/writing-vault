import pathlib,sys,functools,json,hashlib,zipfile,datetime
sys.stdout.reconfigure(encoding='utf-8')
root=pathlib.Path(__file__).resolve().parents[2];sys.path.insert(0,str(root/'distill-novels/scripts'))
from fictionlib.vault import Vault
from fictionlib.exchange import backup,restore,backup_allowed
from fictionlib.storage import atomic_write,json_text
# 原校验函数仍逐项校验；仅为持锁读操作缓存不可变的来源查询。
Vault._source=functools.lru_cache(maxsize=None)(Vault._source)
vault=root/'writing-vault';v=Vault(vault)
stamp=datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
destination=root/'backups'/('writing-vault-collection-'+stamp+'.zip')
names=[p.relative_to(vault).as_posix() for p in vault.rglob('*') if p.is_file() and backup_allowed(p.relative_to(vault).as_posix())]
restore_dir=root/'.verify'/('collection-'+stamp)
if max(len(str(restore_dir/name)) for name in names)>245:
    restore_dir=pathlib.Path('C:/.codex-verify')/('nv-'+stamp)
print('backup start',flush=True)
b=backup(v,destination);print('backup',b,flush=True)
with zipfile.ZipFile(destination) as archive:
    assert not any(n.startswith(('private-sources/','.git/')) for n in archive.namelist())
    manifest=json.loads(archive.read('MANIFEST.json'))
    assert all(hashlib.sha256(archive.read(n)).hexdigest()==h for n,h in manifest['files'].items())
print('restore start',str(restore_dir),flush=True)
r=restore(destination,restore_dir);print('restore',r,flush=True)
report={'backup':b,'restore':r,'archive_sha256':hashlib.sha256(destination.read_bytes()).hexdigest(),'all_manifest_hashes_verified':True,'original_text_excluded':True}
atomic_write(vault/'library/reports/collection/backup-verification.json',json_text(report))
print(json.dumps(report,ensure_ascii=False),flush=True)
