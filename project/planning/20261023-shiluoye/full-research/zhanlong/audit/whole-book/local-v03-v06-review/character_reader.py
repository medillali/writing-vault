"""只读人物接口，按实际执行范围另存接读日志；不生成文学结论。"""
from pathlib import Path
import json,hashlib,sys,datetime
sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent;A=H.parent;R=A.parents[5]
# 使用显式工作区定位，避免层级猜测混入正式路径。
R=Path('C:/Users/Administrator/Documents/ChatGPT/Novel');F=R/'writing-vault/library/reports/zhanlong'
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def emit(x):print(json.dumps(x,ensure_ascii=False,indent=2))
mode=sys.argv[1]
if mode=='schema':
 p=R/'.planning/20261023-shiluoye/full-research/tianxia-wushuang/audit/whole-book/character-arc-audit-draft.json';d=load(p)
 row=d['characters'][0]
 emit({'top_keys':list(d),'count':len(d['characters']),'character_keys':list(row),'example_non_evidence':{k:v for k,v in row.items() if k!='evidence'},'evidence_schema_example':row['evidence'][:1]})
elif mode=='pin':
 paths=[]
 for v in range(1,7):
  paths += [F/f'vol{v:02d}-{s}' for s in ['analysis.json','cards.json','graph.json','handoff.md']]
 paths += [F/'vol02-primary-corrections.json',F/'vol03-note-corrections.json']
 paths += list((F/'audit').glob('priority-corrections-*.json'))
 paths += list((F/'audit/primary-rereads').glob('*.json'))
 paths += list((F/'audit/primary-ending-reread').glob('*.json'))
 out=dict(status='inputs_pinned_before_character_derived_read',actual_reviewer='zongheng_vol05_full',pinned_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),sha256={p.relative_to(R).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in paths if p.exists()},limits='输入哈希不是已读声明；逐步完整接读对应范围另留记录，原文归属不变。')
 p=A/'character-arc-input-manifest.json';assert not p.exists();p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');emit(out)
elif mode in ['inventory','names','cards','compactcards']:
 v=int(sys.argv[2]);d=load(F/f'vol{v:02d}-cards.json')
 if isinstance(d,list):items=[x for x in d if x.get('asset_type')=='character' or x.get('kind')=='character' or x.get('card_type')=='character' or x.get('type')=='character']
 else:items=d.get('characters',d.get('character_cards',[]))
 if mode=='names':print('\n'.join(f'{v}:{n} {r["title"]}' for n,r in enumerate(items,1)))
 elif mode=='inventory':emit({'volume':v,'characters':len(items),'items':[{k:r.get(k) for k in ['origin_key','title']} for r in items]})
 else:
  lo,hi=map(int,sys.argv[3:5]);print(f'BEGIN formal vol{v:02d} character cards {lo}—{hi}/{len(items)}')
  for n,r in enumerate(items[lo-1:hi],lo):
   print(f'BEGIN character {v}:{n}')
   full=dict(asset_id=r.get('asset_id'),origin_key=r.get('origin_key'),title=r.get('title'),content=r.get('content'),evidence_format='[raw,start_line,end_line,claim_kind]; 全部均固定SID/rev',evidence=[[int(e['chapter_id'][3:]),e['start_line'],e['end_line'],e['claim_kind']] for e in r.get('evidence',[])],source_id='src-20f2d16e3d1b472fa4b230ab0e1770c9',revision='61ab0b114c76446fda554abfafdac8c432cd88afaba7c2541f4473a3902134e3')
   if mode=='compactcards':print(json.dumps(full,ensure_ascii=False,separators=(',',':')))
   else:emit(full)
   print(f'END character {v}:{n}')
  print('END character cards')
elif mode=='analysis-keys':
 v=int(sys.argv[2]);d=load(F/f'vol{v:02d}-analysis.json');emit({k:(list(x) if isinstance(x,dict) else f'{type(x).__name__}: {len(x) if hasattr(x,"__len__") else "scalar"}') for k,x in d.items()})
elif mode=='states':
 v,lo,hi=map(int,sys.argv[2:5]);d=load(F/f'vol{v:02d}-analysis.json');rows=d.get('stage_characters',d.get('character_states',[]));print(f'BEGIN vol{v:02d} states {lo}—{hi}/{len(rows)}')
 for i,row in enumerate(rows[lo-1:hi],lo):print(f'STATE {v}:{i} '+json.dumps(row,ensure_ascii=False,separators=(',',':')))
 print('END states')
elif mode=='states-diff':
 v=int(sys.argv[2]);d=load(F/f'vol{v:02d}-analysis.json');rows=d.get('stage_characters',d.get('character_states',d.get('major_character_states',[])));cards=load(F/f'vol{v:02d}-cards.json')
 if not isinstance(cards,list):cards=cards.get('characters',cards.get('character_cards',[]))
 by={x.get('origin_key'):x for x in cards}
 print(f'BEGIN literal states/card difference vol{v:02d}; rows={len(rows)}; identical strings already read in cards are not reprinted; no interpretation generated')
 for i,row in enumerate(rows,1):
  card=by.get(row.get('origin_key'));content=(card or {}).get('content',{});out={};same=[]
  for k,x in row.items():
   if k in ['origin_key','claim_kind','title']:continue
   if k=='name' and x==(card or {}).get('title'):same.append('name=card.title');continue
   if k=='evidence':
    if x==(card or {}).get('evidence'):same.append('evidence');continue
    out[k]=[[int(e['chapter_id'][3:]),e['start_line'],e['end_line'],e.get('claim_kind')] for e in x];continue
   if x==content.get(k):same.append(k)
   else:out[k]=x
  if out:print(json.dumps(dict(index=i,title=row.get('title',row.get('name')),same_fields=same,remaining_actual_values=out),ensure_ascii=False,separators=(',',':')))
 print('END literal differences')
