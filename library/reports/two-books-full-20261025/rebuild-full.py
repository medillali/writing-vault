"""把已实际阅读的研究批次写入既有资料库；缺章时拒绝宣布全书完成。"""
from pathlib import Path
import json,sys,hashlib,collections,copy,html
sys.stdout.reconfigure(encoding='utf-8')
P=Path(__file__).resolve().parent;V=P.parents[2];R=next(p for p in V.parents if (p/'distill-novels/scripts/fictionlib').is_dir());O=P
sys.path.insert(0,str(R/'distill-novels/scripts'))
from fictionlib.vault import Vault,KINDS
from fictionlib.graph import save_graph,render_graph
from fictionlib.storage import digest
S=json.loads((P/'sources.json').read_text(encoding='utf-8'))
BOOK={'z':'贼胆','l':'网游之练级专家'};FOLDER={'z':'zeidan','l':'leveling'}
DIM={'worldbuilding':'世界与规则','characters':'人物与关系','plot':'情节与因果','style':'语言与描写','narrative':'视角与信息','dialogue':'对话与博弈','pacing':'节奏与结构','themes':'主题与价值','continuity':'连续性与原文异常'}
CN={'summary':'概述','goals':'目标','changes':'阶段变化','relationships':'关系','knowledge':'认知与信息边界','source_anomalies':'原文异常','goal':'目标','obstacle':'障碍','choice':'选择','consequence':'后果','state_change':'状态变化','why_it_works':'机制解释','applicability':'适用条件','failure_mode':'失效风险','steps':'抽象步骤','aliases':'已记录别名','name':'人物名','analysis_boundary':'解释边界','snapshots':'阶段快照','stage':'研究阶段','title':'名称','evidence':'证据','ordinal':'阅读序号','events':'事件','state_changes':'状态变化','open_questions':'阶段疑问','source_keys':'阶段键','identity_boundary':'身份边界','status':'状态'}
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def dump(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s.rstrip()+'\n',encoding='utf-8')
def unique(vs):
 out=[];seen=set()
 for v in vs:
  s=json.dumps(v,sort_keys=True,ensure_ascii=False)
  if s not in seen:seen.add(s);out.append(v)
 return out
def evidence(k,es,kind='inference'):
 return unique([{**e,'source_id':S[k]['source_id'],'revision':S[k]['revision'],'claim_kind':kind} for e in es])
def loc(es):return '；'.join(f"[{e['chapter_id']} L{e['start_line']}–{e['end_line']}](chapter-index.md#{e['chapter_id']})" for e in es)
def prose(v):
 if isinstance(v,list):return '\n'.join('- '+prose(x).replace('\n','；') for x in v) or '无已记录条目。'
 if isinstance(v,dict):return '\n'.join('**'+CN.get(k,k)+'**：'+prose(x) for k,x in v.items() if k not in ['key','scene_keys'])
 return '未填写' if v is None else str(v)
def ident(prefix,k,text):return f'{prefix}-full-{k}-'+hashlib.sha256(text.encode()).hexdigest()[:20]
class Cached(Vault):
 def _sources(self):
  if not hasattr(self,'source_cache'):self.source_cache=super()._sources()
  return self.source_cache
def batches(k,complete=True):
 folders=['z','z-b','z-c','z-c2','z-d'] if k=='z' else ['l-a','l-b']
 bs=[]
 for folder in folders:
  for f in sorted((P/'research'/folder).glob('batch-*.json')):
   b=load(f);b['worker_folder']=folder;b['worker_file']=f.name;bs.append(b)
 bs.sort(key=lambda b:b['unit_start'])
 seen=[u['ordinal'] for b in bs for u in b['units']]
 if complete:assert seen==list(range(1,len(S[k]['units'])+1)),f'{k}尚缺实际阅读记录：{sorted(set(range(1,len(S[k]["units"])+1))-set(seen))}'
 for n,b in enumerate(bs,1):b['stage_id']=f'stage-{n:02}';b['stage_number']=n
 return bs
