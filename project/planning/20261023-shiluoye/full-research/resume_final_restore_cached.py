"""重用已生成且逐包核过的新快照，换全新目录实际恢复；只缓存不可变来源索引。"""
from pathlib import Path
import datetime,functools,hashlib,json,zipfile
import backup_and_restore_final as runner
from validate_final_collection import check
from fictionlib.vault import Vault
from fictionlib.exchange import backup_allowed,restore
atomic_write=runner.atomic_write
json_text=runner.json_text

B=Path(__file__).resolve().parent;ROOT=B.parents[2];VAULT=ROOT/'writing-vault'
BACK=ROOT/'backups/three-books-final-20261026-090719'
stamp=datetime.datetime.now().strftime('%Y%m%d-%H%M%S');PARENT=Path('C:/.codex-verify')/('novels-final-cached-'+stamp);DEST=PARENT/'writing-vault'
assert BACK.is_dir() and not PARENT.exists() and not PARENT.resolve().is_relative_to(VAULT.resolve())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
# 标准restore会创建自己的Vault。只在本次独立进程为每个实例加索引缓存，未改工具源文件。
old_init=Vault.__init__
def cached_init(self,*args,**kwargs):
    old_init(self,*args,**kwargs);self._source=functools.lru_cache(maxsize=None)(self._source)
Vault.__init__=cached_init
atomic_write(BACK/'attempt-01-interrupted.json',json_text({'status':'interrupted-during-core-validation-not-accepted','reason':'标准恢复校验反复解析相同不可变来源索引，约十分钟仍在运行；保留已生成的新快照与第一次隔离现场，换新目录采用只读缓存。','verified_process_id':6680,'verified_command':'backup_and_restore_final.py','old_restore_parent':'C:/.codex-verify/novels-final-20261026-090719','original_vault_modified':False,'new_attempt_parent':str(PARENT)}))
print('verify complete snapshot and standard partitions',flush=True)
full_path=BACK/'writing-vault-full.zip'
with zipfile.ZipFile(full_path) as z:
    full=json.loads(z.read('MANIFEST.json'));assert set(z.namelist())==set(full['files'])|{'MANIFEST.json'}
    for name,h in full['files'].items():assert backup_allowed(name) and hashlib.sha256(z.read(name)).hexdigest()==h
core=BACK/'core.zip';supplements=sorted(BACK.glob('reports-*.zip'));assert len(supplements)==3
union={}
for part in [core]+supplements:
    m=runner.verify_archive(part,reports_only=part!=core);assert m['vault_id']==full['vault_id']
    assert not set(union).intersection(m['files']);union.update(m['files'])
assert union==full['files']
current={p.relative_to(VAULT).as_posix():sha(p) for p in VAULT.rglob('*') if p.is_file() and backup_allowed(p.relative_to(VAULT).as_posix())}
assert current==full['files'],'现库与本轮已生成快照不再一致，不能直接复用'
print('validate source collection with immutable-source cache',flush=True);before=check(ROOT,False)
print('standard restore into fresh isolated directory '+str(DEST),flush=True);core_result=restore(core,DEST)
additions=[runner.restore_reports(p,DEST,full['vault_id']) for p in supplements]
actual={p.relative_to(DEST).as_posix():sha(p) for p in DEST.rglob('*') if p.is_file() and backup_allowed(p.relative_to(DEST).as_posix())}
assert actual==full['files'],'实际恢复与完整快照文件/哈希不一致'
print('regenerate views and independently validate actual restored library',flush=True)
support=runner.regenerate_support(DEST);plots=runner.regenerate(DEST);after=check(PARENT,False)
for k in ['vault','reading_unit_segments_exactly_once','checkpoint_partitions_verified','reachable_local_links_checked','immutable_historical_markdown_contexts_verified','historical_context_links_checked']:assert before[k]==after[k],k
result={'status':'fresh-backup-and-actual-restore-validated','full_archive':str(full_path),'full_archive_sha256':sha(full_path),'restore_core':{'path':str(core),'sha256':sha(core)},'report_supplements':[{'path':str(p),'sha256':sha(p)} for p in supplements],'restore_directory':str(DEST),'core_restore':core_result,'report_restore':additions,'all_snapshot_files_sha256_equal':True,'verified_snapshot_files':len(full['files']),'source_current_files_exactly_equal_snapshot_before_restore':True,'standard_restore_limits_preserved':{'max_entries_per_archive':10000,'max_uncompressed_bytes_per_archive':runner.CAP},'original_text_excluded':True,'support_entry_restored':support,'derived_plot_restore':plots,'original_collection_validation':before,'restored_collection_validation':after,'source_cache_policy':'仅本次进程为不可变索引做实例缓存；标准restore源码、路径、大小、哈希和结构校验均未修改。','previous_attempt':'attempt-01-interrupted.json','snapshot_boundary':'本次新回执在快照后保存于归档sidecar及现库；快照保生成时的旧回执，不声称包含自己。'}
atomic_write(BACK/'verification.json',json_text(result));atomic_write(VAULT/'library/reports/collection/backup-verification.json',json_text(result))
atomic_write(BACK/'README.md','\n'.join(['# 本轮完整研究资料库备份','','`writing-vault-full.zip`为本轮完整研究快照；实际恢复核验见`verification.json`。','标准恢复输入为`core.zip`加三个`reports-*.zip`补充包；逐包200MiB/10000条边界未放宽，补充包仅新建报告文件并核全量SHA，禁止覆盖。','原小说TXT、机器配置、Git内部及派生阅读页面不在标准快照中。原TXT须独立保留；根入口/模板等通过归档内SHA支持恢复计划重建，剧情和卡片视图也已实际重建。','首次恢复在重复索引解析阶段中断，现场和原因保`attempt-01-interrupted.json`；最终验收是换新目录后的完整恢复，不是首次未完成现场。','最终验证保全全部快照文件的SHA，并在真实恢复目录再次执行三书审计、包内材料解析、来源/检查点/导航核验。','回执在快照后生成，归档sidecar与现库保存新回执，不声称快照包含自身。未执行Git推送或外部同步。','']))
print(json.dumps({k:result[k] for k in ['status','full_archive','restore_directory','verified_snapshot_files','all_snapshot_files_sha256_equal']},ensure_ascii=False),flush=True)
