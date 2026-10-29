from pathlib import Path
import json, sys
p=Path(__file__).resolve().parents[1]
b=json.loads((p/'sources.json').read_text(encoding='utf-8'))['z']
s=Path(b['normalized_path']).read_text(encoding='utf-8').splitlines()
a,c=map(int,sys.argv[1:3])
sys.stdout.reconfigure(encoding='utf-8')
print('\n'.join(f'L{i}: {s[i-1]}' for i in range(a,c+1)))
