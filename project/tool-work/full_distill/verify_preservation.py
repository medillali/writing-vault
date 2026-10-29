"""核对其他作品、开篇审查快照和既有人工作业字段。"""
import hashlib
import json
from persist import ROOT,HERE
from fictionlib.vault import Vault

def verify():
    initial=json.loads((HERE/'initial-snapshot.json').read_text(encoding='utf-8'))
    vault=Vault(ROOT/'writing-vault')
    for aid,fields in initial['human_fields'].items():
        a=vault.get_asset(aid)
        assert {k:a[k] for k in fields}==fields,('human fields changed',aid)
    for name,digest in initial['unchanged_files'].items():
        assert hashlib.sha256((vault.root/name).read_bytes()).hexdigest()==digest,('protected file changed',name)
    return {'protected_assets':len(initial['human_fields']),'unchanged_files':len(initial['unchanged_files']),'passed':True}

if __name__=='__main__':print(json.dumps(verify(),ensure_ascii=False))
