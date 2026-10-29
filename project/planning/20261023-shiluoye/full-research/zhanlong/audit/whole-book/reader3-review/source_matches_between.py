from common import ROOT,S
import sys,re
lo,hi=map(int,sys.argv[1:3]);terms=sys.argv[3:]
p=ROOT/'writing-vault/private-sources/normalized/sources'/S['source_id']/(S['revision']+'.txt')
for i,line in enumerate(p.read_text(encoding='utf-8').splitlines(),1):
 if lo<=i<=hi and all(re.search(t,line) for t in terms):print(f'L{i} {line}')
