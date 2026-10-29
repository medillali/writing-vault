"""仅构建本代理独立人物交叉复核；不写主池、人物组、分卷或正式库。"""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
WHOLE = HERE.parent
WORKSPACE = next(p for p in HERE.parents if (p / 'writing-vault').is_dir())
SOURCE_ID = 'src-d8926e2a35f04bcf8139cff0ea516bbd'
REV = 'd819f7d0ecf5a2004a0a434e987569bbe25015422d45e16676af913292346857'
SOURCE = WORKSPACE / 'writing-vault/private-sources/normalized/sources' / SOURCE_ID / (REV + '.txt')
source_lines = SOURCE.read_text(encoding='utf-8-sig').splitlines()

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write_json(name, data):
    (HERE / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def ev(raw, start, end, access='targeted-source-range-reread'):
    assert 1 <= start <= end <= len(source_lines)
    return dict(source_id=SOURCE_ID, revision=REV, chapter_id=f'ch-{raw:04d}',
                start_line=start, end_line=end, claim_kind='fact',
                access_level=access, reader='/root/zongheng_vol05_full')

# 本轮工具已完整返回全部人物散文和全部章行定位；仅省去每项重复的source/revision等元数据。
# group01最初后段截断已用11—12整条补读，不沿用截断片段作为完整阅读。
read_versions = {
    1: 'b5051394798319792f07900b9c71eeb84c024356eda14982a4ec0980cfd90a47',
    2: '217194710fc4f756e88e17ad66fbec2981c78e6c6c832edef7a50e9522ca959e',
    3: '225bbb3eddf30e8467fec86cc98aee5a3c6fd6e09eecde6e2c74cca3f3ad7087',
    4: '94f45bb3f786483c2c7f6eba07c1954a70b5fc9129ccc17d97ccb7db4a2687e5',
    5: 'adc3010fbf64dda7cbce28e248d62d3691a084737ae4fe72ba7aa43c55c23a03',
    6: '20388ae51ccf7b93416cb3a26878f843c9bdd6c4a1b37530ecac0b72e6376759',
    7: 'a3c9e10b6993853f1cf96adcf74a430c34a0e77968a5c35c65b32e20094aa733',
    8: '4919621fc8d7fc7a77d60cb9c236ddc0e8ec1b0764ef127957e67c3cb9524d35',
}
inputs = []
coverage = []
all_characters = {}
for group, expected in read_versions.items():
    path = WHOLE / f'character-arcs-part{group:02d}.json'
    assert sha(path) == expected, f'输入变化，须先定向补读：{path.name}'
    data = json.loads(path.read_text(encoding='utf-8-sig'))
    inputs.append(dict(path=path.relative_to(WORKSPACE).as_posix(), sha256=expected,
                       group=group, character_count=len(data['characters']),
                       read_scope='all-character-prose-and-evidence-locators'))
    for item in data['characters']:
        num = int(item['audit_id'].rsplit('-', 1)[1])
        assert num not in all_characters
        all_characters[num] = item
        coverage.append(dict(audit_id=item['audit_id'], name=item['name'], group=group,
                             record_read_complete=True,
                             result='new-later-evidence-omission-reported-and-owner-corrected' if num == 14
                             else 'no-new-substantive-correction-found-within-stated-cross-review-scope'))
assert sorted(all_characters) == list(range(1, 104))

p9 = WHOLE / 'character-arcs-part09.json'
data9 = json.loads(p9.read_text(encoding='utf-8-sig'))
selected9 = [x for x in data9['characters'] if 104 <= int(x['audit_id'].rsplit('-', 1)[1]) <= 109]
assert len(selected9) == 6
inputs.append(dict(path=p9.relative_to(WORKSPACE).as_posix(), sha256=sha(p9), group=9,
                   character_count_read=6, targeted_source_checked_ids=[105,107,109],
                   read_scope='104-through-109-character-prose-and-evidence-locators-plus-105-owner-delta'))

# 确证关键定位确含本轮已人工完整阅读的字面词。结构验证不代替语义判断。
for line, token in [(95482, '我就是喜欢陆尘'), (77771, '一个月内'),
                    (88905, '吻痕（中国）'), (88906, '吻痕（美国）'),
                    (97866, '保护伞公会的盟主'), (92616, '5000人'),
                    (93813, '铸剑师'), (90918, '职业是狩猎')]:
    assert token in source_lines[line-1], (line, token)

findings = [
    {
        'review_id': 'character-cross-01', 'audit_id': 'character-arc-14',
        'name': '晴空雪', 'kind': 'new-later-evidence-omission',
        'fields': ['costs', 'evidence_boundaries', 'evidence'],
        'reviewed_before': '爱慕主只十三话不能作她亲承。',
        'finding': '早期只有十三转述，不能覆盖1185晴空本人面对陆、李明确承认喜欢陆并拒李的后态。',
        'recommendation': '分记早转述与1185本人表明；仍不推陆已接受、正式情侣或排他承诺。',
        'evidence': [ev(1185,95471,95491,'full-raw-chapter-reread-this-pass')],
        'current_disposition': 'owner-already-applied-after-primary-semantic-approval',
        'owner_delta': (WHOLE/'character-qingkong-first-person-delta.json').relative_to(WORKSPACE).as_posix(),
        'discovery_attribution': '本代理独立发现并重新完整回读1185；primary确认有效，唯一组装人定向修改。'
    },
    {
        'review_id': 'character-cross-02', 'audit_id': 'character-arc-105',
        'name': '禹瞳', 'kind': 'primary-directed-contract-stage-verification',
        'fields': ['key_decisions','terminal_state','evidence_boundaries','evidence'],
        'reviewed_before': '终点没有专属转会/借法归还或爱菲林杖具体交付回执。',
        'finding': '943机场对话回忆已明确整批千法不必归还，交换一月内训练千名龙曜的新约且陆同意；旧归还义务不可仍当终点现约。',
        'recommendation': '整批去留新约已成交；千骑实交、禹个人入会手续与1262杖实交仍各自保未见特定回执，不能相互替代。',
        'evidence': [ev(943,77768,77775)],
        'current_disposition': 'owner-delta-applied-pending-primary-group-signature',
        'owner_delta': (WHOLE/'character09-loan-contract-delta.json').relative_to(WORKSPACE).as_posix(),
        'discovery_attribution': 'primary提出943核点，本代理完整读943正式四栏笔记并定向核原文；不是本人此前亲读卷五原章。'
    },
    {
        'review_id': 'character-cross-03', 'audit_id': 'character-arc-107',
        'name': '吻痕', 'kind': 'identity-confirmation-with-precise-citation',
        'fields': ['initial_comparison_stage','evidence_boundaries','evidence'],
        'finding': '现稿分无籍荷兰战士与中国165级刺客、美国192级战士正确，依据在1098，不是误套1209谁与争锋搜索。',
        'recommendation': '保分人语义；可补1098L88904—88909精准证据，避免只引1105之后而缺同名检索原定位。',
        'evidence': [ev(1098,88904,88911)],
        'current_disposition': 'confirmed-no-semantic-correction-needed',
        'discovery_attribution': 'primary定向提出身份疑问，本代理重核本人卷六原读位置。'
    },
    {
        'review_id': 'character-cross-04', 'audit_id': 'character-arc-107',
        'name': '吻痕', 'kind': 'later-office-state-supplement',
        'fields': ['key_decisions','terminal_state'],
        'finding': '现稿虽已有1219证据，人物散文未写吻痕已任保护伞盟主的明确后态。1199陆仍任盟主；1219已由叙述明确吻任盟主并驻黑海岸卫星驻地。',
        'recommendation': '补两个阶段：1199陆仍盟主、驻地计划进行；1219吻已盟主且驻地已成。两次明示之间不编交接镜头、准确日期或全员中国区资格恢复。现稿未相反断言，此为任职弧补录建议。',
        'evidence': [ev(1219,97865,97867)],
        'earlier_interface': {'chapter_id':'ch-1199','start_line':96444,'end_line':96451,
                              'access_level':'complete-derived-four-column-note-read',
                              'original_reader':'zongheng_vol05_full'},
        'current_disposition': 'reported-to-primary-and-owner-for-optional-targeted-supplement',
        'discovery_attribution': '本代理按职务时点专项提出；1219L97866本轮再次核原文。'
    },
    {
        'review_id': 'character-cross-05', 'audit_id': 'character-arc-109',
        'name': '莫娜／尼克职能排查', 'kind': 'function-attribution-confirmation',
        'fields': ['initial_comparison_stage','key_decisions','evidence_boundaries'],
        'finding': '莫娜确为弓箭手并统5000斥候营，后自明兼帝国铸剑师且实复图铸造；尼克确识食人花藤浆为白泽炬石材料并说自身职业狩猎。现稿未把二人互换。',
        'recommendation': '不因初见她持弓就删后期铸剑专长；若精确称职，可写黑铁骑兵团斥候营统帅、弓箭手兼帝国铸剑师。尼克的知识与职业狩猎并记，不擅造他是已能采集的制药者。',
        'evidence': [ev(1147,92615,92636),ev(1162,93808,93830),ev(1123,90916,90920)],
        'current_disposition': 'confirmed-no-semantic-correction-needed',
        'discovery_attribution': 'primary定向提出职能疑虑，本代理核本人卷六原读位置。'
    }
]

log = json.loads((HERE/'character-cross-read-log.json').read_text(encoding='utf-8'))
log.update(status='complete_read_only_cross_review', complete_character_record_ranges=[[1,103],[104,109]],
           truncated_pending=[], final_input_files=inputs,
           supplemental_reads=[{'type':'character-record','audit_id':'character-arc-14','reason':'owner-delta-applied完整补读'},
                               {'type':'owner-delta','path':'character09-loan-contract-delta.json','reason':'105 before/after完整读取'}])
log['additional_full_notes_read'] = [943,1123,1147,1162,1185,1199,1219,1290,1291]
log['source_ranges_read_this_pass'].append(dict(raw=1219,start_line=97861,end_line=97867,scope='targeted_range'))
log['known_fixes_excluded'].append('本轮已读63/93、69/88、81与94—99的修后条目，不将已知旧稿错误当新发现')
write_json('character-cross-read-log.json',log)

report = dict(
    title='无双人物组01—08独立只读交叉复核（附组09三项定向核对）',
    status='complete_independent_review_for_primary_and_sole_assembler',
    reviewer='/root/zongheng_vol05_full',
    scope={'main_character_records':103,'main_groups':list(range(1,9)),
           'ancillary_records_read':[104,105,106,107,108,109],
           'ancillary_targeted_source_checked_ids':[105,107,109]},
    provenance=log['provenance'],
    limits=[
        '完整读取本轮人物散文和章行定位不等逐条重读全部所引原章；新事实修正按下面实际原文范围和正式笔记归属列证。',
        '01—08除14外未发现新的实质纠错，不表示绝无其他错误或各人物全部资料已经穷尽。',
        '已知明宇/林浅、云栈、拾荒者、94—99定向修订由primary和唯一组装人处理，本专项去重，不改其文件。',
        '本专项不新增原子候选、不替代primary逐项主审、不改已签人物组、原分卷、主池或正式库。'
    ],
    input_files=inputs, coverage=coverage, findings=findings,
    result_counts={'new_independent_substantive_correction':1,
                   'primary_directed_substantive_correction_confirmed':1,
                   'later_office_supplement_suggestion':1,
                   'identity_or_function_confirmation':2},
    known_fixes_excluded=log['known_fixes_excluded'])
write_json('character-cross-review.json',report)

md = ['# 无双人物独立交叉复核','',
      '人物组01—08的103条已完整读完；组09前六条派生记录另完整读取，其中105/107/109按primary要求定向核原文。未改人物组、原子池、分卷或正式库。','',
      log['provenance'],'',
      '103条中独立新发现一处后证遗漏（晴空雪），已由唯一组装人经primary批准修正。禹瞳换约是primary提出的定向核点，已确认并有组装人delta。吻痕任职建议补录；两类身份/职能疑虑有原文依据，保现语义。','',
      '| 复核项 | 人物ID | 结论与建议 | 精确定位 |','|---|---|---|---|']
for f in findings:
    loc = '；'.join(f"raw{int(e['chapter_id'][3:]):04d} L{e['start_line']}—{e['end_line']}" for e in f['evidence'])
    md.append(f"| {f['review_id']} | {f['audit_id']} {f['name']} | {f['finding']} {f['recommendation']} | {loc} |")
md += ['', '晴空修后已经重新完整读取人物14；禹瞳delta的before/after已完整读取。组05/07/08既知修订、云栈与拾荒者后证不重复计新发现。','',
       '1199陆仍任保护伞盟主的前态来自本人原读及本轮完整复读的正式四栏笔记；1219后态本轮再核原文。943仅本轮定向原文范围核验，不冒称此前亲读卷五全章。1290/1291尾段由primary原读，本轮复读完整派生笔记确认两龙与战烛先存活后真死分层。','',
       '完整覆盖与输入SHA见[JSON](character-cross-review.json)，实际读取记录见[read-log](character-cross-read-log.json)。结构和定位检查见[validation](character-cross-validation.json)。结构检查不代替文学与事实主审。','',
       '| 输入组 | 条目完整读取数 | SHA256 |','|---|---:|---|']
for item in inputs:
    md.append(f"| {item['group']:02d} | {item.get('character_count',item.get('character_count_read'))} | {item['sha256']} |")
(HERE/'character-cross-review.md').write_text('\n'.join(md)+'\n',encoding='utf-8')

assert len(coverage) == 103 and len({x['audit_id'] for x in coverage}) == 103
assert not log['truncated_pending']
for f in findings:
    assert int(f['audit_id'].rsplit('-',1)[1]) in all_characters or f['audit_id'] in {x['audit_id'] for x in selected9}
    for e in f['evidence']:
        assert e['source_id'] == SOURCE_ID and e['revision'] == REV and e['claim_kind'] == 'fact'
for item in inputs:
    assert sha(WORKSPACE/item['path']) == item['sha256'], '读取期间人物输入变化，需重新锁定'
validation = dict(status='passed', validation_scope='independent-artifact-structure-and-source-locators-only',
                  main_record_count=103, main_record_ids_unique=True,
                  all_character_prose_read=True,truncated_pending=[], findings_count=len(findings),
                  findings_audit_ids_exist=True,evidence_ranges_in_current_source=True,
                  pinpoint_source_tokens_match=True,input_sha_unchanged_during_build=True,
                  semantic_approval='reserved-for-primary-not-fabricated',
                  output_sha256={n:sha(HERE/n) for n in ['character-cross-review.json','character-cross-review.md','character-cross-read-log.json']})
write_json('character-cross-validation.json',validation)
print(json.dumps(validation,ensure_ascii=False,indent=2))
