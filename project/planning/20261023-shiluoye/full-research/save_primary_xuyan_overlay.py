"""按实际已读原文保存徐焰所属军团更正；原七字段仍保历史字节。"""
from pathlib import Path
import copy,hashlib,json
B=Path(__file__).resolve().parent;R=B.parents[2];A=B/'zhanlong/audit/whole-book';F=R/'writing-vault/library/reports/zhanlong/audit'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=A/'reader4-character-review/xuyan-summary-correction-proposal.json'
assert sha(p)=='1949afe6543a4d0d44025fee24a646fdce0b5cb1ae62260d4700b3c3a8667684'
combined=A/'priority-corrections-delta.json';assert sha(combined)=='c194cae95a9bb02b8e620286ad4ec06f9ddbd5856f25c08600252e0b053819aa'
source=read(B/'zhanlong/source.json');proposal=read(p);fields=proposal['affected_fields'];assert len(fields)==7
for row in fields:
    target=R/row['path'];assert sha(target)==row['sha256']
    keys=row['field_path']
    if keys[0]=='line':value=target.read_text(encoding='utf-8').splitlines()[keys[1]-1]
    else:
        value=read(target)
        for k in keys:value=value[k]
    assert value==row['before'] and row['after']==row['before'].replace('御林违令','狂雷军违令')
ev=[dict(source_id=source['source_id'],revision=source['revision'],chapter_id=f'ch-{n:04d}',start_line=a,end_line=z,claim_kind='fact',actual_reader='primary',full_text_read=full,unique_coverage_increment=0) for n,a,z,full in [(1001,74200,74212,False),(1067,78313,78377,True)]]
approval=dict(reviewer='primary',status='approved-for-library-reading-overlay',user_approval=False,approved_fields=7,original_files_unchanged=True,proposal_sha256=sha(p),actual_source_verification=ev)
dest=F/'priority-corrections-xuyan-army.json';raw=F/'priority-corrections-xuyan-army-proposal.json';snap=A/'priority-corrections-before-xuyan-army.json'
assert not any(x.exists() for x in [dest,raw,snap]);raw.write_bytes(p.read_bytes());snap.write_bytes(combined.read_bytes())
bundle=dict(source_id=source['source_id'],revision=source['revision'],issue='徐焰违令被降时属狂雷军，旧summary的御林为研究误录。',primary_approval=approval,affected_fields=fields,evidence=ev,proposal_archive=raw.name,proposal_sha256=sha(p),reading_precedence='after为当前解释；冻结分卷、canonical与旧阅读副本保原字节，非用户审美批准。')
write(dest,bundle)
dest.with_suffix('.md').write_text('# 徐焰所属军团核源更正\n\n徐焰1001受任狂雷统领，1067主角认尸时仍回顾其曾任狂雷统帅。旧summary写“御林违令”属于研究误录，当前采用“狂雷军违令”；不改其降职、死亡及1213死灵再现分期。\n\n[更正七字段与核源范围]('+dest.name+') · [原提案]('+raw.name+') · [本书入口](../README.md)\n',encoding='utf-8')
old=read(combined);oldsha=sha(combined);hd=F/'material-history';archive=hd/(oldsha+'.json');assert not archive.exists();archive.write_bytes(combined.read_bytes())
manifest=read(hd/'manifest.json');manifest['materials'].append(dict(original_path=combined.relative_to(R).as_posix(),original_sha256=oldsha,archive_path=archive.relative_to(R).as_posix(),archived_sha256=oldsha,cause='新增徐焰所属军团更正；旧组合层精确保留。'));write(hd/'manifest.json',manifest)
merged=copy.deepcopy(old);merged['issues'].append(dict(issue_id='xuyan-kuanglei-not-yulin-summary',affected_fields=fields,primary_approval=approval,formal_bundle='audit/'+dest.name,formal_bundle_sha256=sha(dest)));merged['affected_fields'].extend(fields);merged['primary_approval'].update(approved_issues=len(merged['issues']),approved_fields=len(merged['affected_fields']));merged['formal_reading_entries'].append('audit/'+dest.with_suffix('.md').name);write(combined,merged)
assert all(sha(R/x['path'])==x['sha256'] for x in fields)
print(json.dumps(dict(approved_field_records=7,combined_field_records=len(merged['affected_fields']),logical_issues=len(merged['issues']),formal_sha256=sha(dest),combined_sha256=sha(combined),original_files_unchanged=True),ensure_ascii=False))
