from pathlib import Path
import json,sys,hashlib
sys.stdout.reconfigure(encoding='utf-8');R=Path(__file__).resolve().parents[2];P=Path(__file__).parent;rel=Path('library/reports/two-books-full-20261025/research/z-final')
changed=[]
for name in ['final-validation.json','integration-validation.json']:
 src=P/'z-final'/name;v=R/'.verify/two-books'/rel/name;l=R/'writing-vault'/rel/name
 assert v.read_bytes()==l.read_bytes(),'本批验收文件已被外部改动'
 if src.read_bytes()!=v.read_bytes():
  v.write_bytes(src.read_bytes());l.write_bytes(src.read_bytes());changed.append(name)
print(json.dumps({'updated_owned_proofs':changed},ensure_ascii=False))
