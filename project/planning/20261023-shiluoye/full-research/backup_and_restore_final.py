"""三书验收后生成新备份并实际恢复；保留标准恢复规模限制。"""
from pathlib import Path
import argparse,datetime,functools,hashlib,json,stat,sys,zipfile

B=Path(__file__).resolve().parent;ROOT=B.parents[2]
sys.path.insert(0,str(ROOT/'distill-novels/scripts'))
from fictionlib.vault import Vault
from fictionlib.exchange import backup,restore,backup_allowed
from fictionlib.storage import atomic_write,json_text,safe_path
from prepare_view_restore_plan import prepare,regenerate
from prepare_support_restore_plan import prepare as prepare_support,regenerate as regenerate_support
from validate_final_collection import check

CAP=200*1024*1024;TARGET=140*1024*1024;ENTRY_TARGET=6500
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def part_manifest(full,names,role):
    return {**{k:v for k,v in full.items() if k!='files'},'part_role':role,
        'files':{n:full['files'][n] for n in sorted(names)}}

def verify_archive(path,reports_only=False):
    with zipfile.ZipFile(path) as z:
        items=z.infolist();names=[i.filename for i in items]
        assert len(items)<=10000 and len(names)==len(set(names)) and sum(i.file_size for i in items)<=CAP
        assert 'MANIFEST.json' in names
        m=json.loads(z.read('MANIFEST.json'));assert m['schema_version']==1
        assert set(m['files'])==set(names)-{'MANIFEST.json'}
        for item in items:
            n=item.filename;safe_path(Path('C:/.codex-verify/path-check'),n)
            assert not stat.S_ISLNK(item.external_attr>>16)
            if n=='MANIFEST.json':continue
            assert backup_allowed(n) and (not reports_only or n.startswith('library/reports/'))
            assert hashlib.sha256(z.read(n)).hexdigest()==m['files'][n],n
        return m

def partition(full_path,directory):
    with zipfile.ZipFile(full_path) as z:
        full=json.loads(z.read('MANIFEST.json'));sizes={i.filename:i.file_size for i in z.infolist()}
        assert set(full['files'])==set(sizes)-{'MANIFEST.json'}
        for n,h in full['files'].items():assert hashlib.sha256(z.read(n)).hexdigest()==h,n
        if len(sizes)<=10000 and sum(sizes.values())<=CAP:
            verify_archive(full_path)
            return full,full_path,[]
        # 原始完整包保留；只把报告拆出，全部正典/历史/检查点仍在可标准恢复的核心包。
        core=set(full['files']);deferred=[]
        candidates=sorted((n for n in core if n.startswith('library/reports/')),key=lambda n:(-sizes[n],n))
        while sum(sizes[n] for n in core)>TARGET or len(core)>ENTRY_TARGET:
            assert candidates,'正典核心自身超过限制，需人工调整方案，不能放宽恢复保护'
            n=candidates.pop(0);core.remove(n);deferred.append(n)
        groups=[]
        for n in deferred:
            assert sizes[n]<TARGET,'单个报告超过分包上限'
            group=next((g for g in groups if len(g)<ENTRY_TARGET and sum(sizes[x] for x in g)+sizes[n]<TARGET),None)
            if group is None:group=[];groups.append(group)
            group.append(n)
        definitions=[('core',core)]+[(f'reports-{i:02d}',set(g)) for i,g in enumerate(groups,1)]
        union=set();paths=[]
        for role,names in definitions:
            assert not union&names;union|=names
            path=directory/(role+'.zip');assert not path.exists()
            manifest=part_manifest(full,names,role)
            with zipfile.ZipFile(path,'x',compression=zipfile.ZIP_DEFLATED) as out:
                for n in sorted(names):out.writestr(n,z.read(n))
                out.writestr('MANIFEST.json',json_text(manifest))
            verify_archive(path,reports_only=role!='core');paths.append(path)
        assert union==set(full['files'])
        return full,paths[0],paths[1:]

def restore_reports(path,vault,vault_id):
    manifest=verify_archive(path,reports_only=True);assert manifest['vault_id']==vault_id
    with zipfile.ZipFile(path) as z:
        paths={n:safe_path(vault,n) for n in manifest['files']}
        assert all(not p.exists() for p in paths.values()),'补充报告不得覆盖已恢复文件'
        for n,p in paths.items():
            content=z.read(n);assert hashlib.sha256(content).hexdigest()==manifest['files'][n]
            p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(content)
    return {'archive':str(path),'verified_report_files':len(paths)}

