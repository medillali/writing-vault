"""只统计当前标准备份候选，不生成备份或恢复结论。"""
from pathlib import Path
import collections,json,sys
B=Path(__file__).resolve().parent;R=B.parents[2]
sys.path.insert(0,str(R/'distill-novels/scripts'))
from fictionlib.exchange import backup_allowed
v=R/'writing-vault';c=collections.Counter();sizes=collections.Counter()
for p in v.rglob('*'):
    if p.is_file():
        rel=p.relative_to(v).as_posix()
        if backup_allowed(rel):
            group='reports' if rel.startswith('library/reports/') else 'core'
            c[group]+=1;sizes[group]+=p.stat().st_size
print(json.dumps(dict(status='inventory-only-not-backup',files=dict(c),bytes=dict(sizes)),ensure_ascii=False))
