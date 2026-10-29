"""逐项输出全部文学语义；仅折叠重复指纹、署名与等值的take/leave。"""
from pathlib import Path
import hashlib, json, sys
B = Path(__file__).resolve().parent
p = B / 'zhanlong/audit/whole-book/reader3-review' / ('synthesis-'+sys.argv[1]+'.json')
d = json.loads(p.read_text(encoding='utf-8'))
source = json.loads((B / 'zhanlong/source.json').read_text(encoding='utf-8'))
chapters = {c['chapter_id']: c for c in source['chapters']}
print('BEGIN_SYNTHESIS', d['dimension'], len(d['rows']), hashlib.sha256(p.read_bytes()).hexdigest())
scopes = sorted({o.get('synthesizer_original_read_scope','') for r in d['rows'] for o in r['supporting_observations']})
print(json.dumps(dict(actual_synthesizer=d['actual_synthesizer'], personal_complete_book_read=d['personal_complete_book_read'], original_read_scopes=scopes), ensure_ascii=False))
for row in d['rows']:
    out = {k:v for k,v in row.items() if k not in {'supporting_observations','evidence','literary_choice'}}
    out['supporting_observations'] = [{k:v for k,v in o.items() if k not in {'material_path','material_sha256','json_pointer','source_reader','synthesizer_original_read_scope'}} for o in row['supporting_observations']]
    choice = row['literary_choice']
    assert choice['take'] == row['mechanism'] and choice['leave'] == row['limits_and_counterevidence']
    out['literary_choice'] = dict(take_equals_mechanism=True, leave_equals_limits=True,
                                  claim_kind=choice['claim_kind'], user_approval=choice['user_approval'])
    refs = []
    for e in row['evidence']:
        c = chapters[e['chapter_id']]
        assert e['source_id'] == source['source_id'] and e['revision'] == source['revision']
        assert c['start_line'] <= e['start_line'] <= e['end_line'] <= c['end_line']
        refs.append(f"{e['chapter_id']} L{e['start_line']}—{e['end_line']} {e['claim_kind']}")
    out['evidence'] = refs
    print(json.dumps(out, ensure_ascii=False, separators=(',',':')))
print('END_SYNTHESIS', d['dimension'], len(d['rows']))
