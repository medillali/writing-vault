"""仅实施主审两项定向修订，保留实际阅读笔记和其他字段。"""
import pathlib,json,hashlib,importlib.util
H=pathlib.Path(__file__).resolve().parent
old='神隐王子玛法奥之子/卡琳好友为本人话；导师迪背叛；主队明月/心救'
new='云栈·玛法奥为神隐城国王第五子（面板简介）；曾为卡琳珊好友由本人述；导师迪背叛；主队明月/心救'
for name in ['analysis.json','cards.json']:
 p=H/name;t=p.read_text(encoding='utf-8');assert t.count(old)==1;t=t.replace(old,new);p.write_text(t,encoding='utf-8')
p=H/'graph.json';t=p.read_text(encoding='utf-8');oldedge='"id": "v05-e09",\n      "from": "v05-well",\n      "to": "v05-stone",\n      "kind": "payoff"';assert t.count(oldedge)==1;t=t.replace(oldedge,oldedge.replace('"payoff"','"echo"'));p.write_text(t,encoding='utf-8')
oldline='- 云栈先被主北误称死'
newline='- 云栈·玛法奥为神隐城国王第五子（0875面板简介），曾为卡琳珊好友由本人述；不是“王子玛法奥之子”。云栈先被主北误称死'
p=H/'handoff.md';t=p.read_text(encoding='utf-8');assert t.count(oldline)==1;t=t.replace(oldline,newline);t+='\n主审定向修订：v05-e09井→石化边为echo，原标签保留；仅不同控制方法互照，不主张同物铺垫兑现。\n';p.write_text(t,encoding='utf-8')
p=H/'finalize_delivery.py';t=p.read_text(encoding='utf-8');assert t.count(oldline)==1;t=t.replace(oldline,newline);t=t.replace("handoff+=['', '完整源异常", "handoff+=['', '主审定向修订：v05-e09井→石化边为echo，原标签保留；仅不同控制方法互照，不主张同物铺垫兑现。', '', '完整源异常");p.write_text(t,encoding='utf-8')
spec=importlib.util.spec_from_file_location('volume_check',H.parents[1]/'check_volume.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
r=module.load_and_check('tianxia-wushuang',5)[-1]
p=H/'validation.json';v=json.loads(p.read_text(encoding='utf-8'));v.update(r);v['primary_targeted_corrections']=['云栈国王第五子/本人好友证词分层','v05-e09改echo且标签不变'];p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=H/'delivery-freeze.json';f=json.loads(p.read_text(encoding='utf-8'));f['files']={name:hashlib.sha256((H/name).read_bytes()).hexdigest() for name in f['files']};f['primary_targeted_corrections']=v['primary_targeted_corrections'];p.write_text(json.dumps(f,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'validation':r,'core_sha256':{name:f['files'][name] for name in ['analysis.json','cards.json','graph.json','handoff.md','validation.json']}},ensure_ascii=False))
