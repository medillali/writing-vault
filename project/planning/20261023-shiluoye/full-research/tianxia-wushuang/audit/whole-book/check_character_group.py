import hashlib,json,pathlib,sys
sys.stdout.reconfigure(encoding='utf-8');H=pathlib.Path(__file__).resolve().parent
from audit_evidence import chapters,R
name=sys.argv[1];p=H/name;d=json.loads(p.read_text(encoding='utf-8'));rows=d['characters'];ids=[x['audit_id'] for x in rows];assert len(ids)==len(set(ids))
n=0
for x in rows:
 for k in ['name','initial_comparison_stage','key_decisions','costs','terminal_state','evidence_boundaries']:assert x[k]
 for e in x['evidence']:
  c=chapters[int(e['chapter_id'][3:])];assert c['start_line']<=e['start_line']<=e['end_line']<=c['end_line'];assert e['source_id'] and e['revision'] and e['claim_kind'];n+=1
for path,sha in d['formal_input_sha256'].items():assert hashlib.sha256((R/path).read_bytes()).hexdigest()==sha,path
print(json.dumps(dict(status='passed_structure_and_provenance_only_not_semantic_review',characters=len(rows),evidence_references=n,sha256=hashlib.sha256(p.read_bytes()).hexdigest()),ensure_ascii=False))
