"""只刷新主审纠错后的输入哈希，并给旧误读记录绑定历史快照。"""
import json,pathlib,hashlib,sys
sys.stdout.reconfigure(encoding='utf-8')
H=pathlib.Path(__file__).resolve().parent;R=H.parents[5]
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
formal='writing-vault/library/reports/tianxia-wushuang/vol07-analysis.json'
snapshot='writing-vault/library/reports/tianxia-wushuang/audit/research-corrections/v07-analysis-before-raw1305.json'
newsha=hashlib.sha256((R/formal).read_bytes()).hexdigest()
oldsha=hashlib.sha256((R/snapshot).read_bytes()).hexdigest()
assert newsha=='5aed431e426a75bd77361dbc110e0bad9173fc71825be36f259bfb05a556d48f'
cid='v07-local-unresolved_and_anomalies-003-01'
inventory=read(H/'input-inventory.json')
inventory['formal_input_sha256'][formal]=newsha
for x in inventory['inputs']:
 if x['volume']==7:x['analysis_sha256']=newsha
inventory['research_correction_snapshots']={snapshot:oldsha}
save(H/'input-inventory.json',inventory)
history=read(H/'historical-question-pool.json')
for x in history['inputs']:
 if x['volume']==7:x['analysis_sha256']=newsha
local=read(H/'local-question-pool.json')
x=next(x for x in local['candidates'] if x['candidate_id']==cid)
x['original_path']=snapshot;x['original_input_sha256']=oldsha
x['current_corrected_input']=dict(path=formal,sha256=newsha,correction='研究误读minutes已纠正为分盟规模口径；保候选原记录与ID作为纠错历史。')
# 保留历史包中各本地原记录；只给同一旧异常单列版本来源，不改其原文。
def link_old_record(obj):
 if isinstance(obj,dict):
  if obj.get('id')=='v07-a-assassin-duration' and 'description' in obj:
   obj['original_record_source']=dict(path=snapshot,sha256=oldsha)
   obj['current_corrected_input']=dict(path=formal,sha256=newsha)
  for k,v in list(obj.items()):
   if k not in ['original_record_source','current_corrected_input']:link_old_record(v)
 elif isinstance(obj,list):
  for v in obj:link_old_record(v)
link_old_record(history.get('local_issue_records',[]))
history['research_correction_snapshots']={snapshot:oldsha}
save(H/'historical-question-pool.json',history);save(H/'local-question-pool.json',local)
save(H/'v07-input-refresh-delta.json',dict(candidate_id=cid,old_snapshot=snapshot,old_snapshot_sha256=oldsha,new_formal=formal,new_formal_sha256=newsha,preserved='原候选文本/ID/索引及其他候选判断不变；仅本项原来源绑定旧快照。'))
print(json.dumps(dict(snapshot_sha256=oldsha,new_formal_sha256=newsha,candidate_id=cid),ensure_ascii=False))
