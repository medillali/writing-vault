from pathlib import Path
import json,sys
sys.stdout.reconfigure(encoding='utf-8')
for f in ('zeidan','leveling'):
    p=Path(f'.planning/tree-maps-20261025/{f}-topology.json')
    d=json.loads(p.read_text(encoding='utf-8'));print(f)
    for t in d['threads']:
        if t['kind']=='hidden':print(t['id'],t['title'],t['status'],'\n',t['conclusion'])
