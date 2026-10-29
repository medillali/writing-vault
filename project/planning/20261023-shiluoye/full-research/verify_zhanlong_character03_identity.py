"""独立重放批准四字段与精确证据数组，核旧字节和MD最小替换。"""
from pathlib import Path
import copy,hashlib,json
B=Path(__file__).resolve().parent;A=B/'zhanlong/audit/whole-book'
S=A/'local-v03-v06-review/corrections/character03-approved-wang-identity'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
proposal=read(A/'priority-corrections-wang-identity-proposal.json')['signed_character_changes']
ev=read(A/'character-arcs-part03-wang-identity-evidence-material-proposal.json')
delta=read(A/'character-arcs-part03-approved-wang-identity-delta.json')
oldpath=next(p for p in S.rglob('character-arcs-part03.json'))
oldmd=next(p for p in S.rglob('character-arcs-part03.md'))
assert sha(oldpath)==proposal['input_sha256'] and sha(oldmd)==proposal['old_md_sha256']
expected=read(oldpath);md=oldmd.read_text(encoding='utf-8')
for ch in proposal['changes'][:4]:
    target=expected
    for k in ch['path'][:-1]:target=target[k]
    assert target[ch['path'][-1]]==ch['before']
    target[ch['path'][-1]]=ch['proposed_after']
    assert md.count(ch['before'])==1
    md=md.replace(ch['before'],ch['proposed_after'])
refs=expected['characters'][3]['evidence']
assert len(refs)==24 and sum(e in ev['remove_exact_objects'] for e in refs)==1
retained=[e for e in refs if e not in ev['remove_exact_objects']]
expected['characters'][3]['evidence']=retained+ev['append_exact_objects']
assert len(retained)==23 and len(expected['characters'][3]['evidence'])==27
new=read(A/'character-arcs-part03.json');assert expected==new
newmd=(A/'character-arcs-part03.md').read_text(encoding='utf-8')
# 证据定位行从原/新精确对象独立渲染，其余MD必须为四文学句替换。
render=lambda values:'来源：'+'；'.join(f"raw{int(e['chapter_id'][3:])} L{e['start_line']}—{e['end_line']}" for e in values)
assert md.count(render(refs))==1
assert md.replace(render(refs),render(expected['characters'][3]['evidence']))==newmd
assert sha(A/'character-arcs-part03.json')==delta['json_sha256'] and sha(A/'character-arcs-part03.md')==delta['md_sha256']
print(json.dumps({'status':'independently-replayed-approved-identity-fields-and-evidence','literary_fields':4,'retained_original_evidence_objects':23,'new_identity_refs':4,'other_six_characters_and_wrapper_unchanged':True,'new_json_sha256':sha(A/'character-arcs-part03.json')},ensure_ascii=False))
