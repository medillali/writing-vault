"""本卷只读原文及真实读后笔记保存；不生成文学结论，不访问其他书正文。"""
import datetime
import hashlib
import json
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
D = Path(__file__).resolve().parent
BOOK = D.parent
ROOT = D.parents[4]
VOL = int(D.name[3:])
READER = 'zongheng_vol05_full'
SOURCE = json.loads((BOOK / 'source.json').read_text(encoding='utf-8'))
SPEC = next(v for v in SOURCE['volumes'] if v['volume'] == VOL)
SEGMENTS = [s for u in SPEC['units'] for s in u['segments']]
IDS = [s['chapter_id'] for s in SEGMENTS]
META = {s['chapter_id']: s for s in SOURCE['chapters']}
def read(p):
    return json.loads(p.read_text(encoding='utf-8'))
def write(p, x):
    p.write_text(json.dumps(x, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()
def validate_metadata():
    units = read(ROOT / 'writing-vault/library/reports/collection/reading-units.json')
    registered = units[SOURCE['source_id']]
    assert registered['source_revision'] == SOURCE['revision']
    mapped = {u['unit_id']:u for u in registered['units']}
    keys = ('unit_id','segment_ids','title','kind','printed_numbers','start_line','end_line')
    for unit in SPEC['units']:
        assert {k:unit[k] for k in keys} == {k:mapped[unit['unit_id']][k] for k in keys}
        assert all(s == META[s['chapter_id']] for s in unit['segments'])
    assert len(IDS) == len(set(IDS))
    return hashlib.sha256((BOOK / 'source.json').read_bytes()).hexdigest()
def init():
    fingerprint = validate_metadata()
    state_path = D / 'reader-state.json'
    if not state_path.exists():
        write(state_path, dict(source_id=SOURCE['source_id'], revision=SOURCE['revision'], volume=VOL,
             reader=READER, status='reading', read_chapter_ids=[], completed_chapter_ids=[],
             next_chapter_id=IDS[0], pending_chapter_ids=[], truncated_pending=[],
             source_index_sha256=fingerprint, body_units_completed=0, raw_segments_completed=0,
             volume_headers_completed=0, complete_volume=False, complete_book=False,
             current_stage='本卷尚未阅读；前卷仅可读取交接，不据此冒认全文已读。', updated_at=now()))
        write(D / 'read-log.json', dict(source_id=SOURCE['source_id'], revision=SOURCE['revision'],
             volume=VOL, reader=READER, chapters=[], complete_volume=False, complete_book=False,
             method='本代理逐片全文阅读，逐次检查BEGIN/END；每2—4片保存读后笔记；标题片单列不算正文章。', anomalies=[]))
        (D / 'chapter-notes.jsonl').write_text('', encoding='utf-8')
        write(D / 'assignment.json', dict(source_id=SOURCE['source_id'], revision=SOURCE['revision'],
              volume=VOL, reader=READER, body_units=SPEC['body_units'], assigned_chapter_ids=IDS,
              boundary='只写本卷暂存目录；不将别书或后卷状态带入本卷。'))
    state = read(state_path)
    assert state['source_id'] == SOURCE['source_id'] and state['revision'] == SOURCE['revision']
    print(json.dumps(dict(volume=VOL, body_units=SPEC['body_units'], segments=len(IDS),
                         first=META[IDS[0]], second=META[IDS[1]], last=META[IDS[-1]],
                         state=state, unit_example=SPEC['units'][0], mapping_root_keys=list(read(ROOT / 'writing-vault/library/reports/collection/reading-units.json'))), ensure_ascii=False, indent=2))
def output(start, end=None, first_line=None, last_line=None):
    a, b = f'ch-{int(start):04d}', f'ch-{int(end or start):04d}'
    assert a in IDS and b in IDS and IDS.index(a) <= IDS.index(b) and IDS.index(b) - IDS.index(a) < 2
    lines = Path(SOURCE['normalized_path']).read_text(encoding='utf-8').splitlines()
    for cid in IDS[IDS.index(a):IDS.index(b)+1]:
        c = META[cid]
        lo = max(c['start_line'], int(first_line)) if first_line else c['start_line']
        hi = min(c['end_line'], int(last_line)) if last_line else c['end_line']
        print(f'BEGIN {cid} {c["title"]} L{lo}—{hi} FULL_RANGE={c["start_line"]}—{c["end_line"]}')
        for n in range(lo, hi+1):
            print(f'L{n}: {lines[n-1]}')
        print(f'END {cid} L{hi}')
def save():
    batch = read(D / (f'batch-{sys.argv[2]}.json' if len(sys.argv)>2 else 'batch.json'))
    items = batch['chapters']
    assert 1 <= len(items) <= 4
    state, log = read(D / 'reader-state.json'), read(D / 'read-log.json')
    assert state['source_index_sha256'] == validate_metadata(), '来源索引变化，须交主代理核验后续读'
    done = state['read_chapter_ids']
    assert [x['chapter_id'] for x in items] == IDS[len(done):len(done)+len(items)]
    records = []
    for item in items:
        c = META[item['chapter_id']]
        assert item.get('full_text_read') is True and all(k in item for k in ['facts','inferences','state_changes','unresolved'])
        row = dict(source_id=SOURCE['source_id'], revision=SOURCE['revision'], volume=VOL,
                   reader=READER, read_at=now())
        row.update({k:c[k] for k in ['chapter_id','title','start_line','end_line']})
        row.update(item)
        records.append(row)
        log['chapters'].append({k:row[k] for k in ['chapter_id','title','start_line','end_line','reader','full_text_read']})
        done.append(item['chapter_id'])
    with (D / 'chapter-notes.jsonl').open('a', encoding='utf-8') as f:
        for row in records:
            f.write(json.dumps(row, ensure_ascii=False) + '\n')
    state.update(read_chapter_ids=done, completed_chapter_ids=done, raw_segments_completed=len(done),
                 next_chapter_id=IDS[len(done)] if len(done)<len(IDS) else None,
                 pending_chapter_ids=[], truncated_pending=[], current_stage=batch['current_stage'],
                 updated_at=now(), complete_volume=len(done)==len(IDS), complete_book=False)
    completed_units = [u for u in SPEC['units'] if all(x['chapter_id'] in done for x in u['segments'])]
    # 单元类型以已登记kind为准，标题用kind或无正文号判断，不按raw偏移猜章号。
    headers = [u for u in completed_units if u.get('kind') == 'volume_header' or all(META[x['chapter_id']].get('kind') == 'volume_header' for x in u['segments'])]
    # 本书每卷恰一独立卷标题，source spec首单元为该标题；不把它计作正文。
    state['volume_headers_completed'] = int(IDS[0] in done)
    state['body_units_completed'] = len(completed_units) - state['volume_headers_completed']
    log['complete_volume'] = state['complete_volume']
    write(D / 'reader-state.json', state)
    write(D / 'read-log.json', log)
    print(json.dumps(dict(saved=[x['chapter_id'] for x in records], body=state['body_units_completed'], raw=len(done), next=state['next_chapter_id']),ensure_ascii=False))
if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'init': init()
    elif cmd == 'read': output(*sys.argv[2:])
    elif cmd == 'lines': output(sys.argv[2], None, sys.argv[3], sys.argv[4])
    elif cmd == 'save': save()
    elif cmd == 'state': print((D / 'reader-state.json').read_text(encoding='utf-8'))
    elif cmd == 'meta':
        mapping=read(ROOT / 'writing-vault/library/reports/collection/reading-units.json')
        print(json.dumps({k:(list(v)[:6] if isinstance(v,dict) else list(v[0]) if isinstance(v,list) and v and isinstance(v[0],dict) else type(v).__name__) for k,v in mapping.items()},ensure_ascii=False))
