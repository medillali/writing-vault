"""保存手写全书综合；只装配证据与结构，不生成文学判断。"""
import json, hashlib, datetime
from pathlib import Path
P=Path(__file__).parent
B=P.parent.parent.parent
ROOT=B.parents[3]
F=ROOT/'writing-vault/library/reports/zhanlong'
S=json.loads((B/'source.json').read_text(encoding='utf-8'))
CH={int(c['chapter_id'].split('-')[1]):c for c in S['chapters']}
DIMENSIONS=['worldbuilding','characters','plot','style','narrative','dialogue','pacing','themes','continuity']
LABELS=dict(zip(DIMENSIONS,['世界观','人物','情节','文风','叙事','对话','节奏','主题','连续性']))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def text_of(x):
 if isinstance(x,str):return x
 if isinstance(x,dict):return x.get('text',x.get('observation',x.get('claim','')))
 if isinstance(x,list):return '；'.join(text_of(a) for a in x)
 return ''
def ref(n,start=None,end=None,kind='fact'):
 c=CH[n];return {'source_id':S['source_id'],'revision':S['revision'],'chapter_id':c['chapter_id'],'start_line':start or c['start_line'],'end_line':end or c['end_line'],'claim_kind':kind}
def support(v,d,i):
 p=F/f'vol{v:02d}-analysis.json';a=json.loads(p.read_text(encoding='utf-8'));o=a['dimensions'][d][i-1]
 fact=text_of(o.get('textual_fact',o.get('facts',o.get('fact_summary',''))))
 interp=text_of(o.get('observation',o.get('interpretation',o.get('claim',''))))
 return {'volume':v,'dimension':d,'index_zero_based':i-1,'observation_id':o.get('id',f'vol{v:02d}-{d}-{i}'),'reported_fact':fact,'reported_interpretation':interp,'upstream_claim_kind':o.get('claim_kind'),'material_path':str(p.relative_to(ROOT)).replace('\\','/'),'material_sha256':sha(p),'json_pointer':f'/dimensions/{d}/{i-1}','source_reader':'原分卷全文读者见同卷正式read-log；本条为派生材料综合','synthesizer_original_read_scope':'本人原文亲读仅卷1 raw2—151及卷4 raw754—968；卷1尾primary亲读且本人完整读其逐章笔记，其余卷依最终正式研究。'},o
def make(d,num,key,title,claim,facts,mechanism,conditions,limits,transform,late,selectors,extra=(),corrections=()):
 ss=[];ev=[]
 for v,dim,i in selectors:
  su,o=support(v,dim,i);ss.append(su)
  for e in o.get('evidence',[]):
   x={k:e[k] for k in ['source_id','revision','chapter_id','start_line','end_line']};x['claim_kind']='fact';x['research_material_attribution']=f'vol{v:02d}/{dim}/{i}，定位来自正式分卷，非本次新原文阅读';ev.append(x)
 ev.extend(extra);seen=set();out=[]
 for e in ev:
  k=tuple(e[k] for k in ['source_id','revision','chapter_id','start_line','end_line'])
  if k not in seen:seen.add(k);out.append(e)
 row={'id':f'zhanlong-book-{d}-{num:02d}','key':key,'title':title,'claim_kind':'synthesis','claim':claim,'fact_summary':facts,'supporting_observations':ss,'mechanism':mechanism,'conditions':conditions,'limits_and_counterevidence':limits,'originality_transform':transform,'literary_choice':{'take':mechanism,'leave':limits,'claim_kind':'inference','user_approval':False},'late_stage_result':late,'later_tests':{'claim_kind':'synthesis','test':late,'boundary':'全书末期的实际动作与开放状态分别判断；不将终点评语倒填原阶段。'},'evidence':out,'review_status':'draft'}
 if corrections:
  row['priority_corrections']=[{'path':str((F/'audit'/p).relative_to(ROOT)).replace('\\','/'),'sha256':sha(F/'audit'/p),'application':why} for p,why in corrections]
 return row
def save_group(d,rows):
 assert len(rows)==4 and [r['id'] for r in rows]==[f'zhanlong-book-{d}-{i:02d}' for i in range(1,5)]
 p=P/f'synthesis-{d}.json';assert not p.exists(),'已交稳定组不能重生成，请精确delta'
 group={'artifact_type':'derived-book-synthesis-dimension-draft','dimension':d,'label':LABELS[d],'review_status':'draft-awaiting-primary','actual_synthesizer':'/root/zongheng_vol03_full','personal_complete_book_read':False,'rows':rows}
 dump(p,group);render_group(p.with_suffix('.md'),d,rows)
 receipt={'dimension':d,'json':str(p.relative_to(ROOT)).replace('\\','/'),'json_sha256':sha(p),'md_sha256':sha(p.with_suffix('.md')),'observations':4,'status':'stable-awaiting-primary','semantic_generation':'逐条人工撰写，helper仅序列化和取原定位'}
 dump(P/f'synthesis-{d}-receipt.json',receipt)
 stp=P/'reader-state.json';st=json.loads(stp.read_text(encoding='utf-8'));st['synthesis_status']='in-progress';st.setdefault('synthesis_stable_dimensions',[]).append(receipt);dump(stp,st)
 print(json.dumps(receipt,ensure_ascii=False))
def render_rows(rows):
 out=[]
 for r in rows:
  out.extend([f'## {r["title"]}', '', f'`{r["id"]}` · synthesis · 待主审/未获用户审美批准','',r['claim'],'','事实链：'+r['fact_summary'],'','机制：'+r['mechanism'],'','适用条件：'+r['conditions'],'','限制与反证：'+r['limits_and_counterevidence'],'','原创转化：'+r['originality_transform'],'','末期检验：'+r['late_stage_result'],'','上游观察：'+'；'.join(f'卷{s["volume"]}/{s["dimension"]}/{s["index_zero_based"]+1}（{s["material_sha256"][:12]}）' for s in r['supporting_observations']),'','定位：'+'；'.join(f'{e["chapter_id"]} L{e["start_line"]}—{e["end_line"]}' for e in r['evidence']),''])
  if r.get('priority_corrections'):out.extend(['纠正优先：'+'；'.join(x['path']+'：'+x['application'] for x in r['priority_corrections']),''])
  for s in r['supporting_observations']:
   if s.get('reported_fact_boundary'):
    b=s['reported_fact_boundary'];out.extend([f'上游卷{s["volume"]}原事实串的使用边界：'+b['text'],'','边界定位：'+'；'.join(f'{e["chapter_id"]} L{e["start_line"]}—{e["end_line"]}' for e in b['evidence']),''])
 return out
def render_group(p,d,rows):p.write_text('\n'.join([f'# 《斩龙》全书综合 · {LABELS[d]}四条','','材料：六卷最终正式研究；个人亲读范围与分工归属不改变。结构通过不代表文学主审或用户批准。','']+render_rows(rows)),encoding='utf-8')
