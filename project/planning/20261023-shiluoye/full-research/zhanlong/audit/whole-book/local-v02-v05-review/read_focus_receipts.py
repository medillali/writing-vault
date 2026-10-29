import sys,json
sys.stdout.reconfigure(encoding='utf-8')
from save_manual_batch import B,sha
names=sys.argv[1:] or ['batch1375-1376.json','batch1377-1380.json','batch1381-1384.json','batch1385-1386.json']
for name in names:
 p=B/'primary-ending-reread'/name
 print('BEGIN_PRIMARY_DERIVED',name,sha(p));print(p.read_text(encoding='utf-8'));print('END_PRIMARY_DERIVED',name)
