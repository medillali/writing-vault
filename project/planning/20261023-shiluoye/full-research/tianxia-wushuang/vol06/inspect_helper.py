"""只读研究文件的限定行或JSON键，避免控制台截断。"""
from pathlib import Path
import sys,json
sys.stdout.reconfigure(encoding='utf-8')
p=Path(sys.argv[1]); a=int(sys.argv[2]); b=int(sys.argv[3])
for n,line in enumerate(p.read_text(encoding='utf-8').splitlines(),1):
    if a<=n<=b:print(f'{n}: {line}')
