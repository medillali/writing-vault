import sys,json
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
P=Path(__file__).parent
root=next(p for p in P.parents if (p/'writing-vault').exists())
p=root/'writing-vault/private-sources/normalized/sources/src-d8926e2a35f04bcf8139cff0ea516bbd/d819f7d0ecf5a2004a0a434e987569bbe25015422d45e16676af913292346857.txt'
a,b=map(int,sys.argv[1:]);s=p.read_text(encoding='utf-8').splitlines()
assert 0<a<=b<=len(s)
print(f'POINT BEGIN L{a}—L{b}; targeted only; not full chapter coverage')
for i in range(a-1,b):print(f'L{i+1}: {s[i]}')
print('POINT END')
