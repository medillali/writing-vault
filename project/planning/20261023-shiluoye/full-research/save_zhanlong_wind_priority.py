"""主审实际核845/942原行并读完13项提案后，保原稿保存纠正层。"""
from pathlib import Path
import copy, hashlib, json
B=Path(__file__).resolve().parent; R=B.parents[2]
A=B/'zhanlong/audit/whole-book'
P=A/'reader3-review/vol04-wind-layers-correction-proposal.json'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(P)=='7f2789799c7456d7420df5767c4eee0045c3e3796227643f6f9336f3334fd2aa'
proposal=read(P); assert len(proposal['affected_fields'])==13
source=read(B/'zhanlong/source.json'); chapters={c['chapter_id']:c for c in source['chapters']}
for row in proposal['affected_fields']:
    target=(R/row['path']).resolve();assert target.is_relative_to(R)
    assert sha(target)==row['sha256'],row['path']
    keys=row['field'].strip('/').split('/')
    if keys[0]=='line':
        assert len(keys)==2
        value=target.read_text(encoding='utf-8').splitlines()[int(keys[1])-1]
    elif keys[0]=='jsonl':
        value=[json.loads(l) for l in target.read_text(encoding='utf-8').splitlines() if l.strip()][int(keys[1])]
        assert value['chapter_id']=='ch-0845'
        for key in keys[2:]:value=value[int(key)] if isinstance(value,list) else value[key]
    else:
        value=read(target)
        for key in keys:value=value[int(key)] if isinstance(value,list) else value[key]
    assert value==row['before'],(row['path'],row['field'])
    for ev in row['evidence']:
        ch=chapters[ev['chapter_id']]
        assert ev['source_id']==source['source_id'] and ev['revision']==source['revision']
        assert ch['start_line']<=ev['start_line']<=ev['end_line']<=ch['end_line']
out=copy.deepcopy(proposal)
out['primary_approval']=dict(reviewer='primary',status='approved-for-library-reading-overlay',
    user_approval=False,proposal_sha256=sha(P),
    findings='845可突破十层上达27与目前10可以分潜力和现态，实际十剑；942实际十五层支持后续成长。撤回旧研究必自冲解读，27仅潜力，不补具体领悟过程。',
    actual_verification=[dict(chapter_id='ch-0845',start_line=64590,end_line=64616,full_text_read=False),
                         dict(chapter_id='ch-0942',start_line=70485,end_line=70510,full_text_read=False)],
    fields=13,original_files_unchanged=True)
out['approval_precedence']='提案原status保历史；当前研究解释按primary_approval及after读取。'
formal=R/'writing-vault/library/reports/zhanlong/audit'
dest=formal/'priority-corrections-wind-layers.json'; assert not dest.exists()
combined=A/'priority-corrections-delta.json'; old=read(combined)
assert len(old['affected_fields'])==24 and len(old['issues'])==2
before=A/'priority-corrections-before-wind.json'; assert not before.exists()
content=(json.dumps(out,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
before.write_bytes(combined.read_bytes());dest.write_bytes(content)
md='''# 乘风斩成长层数的优先纠正

主代理已定向核对845与942章原行，并读完十三字段提案。845条文可读为能突破十层而上达二十七层，当时面板为十层、实际试出十剑；942明确已到十五层并实际十五击。旧研究将它断成硬上限十层又二十七层的必然矛盾，解读过强，现撤回。

二十七层仍只记潜力，不写845或942已实用二十七剑；不替缺省过程编逐层领悟。部落人口、圣域词义及其他原文数差保持各自记录。

[十三字段前后与核源](priority-corrections-wind-layers.json) · [卷四报告](../vol04.md) · [本书入口](../README.md)
'''
(formal/'priority-corrections-wind-layers.md').write_text(md,encoding='utf-8')
merged=copy.deepcopy(old);merged['issues'].append(out)
merged['affected_fields'].extend(out['affected_fields'])
merged['primary_approval'].update(approved_issues=3,approved_fields=37)
merged['formal_reading_entries'].append('audit/priority-corrections-wind-layers.md')
combined.write_text(json.dumps(merged,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert all(sha(R/r['path'])==r['sha256'] for r in proposal['affected_fields'])
print(json.dumps(dict(approved_fields=13,combined_fields=37,formal_sha256=sha(dest),
    combined_sha256=sha(combined),original_files_unchanged=True),ensure_ascii=False))
