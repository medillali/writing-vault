"""只读检索657裁定中的同类词，供人工核对；不写已签批次。"""
from pathlib import Path
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

root = Path(__file__).resolve().parent
terms = ['巴西','165','192','谁与争锋']
count = 0
hits = []
def visit(value,path):
    if isinstance(value, str):
        return [(path,value)] if any(t in value for t in terms) else []
    if isinstance(value,list):
        return [r for i,v in enumerate(value) for r in visit(v,f'{path}[{i}]')]
    if isinstance(value,dict):
        return [r for k,v in value.items() if k not in ['candidate_id','chapter_id','research_path','original_path','evidence_basis']
                for r in visit(v,f'{path}.{k}' if path else k)]
    return []
for p in sorted(root.glob('adjudications-local-v06-part*.json')):
    for row in json.loads(p.read_text(encoding='utf-8-sig')):
        count += 1
        matched = visit(row,'')
        if matched:
            hits.append(dict(candidate_id=row['candidate_id'],file=p.name,matched_fields=matched))
assert count == 657
print('BEGIN SCAN 657')
for item in hits:
    print(json.dumps(item,ensure_ascii=False))
print(f'END SCAN candidates_with_string_matches={len(hits)} total={count}')
