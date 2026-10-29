from pathlib import Path
import json,hashlib,sys
B=Path(__file__).resolve().parent;R=B.parents[2];D=B/'tianxia-wushuang'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
sys.stdout.reconfigure(encoding='utf-8')
for group in read(D/'book-synthesis-draft.json')['upstream_documents']:
 for x in group['documents']:
  if x['exists'] and sha(R/x['path'])!=x['sha256']:
   print(json.dumps(dict(dependency='synthesis',path=x['path'],old=x['sha256'],new=sha(R/x['path'])),ensure_ascii=False))
for x in read(D/'cross-volume-focused-review.json')['input_sha256_snapshot']:
 if sha(R/x['path'])!=x['sha256']:print(json.dumps(dict(dependency='focused',path=x['path'],old=x['sha256'],new=sha(R/x['path'])),ensure_ascii=False))
