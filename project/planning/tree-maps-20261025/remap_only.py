from pathlib import Path
import sys
p=Path('.verify/tree-maps-20261025/library/reports/two-books-full-20261025').resolve();sys.path.insert(0,str(p))
import rebuild_tree_maps as r
for f in ('zeidan','leveling'):r.make_map(f,r.read(p/f/'plot/topology.json'))
r.run_node('render_full.cjs',p,'views','zeidan','leveling')
