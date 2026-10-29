"""已审组只定向两处定位纠正，保before及逐值差异。"""
import pathlib,json,hashlib
H=pathlib.Path(__file__).resolve().parent;p=H/'adjudications-history-v05-remaining.json'
before=json.loads(p.read_text(encoding='utf-8'));oldsha=hashlib.sha256(p.read_bytes()).hexdigest()
old=H/'reviewed-batches/adjudications-history-v05-before-two-locator-corrections.json'
assert not old.exists();old.write_bytes(p.read_bytes())
after=json.loads(json.dumps(before));ids=['v05-question-011','v05-question-015']
x=next(x for x in after if x['candidate_id']==ids[0]);x['rationale']=x['rationale'].replace('1330前后家庭相见','1342家庭相见');x['later_chapters']=[1342 if c==1330 else c for c in x['later_chapters']]
x=next(x for x in after if x['candidate_id']==ids[1]);x['rationale']=x['rationale'].replace('1313本人愿离烛龙','1314本人愿离烛龙');x['later_chapters']=sorted(set(x['later_chapters']+[1314]))
assert [x['candidate_id'] for x,y in zip(before,after) if x!=y]==ids
p.write_text(json.dumps(after,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
newsha=hashlib.sha256(p.read_bytes()).hexdigest()
delta=dict(before_sha256=oldsha,after_sha256=newsha,changed_ids=ids,unchanged_other_items=34,changes=[dict(candidate_id=x['candidate_id'],before=x,after=y) for x,y in zip(before,after) if x!=y])
(H/'history05-two-locator-delta.json').write_text(json.dumps(delta,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
# 同步可读页与保存器文字；不调用保存器重生已签其他字段。
for name in ['historical-reviewed-vol05-remaining.md','write_history05_remaining.py']:
 q=H/name;s=q.read_text(encoding='utf-8').replace('1330前后家庭相见','1342家庭相见').replace('1313本人愿离烛龙','1314本人愿离烛龙').replace('[892,894,1330,1591]','[892,894,1342,1591]').replace('[837,900,1313,1315,1324,1413,1526]','[837,900,1313,1314,1315,1324,1413,1526]')
 if name.endswith('.md'):
  blocks=s.split('## ')
  for i,b in enumerate(blocks):
   if b.startswith(ids[0]+' '):blocks[i]=b.replace('892, 894, 1330, 1591','892, 894, 1342, 1591')
   if b.startswith(ids[1]+' '):blocks[i]=b.replace('837, 900, 1313, 1315, 1324, 1413, 1526','837, 900, 1313, 1314, 1315, 1324, 1413, 1526')
  s='## '.join(blocks)
 q.write_text(s,encoding='utf-8')
print(oldsha,newsha)