def build(k,vault):
 bs=batches(k);dest=O/FOLDER[k];cards=[];scene_by_stage={};char_names=collections.defaultdict(list)
 # 来源名称仅作已读同书人物的汇总键；不跨作品合并，不推断新别名。
 for b in bs:
  for original in b['characters']:
   c=copy.deepcopy(original);name=c['name'].strip();c['original_record_name']=name
   # 此表来自本次全文与身份审计，不根据名字相似度推断身份。
   canonical={'马尔都克长老':'马尔都克','王阿兰德':'阿兰德（现实身份：萧寒）','阿兰德':'阿兰德（现实身份：萧寒）','萧寒':'阿兰德（现实身份：萧寒）','泰坦巨人恩特':'恩特','水晶石像鬼':'机械石像鬼'} if k=='l' else {}
   suspects=[x for x in c.get('aliases',[]) if any(v in x for v in ['疑','源文变体','异写'])]
   c['aliases']=[x for x in c.get('aliases',[]) if x not in suspects]
   if suspects:c['suspected_name_variants']=suspects
   if k=='l' and name=='奥斯林兰与塔布雷特':
    for single in ['奥斯林兰','塔布雷特']:
     part=copy.deepcopy(c);part['name']=single;part['record_role']='两人关系的结局补记，已分别链接至各自档案';char_names[single].append((b,part))
   else:
    resolved=canonical.get(name,name)
    if resolved!=name:c['aliases']=unique(c['aliases']+[name]);c['identity_resolution']='全文中已确证的同一人物/意识，保留原称呼与阶段证据'
    if name=='其他核心成员':c['record_role']='群体后日谈索引，非单独自然人'
    char_names[resolved].append((b,c))
 def put(typ,key,title,content,es,refs=[]):
  aid=ident(KINDS[typ][1],k,typ+'/'+key);path=V/vault._asset_path(aid)
  data={'asset_id':aid,'asset_type':typ,'scope':'reusable-pattern' if typ=='pattern' else 'source-analysis','origin_key':f'{S[k]["source_id"]}/full-20261025/{typ}/{key}','title':title,'tags':[BOOK[k],'全书细读','2026-10-25',typ],'content':content,'evidence':evidence(k,es,'synthesis' if typ=='pattern' else 'inference'),'derived_from':refs,'user_notes':'','favorite':False,'review_status':'draft'}
  a=vault.put_asset(data,base_revision=load(path)['revision'] if path.exists() else None,generated=True);cards.append(a);return a
 for name,items in sorted(char_names.items()):
  snapshots=[]
  for b,c in items:snapshots.append({'stage':b['stage_id'],'unit_start':b['unit_start'],'unit_end':b['unit_end'],**{kk:vv for kk,vv in c.items() if kk not in ['evidence','key']},'evidence':evidence(k,c['evidence'])})
  put('character',name,f'《{BOOK[k]}》{name}〔全书阶段档案〕',{'summary':items[-1][1]['summary'],'name':name,'aliases':unique([v for _,c in items for v in c.get('aliases',[])]),'source_keys':unique([c['key'] for _,c in items]),'snapshots':snapshots,'identity_boundary':'同一来源中经上下文核对的身份按阶段聚合；已证异名的归并写在identity-resolution中，其他异名未自动合并，跨书同名始终分开。末次专题记录不自动等于人物结局。','analysis_boundary':'人物行动与阶段变化据文本概括；动机、关系解释与可迁移判断为研究草稿。个人评价尚未填写。'},[e for _,c in items for e in c['evidence']])
 for b in bs:
  for s in b['scenes']:
   a=put('scene',b['stage_id']+'/'+s['key'],f'《{BOOK[k]}》{s["title"]}',{kk:vv for kk,vv in s.items() if kk not in ['evidence','key','scene_keys']}|{'stage':b['stage_id'],'analysis_boundary':'目标、行动、结果为文本概括；为何奏效、适用条件和失效风险为研究推断。'},s['evidence'])
   scene_by_stage[(b['stage_id'],s['key'])]=a
 for b in bs:
  for p in b['patterns']:
   refs=[]
   for key in p.get('scene_keys',[]):
    a=scene_by_stage.get((b['stage_id'],key))
    if a:refs.append({'asset_id':a['asset_id'],'revision':a['revision']})
   # 部分阶段机制对应跨阶段场景；只有显式键唯一时连接。
   if not refs:
    for key in p.get('scene_keys',[]):
     found=[a for (stage,sk),a in scene_by_stage.items() if sk==key]
     if len(found)==1:refs.append({'asset_id':found[0]['asset_id'],'revision':found[0]['revision']})
   assert refs,f'机制缺少可追溯场景：{k}/{b["stage_id"]}/{p["key"]}'
   put('pattern',b['stage_id']+'/'+p['key'],p['title'],{kk:vv for kk,vv in p.items() if kk not in ['key','evidence','scene_keys']}|{'stage':b['stage_id'],'analysis_boundary':'由来源场景抽象的创作控制候选，未成为用户偏好或原创正典。'},p['evidence'],refs)
 dump(dest/'asset-manifest.json',[{'asset_id':a['asset_id'],'revision':a['revision'],'type':a['asset_type'],'title':a['title']} for a in cards])
 units=[u for b in bs for u in b['units']]
 dump(dest/'chapter-notes.json',{'source_id':S[k]['source_id'],'source_revision':S[k]['revision'],'reading_method':'逐单元取出完整原文、模型阅读并保存事件/变化记录；文件抽取回执不单独证明阅读。','units':units})
 write(dest/'chapter-notes.md',f'# 《{BOOK[k]}》全书逐单元记录\n\n{len(units)}个实际阅读单元，保留合章、重号与序章。事件为文本概括，状态解释可修订。\n\n'+'\n\n'.join(f'## {u["ordinal"]:03} · {u["title"]}\n\n'+prose({kk:u[kk] for kk in ['events','state_changes','open_questions']})+'\n\n证据：'+loc(u['evidence']) for u in units))
 write(dest/'chapter-index.md',f'# 《{BOOK[k]}》证据索引\n\n来源 `{S[k]["source_id"]}`；修订 `{S[k]["revision"]}`。章前内容只核对书目信息，不计入剧情单元。\n\n'+'\n\n'.join(f'<a id="{c["chapter_id"]}"></a>\n\n## {c["chapter_id"]} · {c["title"]}\n\nL{c["start_line"]}–{c["end_line"]}，字符区间[{c["start_offset"]}, {c["end_offset"]})。' for c in S[k]['chapters']))
 history=[];qgroups=collections.defaultdict(list);thistory=[]
 for b in bs:
  clean={kk:vv for kk,vv in b.items() if kk not in ['worker_folder','worker_file']};clean.update(source_id=S[k]['source_id'],source_revision=S[k]['revision'],reading_status='full_text_read_and_analyzed')
  dump(dest/'stages'/f'{b["stage_id"]}.json',clean)
  parts=[f'# 第{b["stage_number"]}研究阶段：{b["label"]}',f'实际阅读单元{b["unit_start"]}–{b["unit_end"]}。研究分段不是原书卷名。返回[全书入口](../README.md)。']
  for dk,label in DIM.items():
   parts.append('## '+label)
   for f in b['dimensions'][dk]:parts.append(f'**{"文本事实" if f["kind"]=="fact" else "研究推断"}**：{f["claim"]}\n\n证据：'+loc(f['evidence']).replace('(chapter-index.md','(../chapter-index.md'))
  parts+=['## 人物与场景变化',prose([{kk:vv for kk,vv in u.items() if kk in ['ordinal','title','events','state_changes','open_questions']} for u in b['units']])]
  write(dest/'stages'/f'{b["stage_id"]}.md','\n\n'.join(parts))
  for q in b['questions']:
   x={**q,'stage':b['stage_id'],'unit_end':b['unit_end']};history.append(x);qgroups[q['key']].append(x)
  for t in b['threads']:thistory.append({**t,'stage':b['stage_id'],'unit_end':b['unit_end']})
 ledger=[]
 for key,items in qgroups.items():
  last=items[-1];ledger.append({'id':key,'question':last['question'],'latest_recorded_status':last['status'],'latest_answer':last['answer'],'last_observed_at_unit':last['unit_end'],'terminal_status':'resolved-in-observed-event' if last['status']=='resolved' else 'requires-ending-audit','history':items,'boundary':'阶段已回收仅指该问法和已发生事件；非已回收项须结合ending-audit逐项核对，不自动声称全书未解。'})
 terminal_path=P/'research'/('z-final' if k=='z' else 'l-b')/'terminal-question-map.json'
 if terminal_path.exists():
  terminal=load(terminal_path);tm={x['key']:x for x in terminal['items']}
  assert set(tm)==set(qgroups),f'终态核对键未完整覆盖：{set(qgroups)-set(tm)} / {set(tm)-set(qgroups)}'
  for q in ledger:q['final_audit']=tm[q['id']];q['terminal_status']=tm[q['id']]['final_status']
 dump(dest/'question-ledger.json',{'questions':ledger,'history':history,'terminal_audit':'ending-audit.json'})
 write(dest/'question-ledger.md',f'# 《{BOOK[k]}》问题账与历史\n\n{len(ledger)}个阶段键、{len(history)}条观察。不同问法可能指同一条线，未冒称互不重复的问题数。最终回收情况见[结局核对](ending-audit.md)。\n\n'+'\n\n'.join(f'## {q["id"]} · {q["question"]}\n\n全书核对：**{q["terminal_status"]}** · {q.get("final_audit",{}).get("answer","待终态核对")}\n\n'+loc(q.get('final_audit',{}).get('evidence',[]))+f'\n\n最后专题观察：单元{q["last_observed_at_unit"]}，{q["latest_recorded_status"]}。\n\n{q["latest_answer"]}\n\n'+ '\n\n'.join(f'### {x["stage"]} · {x["status"]}\n\n{x["answer"]}\n\n设问：{loc(x.get("setup_evidence",[]))}\n\n回应：{loc(x.get("resolution_evidence",[]))}' for x in q['history']) for q in ledger))
 dump(dest/'thread-history.json',thistory)
 # 场景节点与逐章记录分离：章覆盖由台账证明，图只精选有因果机制的事件。
 nodes=[{'id':'story','title':f'《{BOOK[k]}》全书研究','kind':'story','parent_id':None,'claim_kind':'inference','summary':'结构归属不等于因果；研究阶段不是原著卷。'}];edges=[];threads=[]
 for b in bs:
  st=b['stage_id'];nodes.append({'id':st,'title':b['label'],'kind':'arc','parent_id':'story','narrative_order':b['unit_start'],'claim_kind':'inference','summary':f'阅读单元{b["unit_start"]}–{b["unit_end"]}','evidence':evidence(k,[e for u in b['units'] for e in u['evidence']])})
  for s in b['scenes']:
   a=scene_by_stage[(st,s['key'])];nid='event-'+a['asset_id'].split('-')[-1]
   nodes.append({'id':nid,'title':s['title'],'kind':'scene','parent_id':st,'narrative_order':min(next(u['ordinal'] for u in units if any(e['chapter_id']==ue['chapter_id'] for ue in u['evidence'])) for e in s['evidence']),'claim_kind':'inference','summary':s['summary'],'asset_id':a['asset_id'],'evidence':evidence(k,s['evidence']),'mechanism':{kk:s.get(kk,'') for kk in ['goal','obstacle','choice','consequence','state_change']}})
 def anchor(es):
  ch={e['chapter_id'] for e in es}
  found=[n for n in nodes if n['kind']=='scene' and any(e['chapter_id'] in ch for e in n['evidence'])]
  if found:return found[-1]['id']
  found=[n for n in nodes if n['kind']=='arc' and any(e['chapter_id'] in ch for e in n['evidence'])]
  return found[-1]['id'] if found else 'story'
 for q in ledger:
  items=q['history'];es1=unique([e for x in items for e in x.get('setup_evidence',[])]);es2=unique([e for x in items for e in x.get('resolution_evidence',[])])
  final=q.get('final_audit');status=final['final_status'] if final else q['latest_recorded_status'];answer=final['answer'] if final else q['latest_answer']
  # 问题账允许标注矛盾/异常，剧情图状态只表达回收程度；保留原状态在历史中。
  status={'source-anomaly':'unknown','anomaly':'unknown','conflict':'unknown','unresolved':'unknown'}.get(status,status)
  assert status in {'open','partial','resolved','abandoned','unknown'},status
  if final:es2=unique(es2+final.get('evidence',[]))
  if not es1:continue
  a=anchor(es1[:1]);z=anchor(es2[-1:]) if es2 else a;ids=[a] if a==z else [a,z];eids=[]
  if a!=z:
   eid='relation-'+hashlib.sha256(q['id'].encode()).hexdigest()[:16];kind='payoff' if status=='resolved' else 'reveal' if status=='partial' else 'setup'
   edges.append({'id':eid,'from':a,'to':z,'kind':kind,'label':q['question'][:70],'claim_kind':'inference','evidence':evidence(k,es1+es2),'summary':answer});eids=[eid]
  threads.append({'id':'question-'+hashlib.sha256(q['id'].encode()).hexdigest()[:16],'title':q['question'],'kind':'hidden','status':status,'node_ids':ids,'edge_ids':eids,'resolution_note':answer if status=='resolved' else '', 'status_scope':'全书问题复核' if final else '最后专题观察，未解项以结局审计为准','evidence':evidence(k,es1+es2)})
 grouped_lines=collections.defaultdict(list)
 for t in thistory:
  if t['kind'] in ['main','subplot']:grouped_lines[t['key']].append(t)
 for i,(key,observations) in enumerate(grouped_lines.items()):
  t=observations[-1];line_evidence=unique([e for x in observations for e in x['evidence']]);members=unique([anchor([e]) for e in line_evidence]);
  if not members:continue
  threads.append({'id':f'line-{i+1:03}','title':t['title']+'〔阶段追踪〕','kind':t['kind'],'status':t['status'] if t['status']=='resolved' else 'unknown','node_ids':members,'edge_ids':[],'resolution_note':t['state'] if t['status']=='resolved' else '', 'summary':t['state'],'status_scope':'按专题键聚合的阶段追踪；未定终态以结局问题账为准','observed_stages':[x['stage'] for x in observations],'evidence':evidence(k,line_evidence)})
 causal_path=P/'research/z-final/causal-relations.json' if k=='z' else P/'causal_l.json'
 if causal_path.exists():
  causal=load(causal_path);items=causal['items'] if isinstance(causal,dict) else causal
  for i,x in enumerate(items,1):
   def scene(key):
    found=[a for (st,sk),a in scene_by_stage.items() if sk==key or st+'/'+sk==key];assert len(found)==1,(key,len(found));return found[0]
   a,z=scene(x['from_scene_key']),scene(x['to_scene_key']);es=x.get('evidence') or a['evidence']+z['evidence']
   edges.append({'id':f'craft-link-{i:03}','from':'event-'+a['asset_id'].split('-')[-1],'to':'event-'+z['asset_id'].split('-')[-1],'kind':x['kind'],'label':x['label'],'claim_kind':'inference','evidence':evidence(k,es)})
 graph={'title':f'《{BOOK[k]}》全书场景、伏笔与阶段结构','coverage':[{'source_id':S[k]['source_id'],'revision':S[k]['revision'],'chapter_ids':[c['chapter_id'] for c in S[k]['chapters']],'complete':True}],'nodes':nodes,'edges':edges,'threads':threads,'coverage_note':'全部实际阅读单元有逐单元笔记；章前书目信息另已核对，不算剧情蒸馏。结构父子和阅读顺序不是因果边。'}
 gp=V/f'library/sources/{S[k]["source_id"]}/plot-graph.json';g=save_graph(vault,'source',S[k]['source_id'],graph,load(gp)['revision'] if gp.exists() else None)
 render_graph(g,dest/'plot'/'relations');dump(dest/'plot'/'graph.json',g)
 for b in bs:
  ids={'story',b['stage_id']}|{n['id'] for n in nodes if n.get('parent_id')==b['stage_id']}
  sg={**g,'title':f'《{BOOK[k]}》{b["label"]}','nodes':[n for n in nodes if n['id'] in ids],'edges':[e for e in edges if e['from'] in ids and e['to'] in ids],'threads':[]}
  render_graph(sg,dest/'plot'/'stages'/b['stage_id'])
 # 既有图生成器的段尾空行统一为一个换行。
 for md in (dest/'plot').rglob('plot.md'):write(md,md.read_text(encoding='utf-8'))
 for a in cards:
  body=f'# {a["title"]}\n\n主档 `{a["asset_id"]}` · v{a["revision"]} · {a["scope"]}。返回[全书入口](../README.md)。\n\n'
  for kk,val in a['content'].items():body+='## '+CN.get(kk,kk)+'\n\n'+prose(val)+'\n\n'
  body+='## 来源证据\n\n'+loc(a['evidence']).replace('(chapter-index.md','(../chapter-index.md')+'\n\n## 你的评价\n\n尚未填写；研究解释没有自动成为你的风格标准。\n'
  write(dest/'cards'/f'{a["asset_id"]}.md',body)
 for typ,fn,title in [('character','characters','人物阶段档案'),('scene','scenes','场景因果卡'),('pattern','patterns','可迁移机制卡')]:
  group=[a for a in cards if a['asset_type']==typ];write(dest/f'{fn}.md',f'# 《{BOOK[k]}》{title}\n\n{len(group)}张本次全书研究卡；旧研究另保留。\n\n'+'\n'.join(f'- [{a["title"]}](cards/{a["asset_id"]}.md) · v{a["revision"]}' for a in group))
 counts={typ:sum(a['asset_type']==typ for a in cards) for typ in ['character','scene','pattern']}
 summary={'source_id':S[k]['source_id'],'source_revision':S[k]['revision'],'actual_reading_units':len(units),'indexed_segments':len(S[k]['chapters']),'stages':len(bs),'cards':counts,'questions_by_stage_key':len(ledger),'question_observations':len(history),'thread_observations':len(thistory),'graph_threads':len(threads),'graph_nodes':len(nodes),'graph_relations':len(edges),'graph_revision':g['revision'],'full_text_read':True,'user_review':'pending','original_projects_created':0}
 dump(dest/'coverage.json',summary)
 write(dest/'README.md',f'# 《{BOOK[k]}》全书蒸馏\n\n已完整阅读并保存{len(units)}个实际阅读单元、{len(bs)}个研究阶段的九维观察。阶段为研究分段，不是原著卷。原文事实、文学解释、抽象机制和个人评价分别保存。\n\n| 内容 | 入口 |\n|---|---|\n| 全书九维与人物弧 | [综合报告](book-synthesis.md) |\n| 缩放全书结构图 | [全书地图](plot/map/index.html) |\n| 节点、关系与证据 | [剧情阅读器](plot/relations/index.html) |\n| 人物 | [人物阶段档案](characters.md) |\n| 场景 | [场景因果卡](scenes.md) |\n| 方法 | [机制卡](patterns.md) |\n| 每章发生了什么 | [逐单元记录](chapter-notes.md) |\n| 伏笔与误认 | [问题历史](question-ledger.md) / [结局核对](ending-audit.md) |\n| 精确定位 | [章节索引](chapter-index.md) |\n\n## 分段九维研究\n\n'+'\n'.join(f'- 单元{b["unit_start"]}–{b["unit_end"]}：[{b["label"]}](stages/{b["stage_id"]}.md) · [阶段图](plot/stages/{b["stage_id"]}/index.html)' for b in bs)+'\n\nHTML下载后可离线打开；Markdown可在GitHub直接阅读。所有卡片仍待你审阅，原文全文留本机私有来源目录。')
 return summary
if __name__=='__main__':
 # 完成条件前置检查，避免半途给未读作品写complete。
 selected=sys.argv[1:] or list(BOOK)
 for k in selected:batches(k)
 v=Cached(V);result=load(O/'coverage.json') if (O/'coverage.json').exists() else {}
 result.update({k:build(k,v) for k in selected});assert digest(v.source_cache)==digest(Vault._sources(v))
 v.build_views();dump(O/'coverage.json',result);dump(O/'validation/rebuild-result.json',result);print(json.dumps(result,ensure_ascii=False))
