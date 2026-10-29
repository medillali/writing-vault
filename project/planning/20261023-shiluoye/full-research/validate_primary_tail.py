"""核对主代理末段观察的覆盖与文件一致性；不代替实际阅读或文学判断。"""
import json, pathlib, hashlib

base = pathlib.Path(__file__).resolve().parent
folder = base / 'zongheng-tianxia/vol07-primary-tail'
source = json.loads((base / 'zongheng-tianxia/source.json').read_text(encoding='utf-8'))
chapters = {c['chapter_id']: c for c in source['chapters']}
expected = [f'ch-{i:04d}' for i in range(951, 1061)]
raw = (folder / 'chapter-notes.jsonl').read_bytes()
notes = [json.loads(s) for s in raw.decode('utf-8').splitlines() if s.strip()]
assert [n['chapter_id'] for n in notes] == expected
batches = []
for path in sorted(folder.glob('batch-*.json')):
    batch = json.loads(path.read_text(encoding='utf-8'))
    assert len(batch) == 2
    batches.extend(batch)
assert len(batches) == len(expected) and [n['chapter_id'] for n in batches] == expected
for note, batch in zip(notes, batches):
    assert note['full_text_read'] is True and note['reader'] == 'primary'
    assert batch['model_full_text_read'] is True
    chapter = chapters[note['chapter_id']]
    for key in ('title', 'start_line', 'end_line'):
        assert note[key] == chapter[key]
    for key in ('chapter_id', 'facts', 'inferences', 'state_changes', 'unresolved'):
        assert note[key] == batch[key], (note['chapter_id'], key)
    assert note['facts'] and note['state_changes']
state = json.loads((folder / 'reader-state.json').read_text(encoding='utf-8'))
assert state['completed_chapter_ids'] == expected and state['complete_assigned_segment'] is True
assert state['next_chapter_id'] is None and not state['unresolved_truncations']
result = {
    'status': 'passed', 'reader': 'primary', 'source_id': source['source_id'],
    'revision': source['revision'], 'first': expected[0], 'last': expected[-1],
    'chapters': len(notes), 'batches': len(batches)//2,
    'chapter_notes_sha256': hashlib.sha256(raw).hexdigest(),
    'checks': ['exact-assigned-coverage', 'no-duplicates', 'source-line-boundaries',
               'batch-and-notes-consistent', 'reader-attribution', 'no-unresolved-truncation'],
    'limits': '覆盖和一致性验证不能单独证明阅读已发生或研究解释正确；实际阅读由会话全文输出、观察和审阅共同支撑。'
}
(folder / 'validation.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps(result, ensure_ascii=False))