def run(root,backup_root,restore_parent):
    root=Path(root).resolve();vault=root/'writing-vault';backup_root=Path(backup_root).resolve()
    restore_parent=Path(restore_parent).resolve();restored=restore_parent/'writing-vault'
    assert not backup_root.exists() and not restore_parent.exists()
    assert not backup_root.is_relative_to(vault) and not restore_parent.is_relative_to(vault)
    v=Vault(vault);v._source=functools.lru_cache(maxsize=None)(v._source)
    print('prepare derived plot regeneration data',flush=True);plan=prepare(vault)
    support_plan=prepare_support(vault)
    print('validate completed collection before snapshot',flush=True);before=check(root,True)
    backup_root.mkdir(parents=True)
    full_path=backup_root/'writing-vault-full.zip'
    print('create fresh complete backup',flush=True);created=backup(v,full_path)
    full,core,supplements=partition(full_path,backup_root)
    print('restore core into new isolated directory',str(restored),flush=True)
    core_result=restore(core,restored)
    additions=[restore_reports(p,restored,full['vault_id']) for p in supplements]
    expected=full['files'];actual={p.relative_to(restored).as_posix():sha(p) for p in restored.rglob('*')
        if p.is_file() and backup_allowed(p.relative_to(restored).as_posix())}
    assert actual==expected,'完整恢复文件列表或SHA与原始快照不一致'
    print('regenerate derived plot views and validate restored collection',flush=True)
    support_restored=regenerate_support(restored)
    regenerated=regenerate(restored);after=check(restore_parent,False)
    assert before['vault']==after['vault']
    assert before['reading_unit_segments_exactly_once']==after['reading_unit_segments_exactly_once']
    assert before['reachable_local_links_checked']==after['reachable_local_links_checked']
    result={'status':'fresh-backup-and-actual-restore-validated','created':created,
        'full_archive':str(full_path),'full_archive_sha256':sha(full_path),
        'restore_core':{'path':str(core),'sha256':sha(core)},
        'report_supplements':[{'path':str(p),'sha256':sha(p)} for p in supplements],
        'restore_directory':str(restored),'core_restore':core_result,'report_restore':additions,
        'all_snapshot_files_sha256_equal':True,'verified_snapshot_files':len(expected),
        'standard_restore_limits_preserved':{'max_entries_per_archive':10000,'max_uncompressed_bytes_per_archive':CAP},
        'original_text_excluded':True,'derived_plot_plan':plan,'derived_plot_restore':regenerated,
        'support_entry_plan':support_plan,'support_entry_restored':support_restored,
        'original_collection_validation':before,'restored_collection_validation':after,
        'snapshot_boundary':'备份后生成的本次验收回执保存于同目录sidecar和现库；快照本身保留备份当时的旧回执，不声称包含自身。'}
    atomic_write(backup_root/'verification.json',json_text(result))
    atomic_write(vault/'library/reports/collection/backup-verification.json',json_text(result))
    instructions=['# 本轮完整资料库备份','','完整快照：`writing-vault-full.zip`。校验与实际恢复结果：`verification.json`。',
        '原始小说、机器路径配置、Git目录和派生阅读页面不在标准快照内；章节定位、卡片、历史、报告和检查点均在。',
        '若存在core.zip及reports补充包，完整包超过单次恢复边界；已按同一MANIFEST分包实际恢复，未放宽200MiB/10000条保护。',
        '核心包通过标准restore恢复；补充包仅允许library/reports新文件，先查全部SHA/路径/大小且禁止覆盖；union必须等于完整快照清单。',
        '派生卡片页面由Vault.build_views重建；所有图由collection/qa/view-restore-plan.json及其按SHA保存的图快照重建。',
        '标准白名单外的START-HERE、指南、队列、templates及书库入口通过collection/qa/support-restore-plan.json及SHA附件核验恢复；不会覆盖不同内容的文件。',
        '本回执只证明本地备份和隔离恢复，未执行远程同步或推送。','']
    atomic_write(backup_root/'README.md','\n'.join(instructions))
    return {k:result[k] for k in ['status','full_archive','restore_directory','verified_snapshot_files','all_snapshot_files_sha256_equal']}

if __name__=='__main__':
    sys.stdout.reconfigure(encoding='utf-8');stamp=datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=ROOT)
    p.add_argument('--backup-root',type=Path);p.add_argument('--restore-parent',type=Path)
    args=p.parse_args();backup_root=args.backup_root or args.root/'backups'/('three-books-final-'+stamp)
    restore_parent=args.restore_parent or Path('C:/.codex-verify')/('novels-final-'+stamp)
    print(json.dumps(run(args.root,backup_root,restore_parent),ensure_ascii=False),flush=True)
