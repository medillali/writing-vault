import json,collections
from audit_evidence import H
x=json.loads((H/'preassembly-evidence-metadata-check.json').read_text(encoding='utf-8'))
p=json.loads((H/'local-question-pool.json').read_text(encoding='utf-8'));r=next(r for r in p['candidates'] if r['candidate_id']=='v01-local-notes-unresolved-001-01')
shape={'source_id','revision','chapter_id','start_line','end_line'}
result=dict(issue_count=len(x['issues']),issues_by_field=dict(collections.Counter(i[1] for i in x['issues'])),all_issues_at_notes_original_record=all('/original/original_record' in i[0] and '-notes-unresolved-' in i[0] for i in x['issues']),sample_original_record_keys=list(r['original_record']),sample_is_publish_schema_evidence=shape.issubset(r['original_record']),sample_original_evidence_keys=list(r['original_evidence'][0]),sample_original_evidence_is_publish_schema_evidence=shape.issubset(r['original_evidence'][0]),hypothesis='预检错误地把只有chapter/start/end的原笔记容器当成来源证据；正式发布只匹配完整五字段引用，不能补写原record。')
print(json.dumps(result,ensure_ascii=False))
