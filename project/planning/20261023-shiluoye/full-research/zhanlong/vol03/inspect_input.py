"""本卷隔离的只读来源/阅读单位核对；不声明章节已读。"""
from pathlib import Path
import hashlib,json,sys
sys.stdout.reconfigure(encoding='utf-8')
HERE=Path(__file__).resolve().parent
WS=next(p for p in HERE.parents if (p/'writing-vault').is_dir())
book=HERE.parent
src=json.loads((book/'source.json').read_text(encoding='utf-8-sig'))
print('BEGIN SOURCE METADATA')
print(json.dumps({k:v for k,v in src.items() if k not in ['chapters','volumes']},ensure_ascii=False))
print('chapters',len(src['chapters']))
for volume in src['volumes']:
    print(json.dumps({k:v for k,v in volume.items() if k!='units'},ensure_ascii=False))
    if volume.get('volume') in (3,6) or volume.get('number') in (3,6):
        print('unit count',len(volume['units']))
        print(json.dumps({'first_units':volume['units'][:2],'last_units':volume['units'][-2:],
                          'nonstandard_units':[u for u in volume['units'] if len(u.get('segments',[]))!=1]},ensure_ascii=False))
for index in [505,506,507,752,753,1180,1181,1385,1386]:
    print(json.dumps({'raw_index':index,'chapter':src['chapters'][index-1]},ensure_ascii=False))
print('source_file_sha256',hashlib.sha256((book/'source.json').read_bytes()).hexdigest())
assert src['source_id']=='src-20f2d16e3d1b472fa4b230ab0e1770c9'
assert src['revision']=='61ab0b114c76446fda554abfafdac8c432cd88afaba7c2541f4473a3902134e3'
assert hashlib.sha256(Path(src['normalized_path']).read_bytes()).hexdigest()==src['revision']
units=json.loads((WS/'writing-vault/library/reports/collection/reading-units.json').read_text(encoding='utf-8-sig'))
print('READING_UNITS_KEYS',list(units) if isinstance(units,dict) else 'list')
def find(v):
    if isinstance(v,dict):
        if v.get('source_id')==src['source_id']:
            print(json.dumps({k:x for k,x in v.items() if k!='units'},ensure_ascii=False))
            return
        for k,x in v.items():
            if k in [src['source_id'],'zhanlong']:
                picked=[u for u in x['units'] if 505<=int(u['unit_id'][3:])<=753 or 1180<=int(u['unit_id'][3:])<=1386]
                print(json.dumps({k:{key:value for key,value in x.items() if key!='units'},'assigned_unit_count':len(picked),'assigned_multi_segment_units':[u for u in picked if len(u['segment_ids'])!=1]},ensure_ascii=False))
                source_units=[u for v in src['volumes'] if v['volume'] in [3,6] for u in v['units']]
                assert [(u['unit_id'],u['segment_ids'],u['kind'],u['start_line'],u['end_line']) for u in picked]==[(u['unit_id'],u['segment_ids'],u['kind'],u['start_line'],u['end_line']) for u in source_units]
                print('assigned_collection_mapping_matches_source True'); return
            if isinstance(x,(dict,list)): find(x)
    elif isinstance(v,list):
        for x in v: find(x)
find(units)
print('END SOURCE METADATA')
