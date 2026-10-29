"""只核本目录一个主审指定修订，不写主池或正式库。"""
import hashlib
import json
from pathlib import Path

here = Path(__file__).resolve().parent
before = json.loads((here/'before-v04-part01-city10.json').read_text(encoding='utf-8'))
after = json.loads((here/'adjudications-local-v04-part01.json').read_text(encoding='utf-8'))
changed = [new['candidate_id'] for old,new in zip(before,after) if old != new]
assert len(before)==len(after)==60
assert changed==['v04-local-issue_log-037-02'], changed
old = next(x for x in before if x['candidate_id']==changed[0])
new = next(x for x in after if x['candidate_id']==changed[0])
for key in ('candidate_id','volume','original_path','original_field','original_index','atomic_index','original_record','title','original_evidence'):
    assert old.get(key)==new.get(key), key
result={'status':'passed','changed_candidate_ids':changed,'unchanged_records':59,'historical_original_record_unchanged':True,'reason':'root新发现935系统MVP使暗月升10，独立完整读该原读者notes后补证；不倒写796仍9级。','before':old,'after':new,'outputs':{name:hashlib.sha256((here/name).read_bytes()).hexdigest() for name in ('adjudications-local-v04-part01.json','adjudications-local-v04-part01.md')}}
(here/'delta-v04-part01-city10.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k not in ('before','after')},ensure_ascii=False))
