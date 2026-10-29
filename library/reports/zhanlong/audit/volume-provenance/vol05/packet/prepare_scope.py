"""核对分配范围及合章元数据，不读取正文。"""
import pathlib,json,hashlib
V=pathlib.Path(__file__).resolve().parent;B=V.parent;R=V.parents[4]
s=json.loads((B/'source.json').read_text(encoding='utf-8'));cp=R/'writing-vault/library/reports/collection/reading-units.json';c=json.loads(cp.read_text(encoding='utf-8'))[s['source_id']]
assert s['source_id']=='src-20f2d16e3d1b472fa4b230ab0e1770c9' and s['revision']=='61ab0b114c76446fda554abfafdac8c432cd88afaba7c2541f4473a3902134e3' and c['source_revision']==s['revision']
v=next(x for x in s['volumes'] if x['volume']==5);cm={x['unit_id']:x for x in c['units']};ids=[]
for u in v['units']:
 for k in ['segment_ids','kind','start_line','end_line']:assert u[k]==cm[u['unit_id']][k]
 ids += [seg['chapter_id'] for seg in u['segments']]
assert ids==[f'ch-{i:04d}' for i in range(969,1180)]
out={'status':'scope_verified_only','volume':5,'source_id':s['source_id'],'revision':s['revision'],'source_index_sha256':hashlib.sha256((B/'source.json').read_bytes()).hexdigest(),'reading_units_sha256':hashlib.sha256(cp.read_bytes()).hexdigest(),'collection_mapping_matches':True,'raw_first':ids[0],'raw_last':ids[-1],'indexed_segments':len(ids),'body_units':v['body_units'],'multi_segment_units':[u['unit_id'] for u in v['units'] if len(u['segments'])>1],'reader':'/root/zongheng_vol04_full','prior_reading_boundary':'本代理亲读卷二前段252—404不等已读卷一、三、四；前史若需由正式派生接口读取并注明。卷五仅保本卷阶段，不以后卷倒灌。'}
(V/'reading-scope.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out,ensure_ascii=False));print(json.dumps([x for x in s['chapters'] if x['chapter_id'] in [ids[0],ids[1],ids[-1]]],ensure_ascii=False))
