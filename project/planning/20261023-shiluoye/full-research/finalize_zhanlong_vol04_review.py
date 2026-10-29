"""全文主审后逐值重放获批差异；不据哈希制造阅读记录。"""
import copy, hashlib, json, sys
from datetime import datetime, timezone
from check_volume import WORK, load_and_check, read
sys.stdout.reconfigure(encoding='utf-8')
S,V,P,A,C,G,M,R=load_and_check('zhanlong',4)
B=P/'primary-delta/before'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def objsha(o):return hashlib.sha256(json.dumps(o,ensure_ascii=False,sort_keys=True).encode()).hexdigest()
F=read(P/'freeze-receipt.json')
for n,h in F['core_files'].items():assert sha(P/n)==h,n
assert sha(P/'validation.json')==F['validation_sha256']
receipt=read(P/'primary-delta/application-receipt.json')
for n,h in receipt['before_files'].items():assert sha(B/n)==h,n
proposal=read(P/'continuity-proposal/before-after.json')
assert sha(P/'continuity-proposal/before-after.json')=='1cb9ad3e1dc0c11616667fcbd1d78db314857fb58ff658c6d3d736d7fda5bee7'
assert receipt['proposal_sha256']==sha(P/'continuity-proposal/before-after.json')
assert len(receipt['deltas'])==6
expected={n:read(B/n) for n in ['analysis.json','cards.json','graph.json']}
for i,r in enumerate(receipt['deltas']):
 if i<4:
  q=proposal['changes'][i]
  assert r['before']==q['before'] and r['after']==q['after'] and q['id']==r['after']['id']
 elif i==4:
  q=read(P/'primary-extra-proposal.json')
  assert all(r[k]==q[k] for k in ['file','path','before','after'])
 else:
  assert r['file']=='cards.json' and r['origin_key'].endswith('/character/peier')
  assert r['path']==['content','relationships']
  assert r['before']=='洛克女、欧西姐妹；主敬护，徐翊统军属她。'
  assert r['after']=='洛克之女、西奥多与欧恩之妹；主敬护，徐翊在其南征统下任元帅。'
 t=expected[r['file']]
 if 'origin_key' in r:t=next(c for c in t if c['origin_key']==r['origin_key'])
 for k in r['path'][:-1]:t=t[k]
 assert t[r['path'][-1]]==r['before'];t[r['path'][-1]]=copy.deepcopy(r['after'])
delta=read(P/'primary-delta/equipment-edge-delta.json')
assert sha(P/'primary-delta/graph.before-equipment-edge.json')==sha(B/'graph.json')
old=next(e for e in expected['graph.json']['edges'] if e['id']=='e-equipmentshield')
new=next(e for e in read(P/'graph.json')['edges'] if e['id']=='e-equipmentshield')
assert delta['before']==old and delta['after']==new
assert new['from']==old['from']=='s-deer' and new['to']=='s-riverwar' and new['kind']==old['kind']=='payoff'
assert new['label']=='761英雄盔实戴，778/781免晕在敌控中实际验证；不是持有即全程无伤。'
assert [e['chapter_id'] for e in new['evidence']]==['ch-0761','ch-0778','ch-0781']
expected['graph.json']['edges']=[new if e['id']==new['id'] else e for e in expected['graph.json']['edges']]
for n,o in expected.items():assert o==read(P/n),n
for n in ['chapter-notes.jsonl','read-log.json','handoff.md']:assert (B/n).read_bytes()==(P/n).read_bytes(),n
oldstate=read(B/'reader-state.json');newstate=read(P/'reader-state.json')
for keys,oldvalue,newvalue in [
 (['status'],'full-volume-read-artifacts-pending','full-volume-artifacts-complete-awaiting-primary-review'),
 (['current_state','coverage'],'754—968=215片214正文全部逐章实读/055批全部保存，next null零截断；研究产物尚未完成。','754—968=215片214正文全部逐章实读/055批全部保存，next null零截断；本地研究整包已齐，文学审查/用户审美另层。'),
 (['current_state','next_work'],'不取969及后文，不写其他卷；完整复读本卷canonical四栏并整理9维/人物场景机制/图/全unresolved索引/源异常/报告交接校验待审稿。','全卷draft研究/报告/交接/本地验证已齐，primary独立文学审查后决定正式导入；不取969以后、不自行导库或提前终点审计。')]:
 t=oldstate;u=newstate
 for k in keys[:-1]:t=t[k];u=u[k]
 assert t[keys[-1]]==oldvalue and u[keys[-1]]==newvalue
 t[keys[-1]]=newvalue
