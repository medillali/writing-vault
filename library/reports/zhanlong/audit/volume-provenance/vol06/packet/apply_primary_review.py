"""精确应用primary已经逐项读审并批准的提案；不重生研究或改原阅读记录。"""
from pathlib import Path
import ast
import copy
import datetime
import hashlib
import json
import runpy
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8')
H = Path(__file__).resolve().parent
B = H / 'review-corrections' / 'before-primary'
PROPOSAL_SHA = 'fcdc58e12438ab3752095b0350bc434ac74e7cbbb596c2844df443be8b1f9187'
SCENES_SHA = '557eddc552c9e8454ca344fd6f1fadc204649820c7dacfd7ed9a8c911dff1bed'
FREEZE_SHA = 'b5f408525fba0be8d7a3ef6e192878b5c7a40d8519c442ce7b3897464337786a'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def get_at(value, path):
    for part in path:
        value = value[part]
    return value


def set_at(value, path, replacement):
    for part in path[:-1]:
        value = value[part]
    value[path[-1]] = copy.deepcopy(replacement)


assert sha(H / 'freeze-manifest.json') == FREEZE_SHA
assert sha(H / 'primary-review-proposal.json') == PROPOSAL_SHA
assert sha(H / 'scene-transfer-proposals.json') == SCENES_SHA
manifest = read(H / 'freeze-manifest.json')
proposal = read(H / 'primary-review-proposal.json')
scene_proposal = read(H / 'scene-transfer-proposals.json')
assert len(proposal['changes']) == 23 and len(scene_proposal['proposals']) == 58
assert proposal['base_freeze_sha256'] == FREEZE_SHA
assert all(sha(H / n) == digest for n, digest in manifest['files'].items())
assert all(sha(H / n) == digest for n, digest in manifest['reproduction_inputs'].items())

# 先保留十个旧冻结文件、旧清单、装配代码、获批提案及真实主审范围回执。
assert not B.exists(), '本次修订不得覆盖已有before快照；需人工核实后续运行状态。'
B.mkdir(parents=True)
snapshot_names = list(manifest['files']) + ['freeze-manifest.json'] + list(manifest['reproduction_inputs'])
snapshot_names += ['primary-review-proposal.json', 'primary-review-proposal.md',
                   'scene-transfer-proposals.json', 'scene-transfer-proposals.md',
                   'scene-transfer-proposals-authored.json', 'prepare_primary_review_proposal.py']
for name in snapshot_names:
    shutil.copy2(H / name, B / name)
review_path = H.parent / 'vol06-primary-review-progress.json'
shutil.copy2(review_path, B / review_path.name)
snapshot_hashes = {name: sha(B / name) for name in snapshot_names + [review_path.name]}
write_json(B / 'snapshot.json', dict(created_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                                   source='应用已批准定向修订前的原样快照', files=snapshot_hashes))

before = {name: read(H / name) for name in ['analysis.json', 'cards.json', 'graph.json']}
after = copy.deepcopy(before)
changes = copy.deepcopy(proposal['changes'])
cards_by_origin = {c['origin_key']: i for i, c in enumerate(before['cards.json'])}
for item in scene_proposal['proposals']:
    i = cards_by_origin[item['origin_key']]
    card = before['cards.json'][i]
    assert card['content']['why_it_works'] == item['why_it_works_preserved']
    assert card['evidence'] == item['evidence_preserved']
    for field in ['applicability', 'failure_mode']:
        changes.append(dict(file='cards.json', json_path=[i, 'content', field],
                            before=item['before'][field], proposed_after=item['proposed_after'][field],
                            rationale='primary逐场审读批准的具体适用条件/失败边界；why_it_works及证据不改。',
                            origin_key=item['origin_key']))
assert len(changes) == 139
for item in changes:
    assert get_at(after[item['file']], item['json_path']) == item['before'], item
    set_at(after[item['file']], item['json_path'], item['proposed_after'])

# 用独立的遮蔽比较核验所有未列路径；列表内细节也不能随装配改动。
unchanged = {}
for name in before:
    old_mask = copy.deepcopy(before[name])
    new_mask = copy.deepcopy(after[name])
    paths = [r['json_path'] for r in changes if r['file'] == name]
    assert len({tuple(path) for path in paths}) == len(paths)
    for path in paths:
        set_at(old_mask, path, {'__approved_path__': True})
        set_at(new_mask, path, {'__approved_path__': True})
    assert old_mask == new_mask, name
    unchanged[name] = dict(approved_paths=len(paths), all_other_values_exactly_equal=True)

