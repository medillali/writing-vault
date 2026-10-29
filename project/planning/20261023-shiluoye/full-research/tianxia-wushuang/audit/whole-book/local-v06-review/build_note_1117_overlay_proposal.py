"""冻结笔记错误只提出独立overlay；绝不改原notes、分卷或正式库。"""
from pathlib import Path
from copy import deepcopy
import hashlib,json,subprocess,sys
sys.stdout.reconfigure(encoding='utf-8')
HERE=Path(__file__).resolve().parent
WS=next(p for p in HERE.parents if (p/'writing-vault').is_dir())
BOOK=HERE.parents[2]
SID='src-d8926e2a35f04bcf8139cff0ea516bbd'
REV='d819f7d0ecf5a2004a0a434e987569bbe25015422d45e16676af913292346857'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def write(name,data): (HERE/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
paths=[BOOK/'vol06/chapter-notes.jsonl',BOOK/'vol06/prefix-chapter-notes.jsonl',BOOK/'vol06/batch-1117.json',
       WS/'writing-vault/library/reports/tianxia-wushuang/vol06-chapter-notes.jsonl']
before_file_hashes={p.relative_to(WS).as_posix():sha(p) for p in paths}
owned_before={p.name:sha(p) for p in HERE.glob('adjudications-local-v06-part*.json')}
assert len(owned_before)==11
source=WS/'writing-vault/private-sources/normalized/sources'/SID/(REV+'.txt')
assert sha(source)==REV
lines=source.read_text(encoding='utf-8-sig').splitlines()
assert '林逸欣怔了怔' in lines[90403-1] and '每天都去照顾妈妈' in lines[90403-1]
assert '我在旁笑道' in lines[90404-1] and '低250分' in lines[90407-1]
targets=[]
original_note=None
before_fact=None
for p in paths:
    if p.suffix=='.jsonl':
        rows=[json.loads(s) for s in p.read_text(encoding='utf-8-sig').splitlines()]
        i=next(i for i,r in enumerate(rows) if r.get('chapter_id')=='ch-1117')
        note=rows[i]
        locator=dict(format='jsonl',line=i+1,record_match={'chapter_id':'ch-1117'},field_pointer='/facts/0')
    else:
        data=read(p)
        i=next(i for i,r in enumerate(data['chapters']) if r.get('chapter_id')=='ch-1117')
        note=data['chapters'][i]
        locator=dict(format='json',record_match={'chapter_id':'ch-1117'},field_pointer=f'/chapters/{i}/facts/0')
    value=note['facts'][0]
    if before_fact is None:
        before_fact=value; original_note=deepcopy(note)
    assert value==before_fact
    targets.append(dict(path=p.relative_to(WS).as_posix(),sha256_before=sha(p),locator=locator,
                        expected_fact_sha256=hashlib.sha256(value.encode('utf-8')).hexdigest(),
                        role='formal_frozen_copy' if p.parts[-1]=='vol06-chapter-notes.jsonl' else 'staging_historical_copy'))
after_fact='L90389—90416逸逸自己拒绝与乱月同住，选择陪陆；乱月问林为何在苏州上大学，林逸欣自述离家近、可每天照顾妈妈；陆只附和即使清华录取也未必去，随后自述较清华分数线低250分。下午实际补同号SIM、买手机、挂失重办银行卡及购买衣物用品，未明确身份证已经补发。'
proposed_note=deepcopy(original_note)
proposed_note['facts'][0]=after_fact
assert all(original_note[k]==proposed_note[k] for k in original_note if k!='facts')
assert original_note['facts'][1:]==proposed_note['facts'][1:]
subprocess.run([sys.executable,str(HERE/'scan_note_1117_attribution.py'),'--save'],check=True)
scan=read(HERE/'note-1117-impact-scan.json')
assert scan['affected_physical_file_count']==4 and scan['owned_657_matching_candidate_count']==0
assert {x['path'] for x in scan['affected']}==set(before_file_hashes)
ev=dict(source_id=SID,revision=REV,chapter_id='ch-1117',start_line=90402,end_line=90407,claim_kind='fact',
        access_level='actual-full-raw-chapter-reread-by-this-agent',reader='/root/zongheng_vol05_full')
proposal=dict(schema_version='research-note-correction-overlay-proposal-v1',
    overlay_id='wushuang-note-1117-mother-attribution',
    status='proposal_pending_primary_approval_not_applied',
    correction_type='derived-reader-note-speaker-misattribution-not-novel-source-anomaly',
    owner='/root/zongheng_vol05_full',
    discovery_attribution='/root/zongheng_vol03_full定向原文核发话者并报primary；primary派本人完整复核。原错误记录由本人写成，本人承担派生纠错归属。',
    source_read_check={'reader':'/root/zongheng_vol05_full','chapter_id':'ch-1117','start_line':90388,'end_line':90480,
                       'complete_full_raw_read_this_pass':True,'truncated_pending':[],
                       'earlier_other_reader_check':{'reader':'/root/zongheng_vol03_full','start_line':90389,'end_line':90416,'scope':'targeted-source-lines-only-not-full-chapter'}},
    operation='explicit-reading-overlay-no-in-place-mutation',
    target_chapter_id='ch-1117',field='facts[0]',targets=targets,
    before_fact=before_fact,proposed_corrected_fact=after_fact,
    complete_canonical_note_before=original_note,complete_canonical_note_proposed_after=proposed_note,
    rationale='90402乱月问题指向林，90403林本人答为了每天照顾妈妈留苏州；90404陆只附和，90407差清华250分是陆自述。旧笔记把两位说话者压成陆一人，属于读者记录错误；不能因此增造陆母存活或其选校护理经历。',
    evidence=[ev],
    impact={'logical_fact_count':1,'physical_historical_copies':4,'owned_657_terminal_corrections_needed':[],
            'other_current_signed_semantic_research_corrections_found':[],
            'checked_scope':'无双全书暂存研究/审计与正式报告阅读页、关联林人物卡；657本地候选全量字符串；具体输入/命中在impact-scan。',
            'correct_existing_contexts':['卷3/4林逸欣人物卡护理母亲为正确归属','全书综合characters林的母亲护理动机归属正确','agent3本次核源记录已正确记为林'],
            'limit':'定向检索和命中项语义核对证明此次明确传播范围，不冒称重读所有其他卷原文或每份文件全部语义。'},
    suggested_reader_entry_notice='纠错优先：卷六raw1117旧逐章笔记误把为每天照顾母亲而在苏州上学归给陆尘；L90403实际为林逸欣自述，陆在L90404—90407仅附和并说自己距清华线低250分。请按本overlay理解该句，原冻结笔记保留为历史，不就地改写。',
    preservation=['原notes、prefix、batch、正式vol06复制均不改','原reader/read_at/full_text_read归属保留，新增回读单独列证','不改657终评、当前签组、原分卷分析/卡图、主池或正式库','最终由primary批准overlay后，唯一组装人复制入审计并在读者入口明确优先'],
    impact_scan='note-1117-impact-scan.json')
write('note-1117-mother-attribution-overlay-proposal.json',proposal)
md=['# raw1117照顾母亲主体纠错overlay提案','',
    '待primary核定，尚未应用。已完整回读raw1117 L90388—90480，无待补截断。原notes、分卷与正式库均未改。','',
    'L90402乱月问的是林逸欣为何在苏州上大学；L90403林逸欣本人答离家近、可每天照顾妈妈。L90404陆只附和即使清华录取未必去，L90407陆自述距清华分数线低250分。旧第一事实句误将选校照顾妈妈归给陆尘，是本人派生记录的说话者误配，不是小说异常。','',
    '**原句：** '+before_fact,'','**叠加更正句：** '+after_fact,'',
    '仅一个逻辑事实句有误，沿用到四份物理副本；不需要改657终评或当前现签语义对象。','',
    '| 冻结对象 | 指针 | 当前SHA256 |','|---|---|---|']
for t in targets: md.append(f"| {t['path']} | {t['locator']} | {t['sha256_before']} |")
md += ['',f"定向检索{scan['summary']['files_scanned']}份文件，{scan['summary']['files_with_semantic_string_hits']}份/{scan['summary']['string_hits']}条逻辑字符串命中并已完整核对；本代理657候选均无这类母亲护理/选校表述命中。正确的林护理母亲卡片、全书综合与agent3核源记录不修改。检索定位不冒充全书原文新增全文阅读。",'',
    '发现由agent3定点核源提出，primary派单；本人随后完整回读并承认原记录主体错误。原四份历史文件保持SHA，建议将本overlay独立冻结，在最终审计/人物/阅读入口明确其对1117第一事实句优先。','',
    '**建议读者入口文字：** '+proposal['suggested_reader_entry_notice'],'',
    '[完整before/proposed_after与四指针](note-1117-mother-attribution-overlay-proposal.json) · [影响检索记录](note-1117-impact-scan.json) · [结构与冻结SHA验证](note-1117-overlay-proposal-validation.json)']
(HERE/'note-1117-mother-attribution-overlay-proposal.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
assert before_file_hashes=={p.relative_to(WS).as_posix():sha(p) for p in paths}
assert owned_before=={p.name:sha(p) for p in HERE.glob('adjudications-local-v06-part*.json')}
validation=dict(status='passed',scope='proposal-structure-source-speaker-points-and-no-mutation-only',
    approval_status='pending-primary-not-fabricated',applied=False,
    target_logical_fact_count=1,target_physical_copies=4,
    full_raw_reread_completed=True,full_raw_reread_chapter='ch-1117',truncated_pending=[],
    original_notes_and_formal_copy_unchanged=True,owned_657_all_11_batches_unchanged=True,
    original_reader_and_read_at_preserved=True,only_proposed_fact_0_changed=True,
    owned_657_terminal_corrections_needed=[],
    output_sha256={n:sha(HERE/n) for n in ['note-1117-mother-attribution-overlay-proposal.json',
                     'note-1117-mother-attribution-overlay-proposal.md','note-1117-impact-scan.json']})
write('note-1117-overlay-proposal-validation.json',validation)
print(json.dumps(validation,ensure_ascii=False,indent=2))
