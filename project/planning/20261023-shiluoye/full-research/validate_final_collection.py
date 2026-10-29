"""三书完成后的全库验收；支持真实恢复目录，不以旧批次回执代替。"""
from pathlib import Path
import argparse,collections,functools,hashlib,importlib.util,json,re,sys,time
from urllib.parse import unquote
from validate_book_audit import validate as validate_audit

B=Path(__file__).resolve().parent; TOOL_ROOT=B.parents[2]
sys.path.insert(0,str(TOOL_ROOT/'distill-novels/scripts'))
from fictionlib.vault import Vault
from fictionlib.exchange import backup_allowed

BOOKS=('zongheng-tianxia','tianxia-wushuang','zhanlong')
EXPECTED_BODY={'zongheng-tianxia':1180,'tianxia-wushuang':1599,'zhanlong':1378}
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def check_material_archive(root,slug):
    """正式包与实际恢复包均只依赖包内材料，不回读旧暂存路径。"""
    audit=Path(root)/'writing-vault/library/reports'/slug/'audit/whole-book'
    rel=Path('assembly-prep/assemble_zhanlong_signed_audit.py')
    candidates=[audit/rel,audit/'provenance'/rel]
    code=next((p for p in candidates if p.is_file()),None)
    assert code is not None,'正式包缺独立材料验证接口'
    spec=importlib.util.spec_from_file_location('verified_material_archive',code)
    module=importlib.util.module_from_spec(spec)
    old=sys.dont_write_bytecode
    try:
        sys.dont_write_bytecode=True
        spec.loader.exec_module(module)
        assert module.validate_material_archive(audit) is True
    finally:sys.dont_write_bytecode=old
    return {'status':'exact-archived-material-versions-passed',
            'entries':len(read(audit/'material-resolution-index.json')['entries']),
            'planning_directory_required':False}

