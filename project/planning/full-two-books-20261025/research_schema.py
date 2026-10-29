from pathlib import Path
import json
P=Path(__file__).parent;BOOKS=json.loads((P/'sources.json').read_text(encoding='utf-8'))
DIMS=['worldbuilding','characters','plot','style','narrative','dialogue','pacing','themes','continuity']
def ev(key,a,b=None):
 b=a if b is None else b;out=[]
 for c in BOOKS[key]['chapters']:
  lo=max(a,c['start_line']);hi=min(b,c['end_line'])
  if lo<=hi:out.append({'chapter_id':c['chapter_id'],'start_line':lo,'end_line':hi})
 assert out and out[0]['start_line']==a and out[-1]['end_line']==b
 return out
def unit(key,ordinal,event,state,a,b,questions=None):
 u=BOOKS[key]['units'][ordinal-1]
 return {'ordinal':ordinal,'unit_id':u['unit_id'],'title':u['title'],'events':[event],'state_changes':[state],'open_questions':questions or [],'evidence':ev(key,a,b)}
def finding(key,claim,a,b,kind='inference'):return {'claim':claim,'kind':kind,'evidence':ev(key,a,b)}
def save(folder,number,key,label,units,dimensions,characters,scenes,patterns,threads,questions):
 assert set(dimensions)==set(DIMS) and all(dimensions.values())
 ords=[u['ordinal'] for u in units];assert ords==list(range(min(ords),max(ords)+1))
 data={'source_key':key,'unit_start':min(ords),'unit_end':max(ords),'label':label,'units':units,'dimensions':dimensions,'characters':characters,'scenes':scenes,'patterns':patterns,'threads':threads,'questions':questions}
 dest=P/folder/f'batch-{number:02}.json';dest.parent.mkdir(parents=True,exist_ok=True)
 dest.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 (dest.parent/'progress.md').write_text(f'# root后半研究进度\n\n已完整读并保存至《贼胆》单元{max(ords)}；本文件夹负责233–463。下一单元{max(ords)+1}。\n\n最近阶段：{label}。原始检索回执仅表示正文被取出；完整研究覆盖以batch的逐单元记录为准。\n',encoding='utf-8')
 print('saved',dest.name,min(ords),max(ords))