def obs_line(row):
    return ('- **' + row['title'] + '**：' + row['interpretation']['text'] + ' 事实：' +
            row['facts'][0]['text'] + ' 限制：' + row['limits_and_counterevidence'] +
            '（raw ' + ','.join(e['chapter_id'][3:] for e in row['facts'][0]['evidence']) + '）')


old_report = (H / 'report.md').read_text(encoding='utf-8')
new_report = old_report
text_changes = []
for dim, rows in before['analysis.json']['dimensions'].items():
    for i, row in enumerate(rows):
        updated = after['analysis.json']['dimensions'][dim][i]
        if row != updated:
            old, new = obs_line(row), obs_line(updated)
            assert new_report.count(old) == 1, row['id']
            new_report = new_report.replace(old, new)
            text_changes.append(dict(file='report.md', observation_id=row['id'], before=old, after=new))
assert len(text_changes) == 4
old_handoff = (H / 'handoff.md').read_text(encoding='utf-8')
handoff_old = '终开幕救军并斩几十追兽，留100龙骑守关。'
handoff_new = '终开幕救军并斩几十追兽，允留100名龙骑协防，未另演全部到场。'
assert old_handoff.count(handoff_old) == 1
new_handoff = old_handoff.replace(handoff_old, handoff_new)
text_changes.append(dict(file='handoff.md', before=handoff_old, after=handoff_new))

# 同步人工数据装配入口。这里只替换已经批准的literal与两处edge kind，不运行build()。
codes = {name: (H / name).read_text(encoding='utf-8') for name in
         ['build_artifacts.py', 'research_cards.py', 'research_interfaces.py', 'finalize_validation.py']}
code_changes = []


def replace_once(name, old, new, purpose):
    assert codes[name].count(old) == 1, (name, old)
    codes[name] = codes[name].replace(old, new)
    code_changes.append(dict(file=name, before=old, after=new, purpose=purpose))


def replace_call_arg(name, function, key_index, key, arg_index, value):
    tree = ast.parse(codes[name])
    candidates = [n for n in ast.walk(tree) if isinstance(n, ast.Call)
                  and isinstance(n.func, ast.Name) and n.func.id == function
                  and len(n.args) > key_index and isinstance(n.args[key_index], ast.Constant)
                  and n.args[key_index].value == key]
    assert len(candidates) == 1, (name, function, key)
    node = candidates[0].args[arg_index]
    literal = ast.get_source_segment(codes[name], node)
    # AST列号是UTF-8字节偏移；按节点位置替换，不能误改别处同值的setup或通用短字面量。
    lines = codes[name].splitlines(keepends=True)
    start = sum(len(line.encode('utf-8')) for line in lines[:node.lineno - 1]) + node.col_offset
    end = sum(len(line.encode('utf-8')) for line in lines[:node.end_lineno - 1]) + node.end_col_offset
    encoded = codes[name].encode('utf-8')
    assert encoded[start:end].decode('utf-8') == literal
    codes[name] = (encoded[:start] + repr(value).encode('utf-8') + encoded[end:]).decode('utf-8')
    code_changes.append(dict(file=name, function=function, key=key, argument_index=arg_index,
                             before=literal, after=repr(value), purpose='同步已批准字段的人工装配参数'))


obs_updates = {}
for item in proposal['changes']:
    path = item['json_path']
    if item['file'] == 'analysis.json' and path[0] == 'dimensions':
        row = before['analysis.json']['dimensions'][path[1]][path[2]]
        key = row['id'][4:]
        tail = path[3:]
        if tail == ['title']:
            obs_updates[(key, 2)] = item['proposed_after']
        elif tail == ['facts', 0, 'text']:
            obs_updates[(key, 3)] = item['proposed_after']
        elif tail == ['interpretation', 'text']:
            obs_updates[(key, 4)] = item['proposed_after']
        elif tail == ['limits_and_counterevidence']:
            obs_updates[(key, 5)] = item['proposed_after']
        elif tail in [['facts', 0, 'evidence'], ['interpretation', 'evidence'], ['evidence']]:
            # 三份证据只新增同一个精准章节，旧证据顺序保留。
            assert key == 'source-interface-anomalies'
            evidence = item['proposed_after']
            chapters = []
            for e in evidence:
                n = int(e['chapter_id'][3:])
                if n == 1383:
                    chapters.append((n, e['start_line'], e['end_line']))
                else:
                    chapters.append(n)
            obs_updates[(key, 6)] = chapters
        else:
            raise AssertionError(path)
