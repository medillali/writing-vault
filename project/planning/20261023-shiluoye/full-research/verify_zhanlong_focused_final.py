"""重放主代理实际审定的24重点最小差分，验证精确证据与输入指纹。"""
from pathlib import Path
import copy, hashlib, json
B = Path(__file__).parent
R = B.parents[2]
A = B / 'zhanlong/audit/whole-book'
P = A / 'local-v02-v05-review'
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
history_path = R / 'writing-vault/library/reports/zhanlong/audit/material-history/manifest.json'
history = read(history_path)['materials'] if history_path.exists() else []
def verify_material(path, digest):
    original = (R / path).resolve()
    assert original.is_relative_to(R)
    if original.exists() and sha(original) == digest:
        return
    matches = [m for m in history if m['original_path'] == path and m['original_sha256'] == digest]
    assert len(matches) == 1, (path, digest)
    archived = (R / matches[0]['archive_path']).resolve()
    assert archived.is_relative_to(R) and matches[0]['archived_sha256'] == digest
    assert sha(archived) == digest, matches[0]['archive_path']
pin = 'writing-vault/library/reports/zhanlong/vol06-handoff.md'
old_pin = '23e9fee6f146049c0a169bc9b18ef7c80ea8dc660645e197e461e1a214159963'
new_pin = '476c27db8d91a0ac05f068964ea7c55f59558511b3910f505d3c6e9f2ab3c012'
assert sha(R / pin) == new_pin
final_hashes = ['cbafcb4e55667044901989d87897cf44faf45e15dd59ea630063d168b01f7f63',
                'c21c99602afdb152dfc6fa0af71ec472fec044a2046c370eb1213a83b79943f0',
                'b7604422e6dc3f852b746109f1ec6818432a38a6e41f3464f4c36834a2037cdf']
changes = {1: [('focus01-fracture-precision-delta.json', {'stage_chain'})],
           2: [('focus02-canglan-approved-merged-delta.json', {'stage_chain','conclusion','limits_and_counterevidence','evidence'})],
           3: [('focus03-longlines-precision-delta.json', {'title','conclusion'}),
               ('focus03-rescue-channel-delta.json', {'stage_chain'})]}
all_rows = []
source = read(B / 'zhanlong/source.json')
chapters = {c['chapter_id']: c for c in source['chapters']}
references = 0
for number in (1, 2, 3):
    name = f'focused-findings-part{number:02d}.json'
    current = A / name
    assert sha(current) == final_hashes[number-1]
    expected = read(P / f'focused-findings-part{number:02d}-before-formal-link-pin.json')
    assert expected['formal_input_sha256'][pin] == old_pin
    expected['formal_input_sha256'][pin] = new_pin
    for filename, allowed in changes[number]:
        delta = read(P / filename)
        before, after = delta['before'], delta['after']
        i = next(i for i, row in enumerate(expected['findings']) if row['key'] == before['key'])
        assert expected['findings'][i] == before
        assert {k for k in before if before[k] != after[k]} == allowed
        if number == 1:
            assert before['stage_chain'][:2] == after['stage_chain'][:2]
            assert before['stage_chain'][2].replace('1380断臂活', '1380臂骨震断低垂仍活（非截肢）') == after['stage_chain'][2]
        if number == 2:
            assert before['stage_chain'][:2] == after['stage_chain'][:2]
            assert before['evidence'] == after['evidence'][:-1]
            e = after['evidence'][-1]
            assert e['chapter_id'] == 'ch-1369' and e['research_path'] == 'writing-vault/library/reports/zhanlong/audit/primary-rereads/canglan-1369-addendum.json'
        expected['findings'][i] = copy.deepcopy(after)
    data = read(current)
    assert expected == data and len(data['findings']) == 8
    for path, digest in data['formal_input_sha256'].items():
        assert sha(R / path) == digest, path
    for row in data['findings']:
        assert row['review_status'] == 'draft' and row['terminal_status'] in {'answered','partial','unknown','unrecovered'}
        for e in row['evidence']:
            c = chapters[e['chapter_id']]
            assert e['source_id'] == source['source_id'] and e['revision'] == source['revision']
            assert c['start_line'] <= e['start_line'] <= e['end_line'] <= c['end_line']
            assert e['claim_kind'] in {'fact','inference','synthesis','plan'}
            if e.get('research_path') and e.get('material_sha256'):
                verify_material(e['research_path'], e['material_sha256'])
            references += 1
    all_rows.extend(data['findings'])
assert len({row['key'] for row in all_rows}) == 24
assert read(A / 'end-state-audit-draft.json')['findings'] == all_rows
report = dict(status='exact-primary-approved-deltas-and-evidence-verified', findings=24,
              evidence_references=references, final_group_sha256=final_hashes,
              final_24_equal_groups=True, original_input_receipts_modified_by_verifier=False,
              semantic_reading_created=False, whole_book_accepted=False)
(P / 'primary-focused-final-verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
