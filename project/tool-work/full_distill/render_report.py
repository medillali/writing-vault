"""从已完成的研究 JSON 排出人读报告，不补写任何研究结论。"""
import argparse
import json
from pathlib import Path

HERE=Path(__file__).parent
LABELS={
 'worldbuilding':'世界构建','characters':'人物','plot':'情节','style':'文风','narrative':'叙事','dialogue':'对话','pacing':'节奏','themes':'主题','continuity':'连续性',
 'claim':'主张','mechanism':'机制','application':'原创迁移','limitation':'边界','claim_kind':'结论性质',
 'name':'人物','aliases':'异名','summary':'概述','goal':'目标','conflict':'冲突','arc_change':'本集变化','relationships':'关系','knowledge_limits':'认知边界',
 'key':'记录键','title':'标题','obstacle':'阻碍','choice':'选择','consequence':'后果','state_change':'状态变化','why_it_works':'有效原因','applicability':'适用条件','failure_mode':'失效条件',
 'steps':'迁移步骤','scene_keys':'依赖场景','chapter_id':'章节','observation':'逐章观察','dimensions_checked':'已检查维度',
 'from':'起点','to':'终点','kind':'关系类型','label':'说明','knowledge':'认知记录','observer':'观察者','state':'认知状态','belief':'认知内容',
 'status':'状态','question':'问题','event_keys':'涉及事件','edge_pairs':'涉及关系','resolution_note':'当前回收程度','reason':'原因','evidence':'证据',
 'description':'说明','revision':'来源修订','source_id':'来源'
}
VALUES={'fact':'事实','inference':'推断','synthesis':'机制抽象','plan':'计划','unknown':'未知','suspects':'怀疑','knows':'知道','misbelieves':'错误相信','main':'主线','subplot':'支线','hidden':'暗线','open':'未回收','partial':'部分回收','resolved':'已回收','abandoned':'已放弃','cause':'因果','setup':'铺垫','reveal':'揭示','misdirection':'误导','reversal':'反转','echo':'呼应','payoff':'回收'}

def text(value):
 if isinstance(value,str):return VALUES.get(value,LABELS.get(value,value))
 return str(value)

def evidence(items):
 return '；'.join(f"{e['chapter_id']} L{e['start_line']}–{e['end_line']}" for e in items)

def fields(obj,skip=()):
 out=[]
 for key,value in obj.items():
  if key in skip:continue
  label=LABELS.get(key,key)
  if key=='evidence':out.append(f'- {label}：{evidence(value)}')
  elif isinstance(value,list):
   if not value:out.append(f'- {label}：无。')
   elif all(not isinstance(x,(dict,list)) for x in value):out.append(f'- {label}：'+'；'.join(text(x) for x in value))
   else:
    out.extend(['',f'**{label}**',''])
    for item in value:
     if isinstance(item,dict):out += fields(item)+['']
     else:out.append('- '+' → '.join(text(x) for x in item))
  elif isinstance(value,dict):out.extend(['',f'**{label}**','',*fields(value)])
  else:out.append(f'- {label}：{text(value)}')
 return out

def render(n):
 r=json.loads((HERE/f'vol{n:02d}.json').read_text(encoding='utf-8'))
 out=[f"# {r['title']}：九维研究稿",'',
      f"来源：{r['source_id']}；修订：{r['revision']}。",'',
      f"覆盖：{len(r['chapter_ids'])} 个索引段，完整阅读 {len(r['read_parts'])} 块。包含集标题等非叙事段，不能将索引数等同正文章数。",'',
      '这是基于本集实际全文阅读的分析草稿。事实、推断和机制抽象分别标注；未读后文不作为已确认依据。','','## 本集概括','',r['overview'],'',
      '## 九维分析','']
 for dimension,items in r['dimensions'].items():
  out += [f'### {LABELS[dimension]}','']
  for i,item in enumerate(items,1):out += [f"#### {i}. {item['claim']}",'',*fields(item,('claim',)),'']
 for key,title in [('chapter_notes','逐章覆盖与观察'),('characters','人物变化'),('scenes','精选场景'),('patterns','可迁移机制'),('events','关键事件与认知'),('edges','事件关系'),('threads','主线、支线与暗线'),('questions','待核验事项'),('revisions_to_earlier','对前序判断的修订')]:
  out += [f'## {title}','']
  for i,item in enumerate(r[key],1):
   if isinstance(item,dict):
    heading=item.get('title',item.get('name',item.get('question',item.get('chapter_id',f'记录 {i}'))))
    out += [f'### {heading}','',*fields(item,('title','name')),'']
   else:out += [f'{i}. {item}','']
  if not r[key]:out+=['本集无新增记录。','']
 path=HERE/f'vol{n:02d}.md'
 path.write_text('\n'.join(out).rstrip()+'\n',encoding='utf-8')
 print(path)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('volume',type=int);a=p.parse_args();render(a.volume)
