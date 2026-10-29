from pathlib import Path
import json,sys
P=Path(__file__).parent;b=json.loads((P/'sources.json').read_text(encoding='utf-8'))[sys.argv[1]]
a=int(sys.argv[2]);z=int(sys.argv[3]);lines=Path(b['normalized_path']).read_text(encoding='utf-8').splitlines()
sys.stdout.reconfigure(encoding='utf-8')
for i in range(a,z+1):print(f'L{i}: {lines[i-1]}')
