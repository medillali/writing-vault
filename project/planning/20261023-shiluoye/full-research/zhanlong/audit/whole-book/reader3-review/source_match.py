from common import ROOT,S
import sys,re
p=ROOT/'writing-vault/private-sources/normalized/sources'/S['source_id']/(S['revision']+'.txt')
terms=sys.argv[1:]
for i,line in enumerate(p.read_text(encoding='utf-8').splitlines(),1):
 if all(re.search(t,line) for t in terms):print(f'L{i} {line}')
