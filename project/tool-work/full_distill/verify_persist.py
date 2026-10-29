"""在短路径隔离副本上检查第一集入库、重复运行和人工字段保护。"""
import copy
import json
from persist import ROOT, HERE, SID, check_report, save_volume
from fictionlib.vault import Vault
from fictionlib.exchange import backup, restore

report=json.loads((HERE/'vol01.json').read_text(encoding='utf-8'))
bad=copy.deepcopy(report)
bad['threads'][0]['event_keys']=[bad['threads'][0]['event_keys'][0]]
try:
    check_report(bad)
except AssertionError:
    pass
else:
    raise AssertionError('线程边界检查未拒绝损坏稿件')

target=ROOT/'distill-novels/.verify/d01'
archive=ROOT/'distill-novels/.verify/pre-deep.zip'
assert not target.exists() and not archive.exists(), '隔离目标已经存在，请使用新路径'
print(backup(Vault(ROOT/'writing-vault'),archive))
print(restore(archive,target))
v=Vault(target)
first=save_volume(v,report)
def assets():
    return {a['asset_id']:a for a in v.search()}
before=assets()
graph_before=(target/'library/sources'/SID/'plot-graph.json').read_bytes()
second=save_volume(v,report)
assert assets()==before, '重复运行改变了资产或人工字段'
assert (target/'library/sources'/SID/'plot-graph.json').read_bytes()==graph_before, '重复运行改变了图'
assert first['completed_segments']==12 and second['completed_segments']==12
print(json.dumps({'first':first,'idempotent':True,'bad_thread_rejected':True},ensure_ascii=False,indent=2))
