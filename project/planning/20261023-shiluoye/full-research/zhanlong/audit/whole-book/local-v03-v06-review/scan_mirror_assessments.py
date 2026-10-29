from pathlib import Path
import json,hashlib
H=Path(__file__).resolve().parent;A=H.parent
hits=[];inputs={}
for volume in (3,6):
 for p in sorted(A.glob(f'adjudications-local-v{volume:02d}-batch*.json')):
  inputs[p.name]=hashlib.sha256(p.read_bytes()).hexdigest()
  for row in json.loads(p.read_text(encoding='utf-8')):
   if any(k in row['rationale'] for k in ('武魂','镜像','炼魂')):
    hits.append(dict(file=p.name,candidate_id=row['candidate_id'],rationale=row['rationale'],needs_correction=row['candidate_id'] in ['v06-local-chapter_unresolved_index-0028-01','v06-local-chapter_unresolved_index-0031-01','v06-local-chapter_unresolved_index-0032-01']))
out=dict(status='targeted_assessment_scan_complete',actual_reviewer='zongheng_vol05_full',scope='根目录本代理已交v03/v06批，排除快照及原record/title，仅rationale检查同义后证漏配',input_sha256=inputs,hits=hits,correction_count=sum(x['needs_correction'] for x in hits),limits='搜索命中已逐条读；未冒称重读全卷原文，亦未改冻结或已交批')
p=H/'batch007-mirror-scan.json';p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out,ensure_ascii=False,indent=2))
