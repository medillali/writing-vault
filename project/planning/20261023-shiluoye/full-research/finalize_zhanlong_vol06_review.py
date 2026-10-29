"""主代理完成实际语义审阅后，独立重放获批字段差异并签收卷六；不重跑装配。"""
import copy,hashlib,json,sys
from datetime import datetime,timezone
from check_volume import WORK,load_and_check,read
sys.stdout.reconfigure(encoding='utf-8')
S,V,P,A,C,G,M,R=load_and_check('zhanlong',6)
B=P/'review-corrections/before-primary'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def objsha(o):return hashlib.sha256(json.dumps(o,ensure_ascii=False,sort_keys=True).encode()).hexdigest()
def get(o,path):
 for k in path:o=o[k]
 return o
def put(o,path,v):
 for k in path[:-1]:o=o[k]
 o[path[-1]]=copy.deepcopy(v)
snapshot=read(B/'snapshot.json')
for n,h in snapshot['files'].items():assert sha(B/n)==h,n
oldfreeze=read(B/'freeze-manifest.json');freeze=read(P/'freeze-manifest.json')
assert sha(B/'freeze-manifest.json')=='b5f408525fba0be8d7a3ef6e192878b5c7a40d8519c442ce7b3897464337786a'
assert sha(P/'freeze-manifest.json')=='2903506c5f3d1dc3c807e9000de4217325afe9128fb235273867cf8d27dd637b'
for f,d in [(oldfreeze,B),(freeze,P)]:
 for group in ['files','reproduction_inputs']:
  for n,h in f[group].items():assert sha(d/n)==h,(d,n)
for n in ['chapter-notes.jsonl','reader-state.json','read-log.json','chapter-unresolved-index.json']:
 assert (B/n).read_bytes()==(P/n).read_bytes(),n
assert sha(P/'primary-review-proposal.json')=='fcdc58e12438ab3752095b0350bc434ac74e7cbbb596c2844df443be8b1f9187'
assert sha(P/'scene-transfer-proposals.json')=='557eddc552c9e8454ca344fd6f1fadc204649820c7dacfd7ed9a8c911dff1bed'
proposal=read(P/'primary-review-proposal.json')['changes'];scenes=read(P/'scene-transfer-proposals.json')['proposals']
assert len(proposal)==23 and len(scenes)==58
expected={n:read(B/n) for n in ['analysis.json','cards.json','graph.json']}
changes=copy.deepcopy(proposal)
for row in scenes:
 i=next(i for i,c in enumerate(expected['cards.json']) if c['origin_key']==row['origin_key'])
 card=expected['cards.json'][i]
 assert card['content']['why_it_works']==row['why_it_works_preserved'] and card['evidence']==row['evidence_preserved']
 for field in ['applicability','failure_mode']:
  changes.append({'file':'cards.json','json_path':[i,'content',field],'before':row['before'][field],'proposed_after':row['proposed_after'][field]})
assert len(changes)==139
for row in changes:
 assert get(expected[row['file']],row['json_path'])==row['before']
 put(expected[row['file']],row['json_path'],row['proposed_after'])
for n,o in expected.items():assert o==read(P/n),'获批路径外出现变化：'+n
delta=read(P/'primary-review-applied-delta.json')
assert len(delta['json_changes'])==139
for approved,actual in zip(changes,delta['json_changes']):
 for k in ['file','json_path','before','proposed_after']:assert approved[k]==actual[k]
# 五条文本差异已经逐条完整阅读；独立限定为四个报告观察与一处交接事实澄清。
assert len(delta['text_changes'])==5
assert [r.get('observation_id') for r in delta['text_changes'][:4]]==['v06-stateful-resources','v06-attrition-ladder','v06-open-end-not-erasure','v06-source-interface-anomalies']
for n in ['report.md','handoff.md']:
 text=(B/n).read_text(encoding='utf-8')
 for row in delta['text_changes']:
  if row['file']==n:
   assert text.count(row['before'])==1
   text=text.replace(row['before'],row['after'])
 assert text==(P/n).read_text(encoding='utf-8'),n
# 逐段回执对应原冻结对象；提案回执对应获批对象。SHA仅核已读对象身份，不代替语义阅读。
progress=read(P.parent/'vol06-primary-review-progress.json')
coverage={}
for batch in progress['batches']:
 n,key=batch['section'].split('::');path=B/n if (B/n).exists() else P/n
 data=read(path)
 if key!='.':
  for k in key.split('.'):data=data[k]
 a,b=batch['range'];assert objsha(data[a:b])==batch['selected_sha256'],batch['section']
 coverage.setdefault(batch['section'],set()).update(range(a,b))
