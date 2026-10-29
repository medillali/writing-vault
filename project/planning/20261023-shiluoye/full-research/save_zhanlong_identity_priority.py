"""主审已读60字段及六处原文限定片段，保存两组实体纠正。"""
from pathlib import Path
import copy,hashlib,json
B=Path(__file__).resolve().parent;R=B.parents[2];A=B/'zhanlong/audit/whole-book'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
v2=A/'reader3-review/vol04-identity-two-issues-proposal.v2.json'
p=A/'reader3-review/vol04-identity-two-issues-proposal.v3.json'
assert sha(v2)=='565bf0d201d5d3ccb0ac4441aedacb4b7104b5d193e446ea67c6d4f4d1429c89'
assert sha(p)=='8e01a77c5a46e36f15dac6a76fd556f594a3e158594538318e55de981c48747a'
proposal=read(p);assert len(proposal['affected_fields'])==60
assert proposal['affected_fields'][:57]==read(v2)['affected_fields']
source=read(B/'zhanlong/source.json');cs={c['chapter_id']:c for c in source['chapters']}
for row in proposal['affected_fields']:
    q=(R/row['path']).resolve();assert q.is_relative_to(R) and sha(q)==row['sha256'],row['path']
    keys=row['field'].strip('/').split('/')
    if keys[0]=='line':value=q.read_text(encoding='utf-8').splitlines()[int(keys[1])-1]
    else:
        if keys[0]=='jsonl':
            value=[json.loads(l) for l in q.read_text(encoding='utf-8').splitlines() if l.strip()][int(keys[1])];keys=keys[2:]
        else:value=read(q)
        for key in keys:value=value[int(key)] if isinstance(value,list) else value[key]
    assert value==row['before'],(row['path'],row['field'])
    for ev in row['evidence']:
        ch=cs[ev['chapter_id']]
        assert ev['source_id']==source['source_id'] and ev['revision']==source['revision']
        assert ch['start_line']<=ev['start_line']<=ev['end_line']<=ch['end_line']
out=copy.deepcopy(proposal)
out['primary_approval']=dict(reviewer='primary',status='approved-for-library-reading-overlay',user_approval=False,
    fields=60,proposal_sha256=sha(p),v2_first57_exactly_equal=True,original_files_unchanged=True,
    actual_verification=[dict(chapter_id=f'ch-{n:04d}',start_line=a,end_line=z,full_text_read=False)
        for n,a,z in [(861,65620,65636),(879,66603,66615),(885,66923,66933),
                      (899,67796,67812),(919,69037,69050),(943,70581,70594)]],
    findings='861玩家百里若风与NPC清流统领百里伦分人；899炎龙统龙忠与御林龙硎分人，919三上将主/罗嗣/雷斯，秦烨/龙忠正2；保龙忠跨期称衔差，撤研究误合。')
out['approval_precedence']='原proposal-only仅保历史；当前按primary_approval与after读取。共享handoff after组合继承先前wind层。'
formal=R/'writing-vault/library/reports/zhanlong/audit'
dest=formal/'priority-corrections-identity.json';assert not dest.exists()
combined=A/'priority-corrections-delta.json';assert sha(combined)=='0b128954e48b8ed41a8f0511299fad94efa0414e5f2d2bbe79c55a336b47456d'
old=read(combined);assert len(old['affected_fields'])==37 and len(old['issues'])==3
before=A/'priority-corrections-before-identity.json';assert not before.exists()
wind=read(formal/'priority-corrections-wind-layers.json')
overlaps=[]
for row in out['affected_fields']:
    for prior in wind['affected_fields']:
        if (row['path'],row['field'])==(prior['path'],prior['field']):
            assert row['before']==prior['before']
            assert '乘风当前10→后实15及27仅潜力未实测（非硬上限10自冲）' in row['after']
            overlaps.append(dict(path=row['path'],field=row['field'],previous_after=prior['after'],
                                 current_composed_after=row['after'],rule='本层组合after优先，before仍为原冻结值'))
assert len(overlaps)==2
before.write_bytes(combined.read_bytes())
dest.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
md='''# 两组人物误认的优先纠正

主代理已逐项读完60个直接字段，并定向核六处原文。861系统公告清眸拓墨杀的是玩家百里若风（CBN第5），与879仍活、885被主角斩首的NPC清流军统领百里伦分人；旧笔记的NPC死后再现冲突系研究误读，现撤回。火云帝王紫炎圣君是另一人。

899获上将与炎龙军统领的是龙忠，与御林将领龙硎分人。919三上将为主角、罗嗣、雷斯，秦烨与龙忠被称正二级镇国；龙忠899至919的称衔差保留。943提出撤夏禹番号者是蛟龙军秦烨，不能从笔记缩略“秦龙”生造新人或归给龙硎。

此层同时覆盖导出卡和三张正式人物卡的定位。原稿、原卡及人工字段保留，当前阅读按[60字段前后及核源](priority-corrections-identity.json)；共享handoff字段已组合[乘风斩纠正](priority-corrections-wind-layers.md)，不退回旧解释。

[龙硎旧卡](../../../views/chr-db3efcc2697e551d88e12c1439e2bc6f.md) · [徐翊旧卡](../../../views/chr-736d302e333e5484906b47dc0eb1a44f.md) · [美丽清眸旧卡](../../../views/chr-623eb778fd0255228d29785a5a75b4f1.md) · [本书入口](../README.md)
'''
(formal/'priority-corrections-identity.md').write_text(md,encoding='utf-8')
merged=copy.deepcopy(old)
for issue in sorted({r['issue_id'] for r in out['affected_fields']}):
    subset=[r for r in out['affected_fields'] if r['issue_id']==issue]
    merged['issues'].append(dict(issue_id=issue,affected_fields=subset,primary_approval=out['primary_approval'],
        formal_bundle='audit/priority-corrections-identity.json',formal_bundle_sha256=sha(dest)))
merged['affected_fields'].extend(out['affected_fields'])
merged['primary_approval'].update(approved_issues=5,approved_fields=97)
merged['formal_reading_entries'].append('audit/priority-corrections-identity.md')
merged['overlap_resolution']=overlaps
merged['precedence_rule']='同一冻结path/field有多层时，按issues顺序采用最后组合after；原before及各层历史保留。'
combined.write_text(json.dumps(merged,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert all(sha(R/r['path'])==r['sha256'] for r in out['affected_fields'])
print(json.dumps(dict(approved_fields=60,combined_field_records=len(merged['affected_fields']),
    logical_issues=len(merged['issues']),composed_overlaps=len(overlaps),formal_sha256=sha(dest),
    originals_unchanged=True),ensure_ascii=False))
