from pathlib import Path
import shutil
O=Path('.verify/tree-maps-20261025/library/reports/two-books-full-20261025')
for f in ('zeidan','leveling'):
    p=Path(f'.planning/tree-maps-20261025/{f}-topology.json')
    if p.exists():shutil.copyfile(p,O/f/'plot/curated-topology.json')
    p=Path(f'.planning/tree-maps-20261025/{f}-拓扑审阅.md')
    if p.exists():shutil.copyfile(p,O/f/'plot/拓扑审阅.md')
(O/'render_full.py').write_bytes('"""兼容旧重建入口，默认生成分枝交汇树与同图离线地图。"""\nfrom rebuild_tree_maps import main\nif __name__=="__main__":main()\n'.encode('utf-8'))