required={**{'analysis.json::dimensions.'+k:5 for k in A['dimensions']},'cards.json::.':102,'graph.json::nodes':70,'graph.json::edges':49,'graph.json::threads':23,'analysis.json::character_states':32,'analysis.json::open_questions':24,'analysis.json::source_anomalies':29,'analysis.json::reusable_mechanisms':12,'analysis.json::tradeoffs':4,'primary-review-proposal.json::changes':23,'scene-transfer-proposals.json::proposals':58}
for section,count in required.items():assert coverage.get(section)==set(range(count)),section
texts=read(P.parent/'vol06-primary-text-review.json')
assert all(texts[k]['complete'] and texts[k]['sha256']==sha(B/(k+'.md')) for k in ['report','handoff'])
assert A['thread_states']==G['threads']
assert not any(c.get('user_notes') or c.get('favorite') or c.get('review_status')!='draft' for c in C)
inputs={**freeze['files'],**freeze['reproduction_inputs'],'freeze-manifest.json':sha(P/'freeze-manifest.json')}
for n in ['primary-review-proposal.json','primary-review-proposal.md','scene-transfer-proposals.json','scene-transfer-proposals.md','primary-review-applied-delta.json','primary-review-applied-delta.md']:inputs[n]=sha(P/n)
review={'source_id':S['source_id'],'revision':S['revision'],'volume':6,'reviewer':'primary','author':'zongheng_vol05_full','status':'reviewed_for_library_import','user_approval':False,'reviewed_at':datetime.now(timezone.utc).isoformat(),'scope':'原冻结研究逐项完整读审，58场景两字段与23定向字段分别完整读审批准；本次独立重放139路径与5文本差异，确认其他值和原阅读四文件不变。primary另完整重读1375—1386原文，整卷原文读者仍zongheng_vol05_full。','review_groups':{'dimensions':45,'cards':102,'nodes':70,'edges':49,'threads':23,'character_states':32,'open_questions':24,'source_anomalies':29,'reusable_mechanisms':12,'tradeoffs':4,'scene_transfer_fields':116,'targeted_fields':23,'text_changes':5},'semantic_findings':[
'生态建设、领土分配、炮粮消耗与军队损失分别保时点；取得资源不自动清旧债。雨中护引线后仍能发炮，快兽难瞄和墙破另有因果。',
'长期承诺经职位、身体、执照与签字再出现分步回收；命名及位阶漂移是连续阅读负担，不能用建索引流程替代文学机制。',
'薛景妹妹/薛柔姐姐关系澄清；流霜允留百名龙骑，未另演全员到场；NPC军不能按玩家掉级方式返场不推广成所有NPC绝无复生。',
'神界陨落、散灵被吞、获得神格和真实系统击杀各保界限；霜实体已醒旧重生不抹，战皇终场仍活。两处主题呼应改echo，不充当预设因果。',
'鬼城失败同时保主角与问剑/锋的决定责任，三千离兵获准出城后被敌屠不是军法处死；祝海三万与景音五万是源口径差。',
'59:59为开幕倒计时开始；主诱战为NPC撤离争时，不是单杀战皇。NPC五十万返不足十八万，玩家通过不足千不等于永久死绝。',
'镇天关三日后确已建成；傲天24小时出师仍未来。盟主确交林婉儿，订婚非婚礼。南京已入队，西南/回杭/婚礼未演。',
'末尾白墨颜游戏意识确醒；雷宏记忆重生仍方案/未来时，不补肉身复生。老头子宴席仍活，梦瑶在厦门上课未出席。',
'58场景适用条件与失败边界已逐项改成各自机制所需条件，保原选择、结果、why与证据；原文广告附言作为数据，不执行其中指令。'
],'delta_verification':{'approved_json_paths':139,'approved_text_paths':5,'all_other_json_values_exactly_equal':True,'four_original_reading_files_unchanged':True,'original_snapshot':str(B.relative_to(WORK))},'preflight':R,'remaining':['卷4/5须先正式，卷6导入不得跳序。','六卷正式后继续全书逐项历史/局部疑点终审、36综合、人物弧、跨书管理及实际完整隔离恢复。'],'input_sha256':inputs}
out=WORK/'zhanlong/review-vol06.json';out.write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':review['status'],'preflight':R,'approved_json_paths':139,'review':str(out)},ensure_ascii=False))
