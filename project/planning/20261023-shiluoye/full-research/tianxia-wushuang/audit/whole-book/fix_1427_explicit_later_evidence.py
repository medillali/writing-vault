"""1427完整原文新匹配到两条旧问；只更新对应独立裁定。"""
import copy,hashlib,json,pathlib
H=pathlib.Path(__file__).resolve().parent
def fix(part,expected,domain,new_status,new_rationale,new_chapters):
 p=H/f'adjudications-local-v07-part{part:02}.json'
 oldbytes=p.read_bytes();assert hashlib.sha256(oldbytes).hexdigest()==expected
 old=json.loads(oldbytes);new=copy.deepcopy(old)
 a=next(x for x in old if x['audit_domain']==domain);b=next(x for x in new if x['candidate_id']==a['candidate_id'])
 b.update(status=new_status,rationale=new_rationale,later_chapters=new_chapters)
 assert sum(x!=y for x,y in zip(old,new))==1
 (H/'reviewed-batches'/f'adjudications-local-v07-part{part:02}-before-1427-later-evidence.json').write_bytes(oldbytes)
 p.write_text(json.dumps(new,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 sha=hashlib.sha256(p.read_bytes()).hexdigest()
 delta=dict(candidate_id=a['candidate_id'],before_sha256=expected,after_sha256=sha,unchanged_other_items=59,before=a,after=b,evidence_note='本代理再次BEGIN-END完整重读raw1427；L112982明确弓箭手例外，L112994明确吕布衣持隐龙扇。')
 (H/f'local07-part{part:02}-1427-later-evidence-delta.json').write_text(json.dumps(delta,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 md=H/f'local-v07-reviewed-part{part:02}.md';text=md.read_text(encoding='utf-8').replace(f"{a['status']} / {a['audit_domain']}：{a['rationale']}",f"{b['status']} / {b['audit_domain']}：{b['rationale']}").replace('后证raw：'+', '.join(map(str,a['later_chapters'])),'后证raw：'+', '.join(map(str,b['later_chapters'])))
 md.write_text(text,encoding='utf-8')
 build=H/f'write_local07_part{part:02}.py';text=build.read_text(encoding='utf-8')
 old_tuple=repr((a['status'],a['audit_domain'],a['rationale'],a['later_chapters']))
 # 保存器采用无空格元组，先按整行唯一旧理由定位更新。
 lines=text.splitlines()
 found=0
 for i,line in enumerate(lines):
  if a['rationale'] in line:
   lines[i]=f"({b['status']!r},{b['audit_domain']!r},{b['rationale']!r},{str(b['later_chapters']).replace(' ', '')}),";found+=1
 assert found==1
 build.write_text('\n'.join(lines)+'\n',encoding='utf-8')
 print(part,a['candidate_id'],sha)
fix(3,'b8c6ae7afcc9d310ccf85f26fa111140fde5ff4bca65036bf859fcfea270c8b3','specific-item-delivery','answered','1364隐龙扇主收拟给吕，1427 L112994明确吕布衣手持隐龙扇并加持近四千骑，后续持用足以证目标物已到吕；当场交接过程未叙，不能仍把物件终点记作无交付/持用后证。',[1364,1427])
fix(4,'b646f7366b4cca4392c824004c2d537994557d321da863acd2b101d4486e044c','revival-rule-continuity','answered','1388禁不死卡/1393龙刑绝处逢生复起在1427 L112982得到明确人物规则说明：此图不死狂战卡、返生诀失效，弓箭手绝处逢生有作用。原规则疑点已获后证解释；怪涅槃是否触发仍非该句所证，不推广所有复活技能。',[1388,1393,1394,1427])
