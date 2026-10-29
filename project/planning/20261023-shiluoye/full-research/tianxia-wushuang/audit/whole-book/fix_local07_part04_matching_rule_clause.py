import copy,hashlib,json,pathlib
H=pathlib.Path(__file__).resolve().parent;p=H/'adjudications-local-v07-part04.json'
raw=p.read_bytes();assert hashlib.sha256(raw).hexdigest()=='e165e717fe1b62d34b6e8dcfd9a062e95cb4969088f7b1c84726b0b2af92b0a9'
old=json.loads(raw);new=copy.deepcopy(old)
a=next(x for x in old if x['audit_domain']=='revival-rule-confirmation');b=next(x for x in new if x['candidate_id']==a['candidate_id'])
b['rationale']='1388主确认不死卡在混乱图复活失效、只用攻血属性；1427明确不死卡和返生诀失效而弓箭手绝处逢生有效，后文已给具体例外。怪涅槃只是李玩笑推测，不由弓例外推广全部复活。'
b['later_chapters']=[1384,1388,1393,1427]
assert sum(x!=y for x,y in zip(old,new))==1
(H/'reviewed-batches'/'adjudications-local-v07-part04-before-matching-rule-clause.json').write_bytes(raw)
p.write_text(json.dumps(new,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');sha=hashlib.sha256(p.read_bytes()).hexdigest()
base=json.loads((H/'reviewed-batches'/'adjudications-local-v07-part04-before-1427-later-evidence.json').read_text(encoding='utf-8'))
deltas=[dict(candidate_id=x['candidate_id'],before=x,after=y) for x,y in zip(base,new) if x!=y]
assert len(deltas)==2
(H/'local07-part04-1427-combined-delta.json').write_text(json.dumps(dict(before_signed_sha256='b646f7366b4cca4392c824004c2d537994557d321da863acd2b101d4486e044c',after_sha256=sha,unchanged_other_items=58,deltas=deltas),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
md=H/'local-v07-reviewed-part04.md';text=md.read_text(encoding='utf-8').replace(a['rationale'],b['rationale']).replace('后证raw：'+', '.join(map(str,a['later_chapters'])),'后证raw：'+', '.join(map(str,b['later_chapters'])))
md.write_text(text,encoding='utf-8')
build=H/'write_local07_part04.py';lines=build.read_text(encoding='utf-8').splitlines()
for i,line in enumerate(lines):
 if a['rationale'] in line:lines[i]=f"({b['status']!r},{b['audit_domain']!r},{b['rationale']!r},{str(b['later_chapters']).replace(' ', '')}),"
build.write_text('\n'.join(lines)+'\n',encoding='utf-8');print(a['candidate_id'],sha)
