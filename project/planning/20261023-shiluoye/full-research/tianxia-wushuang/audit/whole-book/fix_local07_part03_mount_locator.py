"""仅纠正已签075-03的实骑后证定位，保留其余59条。"""
import copy, hashlib, json, pathlib
H=pathlib.Path(__file__).resolve().parent
p=H/'adjudications-local-v07-part03.json'
before_bytes=p.read_bytes(); before=json.loads(before_bytes)
assert hashlib.sha256(before_bytes).hexdigest()=='2417135fbe6e8b1f6c77117831ae75c15fb52f53da8d8e1396644db396eb4ac0'
after=copy.deepcopy(before)
old=next(x for x in before if x['candidate_id']=='v07-local-local_historical_questions-075-03')
new=next(x for x in after if x['candidate_id']==old['candidate_id'])
new['rationale']='1407北已实骑火麒麟并控制维助队友脱围，1368火麒麟蛋赠北并绑定到骑乘有明确后证；1389没有实骑场面，不能用该章补成长过程。1514换火凰是另一坐骑，不能据此说火麟从没骑过。'
new['later_chapters']=[1368,1407,1514]
assert sum(a!=b for a,b in zip(before,after))==1
(H/'reviewed-batches'/'adjudications-local-v07-part03-before-mount-locator.json').write_bytes(before_bytes)
p.write_text(json.dumps(after,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
sha=hashlib.sha256(p.read_bytes()).hexdigest()
delta={'candidate_id':old['candidate_id'],'before_sha256':hashlib.sha256(before_bytes).hexdigest(),'after_sha256':sha,'unchanged_other_items':59,'reason':'完整重读raw1389无实骑场面；raw1407四栏记录明确北骑火麟控维。状态不变，仅纠正独立终点判断后证。','before':old,'after':new}
(H/'local07-part03-mount-locator-delta.json').write_text(json.dumps(delta,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
md=H/'local-v07-reviewed-part03.md'
text=md.read_text(encoding='utf-8').replace(old['rationale'],new['rationale']).replace('后证raw：1368, 1389, 1514','后证raw：1368, 1407, 1514')
md.write_text(text,encoding='utf-8')
builder=H/'write_local07_part03.py'
text=builder.read_text(encoding='utf-8').replace(old['rationale'],new['rationale']).replace('[1368,1389,1514]','[1368,1407,1514]')
builder.write_text(text,encoding='utf-8')
print(sha)