for (key, arg_index), value in obs_updates.items():
    replace_call_arg('build_artifacts.py', 'obs', 1, key, arg_index, value)

for key, field, arg_index in [('li-xiaoyao', 'constraints', 4), ('frost', 'stage_change', 7),
                              ('xue-rou', 'relationship_directions', 5)]:
    card = next(c for c in after['cards.json'] if c['origin_key'].endswith('/' + key))
    replace_call_arg('research_cards.py', 'character', 0, key, arg_index, card['content'][field])
rain = next(c for c in after['cards.json'] if c['origin_key'].endswith('/rain-and-split'))
replace_call_arg('research_cards.py', 'scene', 0, 'rain-and-split', 5, rain['content']['obstacle'])
replace_call_arg('research_cards.py', 'scene', 0, 'rain-and-split', 7, rain['content']['consequence'])
replace_once('build_artifacts.py', 'def scene(key,title,order,arc,goal,obstacle,choice,consequence,why,chapters,characters=(),status=\'resolved\',knowledge=()):',
             "SCENE_TRANSFER={r['key']:r for r in json.loads((H/'scene-transfer-proposals-authored.json').read_text(encoding='utf-8'))}\n\n" +
             'def scene(key,title,order,arc,goal,obstacle,choice,consequence,why,chapters,characters=(),status=\'resolved\',knowledge=()):',
             '逐场使用已经主审的手写两字段，不再回退到通用模板。')
replace_once('build_artifacts.py', "applicability='需要让选择改变后续资源/知情/关系的长篇节点。',failure_mode='照抄人名道具或把局部成功写成全局零代价。'",
             "applicability=SCENE_TRANSFER[key]['applicability'],failure_mode=SCENE_TRANSFER[key]['failure_mode']",
             '58场景两字段人工数据接线。')
for key in ['soul-army', 'lanse-loss']:
    replace_call_arg('research_interfaces.py', 'edge', 0, key, 2, 'echo')
replace_once('research_interfaces.py', handoff_old, handoff_new, '流霜允留百龙骑的阶段边界与卡片同步。')
replace_once('finalize_validation.py', "'save_batch.py','finalize_validation.py']",
             "'save_batch.py','finalize_validation.py','scene-transfer-proposals-authored.json']",
             '把新增人工逐场数据列入重现输入SHA。')
replace_once('finalize_validation.py', "correction_records=['prefreeze-reference-corrections.json','prefreeze-reference-corrections-2.json']",
             "correction_records=['prefreeze-reference-corrections.json','prefreeze-reference-corrections-2.json','primary-review-applied-delta.json'],primary_review_revision=dict(status='approved_delta_applied_pending_final_signature',proposal_sha256='" + PROPOSAL_SHA + "',scene_proposals_sha256='" + SCENES_SHA + "',before_snapshot='review-corrections/before-primary/snapshot.json',primary_read_receipt='review-corrections/before-primary/vol06-primary-review-progress.json')",
             '保旧自核历史，记录主审已批准具体delta但最终签章尚待root。')
for name, code in codes.items():
    ast.parse(code)

# 在不落盘的候选定义中先核重现，防止边应用边发现装配有额外变化。
candidate_build = codes['build_artifacts.py']
candidate_build = candidate_build.replace("exec((H/'research_cards.py').read_text(encoding='utf-8'))", 'exec(__candidate_research_cards__)')
candidate_build = candidate_build.replace("exec((H/'research_interfaces.py').read_text(encoding='utf-8'))", 'exec(__candidate_research_interfaces__)')
candidate_module = dict(__file__=str(H / 'build_artifacts.py'), __name__='verify_candidate_definitions',
                        __candidate_research_cards__=codes['research_cards.py'],
                        __candidate_research_interfaces__=codes['research_interfaces.py'])
exec(compile(candidate_build, str(H / 'build_artifacts.py'), 'exec'), candidate_module)
assert candidate_module['D'] == after['analysis.json']['dimensions']
assert candidate_module['CHARACTERS'] + [c for _, c, _, _ in candidate_module['SCENES']] + candidate_module['PATTERNS'] == after['cards.json']
assert candidate_module['build_graph']() == after['graph.json']

