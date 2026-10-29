"""保存已核源的三个燕赵无双举荐对象纠正字段，原冻结件不动。"""
from pathlib import Path
import copy, hashlib, json
B = Path(__file__).resolve().parent
R = B.parents[2]
A = B / 'zhanlong/audit/whole-book'
F = R / 'writing-vault/library/reports/zhanlong/audit'
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p, data): p.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
p = A / 'priority-corrections-yan-recommendation-proposal.json'
assert sha(p) == '514ca22194d8352bf5854928a4a8f81585c04f9be8773ceb0d987ad883d39684'
proposal = read(p)
assert len(proposal['changes']) == 3
source = read(B / 'zhanlong/source.json')
chapters = {c['chapter_id']: c for c in source['chapters']}
for e in proposal['evidence'] + proposal['later_outcome_evidence']:
    c = chapters[e['chapter_id']]
    assert e['source_id'] == source['source_id'] and e['revision'] == source['revision']
    assert c['start_line'] <= e['start_line'] <= e['end_line'] <= c['end_line']
fields = []
for row in proposal['changes']:
    target = (R / row['file']).resolve()
    assert target.is_relative_to(R) and sha(target) == row['input_sha256']
    if 'jsonl_index' in row:
        value = [json.loads(line) for line in target.read_text(encoding='utf-8').splitlines() if line.strip()][row['jsonl_index']]
        assert value['chapter_id'] == row['chapter_id'] and value['reader'] == row['reader']
        pointer = '/jsonl/' + str(row['jsonl_index'])
    else:
        value = read(target)
        pointer = ''
    for key in row['field_path']:
        value = value[key]
        pointer += '/' + str(key)
    assert value == row['before']
    fields.append(dict(path=row['file'], sha256=row['input_sha256'], field=pointer,
                       before=row['before'], after=row['proposed_after'],
                       issue_id='yan-recommendation-subject-object', evidence=proposal['evidence']))
combined = A / 'priority-corrections-delta.json'
assert sha(combined) == 'a60be7a55b50f2ed5eebdedab3902163a816e50d7a14ae057db68204fdaf8109'
prior = read(combined)
assert len(prior['affected_fields']) == 97 and len(prior['issues']) == 5
dest = F / 'priority-corrections-yan-recommendation.json'
raw = F / 'priority-corrections-yan-recommendation-proposal.json'
snapshot = A / 'priority-corrections-before-yan-recommendation.json'
assert not dest.exists() and not raw.exists() and not snapshot.exists()
approval = dict(reviewer='primary', status='approved-for-library-reading-overlay', user_approval=False,
                approved_fields=3, original_files_unchanged=True, proposal_sha256=sha(p),
                actual_verification=[dict(chapter_id=f'ch-{n:04d}', start_line=a, end_line=z, full_text_read=False)
                                    for n,a,z in [(1192,86860,86869),(1234,89535,89546),(1244,90159,90170)]])
bundle = dict(source_id=source['source_id'], revision=source['revision'],
              issue='1192燕请求被荐为长风统领，而不是荐百里宁', primary_approval=approval,
              affected_fields=fields, later_outcome_evidence=proposal['later_outcome_evidence'],
              later_outcome_scope=proposal['later_outcome_scope'],
              proposal_archive=raw.name, proposal_sha256=sha(p),
              scan_summary=proposal['scan_summary'], reading_precedence='本层after优于旧误读；原始事实笔记、读者与人工字段均保历史。')
snapshot.write_bytes(combined.read_bytes())
raw.write_bytes(p.read_bytes())
write(dest, bundle)
(F / 'priority-corrections-yan-recommendation.md').write_text('''# 燕赵无双举荐对象的核源纠正

1192是燕赵无双请求主角在下次军团会议举荐燕本人，接替年迈的百里宁担任长风军统领；主角以功勋达到为条件答应。当时并未新任百里宁，也未即时任命燕。

1234主角临战任燕为代理统领；1244正式升任并已佩统领徽章。承诺、代理和正式任职分别有来源，后来的任命不倒写1192状态。

主代理实际逐字段审阅三个before/after，并定向核三处原文；保留三个冻结原件与原读者署名。当前阅读采用[三个优先字段与核源](priority-corrections-yan-recommendation.json)，完整扫描范围留于[原始提案](priority-corrections-yan-recommendation-proposal.json)。卡片和已签问题没有沿用此误句，不为纠正额外改写它们。

[本书入口](../README.md)
''', encoding='utf-8')
merged = copy.deepcopy(prior)
merged['issues'].append(dict(issue_id='yan-recommendation-subject-object', affected_fields=fields,
                             primary_approval=approval, formal_bundle='audit/priority-corrections-yan-recommendation.json', formal_bundle_sha256=sha(dest)))
merged['affected_fields'].extend(fields)
merged['primary_approval'].update(approved_issues=6, approved_fields=100)
merged['formal_reading_entries'].append('audit/priority-corrections-yan-recommendation.md')
write(combined, merged)
assert all(sha(R / row['path']) == row['sha256'] for row in fields)
print(json.dumps(dict(approved_fields=3, combined_field_records=100, logical_issues=6,
                      formal_sha256=sha(dest), combined_sha256=sha(combined), originals_unchanged=True), ensure_ascii=False))
