import pathlib,json,hashlib,sys
sys.stdout.reconfigure(encoding='utf-8')
root=pathlib.Path(__file__).resolve().parents[3];vault=root/'writing-vault';work=pathlib.Path(__file__).resolve().parent
assets={}
for kind in ['characters','scenes','patterns']:
    for p in (vault/'library'/kind).glob('*.json'):
        record=json.loads(p.read_text(encoding='utf-8'))
        assets[record['asset_id']]={'revision':record['revision'],'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'user_notes':record['user_notes'],'favorite':record['favorite'],'review_status':record['review_status'],'path':p.relative_to(vault).as_posix()}
runs=[]
for p in (vault/'exchanges/runs').glob('*.json'):
    r=json.loads(p.read_text(encoding='utf-8'))
    runs.append({'run_id':r['run_id'],'source_id':r['source_id'],'completed_count':len(r.get('completed_chapters',[])),'pending_count':len(r.get('pending_chapters',[]))})
result={'date':'2026-10-25','assets':assets,'runs':runs}
destination=work/'baseline.json';assert not destination.exists()
destination.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'baseline_assets':len(assets),'runs':runs},ensure_ascii=False))
