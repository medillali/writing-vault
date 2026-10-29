"""仅合成已实际阅过的分卷九维材料；不读取小说正文、不操作正式资料库。"""
import json,hashlib,copy,sys
from pathlib import Path
from datetime import datetime,timezone
sys.stdout.reconfigure(encoding='utf-8')
P=Path(__file__).parent;B=P.parent
def R(p):return json.loads(p.read_text(encoding='utf-8'))
def W(n,v):(P/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def text(x):return x.get('text',x) if isinstance(x,dict) else x
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
S=R(B/'source.json');seed=R(P/'synthesis-seed.json');included=[1,2,3,4,5]
stage={v:R(B/f'vol{v:02d}'/'analysis.json') for v in included}
states={v:R(B/f'vol{v:02d}'/'reader-state.json') for v in included}
assert all(states[v]['complete_volume'] for v in included)
names={'worldbuilding':'世界观与规则','characters':'人物与关系','plot':'情节组织','style':'语言与文风','narrative':'叙事与知识差','dialogue':'对话','pacing':'节奏','themes':'主题与价值张力','continuity':'连续性与阶段边界'}
dimensions={};materials=[];now=datetime.now(timezone.utc).isoformat()
for v in included:
 p=B/f'vol{v:02d}'/'analysis.json'
 materials.append(dict(volume=v,path=p.resolve().as_posix(),sha256=sha(p),source_reader=states[v]['reader'],original_read_by_synthesizer=(v==3),stage_material_read='九维全部条目的fact/inference、存在的mechanism/limits文本已分批完整显示并阅读；原证据引用继承，不冒称逐段复读他卷原文。',observations=sum(len(x) for x in stage[v]['dimensions'].values())))
for dimension,rows in seed.items():
 assert len(rows)==4
 out=[]
 for num,row in enumerate(rows,1):
  basis=[];ev_by={}
  for v,d,i in row['sources']:
   obs=stage[v]['dimensions'][d][i]
   p=B/f'vol{v:02d}'/'analysis.json';pointer=f'/dimensions/{d}/{i}'
   b=dict(volume=v,source_reader=states[v]['reader'],material_path=p.resolve().as_posix(),material_sha256=sha(p),json_pointer=pointer,observation_key=obs.get('key',obs.get('id',obs.get('title'))),source_fact=text(obs['fact']),basis_kind='original_full_text_and_stage_analysis' if v==3 else 'derived_stage_analysis_not_original_reread')
   basis.append(b)
   for original in obs['evidence']:
    e=copy.deepcopy(original)
    assert e.get('claim_kind') in {'fact','inference','synthesis','plan'}
    key=(e['source_id'],e['revision'],e['chapter_id'],e['start_line'],e['end_line'],e['claim_kind'])
    if key not in ev_by:
     e['research_material_attribution']=[];ev_by[key]=e
    origin=dict(volume=v,source_reader=states[v]['reader'],material_path=p.resolve().as_posix(),json_pointer=pointer+'/evidence',synthesizer_original_read=(v==3))
    if origin not in ev_by[key]['research_material_attribution']:ev_by[key]['research_material_attribution'].append(origin)
  out.append(dict(id=f'wushuang-book-{dimension}-{num:02d}',key=row['key'],title=row['title'],status='partial_waiting_vol06_vol07_vol08',fact=dict(claim_kind='fact',text=row['fact']),synthesis=dict(claim_kind='synthesis',text=row['synthesis']),literary_choice=dict(claim_kind='inference',take=row['take'],leave=row['leave'],approval='研究者取舍草案，未获用户批准'),stage_sources=basis,evidence=list(ev_by.values()),later_check=dict(claim_kind='plan',volumes=[6,7,8],question=row['later_check'])))
 dimensions[dimension]=out
covered=sum(v['body_units'] for v in S['volumes'] if v['volume'] in included)
package=dict(source_id=S['source_id'],revision=S['revision'],title='《网游之天下无双》全书九维综合草稿（卷一至五阶段版）',review_status='draft',status='partial_waiting_late_stage_materials',complete_book=False,full_book_synthesis_complete=False,included_volumes=included,pending_volumes=[6,7,8],stage_body_units_covered=covered,total_book_body_units=sum(v['body_units'] for v in S['volumes']),synthesizer='/root/zongheng_vol03_full',reading_attribution='综合者仅亲读卷三raw0229—0606；卷一、二、四、五采用各自原读者的完整研究条目，未宣称他卷原文亲读。卷六至八当前不纳入实质结论。',scope_note='36条为跨阶段观察骨架；条数齐备不代表全书材料齐备。末段须逐条补证、检验反例与改写，不机械拼接新增条目。',materials=materials,dimensions=dimensions,user_notes='',favorite=False,updated_at=now)
W('analysis.json',package)
W('basis-snapshot.json',dict(created_at=now,source_id=S['source_id'],revision=S['revision'],included_volumes=included,materials=materials))
W('stage-material-log.json',dict(status='stage_material_read_not_book_full_text_read',reader='/root/zongheng_vol03_full',included_volumes=included,entries=materials,additional_materials=[dict(volume=2,path=(B/'vol02'/'report.md').resolve().as_posix(),read_status='full_report_read',original_read=False),dict(volume=4,read_status='report_partial_output_not_counted_as_full;九维compact全部补读已完成'),dict(volume=5,read_status='report_partial_output_not_counted_as_full;九维compact全部补读已完成')],original_read_scope=dict(volume=3,raw_start='ch-0229',raw_end='ch-0606',segments=378,body_units=376),pending_full_stage_materials=[6,7,8]))
W('synthesis-state.json',dict(status='partial_waiting_late_stage_materials',complete_book=False,full_book_synthesis_complete=False,completed_skeleton_observations=36,included_volumes=included,pending_volumes=[6,7,8],next_actions=['主代理完成卷三修版冻结与正式导入后保持冻结包不动','待卷六至八完整analysis/cards/graph/handoff交付，逐卷阅读研究材料并记录归属','逐条补晚段证据/反例和终态，不把阶段未决提前判最终未解','输入发生文学修订时核hash与具体字段差异，刷新派生稿','九维最终36条及文学取舍交主审后，仍等用户判断而非自动成为个人风格'],updated_at=now))
lines=['# 《网游之天下无双》全书九维综合草稿：阶段版','',f'本稿实质材料范围为卷一至五（{covered}/1599正文的分卷研究材料），卷六、七、八未纳入完整结论。36条观察骨架已经齐备，但全书综合尚未完成。综合者仅亲读卷三378片/376正文，其余阶段依据原读者分卷九维，不冒称亲读他卷原文。','', '本稿把源事实、跨阶段解释、文学取舍和后续待核分开。每条在analysis.json保留原卷、原读者、文件SHA、JSON字段定位及继承的原文证据。继承证据表示来源可追溯，不表示本代理又逐段复读了他卷正文。全部为待审稿，用户尚未批准任何内容成为个人风格规则。','']
for dim,rows in dimensions.items():
 lines+=['## '+names[dim],'']
 for i,x in enumerate(rows,1):
  lines+=[f'### {i}. {x["title"]}','','已见事实：'+x['fact']['text'],'','综合解释：'+x['synthesis']['text'],'','取舍草案：保留'+x['literary_choice']['take']+' 舍弃或限制：'+x['literary_choice']['leave'],'','后段待检：'+x['later_check']['question'],'']
  refs=[]
  for b in x['stage_sources']:
   obs=stage[b['volume']]['dimensions'][b['json_pointer'].split('/')[2]][int(b['json_pointer'].split('/')[3])]
   cs=list(dict.fromkeys(e['chapter_id'] for e in obs['evidence']))
   refs.append(f"卷{b['volume']} {b['json_pointer']}（{b['source_reader']}；"+'、'.join(cs)+'）')
  lines+=['阶段依据：'+'；'.join(refs)+'。','']
lines+=['## 等待补齐的材料','', '卷六至八的阅读与分卷交付由原读者持续推进。本代理不取未读正文或零散索引代替完整阶段研究，也不使用纵横同名人物的冻结状态填补无双。待材料齐备后逐条检查：后段是否反证前五卷观察、最终代价是否保留、承诺与款项是否兑现、制度与城权如何实际结算、各人物是否有独立终态。','', '输入依赖以basis-snapshot.json为准；material-inventory.json是可更新现况，二者不可混为同一冻结版本。卷三修版已通过check_volume，后续正式导入由主代理处理，本稿不操作正式库。','']
(P/'report.md').write_text('\n'.join(lines),encoding='utf-8')
source_ch={x['chapter_id']:x for x in S['chapters']};refs=0
for dim,rows in dimensions.items():
 assert dim in names and len(rows)==4
 for x in rows:
  assert x['fact']['claim_kind']=='fact' and x['synthesis']['claim_kind']=='synthesis' and x['later_check']['claim_kind']=='plan'
  assert len({b['volume'] for b in x['stage_sources']})>=3
  for e in x['evidence']:
   ch=source_ch[e['chapter_id']]
   assert e['source_id']==S['source_id'] and e['revision']==S['revision']
   assert ch['start_line']<=e['start_line']<=e['end_line']<=ch['end_line']
   assert all(a['volume'] in included for a in e['research_material_attribution'])
   refs+=1
assert set(dimensions)==set(names) and sum(map(len,dimensions.values()))==36 and covered==1051
V=dict(status='local_draft_structure_passed',complete_book=False,full_book_synthesis_complete=False,included_volumes=included,pending_volumes=[6,7,8],dimensions={k:len(v) for k,v in dimensions.items()},inherited_evidence_references_checked=refs,attribution_checked=True,material_hashes_checked=True,vault_accessed=False,limitations=['未获完整卷六至八材料，不能称全书综合完成','其他读者原文证据继承自其阶段研究，综合者不冒称亲读','本地定位/结构通过不表示文学解释和取舍获用户批准'])
V['sha256']={n:sha(P/n) for n in ['analysis.json','report.md','stage-material-log.json','basis-snapshot.json','synthesis-state.json','synthesis-seed.json']};W('validation.json',V)
print(json.dumps({k:V[k] for k in ['status','included_volumes','pending_volumes','dimensions','inherited_evidence_references_checked']},ensure_ascii=False))
