"""独立重放依赖分类修订；人物语义和MD必须全不变。"""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parent;S=B/'zhanlong';A=S/'audit/whole-book';P=A/'reader4-character-review'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
d=read(P/'wrapper-classification-delta.json');assert len(d['changes'])==2
ledger=S/'primary-research-group-review-progress.json';snap=A/'primary-progress-before-character-wrapper-resign.json'
if not snap.exists():snap.write_bytes(ledger.read_bytes())
old_ledger=read(snap)
for row in d['changes']:
    n=row['part'];old=P/f'part{n:02d}-before-wrapper-classification.json';new=A/f'reader4-character-arcs-part{n:02d}.json'
    assert sha(old)==row['before_sha256'] and sha(new)==row['after_sha256']
    expected=read(old)
    for key,h in row['moved_exact_path_sha'].items():
        assert key.startswith('.planning/') and expected['formal_input_sha256'].pop(key)==h
        assert key not in expected.get('additional_support_sha256',{})
        expected.setdefault('additional_support_sha256',{})[key]=h
    assert expected==read(new) and sha(new.with_suffix('.md'))==row['md_unchanged_sha256']
    if n==1:assert next(g for g in old_ledger['groups'] if g['path']==new.name)['sha256']==sha(old)
    print(json.dumps(dict(group=new.name,status='metadata-only-classification-replayed',characters_unchanged=True,md_bytes_unchanged=True,current_sha256=sha(new)),ensure_ascii=False))
q=A/'character-arcs-part06-approved-support-delta.json'
if q.exists():
    row=read(q);old=A/'local-v03-v06-review/corrections/character06-approved-support-classification/character-arcs-part06.json';new=A/'character-arcs-part06.json'
    assert sha(old)==row['before_json_sha256']=='1db6a17252d8e0fb164dd20c16ae3184077f7fc66ae6825c60dbcaa949e74714'
    assert sha(new)==row['after_json_sha256']
    expected=read(old);assert len(row['changes'])==1
    change=row['changes'][0];key=change['from_path'][1]
    assert change['from_path'][0]=='formal_input_sha256' and change['to_path']==['additional_support_sha256',key]
    assert expected['formal_input_sha256'].pop(key)==change['before']==change['after']
    assert key not in expected.get('additional_support_sha256',{});expected.setdefault('additional_support_sha256',{})[key]=change['after']
    assert expected==read(new) and sha(new.with_suffix('.md'))==row['before_md_sha256']==row['after_md_sha256']
    assert next(g for g in old_ledger['groups'] if g['path']==new.name)['sha256']==sha(old)
    print(json.dumps(dict(group=new.name,status='metadata-only-classification-replayed',characters_unchanged=True,md_bytes_unchanged=True,current_sha256=sha(new)),ensure_ascii=False))
