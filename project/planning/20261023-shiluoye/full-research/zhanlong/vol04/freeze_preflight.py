"""最终分卷校验/冻结；仅本隔离目录写入，不导库。"""
import json,hashlib,sys,runpy,re,collections
from pathlib import Path
P=Path(__file__).parent
def load(f):return json.loads((P/f).read_text(encoding='utf-8'))
def save(f,x):(P/f).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(f):return hashlib.sha256((P/f).read_bytes()).hexdigest()
# 不重跑builder，保护primary已经逐项阅读的其他语义。
assert load('continuity-proposal/application-receipt.json')['status']=='applied-primary-approved'
state=load('reader-state.json');before=(P/'reader-state.json').read_bytes()
assert state['complete'] and state['next_chapter_id'] is None and not state['pending_truncations']
assert state['read_raw_fragments']==215 and state['read_body_units']==214
if not (P/'reader-state.before-artifacts.json').exists():(P/'reader-state.before-artifacts.json').write_bytes(before)
state['status']='full-volume-artifacts-complete-awaiting-primary-review'
state['current_state']['next_work']='全卷draft研究/报告/交接/本地验证已齐，primary独立文学审查后决定正式导入；不取969以后、不自行导库或提前终点审计。'
state['current_state']['coverage']='754—968=215片214正文全部逐章实读/055批全部保存，next null零截断；本地研究整包已齐，文学审查/用户审美另层。'
save('reader-state.json',state)
runpy.run_path(str(P/'self_audit.py'))
runpy.run_path(str(P/'write_report.py'))
sys.path.insert(0,str(P.parent.parent))
from check_volume import load_and_check
result=load_and_check('zhanlong',4)[-1]
missing=[]
for f in ['report.md','handoff.md']:
 for target in re.findall(r'\]\(([^)]+)\)',(P/f).read_text(encoding='utf-8')):
  if not target.startswith(('http:','https:','#')) and not (P/target.split('#')[0]).exists():
   # validation为本脚本随后生成。
   if target!='validation.json':missing.append([f,target])
assert not missing,missing
A=load('analysis.json');C=load('cards.json');G=load('graph.json')
assert len(C)==104 and len(G['nodes'])==54 and len(G['edges'])==39 and len(G['threads'])==20
assert all(c['content']['claim_kind'] in ['inference','synthesis'] for c in C)
files=['analysis.json','cards.json','graph.json','read-log.json','chapter-notes.jsonl','reader-state.json','report.md','handoff.md','reading-attribution.json','self-audit.json']
v={'status':'passed-awaiting-primary-literary-review','source_id':A['source_id'],'revision':A['revision'],'volume':4,'read_only_preflight':result,'coverage':{'expected_raw':215,'read_raw':215,'body':214,'full_text_reading_reader':'/root/zongheng_vol03_full','batches':55,'unresolved_truncations':0},'literary_review':{'reviewer':'primary','status':'in-progress-not-fabricated-complete','note':'已预审九维/正在审其他核心；精确连续性提案另有应用回执。此文件不替primary独立签收。'},'user_evaluation':None,'local_links':'passed','self_audit':'self-audit.json','files':{f:{'sha256':sha(f),'bytes':(P/f).stat().st_size} for f in files},'no_formal_import_performed':True}
save('validation.json',v)
save('freeze-receipt.json',{'status':'draft-frozen-for-primary-review','validation_sha256':sha('validation.json'),'core_files':{f:sha(f) for f in ['analysis.json','cards.json','graph.json','report.md','handoff.md','validation.json']},'warning':'冻结后不重跑builder；若primary定向修改，保before/精确delta，复验后新freeze接续。'})
save('research-checkpoint.json',{'status':'full-volume-draft-frozen-awaiting-primary','observations':36,'cards':dict(collections.Counter(c['asset_type'] for c in C)),'graph':{'nodes':54,'edges':39,'threads':20,'knowledge':27},'coverage':{'raw':215,'body':214,'complete':True},'next_work':'交primary逐项主审/顺序导入；不提前启动local终评/全书综合。'})
print(json.dumps({'validation_sha256':sha('validation.json'),'files':load('freeze-receipt.json')['core_files'],'preflight':result},ensure_ascii=False))
