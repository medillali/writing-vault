"""将逐项人工裁定按冻结序号展开稳定ID；不生成语义判断。"""
import json
import sys
from pathlib import Path

here = Path(__file__).resolve().parent
rows = json.loads((here/'assigned-candidates.json').read_text(encoding='utf-8'))
spec = json.loads((here/sys.argv[1]).read_text(encoding='utf-8'))
out = []
for number, status, domain, rationale, chapters in spec:
    row = rows[number-1]
    if row['volume'] != 6:
        raise ValueError(row['candidate_id'])
    out.append([row['candidate_id'], status, domain, rationale, chapters,
                '.planning/20261023-shiluoye/full-research/tianxia-wushuang/vol06/chapter-notes.jsonl'])
target = here/sys.argv[2]
target.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(str(target))
