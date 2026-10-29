"""重放连续性稳定组已批准的三处澄清，不重写任何研究对象。"""
from pathlib import Path
import copy, difflib, hashlib, json
P=Path(__file__).resolve().parent/'zhanlong/audit/whole-book/reader3-review'
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
proposal=P/'synthesis-continuity-two-boundaries-proposal.json'
assert sha(proposal)=='4abaac2c3c3eb6936bedad334c932da0899b94f97cdb66b3a35af75bc0cec8ab'
p=read(proposal); d=read(P/'synthesis-continuity-approved-boundaries-delta.json')
old=P/'synthesis-continuity-before-approved-boundaries.json'; new=P/'synthesis-continuity.json'
assert sha(old)==d['before_json_sha256']=='f023af8e3fd40bc83cf8b67625d803fcaeaf667d13feac821e2207bedab4c3d2'
assert sha(new)==d['after_json_sha256']=='ed1b98830e1d6c85d80079970b08ee70e611559ef091d55ebe1da326e6713393'
expected=read(old); before=expected['rows'][0]; assert before==p['before']==d['before']
after=copy.deepcopy(before)
after['fact_summary']=before['fact_summary'].replace('后期镇国刀用于求援','末期命人取镇国刀求援')
boundary=p['after']['supporting_observations'][3]['reported_fact_boundary']
assert 'reported_fact_boundary' not in after['supporting_observations'][3]
assert '尚余9小时17分' in boundary['text'] and '不是等满十小时才转手' in boundary['text']
after['supporting_observations'][3]['reported_fact_boundary']=boundary
priority=p['after']['priority_corrections'][-1]
assert priority['sha256']=='ae71dd7a224fb36a50ba83bcbed3878e61887a740a987e4b451e99fedbdb2f5f'
after['priority_corrections'].append(priority)
assert after==p['after']==d['after']; expected['rows'][0]=after; assert expected==read(new)
om=P/'synthesis-continuity-before-approved-boundaries.md'; nm=P/'synthesis-continuity.md'
assert sha(om)==d['before_md_sha256'] and sha(nm)==d['after_md_sha256'] and b'\r\r\n' not in nm.read_bytes()
a=om.read_text(encoding='utf-8').replace(before['fact_summary'],after['fact_summary']); b=nm.read_text(encoding='utf-8')
diff=list(difflib.unified_diff(a.splitlines(),b.splitlines(),n=1)); print('\n'.join(diff))
assert not any(x.startswith('-') and not x.startswith('---') for x in diff)
assert boundary['text'] in b
print(json.dumps(dict(status='only-three-approved-paths',other_three_rows_unchanged=True,json_sha256=sha(new),md_sha256=sha(nm)),ensure_ascii=False))
