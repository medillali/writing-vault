from pathlib import Path
import json
P=Path(__file__).parent
BOOK=json.loads((P.parent/'sources.json').read_text(encoding='utf-8'))['l']
def ev(ch,a,b):return {'chapter_id':f'ch-{ch:04d}','start_line':a,'end_line':b}
def save(number,start,end,label,notes,dimensions,characters,scenes,patterns,threads,questions):
 units=[]
 for ordinal,n in zip(range(start,end+1),notes):
  u=BOOK['units'][ordinal-1];units.append({'ordinal':ordinal,'unit_id':u['unit_id'],'title':u['title'],'events':n[0],'state_changes':n[1],'open_questions':n[2],'evidence':[ev(int(u['unit_id'][3:]),u['start_line'],u['end_line'])]})
 assert len(units)==end-start+1
 obj={'source_key':'l','source_id':BOOK['source_id'],'unit_start':start,'unit_end':end,'label':label,'units':units,'dimensions':dimensions,'characters':characters,'scenes':scenes,'patterns':patterns,'threads':threads,'questions':questions}
 (P/f'batch-{number:02d}.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
 (P/'progress.md').write_text(f'# 《网游之练级专家》后半全文阅读\n\n已逐段阅读并保存：194..{end}。下一单元：{end+1}。\n\n阶段：{label}。单次输出截断均缩小范围补读；检索收据不等同于模型阅读证明。\n',encoding='utf-8')
def claim(s,*e,kind='fact'):return {'claim':s,'kind':kind,'evidence':list(e)}
def char(key,name,summary,goals,changes,relations,knowledge,e,anomalies=[]):return {'key':key,'name':name,'aliases':[],'summary':summary,'goals':goals,'changes':changes,'relationships':relations,'knowledge':knowledge,'source_anomalies':anomalies,'evidence':e}
def scene(key,title,summary,goal,obstacle,choice,consequence,state,why,app,fail,e):return dict(key=key,title=title,summary=summary,goal=goal,obstacle=obstacle,choice=choice,consequence=consequence,state_change=state,why_it_works=why,applicability=app,failure_mode=fail,evidence=e)
def pattern(key,title,summary,steps,app,fail,scene_keys,e):return dict(key=key,title=title,summary=summary,steps=steps,applicability=app,failure_mode=fail,scene_keys=scene_keys,evidence=e)
def thread(key,title,kind,status,state,ords,e):return dict(key=key,title=title,kind=kind,status=status,state=state,unit_ordinals=ords,evidence=e)
def question(key,q,status,answer,setup,res=[],kind='unresolved'):return dict(key=key,question=q,status=status,answer=answer,setup_evidence=setup,resolution_evidence=res,kind=kind)
