import json, hashlib, shutil
from pathlib import Path

D = Path(__file__).resolve().parent
A = D.parent
def rd(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def wr(p, x): p.write_text(json.dumps(x, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
before = D/'part07-unsubmitted-before-anna-attribution'
assert not before.exists()
before.mkdir()
paths = [D/'authored-part07.json', D/'part07-access-receipt.json', A/'reader4-character-arcs-part07.json', A/'reader4-character-arcs-part07.md']
for p in paths: shutil.copy2(p, before/p.name)
old = '子舒求同族饶命时她拒绝并反咬'
new = '子舒提出替她向流霜求情、以加入龙城换饶她一命，她拒绝并反咬'
auth = rd(paths[0]); assert old in auth['rows'][1]['key_decisions']
auth['rows'][1]['key_decisions'] = auth['rows'][1]['key_decisions'].replace(old, new)
auth['direct_full_chapters'] = [1177, 1349]
wr(paths[0], auth)
access = rd(paths[1]); access['targeted_full_indexed_chapters_actual_begin_end'] = [1177, 1349]
wr(paths[1], access)
group = rd(paths[2]); changes = []
for row in group['characters']:
 if row['audit_id'] == 'character-arc-r4-040':
  old_value = row['key_decisions']; assert old in old_value
  row['key_decisions'] = old_value.replace(old, new)
  changes.append({'audit_id': row['audit_id'], 'field_path':'key_decisions', 'before':old_value, 'after':row['key_decisions']})
 for ref in row['evidence']:
  if ref.get('research_path','').endswith('part07-access-receipt.json'):
   ref['research_sha256'] = sha(paths[1])
for key in group['additional_support_sha256']:
 if key.endswith('part07-access-receipt.json'): group['additional_support_sha256'][key] = sha(paths[1])
wr(paths[2], group)
md = paths[3].read_text(encoding='utf-8'); assert old in md
paths[3].write_text(md.replace(old,new), encoding='utf-8')
wr(D/'part07-unsubmitted-selfcheck-delta.json', {'status':'selfcheck-before-first-submission-not-primary-review','changes':changes,'source_check':{'chapter_id':'ch-1177','start_line':85870,'end_line':85951,'scope':'full-indexed-chapter-BEGIN-END','precise_lines':[85921,85922],'additional_unique_chapters':0},'metadata_change':'access receipt adds actual full reread 1177; dependent hashes refreshed; other literary fields unchanged','before_sha256':{p.name:sha(before/p.name) for p in paths},'after_sha256':{p.name:sha(p) for p in paths}})
print(json.dumps({'json_sha256':sha(paths[2]),'md_sha256':sha(paths[3]),'delta_sha256':sha(D/'part07-unsubmitted-selfcheck-delta.json')},ensure_ascii=False))
