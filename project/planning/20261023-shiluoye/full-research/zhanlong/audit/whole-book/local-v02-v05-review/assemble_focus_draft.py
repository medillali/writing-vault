from save_focus_manual import P,A,B,F,ROOT,notes,read,write,sha
import json,collections
parts=[];items=[];pins=None;maps={}
for n in [1,2,3]:
 p=A/f'focused-findings-part{n:02d}.json';x=read(p);assert isinstance(x,dict) and len(x['findings'])==8
 if pins is None:pins=x['formal_input_sha256']
 else:assert pins==x['formal_input_sha256']
 parts.append(dict(path=p.name,sha256=sha(p),count=8));items+=x['findings']
 for z in x['findings']:maps[z['key']]=dict(path=p.name,sha256=sha(p))
assert len(items)==len(maps)==24
for p,s in pins.items():assert sha(ROOT/p)==s
for x in items:
 assert x['terminal_status'] in ['answered','partial','unknown','unrecovered']
 for e in x['evidence']:
  assert e['source_id']=='src-20f2d16e3d1b472fa4b230ab0e1770c9' and e['revision']=='61ab0b114c76446fda554abfafdac8c432cd88afaba7c2541f4473a3902134e3'
  k=int(e['chapter_id'].split('-')[1]);n=notes[k];assert n['start_line']<=e['start_line']<=e['end_line']<=n['end_line']
  assert e['claim_kind']=='fact' and sha(ROOT/e['research_path'])==e['material_sha256']
out=dict(source_id=items[0]['evidence'][0]['source_id'],revision=items[0]['evidence'][0]['revision'],status='draft-groups-actually-read-by-primary-pending-final-delta-registration',scope='六卷正式派生与独立复核的跨卷重点；本代理旧原读卷2prefix/卷5，卷2尾原读primary，末12使用primary独立核读，不冒个人全书原文重读。',formal_input_sha256=pins,group_provenance=maps,findings=items)
write(A/'end-state-audit-draft.json',out)
md=['# 《斩龙》全书重点终态审计草稿','',out['scope'],'','24项由3组各8项按原对象合并；当前逐值镜像，主审差分与来源元数据修正分别保留。','']
for n in [1,2,3]:
 s=(A/f'focused-findings-part{n:02d}.md').read_text(encoding='utf-8');md.append(s)
(A/'end-state-audit-draft.md').write_text('\n'.join(md),encoding='utf-8')
val={'status':'passed-structural-and-group-object-identity-not-a-new-semantic-review','count':24,'parts':parts,'unique_keys':True,'all_final_objects_equal_current_group_objects':True,'source_ranges_sid_revision_and_material_sha_valid':True,'formal_input_sha256_matches':True,'by_status':dict(collections.Counter(x['terminal_status'] for x in items)),'evidence_count':sum(len(x['evidence']) for x in items),'draft_json_sha256':sha(A/'end-state-audit-draft.json'),'draft_md_sha256':sha(A/'end-state-audit-draft.md'),'limits':'primary已经实际全读各组，最后定向delta仍按root登记签收；此脚本不伪造语义或用户批准。'}
write(A/'focused-validation.json',val)
links=[A/'priority-corrections-delta.json',B/'primary-focused-rereads.json',B/'primary-additional-rereads-20261026.json',ROOT/'writing-vault/library/reports/zhanlong/audit/primary-rereads/canglan-1369-addendum.json']+list((B/'primary-ending-reread').glob('batch*.json'))
write(A/'focused-input-receipt.json',{'formal_input_sha256':pins,'additional_support_sha256':{str(p.relative_to(ROOT)).replace('\\','/'):sha(p) for p in links},'source_notes':'原始40指纹在local-v02-v05-review/input-receipt.json保历史；正式handoff适配仅顶层pin定向更正；不改冻结分卷。','original_input_receipt_sha256':sha(P/'input-receipt.json')})
handoff=['# 《斩龙》重点终态交接','',f"24项（{val['by_status']}），3组每组8项。source_id/revision/章行/实际材料SHA已结构校验，最终findings与三组逐对象完全相同。",'',f"总稿JSON SHA `{val['draft_json_sha256']}`",f"总稿MD SHA `{val['draft_md_sha256']}`",'', '原文阅读与派生归属按每处证据；新增1369吞魂承接引用primary独立整章证明，旧notes未记的两句不独担新主张。1358是本代理实际完整原章复读，root同章限定复读不冒成全章。','', '研究事实不是用户评价/原创正典，跨卷对照不把另一部小说人物/规则倒灌本作。末局开放事项不是项目尚未读：战皇/傲天新版本、西南KILLS成败、婚礼、阿雷数字出场与新神兵等均按本源边界保留。','']
for p in parts:handoff.append(f"- {p['path']} · SHA `{p['sha256']}`")
(A/'focused-handoff.md').write_text('\n'.join(handoff)+'\n',encoding='utf-8')
print(json.dumps(val,ensure_ascii=False))
