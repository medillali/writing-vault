import json,hashlib
from audit_evidence import H,B,R,chapters,volume_by_id
p=H/'research-interface-read-log.json';x=json.loads(p.read_text(encoding='utf-8'))
extra_full=[39,42,889,986,987,1082,1147,1268,1299,1367,1368,1380]
present={r.get('chapter_id') for r in x.get('targeted_interfaces',[])}
for n in extra_full:
 c=chapters[n]
 if c['chapter_id'] not in present:
  x['targeted_interfaces'].append(dict(volume=volume_by_id[c['chapter_id']],interface='novel full chapter targeted audit reading',chapter_id=c['chapter_id'],start_line=c['start_line'],end_line=c['end_line'],purpose='姓名/施为者/事件阶段定向复核，BEGIN-END输出完整；只此章，不冒整卷重读。'))
note_ids={2:[214,215,216],4:[628,629,632,633,644,771,772],5:[888,889,890,943],6:[1086,1087,1098,1145,1146,1165,1185,1194,1199,1202,1209,1212,1215,1216,1219,1221,1239,1257,1258,1259,1260,1261,1262,1263,1264,1265,1266,1267,1268,1269,1270,1271,1272,1273,1290,1291,1293]}
x['additional_complete_targeted_note_reads']=[]
for v,ids in note_ids.items():
 q=B/f'vol{v:02}/chapter-notes.jsonl'
 x['additional_complete_targeted_note_reads'].append(dict(volume=v,raw_chapter_ids=[f'ch-{n:04}' for n in ids],access_kind='full-four-column-derived-note-reading-not-full-novel-reread',input_sha256=hashlib.sha256(q.read_bytes()).hexdigest(),reader='/root/zongheng_vol04_full'))
x['mechanical_scope_supplement']='卷一/三/八notes未明栏1291追加ID已保留。v1/v3由agent3独立完成995裁定、v8由本代理完成296；这不冒称本代理亲读v1/v3整卷原文或每条notes。实际主审以primary签表逐组SHA为准。'
if '最近晚段关键词' not in x['truncation_handling']:x['truncation_handling']+='；最近晚段关键词notes合并输出在战痕/十月段裁切，已单独完整输出补读两词末三章；未以裁切输出登记完整。'
p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
inv=H/'input-inventory.json';y=json.loads(inv.read_text(encoding='utf-8'));y['status']='all_formal_volume_inputs_verified_terminal_audit_in_separate_signed_groups_pending_final_assembly';inv.write_text(json.dumps(y,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
cp=json.loads((B/'primary-audit-review-progress.json').read_text(encoding='utf-8'));rp=json.loads((B/'primary-research-group-review-progress.json').read_text(encoding='utf-8'))
counts={s:sum(g['count'] for g in rp['groups'] if g['section']==s) for s in ['characters','findings']}
text=f'''# 无双全书终点审计进度（独立研究草稿）

本代理指定原文亲读卷五265正文/266片与卷七210正文/211片，两卷已正式冻结。八卷团队正式覆盖1599正文/1609原片，不等本代理个人重读全书。其他卷以实际读取的正式人物状态/历史问题/图线程与必要四栏notes派生。

历史214含全部resolved历史；本地旧2625加卷一/三/八漏栏1291，总3916。原ID/顺序/原记录均保，只有terminal层组装。历史214与本代理卷七476/卷八309已全部独立终判并经分组主审。当前primary签表实际记录{cp['distinct_reviewed_candidates']}/4130候选；人物已交115、重点已交30，签表现为{counts['characters']}人物与{counts['findings']}重点。签表未齐不冻结，不以覆盖数冒称语义主审已完。

分工：agent3早历史55与v1/v3新增notes995，后接旧v5的1基178—556共379；agent5旧v1—4的923及旧v6的657；primary旧v5前177。本代理旧v7/8、历史5—7、人物/重点以及唯一总装。各自只写隔离批；最终只取primary-audit-review-progress.json与primary-research-group-review-progress.json实际签SHA白名单，聚合/快照不重复输入。

定向纠正保before/proposal/delta：1305分盟原误读绑旧正式snapshot；母亲已亡与扫墓主体纠去串书；吞林浅魂为明宇自述；1299拾荒死报告/剑到卡琳与1458再现并存；神泣旧版真删与860小范围改版分层；修罗王579与821/831旧值异文保留。所有原211卷七笔记和冻结分卷包不修改。

assemble_signed_batches.py默认只查就绪。正式组装前须4130候选、115人物、30重点全部根签，且所有签组SHA相符；研究对象逐值复制，候选status/rationale/audit_domain/later_chapters逐ID相等，后证集合相同，原字段除terminal外不变。来源元数据null补齐仅在副本进行并逐处记metadata-enrichment-log，不回写签批、不生成原文阅读。

不读斩龙、不写正式库、不创建整书primary凭据；最终发布/独立验收由primary完成，研究仍非用户审美批准。
'''
(H/'progress.md').write_text(text,encoding='utf-8')