for name, value in after.items():
    write_json(H / name, value)
(H / 'report.md').write_text(new_report, encoding='utf-8')
(H / 'handoff.md').write_text(new_handoff, encoding='utf-8')
for name, code in codes.items():
    (H / name).write_text(code, encoding='utf-8')

# 导入修改后的装配定义，不执行build()，核验可精确重现且无其他语义漂移。
module = runpy.run_path(str(H / 'build_artifacts.py'), run_name='verify_primary_revision_definitions')
assert module['D'] == after['analysis.json']['dimensions']
assembled_cards = module['CHARACTERS'] + [c for _, c, _, _ in module['SCENES']] + module['PATTERNS']
assert assembled_cards == after['cards.json']
assert module['build_graph']() == after['graph.json']
assert after['analysis.json']['character_states'] == [dict(origin_key=c['origin_key'], title=c['title'],
    summary=c['content']['summary'], stage_change=c['content']['stage_change'],
    identity_notes=c['content']['identity_notes'], claim_kind='synthesis', evidence=c['evidence']) for c in module['CHARACTERS']]

preserved_names = ['chapter-notes.jsonl', 'reader-state.json', 'read-log.json', 'chapter-unresolved-index.json']
preserved_hashes = {name: sha(H / name) for name in preserved_names}
assert all(digest == manifest['files'][name] for name, digest in preserved_hashes.items())
assert after['analysis.json']['chapter_unresolved_index'] == before['analysis.json']['chapter_unresolved_index']
assert len(after['analysis.json']['chapter_unresolved_index']) == 207
assert after['analysis.json']['chapter_unresolved_index'][0]['original_unresolved'] == []
assert sha(H / 'primary-review-proposal.json') == PROPOSAL_SHA
assert sha(H / 'scene-transfer-proposals.json') == SCENES_SHA
receipt = dict(status='approved_delta_applied_pending_final_signature',
               approval_basis='primary已完整读审23字段及58场景，明确消息批准按固定双SHA精确应用；本回执不代签最终卷审。',
               applied_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
               proposal_sha256=PROPOSAL_SHA, scene_proposals_sha256=SCENES_SHA,
               before_freeze_sha256=FREEZE_SHA, before_snapshot='review-corrections/before-primary/snapshot.json',
               json_changes=changes, text_changes=text_changes, assembly_code_changes=code_changes,
               invariants=dict(json_unchanged_outside_approved_paths=unchanged,
                               original_reading_files_same_sha256=preserved_hashes,
                               original_unresolved_index_rows=207, original_empty_volume_title_preserved=True,
                               all_scene_why_it_works_and_evidence_preserved=True,
                               assembly_definitions_reproduce_approved_dimensions_cards_graph_and_states=True,
                               proposal_files_still_match_approved_sha256=True),
               revised_output_sha256={name: sha(H / name) for name in ['analysis.json', 'cards.json', 'graph.json', 'report.md', 'handoff.md']},
               revised_code_sha256={name: sha(H / name) for name in codes}, application_script_sha256=sha(Path(__file__)))
write_json(H / 'primary-review-applied-delta.json', receipt)
md = ['# 卷六已批准修订实际delta', '', '按固定双提案SHA精确应用；旧十文件/清单/装配源已原样快照。最终卷审仍待primary核新SHA，不代签。', '',
      'JSON共139个批准路径（23定向字段＋58场景各2字段）；其余所有值逐值不变。原笔记、状态、日志和207行原未明索引保原SHA。', '']
for n, item in enumerate(changes, 1):
    md += [f"## {n}. {item['file']} / " + '.'.join(map(str, item['json_path'])), '',
           '原：' + json.dumps(item['before'], ensure_ascii=False), '',
           '现：' + json.dumps(item['proposed_after'], ensure_ascii=False), '']
md += ['## 可读报告及交接同步', '']
for item in text_changes:
    md += ['- ' + item['file'], '', '原：' + item['before'], '', '现：' + item['after'], '']
(H / 'primary-review-applied-delta.md').write_text('\n'.join(md), encoding='utf-8')
print(json.dumps(dict(json_changes=len(changes), scene_fields=116, other_json_values_unchanged=True,
                     reading_files_unchanged=preserved_hashes, delta_sha256=sha(H / 'primary-review-applied-delta.json'),
                     revised_output_sha256=receipt['revised_output_sha256']), ensure_ascii=False))
