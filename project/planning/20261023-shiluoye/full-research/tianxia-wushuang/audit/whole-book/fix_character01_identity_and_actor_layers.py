"""未签首组人物弧三条定向核源修订，其余9条逐值不变。"""
import copy,hashlib,json
from audit_evidence import H,evidence,render_characters
p=H/'character-arcs-part01.json';raw=p.read_bytes();assert hashlib.sha256(raw).hexdigest()=='56d9924255b052c087733974da70a7c727177d233a0d81eee057e173722a192c'
before=json.loads(raw);after=copy.deepcopy(before)
by={x['audit_id']:x for x in after['characters']}
by['character-arc-06']['terminal_state']=by['character-arc-06']['terminal_state'].replace('末队核心法神','末队核心法师')
g=by['character-arc-08'];g['name']='鬼谷子／王诩（公孙谷为旧假证名）'
g['evidence_boundaries']='0039以公孙谷介绍，1147 L92663鬼自称王诩，L92678—79明确解释公孙谷是五百元假身份证/毕业证之名：同一人物的旧假名与后自称，不是未解释的姓名异文，也不另造人。北/鬼无亲兄妹证；兄弟称呼/义气不代金钱归还。'
g['identity_names']=dict(game_name='鬼谷子',real_name_as_self_identified='王诩',prior_false_document_name='公孙谷',explanation_chapter='ch-1147',separate_entity=False)
g['evidence']=evidence([int(e['chapter_id'][3:]) for e in g['evidence']]+[1147])
for e in g['evidence']:
 if e['chapter_id'] in ['ch-0039','ch-1147']:e['access_level']='targeted-full-chapter-source-reread-during-audit-not-whole-volume-reading'
c=by['character-arc-12'];c['key_decisions']='旧SSS失败后成为可拒令妖仆→逐渐改称哥哥并自主护人→选择人格怜悯/复蒙川→986本人自述救赎血指灵魂并用战神血液制剂复体、无头血指当场已现（净化复体过程未现场叙）→寻到并引苏见母，母魂竭后施救赎阵，苏自主立守善誓、卡邀请/陆建议驻地→龙神战失腿后再生→援寒/杀米/抗冰与圣→1459主动携林坠渊送主出→受囚仍断林臂、笼中助杀夜→被救后接受现实身体并练走。'
c['evidence_boundaries']='徐宁解释身体/人格关系是小说内科幻来源，非物质穿越证明。884血指由苏斩首/北系统末杀，986才心自述救赎复体且无头体实现，不能混阶段或把离场过程作亲见。苏母衰竭消逝、心施阵、苏立誓/卡邀请/陆择驻地是多方动作，非心独力洗白旧杀戮。1455爱语主未听、1459才当面说；苏伦性侵虐杀为敌话且心活反证，不定她已遭性侵。'
assert sum(a!=b for a,b in zip(before['characters'],after['characters']))==3
(H/'reviewed-batches'/'character-arcs-part01-before-identity-actor-layer-delta.json').write_bytes(raw)
p.write_text(json.dumps(after,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');sha=hashlib.sha256(p.read_bytes()).hexdigest()
deltas=[dict(audit_id=a['audit_id'],before=a,after=b) for a,b in zip(before['characters'],after['characters']) if a!=b]
(H/'character01-identity-actor-layer-delta.json').write_text(json.dumps(dict(before_sha256=hashlib.sha256(raw).hexdigest(),after_sha256=sha,unchanged_other_characters=9,deltas=deltas,source_verification='BEGIN-END全文复读0039/0986/0987/1147；只增加定向审计读取，不冒卷一/六全卷亲读。'),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
render_characters('character-arcs-part01.md',after['characters'],after['title'])
print(sha)
