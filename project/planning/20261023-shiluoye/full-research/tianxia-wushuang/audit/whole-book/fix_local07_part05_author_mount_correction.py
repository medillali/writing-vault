"""1440作者明确纠正坐骑名；不把源内已解释项留成未知。"""
import copy,hashlib,json,pathlib
H=pathlib.Path(__file__).resolve().parent;p=H/'adjudications-local-v07-part05.json'
oldbytes=p.read_bytes();assert hashlib.sha256(oldbytes).hexdigest()=='37899728ef4ddf57d75ade35a722835741d824d2f64916cc3a357124412de267'
old=json.loads(oldbytes);new=copy.deepcopy(old);deltas=[]
for domain in ['mount-acquisition-route','source-mount-transition']:
 a=next(x for x in old if x['audit_domain']==domain);b=next(x for x in new if x['candidate_id']==a['candidate_id'])
 b.update(status='answered',rationale='1440 L114048作者括号明确一抹阳光骑踏云魔豹，先前写墨麒麟纯属笔误、那是小小猪的坐骑；因此本项由源内明确纠错解决，不再编造取得/换骑过渡，也不把研究原观察抹去。',later_chapters=[1404,1411,1440])
 deltas.append(dict(candidate_id=a['candidate_id'],before=a,after=b))
assert sum(a!=b for a,b in zip(old,new))==2
(H/'reviewed-batches'/'adjudications-local-v07-part05-before-author-mount-correction.json').write_bytes(oldbytes)
p.write_text(json.dumps(new,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');sha=hashlib.sha256(p.read_bytes()).hexdigest()
(H/'local07-part05-author-mount-correction-delta.json').write_text(json.dumps(dict(before_sha256=hashlib.sha256(oldbytes).hexdigest(),after_sha256=sha,unchanged_other_items=58,deltas=deltas,evidence_note='本代理BEGIN-END完整重读raw1440，原文作者明确纠错。'),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
md=H/'local-v07-reviewed-part05.md';text=md.read_text(encoding='utf-8')
build=H/'write_local07_part05.py';lines=build.read_text(encoding='utf-8').splitlines()
for d in deltas:
 a,b=d['before'],d['after'];text=text.replace(f"{a['status']} / {a['audit_domain']}：{a['rationale']}",f"{b['status']} / {b['audit_domain']}：{b['rationale']}").replace('后证raw：'+', '.join(map(str,a['later_chapters'])),'后证raw：'+', '.join(map(str,b['later_chapters'])))
 for i,line in enumerate(lines):
  if a['rationale'] in line:lines[i]=f"({b['status']!r},{b['audit_domain']!r},{b['rationale']!r},{str(b['later_chapters']).replace(' ', '')}),"
md.write_text(text,encoding='utf-8');build.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(sha)
