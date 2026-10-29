"""只读列出研究包字段与数组数量，供分批语义审阅选键，不创建审阅回执。"""
import json, pathlib, sys
sys.stdout.reconfigure(encoding='utf-8')
d = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding='utf-8'))
for p in sys.argv[2:]:
    d = d[p]
print(json.dumps({k: len(v) if isinstance(v, (list, dict)) else v for k, v in d.items()} if isinstance(d, dict) else {'array_length': len(d)}, ensure_ascii=False))
