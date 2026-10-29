import json, hashlib
from pathlib import Path

D = Path(__file__).resolve().parent
ROOT = D.parents[6]
def rd(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
m = rd(D/'delivery-manifest.json')
for path, expected in m['files_sha256'].items():
 assert sha(ROOT/path) == expected, path
groups = [D.parent/f'reader4-character-arcs-part{i:02}.json' for i in range(1,9)]
rows = [x for p in groups for x in rd(p)['characters']]
assert len(rows) == len({r['audit_id'] for r in rows}) == 52
assert sum(len(r['evidence']) for r in rows) == 673
byid = {r['audit_id']:r for r in rows}
mapping = rd(D/'stage-card-to-character-arc-map.json')
assert len(mapping['stage_card_rows']) == 69
for x in mapping['entities']:
 assert x['stage_cards'] == byid[x['audit_id']]['stage_card_mapping']
for x in mapping['stage_card_rows']:
 card = rd(ROOT/x['source_cards_path'])[x['index']-1]
 assert all(card[k] == x[k] for k in ['asset_id','origin_key','title'])
print(json.dumps({'status':'passed-fresh-read-only-delivery-byte-and-mapping-verification',
                  'frozen_files_verified':len(m['files_sha256']),'characters':52,'groups':8,'stage_cards':69,'evidence_count':673,
                  'manifest_sha256':sha(D/'delivery-manifest.json'),'boundary':'not-primary-literary-approval'},ensure_ascii=False))
