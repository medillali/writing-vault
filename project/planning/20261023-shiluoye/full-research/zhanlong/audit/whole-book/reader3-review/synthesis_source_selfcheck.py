from synthesis_common import *
import sys
path=ROOT/'writing-vault/private-sources/normalized/sources'/S['source_id']/(S['revision']+'.txt')
lines=path.read_text(encoding='utf-8').splitlines()
for raw in map(int,sys.argv[1:]):
 c=CH[raw];print('BEGIN TARGETED ORIGINAL',c['chapter_id'],c['start_line'],c['end_line'])
 for i in range(c['start_line'],c['end_line']+1):print(f'L{i}: {lines[i-1]}')
 print('END TARGETED ORIGINAL',c['chapter_id'])
