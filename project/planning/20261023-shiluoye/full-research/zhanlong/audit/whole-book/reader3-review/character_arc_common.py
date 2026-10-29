"""保存逐人手写人物弧；证据装配不代人物判定。"""
from synthesis_common import *
from collections import Counter
A=P.parent
roster_path=A/'character-arc-entity-roster-proposal.json'
roster=json.loads(roster_path.read_text(encoding='utf-8'))
npc=[e for e in roster['entities'] if e['proposed_owner']=='reader3_npc']
scope=npc[:40]+[{'name':n,'stage_cards':[],'source_check_required':True} for n in roster['supplementary_entities_for_source_check']['reader3_npc']]
assert len(scope)==64 and scope[39]['name']=='云飘飘'
scope_path=P/'character-arc-reader3-scope.json'
if scope_path.exists():assert json.loads(scope_path.read_text(encoding='utf-8'))['entities']==scope
else:dump(scope_path,{'roster_path':str(roster_path.relative_to(ROOT)).replace('\\','/'),'roster_sha256':sha(roster_path),'assignment':'primary明确前40既有NPC+24补核；后20不属本代理','entities':scope})
def getcard(st):
 p=F/f'vol{st["volume"]:02d}-cards.json';a=json.loads(p.read_text(encoding='utf-8'));c=a[st['index']-1]
 assert c['origin_key']==st['origin_key'] and c['asset_id']==st['asset_id']
 return p,c
def make_arc(n,initial,decisions,costs,terminal,boundaries,extra=(),layers=(),source_access='完整接读对应正式卡content/evidence、六卷对应人物状态及交接；必要四栏另列，非新独读全书。'):
 e=scope[n-1];ev=[];mapping=[]
 for st in e['stage_cards']:
  p,c=getcard(st);mapping.append({**st,'material_path':str(p.relative_to(ROOT)).replace('\\','/'),'material_sha256':sha(p),'json_pointer':f'/{st["index"]-1}/content'})
  for x in c.get('evidence',[]):
   x=deepcopy(x);raw=int(x['chapter_id'][3:]);x['access_level']='direct-initial-assigned-full-text' if (2<=raw<=151 or 754<=raw<=968) else 'derived-formal-character-state-and-handoff';x['research_path']=str(p.relative_to(ROOT)).replace('\\','/');x['research_sha256']=sha(p);ev.append(x)
 ev.extend(extra);seen=set();out=[]
 for x in ev:
  k=(x['chapter_id'],x['start_line'],x['end_line'])
  if k not in seen:seen.add(k);out.append(x)
 row={'audit_id':f'character-arc-r3-{n:03d}','name':e['name'],'roster_onebased_index':n,'initial_comparison_stage':initial,'key_decisions':decisions,'costs':costs,'terminal_state':terminal,'evidence_boundaries':boundaries,'review_status':'draft','claim_kind':'synthesis','terminal_certainty':'last_explicit_state_with_labelled_limits','evidence':out,'stage_card_mapping':mapping,'actual_reviewer':'/root/zongheng_vol03_full','reading_attribution':'首次本人原文为卷1raw2—151与卷4raw754—968；卷1尾primary，本人全读其四栏；他卷保原读者。本次为所列人物接口完整派生接读，另记原文定向核验不增加项目唯一覆盖。','source_access':source_access,'priority_layers':list(layers)}
 return row
from copy import deepcopy
def save_arc_group(number,rows,access):
 assert 5<=len(rows)<=8
 path=A/f'reader3-character-arcs-part{number:02d}.json';assert not path.exists(),'交付稳定组不可覆写'
 hashes={}
 for v in range(1,7):
  for kind in ['cards.json','analysis.json','handoff.md','read-log.json']:
   p=F/f'vol{v:02d}-{kind}';hashes[str(p.relative_to(ROOT)).replace('\\','/')]=sha(p)
 for row in rows:
  for rel in row['priority_layers']:
   p=ROOT/rel;assert p.is_file();hashes[rel]=sha(p)
  for ev in row['evidence']:
   c=CH[int(ev['chapter_id'][3:])];assert ev['source_id']==S['source_id'] and ev['revision']==S['revision'] and c['start_line']<=ev['start_line']<=ev['end_line']<=c['end_line']
 wrapper={'status':'stable_group_draft_pending_primary_review','section':'characters','scope':'仅primary分配reader3前40既有NPC及24补核对象；六卷团队全文覆盖，不冒本人全书独读。','source_id':S['source_id'],'revision':S['revision'],'group_number':number,'actual_reviewer':'/root/zongheng_vol03_full','formal_input_sha256':hashes,'characters':rows,'access_log':access}
 dump(path,wrapper)
 md=['# 《斩龙》人物全弧 · reader3第'+str(number)+'组','','稳定草稿，待primary逐项主审；原阶段卡和原始reader不改。','',access,'']
 for r in rows:
  md += ['## '+r['audit_id']+' '+r['name'],'','初态比较：'+r['initial_comparison_stage'],'','关键选择：'+r['key_decisions'],'','代价：'+r['costs'],'','最后实证/终点：'+r['terminal_state'],'','证据边界：'+r['evidence_boundaries'],'','阶段映射：'+'；'.join(f'卷{x["volume"]} #{x["index"]} {x["asset_id"]}' for x in r['stage_card_mapping']),'','定位：'+'；'.join(f'{e["chapter_id"]} L{e["start_line"]}—{e["end_line"]}' for e in r['evidence']),'']
 path.with_suffix('.md').write_bytes(('\n'.join(md)).encode('utf-8'))
 receipt={'status':'frozen-awaiting-primary','path':str(path.relative_to(ROOT)).replace('\\','/'),'sha256':sha(path),'md_sha256':sha(path.with_suffix('.md')),'characters':len(rows),'audit_ids':[r['audit_id'] for r in rows],'formal_inputs':len(hashes),'source_refs':sum(len(r['evidence']) for r in rows),'structure_only':True}
 dump(P/f'character-arcs-part{number:02d}-validation.json',receipt)
 state=P/'character-arc-reader-state.json';s=json.loads(state.read_text(encoding='utf-8')) if state.exists() else {'scope_total':64,'completed_ids':[],'groups':[],'personal_complete_book_read':False}
 assert not set(s['completed_ids'])&set(receipt['audit_ids']);s['completed_ids']+=receipt['audit_ids'];s['groups'].append(receipt);s['next_onebased_index']=max(r['roster_onebased_index'] for r in rows)+1;dump(state,s)
 print(json.dumps(receipt,ensure_ascii=False))
