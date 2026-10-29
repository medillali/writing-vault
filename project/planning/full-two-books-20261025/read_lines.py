from pathlib import Path
import sys
p=Path(sys.argv[1]);start=int(sys.argv[2]) if len(sys.argv)>2 else 1;end=int(sys.argv[3]) if len(sys.argv)>3 else start+180
sys.stdout.reconfigure(encoding='utf-8')
for n,line in enumerate(p.read_text(encoding='utf-8').splitlines(),1):
 if start<=n<=end:print(f'{n}: {line}')
