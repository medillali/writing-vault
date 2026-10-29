"""定点原行复核，不据此增加全文阅读覆盖。"""
import json,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');R=Path(__file__).parent
S=json.loads((R.parent/'source.json').read_text(encoding='utf-8'));lines=Path(S['normalized_path']).read_text(encoding='utf-8').splitlines()
a,b=map(int,sys.argv[1:3]);assert 1<=a<=b<=len(lines)
for i in range(a,b+1):print(f'L{i}: {lines[i-1]}')
