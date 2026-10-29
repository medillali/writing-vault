from character_arc_interface import cards,all_states,locator_compact
from synthesis_common import *
import sys
mode=sys.argv[1]
names=sys.argv[2:]
if mode=='card-context':
 for v in range(1,7):
  for i,c in enumerate(cards(v)):
   if c.get('asset_type',c.get('type')) not in [None,'character']:continue
   if any(n in json.dumps(c.get('content',{}),ensure_ascii=False) or n in c.get('title','') for n in names):
    print('FULL MATCHING CARD',v,i+1,json.dumps(locator_compact({k:c.get(k) for k in ['title','asset_id','origin_key','content','evidence']}),ensure_ascii=False))
elif mode=='source-hits':
 lines=(ROOT/'writing-vault/private-sources/normalized/sources'/S['source_id']/(S['revision']+'.txt')).read_text(encoding='utf-8').splitlines()
 start=int(names.pop(0))
 for n in names:
  hits=[]
  for raw,c in CH.items():
   if raw<start:continue
   got=[i for i in range(c['start_line'],c['end_line']+1) if n in lines[i-1]]
   if got:hits.append({'raw':raw,'lines':got})
  print('LOCATOR ONLY',n,json.dumps(hits,ensure_ascii=False))
elif mode=='source-range':
 lines=(ROOT/'writing-vault/private-sources/normalized/sources'/S['source_id']/(S['revision']+'.txt')).read_text(encoding='utf-8').splitlines()
 lo,hi=map(int,names);assert hi-lo<150
 print('BEGIN TARGETED RANGE',lo,hi)
 for i in range(lo,hi+1):print(f'L{i}: {lines[i-1]}')
 print('END TARGETED RANGE',lo,hi)
elif mode=='name-contexts':
 lines=(ROOT/'writing-vault/private-sources/normalized/sources'/S['source_id']/(S['revision']+'.txt')).read_text(encoding='utf-8').splitlines()
 start=int(names.pop(0))
 for n in names:
  for raw,c in CH.items():
   if raw<start:continue
   ids=set()
   for i in range(c['start_line'],c['end_line']+1):
    if n in lines[i-1]:ids.update(range(max(c['start_line'],i-2),min(c['end_line'],i+2)+1))
   if ids:
    print('BEGIN NAME CONTEXTS NOT FULL CHAPTER',n,raw)
    for i in sorted(ids):print(f'L{i}: {lines[i-1]}')
    print('END NAME CONTEXTS',n,raw)
