import json,copy,hashlib
from audit_evidence import H,render_characters
p=H/'character-arcs-part08.json';before=json.loads(p.read_text(encoding='utf-8'));after=copy.deepcopy(before)
edits={
 'character-arc-94':dict(name='紫水／嗜血使者',key_decisions='1365—1367多轮战后实际死亡，求护女；陆拒割头而整尸带回→1368委托结算后父亲冥婚动机揭→新复活石使紫水真正复活，带已醒且拒绝冥婚的瑟琳娜离开。'),
 'character-arc-95':dict(key_decisions='1368复活咒显现后真实醒来，明确拒嫁死人，认出紫水梦中声音与模样；随后紫水拥住她并飞离。',terminal_state='1368实际醒来、拒婚、认出梦中声音以及紫水拥其飞离已明示；后续生活未展开，不能把抱走镜头额外升级成她已独立说出同意同行。梦/记忆与旧面板矛盾未给专门解释，不编新失忆设定。'),
 'character-arc-96':dict(initial_comparison_stage='暗黑族父亲，以救女委托陆割紫水头；后自述为族借血鬼族鲜血力量而安排女儿冥婚，四十年前亡者为血鬼族族长唯一子嗣。',key_decisions='陆交整尸令其不满，1368系统结算后揭冥婚意图；女醒后明确拒嫁死人，紫水拥其飞离，父未能执行当场婚事。',evidence_boundaries='四十年前亡子属于血鬼族族长，不是菲特烈之子；旧婚约七年前与亡者四十年前死均为父陈述。女明确拒婚与被紫水带走分层，不以委托者满意度替代受救者意愿。'),
 'character-arc-97':dict(evidence_boundaries='主对他不信任与其真实所知分层，未杀不是洗罪；1495血指灰飞回顾的发言者是飞银龙，不归百兽老人，也非当场又杀一次。'),
 'character-arc-99':dict(key_decisions='1491逼二人败走，恢复满血后二战→1492杀奥丹蛊惑的三万冰巨、刺穿奥胸→1493在多重牺牲与配合后被陆最后紫啸杀。')}
changes=[]
for row in after['characters']:
 if row['audit_id'] in edits:
  old=copy.deepcopy(row);row.update(edits[row['audit_id']]);changes.append(dict(audit_id=row['audit_id'],before=old,after=copy.deepcopy(row),changed_fields=[k for k in old if old[k]!=row[k]]))
assert len(changes)==5
assert all(a==b for a,b in zip(before['characters'],after['characters']) if a['audit_id'] not in edits)
(H/'reviewed-batches/character-arcs-part08-before-event-attribution.json').write_bytes(p.read_bytes())
p.write_text(json.dumps(after,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
render_characters('character-arcs-part08.md',after['characters'],after['title'])
delta=dict(status='draft_group_targeted_corrections_pending_primary_signature',reason='root逐项主审并本人BEGIN-END全文复读1367/1368及复读四栏1365/1366后定向修5对象，其余7逐值不变；94另清除研究误加的龙蛇称谓，原文称嗜血使者。',before_sha256=hashlib.sha256((H/'reviewed-batches/character-arcs-part08-before-event-attribution.json').read_bytes()).hexdigest(),after_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),changes=changes)
(H/'character08-event-attribution-delta.json').write_text(json.dumps(delta,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(delta['after_sha256'])
