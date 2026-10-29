"""记录本轮不应改变的其他作品与人工字段，供最终核验。"""
import hashlib
import json
from pathlib import Path
from persist import ROOT,HERE,SID

output=HERE/'initial-snapshot.json'
if output.exists():
    raise SystemExit('已有本轮基线，拒绝覆盖')
v=ROOT/'writing-vault'
protected={};unchanged={}
for kind in ['characters','scenes','patterns']:
    for p in (v/'library'/kind).glob('*.json'):
        a=json.loads(p.read_text(encoding='utf-8'))
        protected[a['asset_id']]={k:a[k] for k in ['user_notes','favorite','review_status']}
        if not any(e['source_id']==SID for e in a['evidence']):
            unchanged[p.relative_to(v).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
for p in (v/'library/sources').glob('*/plot-graph.json'):
    if p.parent.name!=SID:unchanged[p.relative_to(v).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
for folder in ['library/views/plots/'+SID]:
    for p in (v/folder).rglob('*'):
        if p.is_file():unchanged[p.relative_to(v).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
p=v/'library/views/四书实测.html'
unchanged[p.relative_to(v).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
output.write_text(json.dumps({'human_fields':protected,'unchanged_files':unchanged},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'assets_with_protected_fields':len(protected),'unchanged_files':len(unchanged)}))
