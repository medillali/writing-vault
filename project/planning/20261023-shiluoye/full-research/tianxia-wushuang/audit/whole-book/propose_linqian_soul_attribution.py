import json,hashlib,copy
from audit_evidence import H
changes=[]
for filename,cid in [('character-arcs-part05.json','character-arc-69'),('character-arcs-part07.json','character-arc-88')]:
 p=H/filename;obj=json.loads(p.read_text(encoding='utf-8'));before=next(x for x in obj['characters'] if x['audit_id']==cid);after=copy.deepcopy(before)
 if cid.endswith('69'):
  after['initial_comparison_stage']='1268明宇本人自述灵魂寄斩龙，并因林浅贪力而吞噬其灵魂、使之成傀儡并借其身体；这是明确的NPC说明来源，吞魂旧过程未现场重演。'
  after['costs']='他以秩序压迫妻女的悲史自辩不能使伤人全正当；借身救赎三师承诺失败。原林浅遭吞魂已有明宇明确自述，后续无原魂恢复/再现确证；自愈和契约也救不了最终神格被碎。'
  after['evidence_boundaries']='林浅原魂被吞为明宇1268自述，不写全书没有魂相关说明；过程未现场验证、原魂之后未恢复/再现与借体者1456化尘分开，不能把1456自动当原魂死亡时刻。更不倒改纵横明宇旧终态。'
 else:
  after['terminal_state']='1268明宇明确自述吞噬林浅灵魂、使其成力量傀儡；此旧过程未现场验证，后文没有原魂恢复/再现确证。明宇借此体1456化尘死明确，但不将该时点自动当成原林浅魂死亡时刻。'
  after['evidence_boundaries']='本条与明宇弧互指却不混人；既有吞魂自述不能漏作全书没有说明，来源又不升级成独立现场验证。原王子真心悔罪不能因先话断言，也不能因明后背叛反推王子每句自述都确假。'
 changes.append(dict(path=filename,audit_id=cid,input_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),changed_fields=[k for k in before if before[k]!=after[k]],before=before,after=after))
out=dict(status='proposal_pending_primary_review_no_signed_group_modified',reason='定向BEGIN-END全文阅读raw1268，L101279明宇已有吞噬林浅灵魂/成傀儡自述；补已存在说明及来源层级，不把借体者1456死时并作原魂死时。',source_locator=dict(chapter_id='ch-1268',start_line=101279,end_line=101279,claim_kind='fact',attribution='明宇角色自述'),changes=changes)
(H/'character-linqian-soul-attribution-proposal.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('proposal only',[(x['audit_id'],x['changed_fields']) for x in changes])