assert oldstate==newstate,'阅读状态仅允许产物完成的三项元信息变化'
progress=read(P.parent/'vol04-primary-review-progress.json');coverage={}
for b in progress['batches']:
 n,key=b['section'].split('::');q=B/n if (B/n).exists() else P/n
 assert sha(q)==b['input_sha256'],n
 data=read(q)
 if key!='.':
  for k in key.split('.'):data=data[k]
 a,z=b['range'];assert objsha(data[a:z])==b['selected_sha256'],b['section']
 coverage.setdefault(b['section'],set()).update(range(a,z))
needed={**{'analysis.json::dimensions.'+k:4 for k in A['dimensions']},'cards.json::.':104,'graph.json::nodes':54,'graph.json::edges':39,'graph.json::threads':20,'analysis.json::source_anomalies':32,'analysis.json::unresolved_volume_end':19,'analysis.json::transferable_patterns':12,'continuity-proposal/before-after.json::changes':4}
for k,n in needed.items():assert coverage.get(k)==set(range(n)),k
by={c['title']:c for c in C if c['asset_type']=='character'}
for r in A['stage_characters']:
 c=by[r['name']];assert r['stage_change']==c['content']['stage_change'] and r['evidence']==c['evidence']
assert A['threads']==read(P/'graph.json')['threads']
review={'source_id':S['source_id'],'revision':S['revision'],'volume':4,'reviewer':'primary','status':'reviewed_for_library_import','user_approval':False,'reviewed_at':datetime.now(timezone.utc).isoformat(),'scope':'逐项完整主审36九维、104卡、54节点39边20线、32异常19卷末问题12机制摘要；report全文1100行与handoff全文。45人物阶段与20线是已读卡/图精确投影。不是primary个人整卷原文阅读，逐章历史疑点留全书终审。','review_groups':{'dimensions':36,'cards':104,'nodes':54,'edges':39,'threads':20,'stage_characters_exact_projection':45,'source_anomalies':32,'volume_end_questions':19,'transferable_patterns':12,'approved_continuity_objects':4,'approved_other_fields':2,'approved_edge':1},'semantic_findings':[
'军职/统兵cap/编制批准/实到兵数分别记录，死亡、伤兵、补员与战报口径不能用总数相抵。',
'兰馨活返、剿盗任务完成、俘兵五千被杀等分别回答不同承诺；护弱愿望不能洗去明确失败和主动舍救。',
'843主重创昏迷后844醒与雷现实死亡、唐琦救月分开；主当时已有阳炎，师父林成活归不等父母失踪已解。',
'佩儿是西奥多/欧恩之妹；徐翊/佩儿死亡不由占双城抵消，临海中国王权、印度居留、系统委托及税额各属不同层。',
'抹茶夺城杀友是实际行动；方召回不自动证明每步命令，915行动/916舞揭名林释亲缘/960堂姐妹与946爱主推测分开，956主修正强逼说。',
'两把蝴蝶不同币种与工序，现实10万材料款/926剑到，游戏957龙池重铸；968原镇国刀比较疑误称，主武实际蝴蝶/镇岳。',
'罗鼎破甲/拘逃/池三剑与主末刀分功；英雄盔761实戴、778/781免晕实效，纠正原图把装备所得与后续实用误接。',
'连续性四项改为旧物后用、死者缺席留代价、身份揭露重估关系、承诺不同回声的实际叙事机制；不把我们的研究管理流程当原作技巧。',
'兰馨非813已死少女；魏854保释与959仍羁押留源差，百里伦两死保异常，不能自造再捕或复活。',
'矿战尚未定权、刺杀魔山失败、最高酒未制、寻薛柔未回、主父母未明等按卷末保存，待全书后证终审。'
],'delta_verification':{'approved_continuity_objects':4,'approved_anomaly_description':1,'approved_character_relationship':1,'approved_edge':1,'all_other_research_values_exactly_equal':True,'chapter_notes_read_log_handoff_byte_unchanged':True,'reader_state_metadata_changes':3,'reader_state_coverage_and_other_values_unchanged':True},'preflight':R,'remaining':['依次正式保存4/5/6后，全候选终审、全书综合/人物弧、跨书管理与fresh全量备份实际恢复。'],'input_sha256':{**F['core_files'],**{n:sha(P/n) for n in ['read-log.json','reader-state.json','chapter-notes.jsonl','freeze-receipt.json']}}}
out=WORK/'zhanlong/review-vol04.json';out.write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':review['status'],'preflight':R,'review':str(out)},ensure_ascii=False))
