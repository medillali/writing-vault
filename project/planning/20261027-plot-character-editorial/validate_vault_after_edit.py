"""复用标准全库验证；来源表在本次只读验证期间不可变。"""
import json
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'distill-novels/scripts'))
from fictionlib.vault import Vault
vault=Vault(ROOT/'writing-vault')
sources={s['source_id']:s for s in vault.sources()}
fallback=vault._source
vault._source=lambda sid:sources[sid] if sid in sources else fallback(sid)
result=vault.validate()
Path(__file__).with_name('vault-validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
