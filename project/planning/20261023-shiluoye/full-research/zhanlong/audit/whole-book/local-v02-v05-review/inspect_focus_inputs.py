import json,pathlib,hashlib,sys
sys.stdout.reconfigure(encoding='utf-8')
from save_manual_batch import P,ROOT,B,read,write,sha
target=ROOT/'.planning/20261023-shiluoye/full-research/tianxia-wushuang/audit/whole-book/end-state-audit-draft.json'
x=read(target);print('FINDING_KEYS',list(x['findings'][0]));print('EXAMPLE',json.dumps({k:v for k,v in x['findings'][0].items() if k!='evidence'},ensure_ascii=False));print('EVIDENCE_EXAMPLE',json.dumps(x['findings'][0]['evidence'][0],ensure_ascii=False))
for name in ['primary-focused-rereads.json','primary-additional-rereads-20261026.json']:
 p=B/name
 if p.exists(): print('PRIMARY_INPUT',name,sha(p));print(p.read_text(encoding='utf-8'))
