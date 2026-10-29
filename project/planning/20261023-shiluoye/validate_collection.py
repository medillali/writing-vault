import pathlib,sys,json,functools,re,hashlib,collections,time
from urllib.parse import unquote
sys.stdout.reconfigure(encoding='utf-8')
root=pathlib.Path(__file__).resolve().parents[2];sys.path.insert(0,str(root/'distill-novels/scripts'))
from fictionlib.vault import Vault
from fictionlib.storage import atomic_write,json_text
from fictionlib.exchange import backup_allowed
vault=root/'writing-vault';v=Vault(vault)
# 校验全程持有库锁。仅缓存只读来源查询，沿用原始查询和全部验证规则。
v._source=functools.lru_cache(maxsize=None)(v._source)
started=time.monotonic();print('validation started',flush=True)
status=v.validate();print('vault',status,'seconds',round(time.monotonic()-started,2),flush=True)
print('views',v.build_views(),flush=True)
sources={s['source_id']:s for s in v.sources()}; unit_map=json.loads((vault/'library/reports/collection/reading-units.json').read_text(encoding='utf-8'))
mapping_count=0
for sid,record in unit_map.items():
    src=sources[sid]; rev=next(r for r in src['revisions'] if r['revision']==record['source_revision'])
    index_fields=[[c.get(k) for k in ['chapter_id','title','start_line','end_line']] for c in rev['chapters']]
    assert record['index_fingerprint']==hashlib.sha256(json.dumps(index_fields,ensure_ascii=False,separators=(',',':')).encode('utf-8')).hexdigest()
    expected={c['chapter_id'] for c in rev['chapters']};actual=[c for u in record['units'] for c in u['segment_ids']]
    assert len(actual)==len(set(actual)) and set(actual)==expected
    mapping_count+=len(actual)
run_count=0;nonbody_exclusions=[]
for p in (vault/'exchanges/runs').glob('*.json'):
    run=json.loads(p.read_text(encoding='utf-8'));src=sources[run['source_id']];rev=next(r for r in src['revisions'] if r['revision']==run['source_revision'])
    complete=run['completed_chapters'];pending=run['pending_chapters']
    assert not set(complete)&set(pending)
    assert len(set(complete+pending))==len(complete+pending)
    expected={c['chapter_id'] for c in rev['chapters']};partition=set(complete+pending)
    assert partition.issubset(expected)
    required={cid for u in unit_map[run['source_id']]['units'] if u['kind'] in ['body','prologue'] for cid in u['segment_ids']}
    assert required.issubset(partition)
    omitted=expected-partition
    if omitted:nonbody_exclusions.append({'run_id':run['run_id'],'nonbody_segments_omitted':sorted(omitted)})
    run_count+=1
links=[];broken=[]
for directory in [vault/'library/reports/collection',vault/'library/reports/zeidan',vault/'library/reports/zongheng-tianxia']:
    if not directory.exists():continue
    for p in directory.rglob('*.md'):
        for target in re.findall(r'\]\(([^\n)]+)\)',p.read_text(encoding='utf-8')):
            target=target.strip('<>');pieces=target.split('#',1);fragment=pieces[1] if len(pieces)>1 else None;target=unquote(pieces[0])
            if not target or re.match(r'^[a-z]+://',target):continue
            q=(p.parent/target).resolve();links.append((str(p),target))
            if not q.is_file():broken.append((str(p),target))
            elif fragment and q.name=='evidence-index.md' and ('id="'+fragment+'"') not in q.read_text(encoding='utf-8'):broken.append((str(p),target+'#'+fragment))
sizes=[p.stat().st_size for p in vault.rglob('*') if p.is_file() and backup_allowed(p.relative_to(vault).as_posix())]
queries={}
for tag in ['作者:失落叶','作者:发飙的蜗牛']:
    matches=v.search(tags=[tag]);assert matches and all(tag in a['tags'] for a in matches)
    queries[tag]={'total':len(matches),'types':dict(collections.Counter(a['asset_type'] for a in matches))}
report={'vault':status,'reading_unit_segments_exactly_once':mapping_count,'checkpoint_partition_verified':run_count,'checkpoint_nonbody_exclusions':nonbody_exclusions,'checked_local_links':len(links),'broken_local_links':broken,'author_query_checks':queries,'backup_candidate_files':len(sizes),'backup_candidate_bytes':sum(sizes),'limitations':['结构校验不证明所有文学判断正确','已导入旧研究不等于本轮重新全文阅读','本轮没有完成三部全书蒸馏或用户审阅']}
atomic_write(vault/'library/reports/collection/validation.json',json_text(report))
print(json.dumps(report,ensure_ascii=False),flush=True)
if broken:raise SystemExit(1)
