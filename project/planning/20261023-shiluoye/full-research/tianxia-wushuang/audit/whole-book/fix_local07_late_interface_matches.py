"""后段接口通读后，补同物持用及缴械周期；不扩写未叙交接。"""
import copy,hashlib,json,pathlib
H=pathlib.Path(__file__).resolve().parent
configs=[(3,'8fcae660e05a93f6d95b4bbafbd8445cbca68a26fcf734ed1a17910c2fa3bd4c','loot-allocation','partial','1364龙幽连实戴、明晶ROLL得，1427吕布衣明确持隐龙扇，扇后续持用已有回执；1364当场交扇过程及所有其余物件最后实穿未逐件给，不由其中一件回收补齐全部。',[1363,1364,1427]),(5,'a5a8e2e1e8ed1b948a3d0f33d0c75504d3d4346ea584e47676ecebd7bc3fe5ed','source-cooldown-and-drop-tier','partial','1471明确缴械15秒与非缴械15秒轮换，后期实战周期与原30秒CD相容；1418“15秒冷却到”可按剩时理解，但无作者专门改字，不写全规则改成15秒。本Boss无十二神器掉落确证，期待不能补实爆。',[1418,1419,1420,1471])]
for n,expected,domain,status,rationale,chapters in configs:
 p=H/f'adjudications-local-v07-part{n:02}.json';raw=p.read_bytes();assert hashlib.sha256(raw).hexdigest()==expected
 old=json.loads(raw);new=copy.deepcopy(old);a=next(x for x in old if x['audit_domain']==domain);b=next(x for x in new if x['candidate_id']==a['candidate_id']);b.update(status=status,rationale=rationale,later_chapters=chapters)
 assert sum(x!=y for x,y in zip(old,new))==1
 (H/'reviewed-batches'/f'adjudications-local-v07-part{n:02}-before-late-interface-match.json').write_bytes(raw)
 p.write_text(json.dumps(new,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');sha=hashlib.sha256(p.read_bytes()).hexdigest()
 (H/f'local07-part{n:02}-late-interface-match-delta.json').write_text(json.dumps(dict(candidate_id=a['candidate_id'],before_sha256=expected,after_sha256=sha,unchanged_other_items=59,before=a,after=b),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 md=H/f'local-v07-reviewed-part{n:02}.md';text=md.read_text(encoding='utf-8').replace(f"{a['status']} / {a['audit_domain']}：{a['rationale']}",f"{b['status']} / {b['audit_domain']}：{b['rationale']}").replace('后证raw：'+', '.join(map(str,a['later_chapters'])),'后证raw：'+', '.join(map(str,b['later_chapters'])))
 md.write_text(text,encoding='utf-8');build=H/f'write_local07_part{n:02}.py';lines=build.read_text(encoding='utf-8').splitlines()
 for i,line in enumerate(lines):
  if a['rationale'] in line:lines[i]=f"({b['status']!r},{b['audit_domain']!r},{b['rationale']!r},{str(b['later_chapters']).replace(' ', '')}),"
 build.write_text('\n'.join(lines)+'\n',encoding='utf-8');print(n,a['candidate_id'],sha)
