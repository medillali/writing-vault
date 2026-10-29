"""独立重放已批准的三个事实句与一处上游边界，逐值核对其余数据。"""
from pathlib import Path
import copy, difflib, hashlib, json
B=Path(__file__).resolve().parent
P=B/'zhanlong/audit/whole-book/reader3-review'
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
d=load(P/'synthesis-approved-selfcheck-combined-delta.json')
approved={'characters': 'dc24bd9163455e43b17e7b1938392d6cfa505174181a10e3948048f37d6338cb', 'themes':'a3f67ac709c4ddcb306ccf6c54944491920e4f4d34af016547f75124786475b6','plot':'883a87878f8f1c08eef5dcc5251a1fe349041c7ba80b0799fc7ab805d44c992d'}
assert len(d['changes_by_file'])==3
for f in d['changes_by_file']:
    dim=f['dimension']; old=P/f'synthesis-{dim}-before-approved-selfcheck.json'; new=P/f'synthesis-{dim}.json'
    assert sha(old)==f['before_json_sha256']==approved[dim]
    assert sha(new)==f['after_json_sha256']
    expected=load(old)
    assert len(f['changes'])==(2 if dim=='characters' else 1)
    for c in f['changes']:
        ptr=c['json_pointer'].strip('/').split('/'); parent=expected
        for key in ptr[:-1]: parent=parent[int(key)] if isinstance(parent,list) else parent[key]
        key=ptr[-1]
        if c.get('before_key_present') is False:
            assert key not in parent and key=='reported_fact_boundary'
        else: assert parent[key]==c['before'] and key=='fact_summary'
        parent[key]=c['after']
    assert expected==load(new), dim
    om=P/f'synthesis-{dim}-before-approved-selfcheck.md'; nm=P/f'synthesis-{dim}.md'
    assert sha(om)==f['before_md_sha256'] and sha(nm)==f['after_md_sha256']
    assert b'\r\r\n' not in nm.read_bytes()
    a=om.read_text(encoding='utf-8'); b=nm.read_text(encoding='utf-8')
    fact=f['changes'][0]
    assert a.count(fact['before'])==1 and b.count(fact['after'])==1
    transformed=a.replace(fact['before'],fact['after'])
    if dim!='characters': assert transformed==b
    else:
        delta=list(difflib.unified_diff(transformed.splitlines(),b.splitlines(),n=1))
        print('CHARACTERS_MD_BOUNDARY_DIFF\n'+'\n'.join(delta))
        assert not any(line.startswith('-') and not line.startswith('---') for line in delta)
        assert f['changes'][1]['after']['text'] in b
    print(json.dumps({'dimension':dim,'status':'approved-delta-only','json_sha256':sha(new),'md_sha256':sha(nm)},ensure_ascii=False))
