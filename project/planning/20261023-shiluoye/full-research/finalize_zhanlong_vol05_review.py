"""真实主审后独立重放卷五精准差分；哈希检查不产生文学阅读。"""
import copy,hashlib,json,sys,runpy
from datetime import datetime,timezone
from check_volume import ROOT,WORK,load_and_check,read
sys.stdout.reconfigure(encoding='utf-8')
S,V,P,A,C,G,M,R=load_and_check('zhanlong',5);B=P/'review-corrections/primary-before'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def objsha(o):return hashlib.sha256(json.dumps(o,ensure_ascii=False,sort_keys=True).encode()).hexdigest()
F=read(P/'freeze-manifest.json')
assert sha(P/'freeze-manifest.json')=='dd90b733d2d3cac54c2906259e17f1b0ac9ee8246f814e5511336c91644d4f26'
for group in ['core_sha256','support_sha256']:
 for n,h in F[group].items():assert sha(P/n)==h,n
for n,h in F['external_input_sha256'].items():
 q=ROOT/'writing-vault/library/reports'/n if n.startswith('collection/') else P/n
 assert sha(q)==h,n
for n,h in read(B/'snapshot.json')['core_sha256'].items():assert sha(B/n)==h,n
proposal=read(P/'primary-review-proposal.json')
assert sha(P/'primary-review-proposal.json')=='aad046aaea881c6801ed6c290d6a7b464eb90bdd7ad6abcb499ade105e6570fb'
expected={n:read(B/n) for n in ['analysis.json','cards.json','graph.json']}
for r in proposal['changes']:
 t=expected[r['file']]
 for k in r['path'][:-1]:t=t[k]
 assert t[r['path'][-1]]==r['before'];t[r['path'][-1]]=copy.deepcopy(r['after'])
for n,o in expected.items():assert o==read(P/n),n
for n in ['chapter-notes.jsonl','read-log.json','reader-state.json']:
 assert (B/n).read_bytes()==(P/n).read_bytes(),n
oldfreeze=read(B/'freeze-manifest.json')
assert sha(P/'handoff.md')==oldfreeze['support_sha256']['handoff.md']
report=(P/'report.md').read_bytes()
assert len(proposal['text_changes'])==1
for r in proposal['text_changes']:
 assert r['file']=='report.md' and report.count(r['after'].encode())==1
 report=report.replace(r['after'].encode(),r['before'].encode())
assert hashlib.sha256(report).hexdigest()==oldfreeze['support_sha256']['report.md']
for k in ['chapter_unresolved_index','chapter_source_anomaly_index','major_character_states']:
 assert read(B/'analysis.json')[k]==A[k],k
progress=read(P.parent/'vol05-primary-review-progress.json');coverage={}
for b in progress['batches']:
 n,key=b['section'].split('::');q=B/n if (B/n).exists() else P/n
 data=read(q)
 if key!='.':
  for k in key.split('.'):data=data[k]
 a,z=b['range'];assert objsha(data[a:z])==b['selected_sha256'],b['section']
 coverage.setdefault(b['section'],set()).update(range(a,z))
needed={**{'analysis.json::dimensions.'+k:5 for k in A['dimensions']},'cards.json::.':126,'graph.json::nodes':64,'graph.json::edges':44,'graph.json::threads':19,'analysis.json::open_questions':25,'analysis.json::unresolved_and_anomalies':19,'analysis.json::named_life_state_audit':18,'analysis.json::transferable_patterns':16,'analysis.json::literary_limits':4,'primary-review-proposal.json::changes':10,'primary-review-supplement-delta.json::changes':10,'primary-review-supplement-delta.json::text_changes':1}
for section,n in needed.items():assert coverage.get(section)==set(range(n)),section
by={c['origin_key']:c for c in C}
for r in A['major_character_states']:
 c=by[r['origin_key']]
 assert r==dict(origin_key=c['origin_key'],name=c['title'],summary=c['content']['summary'],stage_change=c['content']['stage_change'],relationships=c['content']['relationship_direction'],evidence=c['evidence'])
assert A['plot_and_hidden_threads']==G['threads']
assert not any(c.get('user_notes') or c.get('favorite') or c['review_status']!='draft' for c in C)
review={'source_id':S['source_id'],'revision':S['revision'],'volume':5,'reviewer':'primary','status':'reviewed_for_library_import','user_approval':False,'reviewed_at':datetime.now(timezone.utc).isoformat(),'scope':'完整逐项读45九维/126卡/64节点44边19线/25问题19异常18生死16摘要4限制、report全文37行和handoff41行；56人物阶段及19线是已读卡/图精确投影。本轮另全文复读1091—1094核武汉同场分区，不冒称primary个人整卷原文阅读。','review_groups':{'dimensions':45,'cards':126,'nodes':64,'edges':44,'threads':19,'major_character_states_exact_projection':56,'open_questions':25,'source_anomalies':19,'named_life_states':18,'transferable_patterns':16,'literary_limits':4,'approved_changed_objects':10,'approved_report_paragraph':1},'semantic_findings':[
'口授大执戈、正式仪式/界面、王准实际远征分时；军政能力不自动等资源产权，主屠民/替死/强迁责任不能由胜利清账。',
'ALLSTAR主八强/林冠军；会猎印度阵营赢主个人MVP；二战中国总胜而方MVP，帝国主权与葡临海公会各属不同层。',
'普通军部分系统恢复、凡书设施全部恢复与玩家80%经验各记；徐焰尸证不由泛恢复抹去，韩重伤起身与兰濒死救醒非死而无证复。',
'薛柔本人认抹/小妖/为爱后分步归会返现实；纸上画魅=薛景/薛柔堂妹，颜沫牛奶另人。撤原连续性事实纸为景堂妹之误，原稿保。',
'雷丁1125系统死亡，1126得铠复制后才六件重生；1151首次实复，后全五星与取魂的物料/交易/外交债分列，弗雷活剥后仍活返。',
'root完整原文1091—1094确认武汉同一现场南北分区，上海为小队籍属，唐林是上海队长不是唐琦/林成两人。北片普通持刀者与南片殖装分开，杭州队主轻伤不掩其他伤亡。',
'神威炮场撤误连现实王信的卡/图引用；五A只有一名日本活口已核，不扩大四死者国籍。布斯特样本和活口不等指汪司法结案。',
'现实阳炎已有，北辰观三日完善中阶/心眼火甲非首次突破；女友亲密与东无男友边界、母认可与莓本人充分同意分层。',
'安娜子舒击杀，银戈主末刀且NPC主要输出；群龙实际归城、尚未封龙神。1179戒千万只是竞价未落槌/净额/分款。',
'连续性五条改成当面认名、延迟实装、不同恢复风险、漂移阅读负担与局部收束接新期待；不是我们的建卡审计流程。事实和新增后证逐项核。'
],'delta_verification':{'approved_objects':10,'report_paragraphs':1,'all_other_values_exactly_equal':True,'reading_files_and_chapter_indices_unchanged':True,'proof':'独立从before重放获批proposal，与当前全JSON及完整文本相等。'},'preflight':R,'remaining':['按序等待卷4先正式，再导入5/6。','六卷正式后全部历史/局部候选逐项终审、36全书综合/人物弧、跨书管理及fresh完整备份实际恢复继续。'],'input_sha256':{**F['core_sha256'],**{n:h for n,h in F['support_sha256'].items() if '/' not in n},'freeze-manifest.json':sha(P/'freeze-manifest.json')}}
out=WORK/'zhanlong/review-vol05.json';out.write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':review['status'],'preflight':R,'review':str(out)},ensure_ascii=False))
