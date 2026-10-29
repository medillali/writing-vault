from save_tail_manual import Q,read,write,sha
import json
p=Q/'adjudications-local-v06-tail-batch001.json';rows=read(p);before=json.loads(json.dumps(rows,ensure_ascii=False))
patches={
8:'1263托交之后，1266林的中位飞升系统与本人回城状态确证取冬格成功；同章林回城、东从练级地回补给并实际来到桥边，已直接回答东安全出境，无须只依1281/1290较晚活动侧证。该后证不倒写1263当时双方已相聚，不另造寄存UI，也不把主背包被清除的鲁/空间格套在林格上。',
15:'1272鬼将卡与两枚丹都实际消耗，掉级后保235方案已验证且帮助杀云浅。1266的235级87%是主自己练到的等级进度，同时主帮助南宫灵通过S6，不能转为灵升到235；后来1281造弓与1290神铸亦不能补成该次副本全套掉装，她当次各件结算仍无独立清单。'}
for i,t in patches.items():rows[i]['rationale']=t
for i,(b,a) in enumerate(zip(before,rows)):
 if i in patches:
  b=dict(b);a=dict(a);b.pop('rationale');a.pop('rationale');assert b==a
 else:assert b==a
write(Q/'batch001-before-primary-precision.json',before)
write(p,rows)
delta=dict(primary_instruction='root已明确批准仅两项rationale；非用户审美批准',batch_before_sha256=__import__('hashlib').sha256((json.dumps(before,ensure_ascii=False,indent=2)+'\n').encode()).hexdigest(),batch_after_sha256=sha(p),changes=[dict(candidate_id=rows[i]['candidate_id'],before=before[i],after=rows[i]) for i in patches],other_18_objects_equal=True,status_domain_refs_later_chapters_equal=True)
write(Q/'batch001-primary-precision-delta.json',delta)
md=['# 《斩龙》卷六尾199候选终评草稿','独占原序[200:399]，本批assigned offset 0—19；待primary登记当前差分。','']
for x in rows:md += [f"- **{x['candidate_id']}** · {x['status']} / {x['audit_domain']}",f"  原题：{x['title']}",f"  终评：{x['rationale']}",f"  后证raw：{', '.join(map(str,x['later_chapters']))}；派生保原reader。",'']
p.with_suffix('.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
s=read(Q/'reader-state.json');s['batches'][0]['sha256']=sha(p);write(Q/'reader-state.json',s);print(sha(p));print(sha(Q/'batch001-primary-precision-delta.json'))
