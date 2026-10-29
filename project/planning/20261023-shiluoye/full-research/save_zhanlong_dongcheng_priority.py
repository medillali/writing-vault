"""保存已核源的收养家庭关系纠正；五个冻结原字段及署名均保留。"""
from pathlib import Path
import copy, hashlib, json
B = Path(__file__).resolve().parent
R = B.parents[2]
A = B / 'zhanlong/audit/whole-book'
F = R / 'writing-vault/library/reports/zhanlong/audit'
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p, x): p.write_text(json.dumps(x, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
p = A / 'priority-corrections-dongcheng-kinship-proposal.json'
assert sha(p) == '73e37d241aef23f87842e0e8be27fc2c20b52ebef6de4de715b97cbb9065a16f'
proposal = read(p)
assert len(proposal['changes']) == 5
source = read(B / 'zhanlong/source.json')
c = next(c for c in source['chapters'] if c['chapter_id'] == 'ch-0139')
assert (c['start_line'], c['end_line']) == (12116, 12218)
evidence = [dict(source_id=source['source_id'], revision=source['revision'], chapter_id='ch-0139',
                 start_line=a, end_line=z, claim_kind='fact', actual_reader='primary',
                 reading_scope='本次完整重读该章；不扩大唯一覆盖或改变首次读者归属。') for a,z in [(12149,12149),(12174,12181)]]
fields = []
for row in proposal['changes']:
    target = (R / row['file']).resolve()
    assert target.is_relative_to(R) and sha(target) == row['input_sha256']
    keys = row['field_path']
    if keys[0] == 'line':
        value = target.read_text(encoding='utf-8').splitlines()[keys[1]-1]
    else:
        value = read(target)
        for key in keys:
            value = value[key]
    assert value == row['before']
    fields.append(dict(path=row['file'], sha256=row['input_sha256'], field_path=keys,
                       before=row['before'], after=row['proposed_after'],
                       issue_id='dongcheng-adoptive-family-not-certified-blood-siblings', evidence=evidence))
combined = A / 'priority-corrections-delta.json'
old_digest = '829548507f2346a9384af96ac740cccaafd1cca2a7e9d205b22f40f4bde696cb'
assert sha(combined) == old_digest
prior = read(combined)
assert len(prior['affected_fields']) == 100 and len(prior['issues']) == 6
dest = F / 'priority-corrections-dongcheng-kinship.json'
raw = F / 'priority-corrections-dongcheng-kinship-proposal.json'
snapshot = A / 'priority-corrections-before-dongcheng-kinship.json'
assert not dest.exists() and not raw.exists() and not snapshot.exists()
approval = dict(reviewer='primary', status='approved-for-library-reading-overlay', user_approval=False,
                approved_fields=5, original_files_unchanged=True, proposal_sha256=sha(p),
                actual_verification=dict(chapter_id='ch-0139', start_line=12116, end_line=12218,
                                         full_text_read=True, additional_unique_chapters=0))
bundle = dict(source_id=source['source_id'], revision=source['revision'],
              issue='雷为风收养的故人之子；月雷为同一收养家庭兄妹，不以亲妹标签确立血缘。',
              primary_approval=approval, affected_fields=fields, evidence=evidence,
              proposal_archive=raw.name, proposal_sha256=sha(p),
              scan_summary=dict(input_files=proposal['scan']['input_files'], matching_fields=12, approved_fields=5,
                                other_7_hits='梦瑶真亲妹或关系线程上下文，不改。', semantic_reading_of_all_scanned_files_claimed=False),
              reading_precedence='采用after作为当前研究解释，旧卡/代码/阅读副本与实际署名保历史；不编未给出的亲史。')
snapshot.write_bytes(combined.read_bytes())
raw.write_bytes(p.read_bytes())
write(dest, bundle)
(F / 'priority-corrections-dongcheng-kinship.md').write_text('''# 东城月与东城雷的收养家庭关系

139先由林婉儿所查资料明确东城风膝下一女东城月、另有养子东城雷；随后东城风本人解释雷是故人之子，七岁失去双亲后由自己养大。月与雷作为同一家庭的兄妹互相关心，不应把末卷卡片的“亲妹”直接用作血缘事实，也不补造未写出的亲史。

本次分别核对了五处受影响字段，并由主代理完整重读139。当前采用[五字段优先解释](priority-corrections-dongcheng-kinship.json)；[原提案与扫描](priority-corrections-dongcheng-kinship-proposal.json)保留其实际范围。分卷卡、正式人物材料和派生阅读副本均保留旧字节与署名，用户评价没有改写。

[本书入口](../README.md)
''', encoding='utf-8')
# 已签研究仍可凭原path+SHA解析旧层；不倒填新的105字段层。
history_dir = F / 'material-history'
history_dir.mkdir(exist_ok=True)
historical = history_dir / (old_digest + '.json')
assert not historical.exists()
historical.write_bytes(snapshot.read_bytes())
mp = history_dir / 'manifest.json'
manifest = read(mp)
assert not any(m['original_sha256'] == old_digest for m in manifest['materials'])
manifest['materials'].append(dict(original_path=combined.relative_to(R).as_posix(), original_sha256=old_digest,
                                  archive_path=historical.relative_to(R).as_posix(), archived_sha256=old_digest,
                                  cause='新增收养家庭关系纠正；前105字段层之前的100字段版本原样留存。'))
write(mp, manifest)
merged = copy.deepcopy(prior)
merged['issues'].append(dict(issue_id='dongcheng-adoptive-family-not-certified-blood-siblings',
                            affected_fields=fields, primary_approval=approval,
                            formal_bundle='audit/'+dest.name, formal_bundle_sha256=sha(dest)))
merged['affected_fields'].extend(fields)
merged['primary_approval'].update(approved_issues=7, approved_fields=105)
merged['formal_reading_entries'].append('audit/priority-corrections-dongcheng-kinship.md')
write(combined, merged)
assert all(sha(R / row['path']) == row['sha256'] for row in fields)
print(json.dumps(dict(approved_fields=5, combined_field_records=105, logical_issues=7,
                      formal_sha256=sha(dest), combined_sha256=sha(combined), originals_unchanged=True), ensure_ascii=False))
