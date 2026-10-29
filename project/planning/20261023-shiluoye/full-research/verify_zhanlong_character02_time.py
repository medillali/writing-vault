"""人物02完整主审后，仅重放已核源的一字段时点校正。"""
from pathlib import Path
import hashlib,json
A=Path(__file__).resolve().parent/'zhanlong/audit/whole-book'
H=A/'local-v03-v06-review/corrections/character02-approved-time'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
d=read(A/'character-arcs-part02-approved-time-delta.json')
old_candidates=[p for p in H.rglob('*.json') if sha(p)==d['before_json_sha256']]
assert old_candidates
old=old_candidates[0]; new=A/'character-arcs-part02.json'
assert sha(old)=='1beb29e39d3e3de9a4a6168fa3c1a89217af561c2c479f03854bae7ce0a0922c'
assert sha(new)==d['after_json_sha256']=='4629326e89133a8dc661448ae395c76c43913dbe4b6ef2c170849a40891b4737'
expected=read(old); assert len(d['changes'])==1
c=d['changes'][0]; assert c['path']==['characters',1,'terminal_state'] and expected['characters'][1]['terminal_state']==c['before']
assert c['proposed_after']==c['before'].replace('1357沈母','1359沈母').replace('1359队友','1357队友')
expected['characters'][1]['terminal_state']=c['proposed_after']; assert expected==read(new)
om=next(p for p in H.rglob('*.md') if sha(p)==d['before_md_sha256'])
nm=A/'character-arcs-part02.md'
assert sha(nm)==d['after_md_sha256'] and nm.read_bytes()==om.read_bytes().replace(c['before'].encode(),c['proposed_after'].encode())
print(json.dumps(dict(status='one-approved-field-and-exact-md-sentence-only',other_two_characters_unchanged=True,json_sha256=sha(new)),ensure_ascii=False))
