"""将已实际核源的狐狸别名纠正保存为外置层，冻结输入保持原样。"""
from pathlib import Path
import copy, hashlib, json
B=Path(__file__).resolve().parent; R=B.parents[2]
A=B/'zhanlong/audit/whole-book'; F=R/'writing-vault/library/reports/zhanlong/audit'
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x): p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=A/'priority-corrections-fox-identity-proposal.json'
assert sha(p)=='f2a24e3398a2d9905295f6ab9d7ce21b1838c4107771791f6b839323528e1180'
proposal=read(p); assert len(proposal['changes'])==12
source=read(B/'zhanlong/source.json')
evidence=[dict(source_id=source['source_id'],revision=source['revision'],chapter_id=c,start_line=a,end_line=z,claim_kind='fact',actual_reader='primary',reading_scope='本次定向复读；新增唯一覆盖0，首次读者归属保持。') for c,a,z in [('ch-0102',8859,8885),('ch-0103',8967,8977)]]
fields=[]
for row in proposal['changes']:
    target=(R/row['path']).resolve(); assert target.is_relative_to(R) and sha(target)==row['input_sha256']
    if 'field_path' in row:
        keys=row['field_path']; value=read(target)
        for key in keys: value=value[key]
    else:
        keys=['line',row['line']]; value=target.read_text(encoding='utf-8').splitlines()[row['line']-1]
    assert value==row['before'] and '慕天' in value
    assert row['proposed_after']==value.replace('慕天','刘庸')
    fields.append(dict(path=row['path'],sha256=row['input_sha256'],field_path=keys,before=value,after=row['proposed_after'],issue_id='fox-liuyong-unsupported-mutian-alias',evidence=evidence))
combined=A/'priority-corrections-delta.json'; old_digest='5e796e3dd706f6bfd59c6f7eabf3b5a0e0f1288063fce2dcbd4c6261c47b4c01'
assert sha(combined)==old_digest
prior=read(combined); assert len(prior['affected_fields'])==105 and len(prior['issues'])==7
dest=F/'priority-corrections-fox-identity.json'; raw=F/p.name; snap=A/'priority-corrections-before-fox-identity.json'
assert not any(x.exists() for x in [dest,raw,snap])
approval=dict(reviewer='primary',status='approved-for-library-reading-overlay',user_approval=False,approved_fields=12,original_files_unchanged=True,proposal_sha256=sha(p),actual_verification=dict(limited_rereads=['ch-0102 L8859—8885','ch-0103 L8967—8977'],full_book_reread=False,additional_unique_chapters=0))
bundle=dict(source_id=source['source_id'],revision=source['revision'],issue='狐狸本名刘庸，惯用ID琉璃狐；慕天为派生标题无证别名。',primary_approval=approval,affected_fields=fields,evidence=evidence,proposal_archive=raw.name,proposal_sha256=sha(p),reading_precedence='当前采用after；冻结卡片、分析、导入映射和派生阅读页保留历史字节，不据错名另造人或称源文姓名漂移。',scan_boundary='12处传播字段已逐值核验；全源字符串零命中仅作排查支持，不等本次重读全书。')
snap.write_bytes(combined.read_bytes()); raw.write_bytes(p.read_bytes()); write(dest,bundle)
(F/'priority-corrections-fox-identity.md').write_text('''# 狐狸的本名与旧卡无证别名

原文102由李逍遥明确说明狐狸名叫刘庸、惯用ID琉璃狐，厂主随后直呼刘庸；103林婉儿所读资料再次对应这两个名字。卷三旧卡标题的“慕天”没有这些身份依据，当前采用刘庸，不能另造一个人物，也不称小说本身发生姓名漂移。

[十二字段优先解释](priority-corrections-fox-identity.json)记录主代理实际定向核读与逐值检查；[原提案](priority-corrections-fox-identity-proposal.json)保留扫描范围。所有分卷卡、导入记录及阅读副本均保原字节和署名，当前检索解释以本层为准。

[本书入口](../README.md)
''',encoding='utf-8')
hd=F/'material-history'; historical=hd/(old_digest+'.json'); assert not historical.exists()
historical.write_bytes(snap.read_bytes()); mp=hd/'manifest.json'; manifest=read(mp)
assert not any(m['original_sha256']==old_digest for m in manifest['materials'])
manifest['materials'].append(dict(original_path=combined.relative_to(R).as_posix(),original_sha256=old_digest,archive_path=historical.relative_to(R).as_posix(),archived_sha256=old_digest,cause='新增狐狸别名纠正；旧105字段层原样保存。'))
write(mp,manifest)
merged=copy.deepcopy(prior)
merged['issues'].append(dict(issue_id='fox-liuyong-unsupported-mutian-alias',affected_fields=fields,primary_approval=approval,formal_bundle='audit/'+dest.name,formal_bundle_sha256=sha(dest)))
merged['affected_fields'].extend(fields); merged['primary_approval'].update(approved_issues=8,approved_fields=117)
merged['formal_reading_entries'].append('audit/priority-corrections-fox-identity.md'); write(combined,merged)
assert all(sha(R/f['path'])==f['sha256'] for f in fields)
print(json.dumps(dict(approved_field_records=12,combined_field_records=117,logical_issues=8,formal_sha256=sha(dest),combined_sha256=sha(combined),originals_unchanged=True),ensure_ascii=False))
