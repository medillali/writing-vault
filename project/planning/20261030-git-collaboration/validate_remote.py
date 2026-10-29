"""从相邻克隆的工具验证远端资料库，不依赖本机原小说。"""
import json,sys
from pathlib import Path
root=Path(sys.argv[1])
sys.path.insert(0,str(root/'distill-novels/scripts'))
from fictionlib.vault import Vault
v=Vault(root/'writing-vault')
sources={s['source_id']:s for s in v.sources()}
fallback=v._source
v._source=lambda sid:sources[sid] if sid in sources else fallback(sid)
result=v.validate()
Path(sys.argv[2]).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
assert result.get('valid'),result
