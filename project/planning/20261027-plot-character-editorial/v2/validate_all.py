"""标准全库验收，缓存本次不可变来源表以避免重复磁盘读取。"""
import json
import sys
from pathlib import Path
P = Path(__file__).resolve().parent
R = P.parents[2]
sys.path.insert(0, str(R / 'distill-novels/scripts'))
from fictionlib.vault import Vault
v = Vault(R / 'writing-vault')
sources = {s['source_id']: s for s in v.sources()}
fallback = v._source
v._source = lambda sid: sources[sid] if sid in sources else fallback(sid)
result = v.validate()
(P / 'vault-validation.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(result, ensure_ascii=False))
