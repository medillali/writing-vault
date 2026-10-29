from character_arc_common import *
hits=json.loads((P/'luoxun-timing-string-hits.json').read_text(encoding='utf-8'));assert len(hits)==8
rows=[]
for x in hits:
 before=x['value'];assert before.count('999现场自刎')==1
 after=before.replace('999现场自刎','999被逼令自尽、1000现场自刎')
 rows.append({'path':x['path'],'sha256':x['sha256'],'field_path':x['field_path'],'before':before,'after':after,'issue_id':'luoxun-command-999-execution-1000','evidence':[ref(999,74070,74078),ref(1000,74083,74088)]})
ts=json.loads((P/'luoxun-terminal-timing-candidate-hits.json').read_text(encoding='utf-8'))
checked=[]
for x in ts:
 t=x['terminal'];assert 1000 in t['later_chapters'] and '1000' in t['rationale']
 checked.append({'pool':x['pool'],'candidate_id':x['candidate_id'],'adjudication_provenance':t['adjudication_provenance'],'finding':'终评已含1000且叙述分期或999—1000连续范围，没有把仅999当实死回执；不建议改此终评。'})
out={'status':'proposal-only-not-applied','source_id':S['source_id'],'revision':S['revision'],'actual_reviewer':'/root/zongheng_vol03_full','finding':'死亡事实不变，原部分阶段研究把999逼令提前写为现场自刎；实际自刎在raw1000 L74085。','actual_source_access':'本轮完整BEGIN-END实读raw999 L74019—74080与raw1000 L74081—74160，无截断；分工首次reader保持。','affected_fields':rows,'scan_scope':'正式六卷报告根与stage卷5顶层JSON/MD，再核洛洵canonical character/view；定位扫描后逐一完整读取8命中值。未宣全量脚本或所有历史快照语义重读。','terminal_pool_check':{'pool_sha256':{p.name:sha(p) for p in [A/'historical-question-pool.json',A/'local-question-pool.json']},'method':'只筛terminal_assessment中999与洛洵/自刎同现，8项逐项读完整rationale/later_chapters/later_evidence；原record不是待涂改终评。','matched_and_reviewed':checked,'affected_candidate_ids':[],'finding':'8个命中终评均已含1000，未发现只用999断现场死而缺1000的已合池终评。'},'original_notes':'原999四栏本来写章末未自刎，不改其原文或reader；1000笔记/原文相符。','limits':'只修8字段定位，不改变死亡、人物责任、原阶段证据数组与其他值，不写池/正式库/primary账。'}
f=P/'priority-luoxun-timing-proposal.json';dump(f,out)
md=['# 洛洵死亡时点最小外置提案','','999逼令，1000 L74085实际划颈倒地；死亡事实不变，原件未改。','']
for i,r in enumerate(rows,1):md += [f'## {i} {r["path"]}',str(r['field_path']),f'SHA {r["sha256"]}','',r['before'],'','→ '+r['after'],'']
md += ['# 已合池终评核对','','8命中均已含1000；affected_candidate_ids为空，不涂改正确终评。']+[x['candidate_id']+'：'+x['finding'] for x in checked]
f.with_suffix('.md').write_bytes(('\n'.join(md)).encode('utf-8'));print(sha(f),sha(f.with_suffix('.md')))
