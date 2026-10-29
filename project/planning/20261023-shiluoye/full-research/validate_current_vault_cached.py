"""仍用现有完整validate；只缓存本次调用内不变的来源索引。"""
import functools,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;R=B.parents[2]
sys.path.insert(0,str(R/'distill-novels/scripts'))
from fictionlib.vault import Vault
v=Vault(R/'writing-vault');v._source=functools.lru_cache(maxsize=None)(v._source)
started=time.monotonic();result=v.validate()
sys.stdout.reconfigure(encoding='utf-8')
print(json.dumps({'validation':result,'elapsed_seconds':round(time.monotonic()-started,2),'limits':'当前全库结构核验，不等整书文学终审/三书最终验收'},ensure_ascii=False),flush=True)
