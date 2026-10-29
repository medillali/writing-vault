import json,pathlib,hashlib
V=pathlib.Path(__file__).resolve().parent;B=V.parent;R=V.parents[4];sp=B/'source.json';cp=R/'writing-vault/library/reports/collection/reading-units.json';s=json.loads(sp.read_text(encoding='utf-8'));c=json.loads(cp.read_text(encoding='utf-8'))[s['source_id']];v=next(v for v in s['volumes'] if v['volume']==2);cm={u['unit_id']:u for u in c['units']}
assert c['source_revision']==s['revision']
for u in v['units']:
 other=cm[u['unit_id']]
 for k in ['segment_ids','kind','start_line','end_line']:assert u[k]==other[k]
x=dict(status='scope_verified_actual_reading_in_reader_state',source_id=s['source_id'],revision=s['revision'],source_index_sha256=hashlib.sha256(sp.read_bytes()).hexdigest(),reading_units_sha256=hashlib.sha256(cp.read_bytes()).hexdigest(),collection_mapping_matches=True,volume=2,raw_first='ch-0252',raw_last='ch-0504',indexed_segments=253,body_units=252,volume_headers=1,multi_segment_units=[],reader='/root/zongheng_vol04_full',read_method='逐1—2片BEGIN-END完整原文，截断补读后才计full_text_read；每2—4片手写笔记/保存state/log。',next_assignment=dict(volume=5,raw_first='ch-0969',raw_last='ch-1179',body_units=210,indexed_segments=211,status='metadata_checked_only_no_body_read'),boundaries=['只写zhanlong/vol02与后续vol05','前卷研究不计本代理亲读','无双全部研究冻结不再修改','unresolved不机械制造每章研究边界，但真正剧情/承诺/身份/规则未明保全'])
(V/'reading-scope.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
