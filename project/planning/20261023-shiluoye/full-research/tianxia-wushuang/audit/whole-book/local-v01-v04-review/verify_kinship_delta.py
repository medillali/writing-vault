"""核主审指定亲属误判修订，原历史记录与其余59项不动。"""
import hashlib
import json
from pathlib import Path

here=Path(__file__).resolve().parent
before=json.loads((here/'before-v04-part03-kinship.json').read_text(encoding='utf-8'))
after=json.loads((here/'adjudications-local-v04-part03.json').read_text(encoding='utf-8'))
changed=[n['candidate_id'] for o,n in zip(before,after) if o!=n]
assert len(before)==len(after)==60
assert changed==['v04-local-chapter_unresolved_index-047-02'],changed
old=next(x for x in before if x['candidate_id']==changed[0])
new=next(x for x in after if x['candidate_id']==changed[0])
for key in ('candidate_id','volume','original_path','original_field','original_index','atomic_index','original_record','title','original_evidence'):
    assert old.get(key)==new.get(key),key
result={'status':'passed','changed_candidate_ids':changed,'unchanged_records':59,'historical_original_record_unchanged':True,'reason':'实际全文复读raw653/694并完整读取142—145派生notes，未见北冥/鬼谷血缘证，删除多余亲兄妹断言。','full_source_rereads':[{'chapter':653,'start_line':55558,'end_line':55609,'reader':'/root/zongheng_vol05_full'},{'chapter':694,'start_line':58439,'end_line':58511,'reader':'/root/zongheng_vol05_full'}],'before':old,'after':new,'outputs':{name:hashlib.sha256((here/name).read_bytes()).hexdigest() for name in ('adjudications-local-v04-part03.json','adjudications-local-v04-part03.md')}}
(here/'delta-v04-part03-kinship.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k not in ('before','after','reason')},ensure_ascii=False))
