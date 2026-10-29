"""分别核两批各一条神泣改版后证，其余对象不变。"""
import hashlib
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
here=Path(__file__).resolve().parent
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
results=[]
for part,target in (('01','v04-local-issue_log-030-01'),('06','v04-local-chapter_unresolved_index-170-02')):
    before=read(here/f'before-v04-part{part}-godcry.json')
    after=read(here/f'adjudications-local-v04-part{part}.json')
    changed=[n['candidate_id'] for o,n in zip(before,after) if o!=n]
    assert len(before)==len(after)==60 and changed==[target],changed
    old=next(x for x in before if x['candidate_id']==target)
    new=next(x for x in after if x['candidate_id']==target)
    for key in ('candidate_id','volume','original_path','original_field','original_index','atomic_index','original_record','title','original_evidence'):
        assert old.get(key)==new.get(key),key
    results.append({'batch':part,'changed_candidate_id':target,'unchanged_records':59,'historical_original_record_unchanged':True,'before':old,'after':new,'outputs':{name:sha(here/name) for name in (f'adjudications-local-v04-part{part}.json',f'adjudications-local-v04-part{part}.md')}})
receipt={'status':'passed','reason':'root新后证860；本代理随后完整读原读者四栏notes确认20码新版实际可用，旧全屏删号形式禁用与后改版分层。','results':results}
(here/'delta-v04-godcry-revision.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':'passed','results':[{k:v for k,v in r.items() if k not in ('before','after')} for r in results]},ensure_ascii=False))
