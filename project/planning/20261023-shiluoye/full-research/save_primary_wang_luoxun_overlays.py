"""保存两项已实际核源的最小外置更正；旧研究、已合并池字节均不改。"""
from pathlib import Path
import copy,hashlib,json
B=Path(__file__).resolve().parent;R=B.parents[2];A=B/'zhanlong/audit/whole-book';F=R/'writing-vault/library/reports/zhanlong/audit'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
s=read(B/'zhanlong/source.json');combined=A/'priority-corrections-delta.json'
assert sha(combined)=='622d7815796ff0ed6b1f6b79318f9537be538fd23cd2fd94c469c96cc08cc5c6'
definitions=[dict(slug='wang-identity',proposal=A/'priority-corrections-wang-identity-proposal.json',proposal_sha='584a5d0123215cc224a5deaf38d90c9fa1e6077220c370ebbf096a1077f261e8',field='changes',count=38,issue_id='wangjiang-and-wangjian-distinct-players',summary='王将与王翦为独立玩家；秦雨表白线归王将，不是王翦的早期恋情。',ranges=[(445,37035,37045,False),(499,40949,41036,True),(500,41037,41107,True),(1199,87370,87386,False)],title='王将与王翦分人核源更正'),dict(slug='luoxun-timing',proposal=A/'reader3-review/priority-luoxun-timing-proposal.json',proposal_sha='b1d131b55544cd36ad53ddfbc88e26ce090c40d57eb363971a8dfc44b0883aab',field='affected_fields',count=8,issue_id='luoxun-command-999-execution-1000',summary='999仅逼令洛洵自尽，1000才现场自刎并收尸；死亡事实不变。',ranges=[(999,74066,74078,False),(1000,74083,74100,False)],title='洛洵自尽命令与实际死亡的时点更正')]
for spec in definitions:
    p=spec['proposal'];assert sha(p)==spec['proposal_sha'];proposal=read(p);rows=proposal[spec['field']];assert len(rows)==spec['count']
    ev=[dict(source_id=s['source_id'],revision=s['revision'],chapter_id=f'ch-{c:04d}',start_line=a,end_line=z,claim_kind='fact',actual_reader='primary',full_text_read=full,unique_coverage_increment=0) for c,a,z,full in spec['ranges']]
    fields=[]
    for row in rows:
        path=row['path'];target=(R/path).resolve();h=row.get('input_sha256',row.get('sha256'));assert target.is_relative_to(R) and sha(target)==h
        keys=row['field_path']
        if keys[0]=='line':value=target.read_text(encoding='utf-8').splitlines()[keys[1]-1]
        else:
            value=read(target)
            for key in keys:value=value[key]
        assert value==row['before']
        fields.append(dict(path=path,sha256=h,field_path=keys,before=value,after=row.get('proposed_after',row.get('after')),issue_id=spec['issue_id'],evidence=ev))
    dest=F/('priority-corrections-'+spec['slug']+'.json');raw=F/('priority-corrections-'+spec['slug']+'-proposal.json');snap=A/('priority-corrections-before-'+spec['slug']+'.json')
    assert not any(p.exists() for p in [dest,raw,snap])
    prior=read(combined);h=sha(combined);snap.write_bytes(combined.read_bytes());raw.write_bytes(p.read_bytes())
    approval=dict(reviewer='primary',status='approved-for-library-reading-overlay',user_approval=False,approved_fields=len(fields),original_files_unchanged=True,proposal_sha256=sha(p),actual_source_verification=ev)
    bundle=dict(source_id=s['source_id'],revision=s['revision'],issue=spec['summary'],primary_approval=approval,affected_fields=fields,evidence=ev,proposal_archive=raw.name,proposal_sha256=sha(p),reading_precedence='采用after作为当前解释；分卷原件、历史导入、canonical与阅读副本保原字节及署名。纠正层不等用户审美批准。',candidate_pools_unchanged=True,pool_check_boundary='原终评中相关条目已由提案者实际核查，未发现需改终评；root本次不重审全部两池，也不把原错录倒变成新故事事实。')
    write(dest,bundle)
    (dest.with_suffix('.md')).write_text('# '+spec['title']+'\n\n'+spec['summary']+'\n\n当前使用[已核更正层]('+dest.name+')；[原提案]('+raw.name+')保留有限扫描、字段与实际阅读范围。旧阶段材料保历史，不能把旧误合或错误时点解释成原作改名、恋情转移或人物复生。\n\n[返回本书入口](../README.md)\n',encoding='utf-8')
    hd=F/'material-history';historical=hd/(h+'.json');assert not historical.exists();historical.write_bytes(snap.read_bytes());mp=hd/'manifest.json';manifest=read(mp)
    manifest['materials'].append(dict(original_path=combined.relative_to(R).as_posix(),original_sha256=h,archive_path=historical.relative_to(R).as_posix(),archived_sha256=h,cause='新增'+spec['title']+'；旧组合层按精确字节保留。'));write(mp,manifest)
    merged=copy.deepcopy(prior);merged['issues'].append(dict(issue_id=spec['issue_id'],affected_fields=fields,primary_approval=approval,formal_bundle='audit/'+dest.name,formal_bundle_sha256=sha(dest)))
    merged['affected_fields'].extend(fields);merged['primary_approval'].update(approved_issues=len(merged['issues']),approved_fields=len(merged['affected_fields']));merged['formal_reading_entries'].append('audit/'+dest.with_suffix('.md').name);write(combined,merged)
    assert all(sha(R/f['path'])==f['sha256'] for f in fields)
    print(json.dumps(dict(issue=spec['slug'],approved_field_records=len(fields),combined_field_records=len(merged['affected_fields']),logical_issues=len(merged['issues']),formal_sha256=sha(dest),combined_sha256=sha(combined),originals_unchanged=True),ensure_ascii=False))
