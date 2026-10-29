from pathlib import Path
import json,sys,collections
sys.stdout.reconfigure(encoding='utf-8')
P=Path(__file__).parent;S=json.loads((P/'sources.json').read_text(encoding='utf-8'));DIMS={'worldbuilding','characters','plot','style','narrative','dialogue','pacing','themes','continuity'}
errors=[];stats={};names={};batches=[]
def walk(obj):
 if isinstance(obj,dict):
  for key,v in obj.items():
   if key.endswith('evidence'):
    assert isinstance(v,list)
    for e in v:
     if not isinstance(e,dict) or 'chapter_id' not in e:errors.append([file.name,'bad evidence',e]);continue
     c=chap.get(e['chapter_id'])
     if not c or not c['start_line']<=e.get('start_line',c['start_line'])<=e.get('end_line',c['end_line'])<=c['end_line']:errors.append([str(file.relative_to(P)),'out of bounds',e])
   else:walk(v)
 elif isinstance(obj,list):
  for v in obj:walk(v)
for k,folders in [('z',['z','z-b','z-c','z-c2','z-d']),('l',['l-a','l-b'])]:
 chap={c['chapter_id']:c for c in S[k]['chapters']};units=[];ns=collections.defaultdict(set);st=collections.Counter()
 for folder in folders:
  for file in sorted((P/folder).glob('batch-*.json')):
   b=json.loads(file.read_text(encoding='utf-8'));batches.append(b)
   if set(b['dimensions'])!=DIMS or not all(b['dimensions'].values()):errors.append([str(file),'missing dimensions'])
   ords=[u['ordinal'] for u in b['units']]
   if ords!=list(range(b['unit_start'],b['unit_end']+1)):errors.append([str(file),'unit gap'])
   for u in b['units']:
    original=S[k]['units'][u['ordinal']-1]
    if u['unit_id']!=original['unit_id']:errors.append([str(file),'wrong unit',u['ordinal']])
   for c in b['characters']:ns[c['name']].add(c['key'])
   scene_keys={s['key'] for s in b['scenes']}
   for p in b['patterns']:
    if not p.get('scene_keys'):errors.append([str(file.relative_to(P)),'pattern without scene_keys',p['key']])
    elif not set(p['scene_keys'])<=scene_keys:errors.append([str(file.relative_to(P)),'pattern dangling scene_keys',p['key'],p['scene_keys']])
   for typ in ['characters','scenes','patterns','questions','threads']:st[typ]+=len(b[typ])
   st['batches']+=1;units+=ords;walk(b)
 stats[k]={**st,'saved_units':len(units),'gaps':[n for n in range(1,len(S[k]['units'])+1) if n not in units], 'duplicates':[v for v,n in collections.Counter(units).items() if n>1]}
 names[k]={name:sorted(keys) for name,keys in ns.items()}
(P/'staging-audit.json').write_text(json.dumps({'errors':errors,'stats':stats,'names':names},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'errors':errors,'stats':{k:{kk:vv for kk,vv in v.items() if kk!='gaps'}|{'gap_count':len(v['gaps'])} for k,v in stats.items()},'different_key_same_name':{k:{n:ks for n,ks in d.items() if len(ks)>1} for k,d in names.items()}},ensure_ascii=False))
if errors:sys.exit(1)
