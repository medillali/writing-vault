from pathlib import Path
import sys,json,time
R=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(R/'distill-novels/scripts'))
from fictionlib.vault import Vault
from fictionlib.storage import locked,digest
class ReadSnapshotVault(Vault):
    """临时校验程序只缓存持锁期间的来源读取，不改任何验证规则。"""
    def _sources(self):
        if not hasattr(self,'source_snapshot'):
            self.source_snapshot=super()._sources()
        return self.source_snapshot
start=time.monotonic()
print('执行原Vault全库校验规则；临时缓存持锁期间的来源索引，避免每条证据重复读取全文索引。',flush=True)
vault=ReadSnapshotVault(R/'.verify/two-books')
with locked(vault.root):
    result=vault._validate_locked()
    assert digest(vault.source_snapshot)==digest(Vault._sources(vault))
result['runner']='原Vault._validate_locked与validate_graph规则；只缓存持锁期间_sources读取；缓存前后哈希一致；生产代码未修改'
result['elapsed_seconds']=round(time.monotonic()-start,2)
p=R/'.verify/two-books/library/reports/two-books-20261023/validation/library-validate.json'
p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False),flush=True)