def check(root,write_report=False):
    root=Path(root).resolve();vault=root/'writing-vault';collection=vault/'library/reports/collection'
    receipts={}
    for slug in BOOKS:
        d=vault/'library/reports'/slug;r=read(d/'ACCEPTANCE.json')
        assert r['status']=='full-source-nine-dimensions-and-terminal-audit-complete'
        assert r['body_units']==EXPECTED_BODY[slug] and r['user_approval'] is False
        coverage=read(d/'audit/full-reading-validation.json')
        assert coverage['status']=='passed' and coverage['body_units']==r['body_units']
        for name,digest in coverage['formal_input_sha256'].items():assert sha(d/name)==digest,(slug,name)
        sreview=read(d/'audit/book-synthesis-review.json')
        assert sha(d/'book-synthesis.json')==sreview['published_json_sha256']
        assert sha(d/'book-synthesis.md')==sreview['published_markdown_sha256']
        synthesis=read(d/'book-synthesis.json')
        assert len(synthesis['dimensions'])==9 and sum(map(len,synthesis['dimensions'].values()))==36
        receipts[slug]={'acceptance':r['status'],'body_units':r['body_units'],'audit':validate_audit(root,slug)}
        if slug=='zhanlong':receipts[slug]['archived_materials']=check_material_archive(root,slug)
    v=Vault(vault);v._source=functools.lru_cache(maxsize=None)(v._source)
    started=time.monotonic();status=v.validate()
    # 仅重建排除在默认备份外的卡片阅读副本，不触碰已冻结分卷/审计导航。
    views=v.build_views()
    sources={s['source_id']:s for s in v.sources()}
    units=read(collection/'reading-units.json');mapped=0
    for sid,mapping in units.items():
        src=sources[sid];rev=next(x for x in src['revisions'] if x['revision']==mapping['source_revision'])
        fields=[[c.get(k) for k in ['chapter_id','title','start_line','end_line']] for c in rev['chapters']]
        assert mapping['index_fingerprint']==hashlib.sha256(json.dumps(fields,ensure_ascii=False,separators=(',',':')).encode('utf-8')).hexdigest()
        ids=[cid for u in mapping['units'] for cid in u['segment_ids']]
        assert len(ids)==len(set(ids)) and set(ids)=={c['chapter_id'] for c in rev['chapters']}
        mapped+=len(ids)
    runs=0;omitted_nonbody=[]
    for p in (vault/'exchanges/runs').glob('*.json'):
        r=read(p);src=sources[r['source_id']];rev=next(x for x in src['revisions'] if x['revision']==r['source_revision'])
        done,pending=r['completed_chapters'],r['pending_chapters'];partition=done+pending
        assert len(partition)==len(set(partition)) and set(partition)<={c['chapter_id'] for c in rev['chapters']}
        body={cid for u in units[r['source_id']]['units'] if u['kind'] in ['body','prologue'] for cid in u['segment_ids']}
        assert body<=set(partition)
        missing={c['chapter_id'] for c in rev['chapters']}-set(partition)
        if missing:omitted_nonbody.append({'run_id':r['run_id'],'segments':sorted(missing)})
        runs+=1
    config=read(collection/'catalog-config.json');catalog=read(collection/'catalog.json')
    assert config['active_source_id'] is None,'三书完结后仍有活动正文来源'
    assert len(catalog['books'])==8 and catalog['active_source_id'] is None
    for slug in BOOKS:
        entry=next(x for x in catalog['books'] if x['slug']==slug)
        assert entry['task_state']=='completed_full_nine'
        assert entry['completed_body_units']==entry['body_reading_units']==EXPECTED_BODY[slug]
        assert entry['next_reading_unit'] is None
    # 两部蜗牛已有全书成果继续采用原任务检查点，不追认为本轮重读。
    for suffix in ['z','l']:
        r=read(vault/'exchanges/runs'/f'run-full-two-books-20261025-{suffix}.json')
        assert r['state']=='full-source-read-and-distilled' and not r['pending_chapters']
    checks={}
    for tag in ['作者:失落叶','作者:发飙的蜗牛']:
        rows=v.search(tags=[tag]);assert rows and all(tag in x['tags'] for x in rows)
        checks[tag]={'cards':len(rows),'types':dict(collections.Counter(x['asset_type'] for x in rows))}
    broken=[];links=0;historical_links=0;historical_contexts={}
    registry=collection/'qa/historical-markdown-contexts.json'
    if registry.is_file():
        for row in read(registry)['entries']:
            p=(vault/row['archive_path']).resolve();assert p.is_relative_to(vault) and sha(p)==row['sha256']
            base=(vault/row['original_navigation_base']).resolve();assert base.is_relative_to(vault) and base.is_dir()
            for target in row['exact_snapshot_targets'].values():
                q=(vault/target['path']).resolve();assert q.is_relative_to(vault) and sha(q)==target['sha256']
            historical_contexts[p]=row
    dirs=[collection,vault/'library/reports/zeidan',vault/'library/reports/two-books-full-20261025']+[vault/'library/reports'/s for s in BOOKS]
    for d in dirs:
        if not d.exists():continue
        for p in d.rglob('*.md'):
            if 'provenance' in p.relative_to(d).parts:continue
            for raw in re.findall(r'\]\(([^\n)]+)\)',p.read_text(encoding='utf-8')):
                raw=raw.strip().strip('<>')
                if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',raw) or raw.startswith('#'):continue
                target,_,fragment=raw.partition('#');target=unquote(target)
                if not target:continue
                if p.resolve() in historical_contexts:
                    context=historical_contexts[p.resolve()];override_target=context['exact_snapshot_targets'].get(target)
                    q=(vault/override_target['path']).resolve() if override_target else (vault/context['original_navigation_base']/target).resolve();historical_links+=1
                else:q=(p.parent/target).resolve();links+=1
                if not q.exists():broken.append((str(p.relative_to(vault)),raw))
                elif q.is_file() and fragment and q.name=='evidence-index.md' and f'id="{fragment}"' not in q.read_text(encoding='utf-8'):
                    broken.append((str(p.relative_to(vault)),raw))
    assert not broken,broken[:20]
    assert type(mapped) is int and mapped>0,'原阅读单元计数不得被导航解析变量覆盖'
    files=[p for p in vault.rglob('*') if p.is_file() and backup_allowed(p.relative_to(vault).as_posix())]
    result={'status':'three-books-and-collection-local-validation-passed','vault':status,
        'books':receipts,'reading_unit_segments_exactly_once':mapped,'checkpoint_partitions_verified':runs,
        'checkpoint_nonbody_exclusions':omitted_nonbody,'reachable_local_links_checked':links,
        'immutable_historical_markdown_contexts_verified':len(historical_contexts),'historical_context_links_checked':historical_links,
        'author_queries':checks,'rebuilt_asset_views':views['assets'],
        'backup_candidate_files':len(files),'backup_candidate_bytes':sum(p.stat().st_size for p in files),
        'elapsed_seconds':round(time.monotonic()-started,2),
        'limits':['结构和哈希验收不代替文学主审或用户审美认可','旧蜗牛全书成果按原任务检查点接入，未追认本轮重读','此回执不等备份/实际恢复/远程推送已经执行']}
    if write_report:
        (collection/'full-project-validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return result

if __name__=='__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=TOOL_ROOT)
    p.add_argument('--write-report',action='store_true');args=p.parse_args()
    print(json.dumps(check(args.root,args.write_report),ensure_ascii=False),flush=True)
