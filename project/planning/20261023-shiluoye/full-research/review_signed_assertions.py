"""只读检索当前已签候选的完整判断文字；不把命中计为原文阅读。"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
book, *terms = sys.argv[1:]
assert terms
stage = Path(__file__).resolve().parent/book
audit = stage/'audit/whole-book'
progress = json.loads((stage/'primary-audit-review-progress.json').read_text(encoding='utf-8'))
matches = []
for group in progress['batches']:
    for row in json.loads((audit/group['path']).read_text(encoding='utf-8')):
        text = ' '.join(str(row.get(k, '')) for k in ('title', 'rationale'))
        if any(t in text for t in terms):
            matches.append({'batch': group['path'], **{k: row.get(k) for k in
                ('candidate_id', 'title', 'status', 'audit_domain', 'rationale', 'later_chapters')}})
for row in matches:
    print(json.dumps(row, ensure_ascii=False, separators=(',', ':')))
print('MATCHED_CURRENT_SIGNED_ASSERTIONS', len(matches))
