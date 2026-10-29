"""人工已核原文后的优先纠正层提案；只附定位/旧值/SHA，不改任何正式与冻结输入。"""
from pathlib import Path
import hashlib,json,sys
sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent;A=H.parent;BOOK=A.parents[1];ROOT=BOOK.parents[3]
F=ROOT/'writing-vault/library/reports/zhanlong'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def at(obj,path):
    for k in path:obj=obj[k]
    return obj
source=read(BOOK/'source.json');refs=[]
for n,start,end in [(740,57974,57978),(743,58115,58118),(743,58142,58149),(743,58158,58171),(744,58218,58220),(749,58537,58600)]:
    refs.append(dict(source_id=source['source_id'],revision=source['revision'],chapter_id=f'ch-{n:04d}',start_line=start,end_line=end,claim_kind='fact'))
correction='原公告用“10小时内”转普通装备可装备/交易，并未规定必须十小时后才可装备；743倒计时仍在时已交抹并实际用群狮，不能据错误的“后”字诊断规则冲突。进城/下线/掉落限制与最终保有倒计时另记，不能由可装备推已过十小时。'
items=[]
def add_json(file,path,after,kind='direct-misreading',reader='primary'):
    data=read(file);old=at(data,path)
    assert old!=after
    items.append(dict(file=file.relative_to(ROOT).as_posix(),input_sha256=sha(file),json_path=path,before=old,proposed_after=after,delta_kind=kind,original_research_reader=reader))
def add_notes(file,chapter,path,after):
    rows=[json.loads(line) for line in file.read_text(encoding='utf-8').splitlines() if line.strip()]
    i=next(i for i,r in enumerate(rows) if r['chapter_id']==f'ch-{chapter:04d}')
    old=at(rows[i],path);assert old!=after
    items.append(dict(file=file.relative_to(ROOT).as_posix(),input_sha256=sha(file),jsonl_index=i,chapter_id=f'ch-{chapter:04d}',json_path_within_row=path,before=old,proposed_after=after,delta_kind='direct-misreading',original_research_reader=rows[i]['reader'],original_read_at=rows[i]['read_at']))
facts_after='20分后系统滑获得狮王盾，10h持者禁入城禁下线、死下线掉；公告说10h内转普通可装备交易，坐标公开。不能把“内”改成“后”；主此前对不可回城/下线的猜测得到公告实证。'
anomaly_after='旧摘要把740公告“10小时内”误读成“十小时后才可装备”；743倒计时内交抹、实际装备并用特技，不与该公告字面直接冲突。本项应作为派生研究纠正，保原notes历史，不继续当小说规则异常。'
for notes in [F/'vol03-chapter-notes.jsonl',BOOK/'vol03/chapter-notes.jsonl',BOOK/'primary-vol03-tail/chapter-notes.jsonl']:
    add_notes(notes,740,['facts',2],facts_after)
    add_notes(notes,743,['source_anomalies',0],anomaly_after)
add_json(F/'vol03-analysis.json',['chapter_source_anomaly_index',18,'source_anomalies',0],anomaly_after)
add_json(F/'vol03-analysis.json',['unresolved_and_anomalies',26,'description'],anomaly_after)
add_json(F/'vol03-analysis.json',['unresolved_and_anomalies',26,'handling'],'优先按原公告的“内”及743实际装备解释；保原误读摘要供回溯，不补隐藏权限/补丁，也不再把提前使用列为规则冲突。')
add_json(F/'vol03-analysis.json',['dimensions','worldbuilding',2,'textual_fact'],'龙池融合圣天保特性而阶变；狮盾在十小时争夺中转手、抹先实用后最终保有，镇岳在多国多手后归主；NPC佩剑与王权剑各有身份。','related-wording-clarification')
cards=read(F/'vol03-cards.json');assert '十小时后可装备' in cards[97]['content']['failure_mode']
add_json(F/'vol03-cards.json',[97,'content','failure_mode'],'不能把公告“十小时内可转普通装备”误读成“十小时后才可装备”，也不能把期间装备/使用混成争夺计时已结束；职业与120怒门槛仍须满足。')
items[-1]['origin_key']=cards[97]['origin_key'];items[-1]['title']=cards[97]['title']
proposal=dict(status='proposal_only_not_applied',book='zhanlong',issue_id='lion-shield-within-not-after',
              actual_reviewer='zongheng_vol05_full',original_full_text_reader='primary（raw740/743/744/749所属卷3尾）',
              new_verification='本裁定者本轮BEGIN-END完整重读740/743；定向读744 L58187—58245，完整派生读749原notes。不同实际范围分别登记，不替换原reader。',
              finding=correction,source_evidence=refs,affected_fields=items,
              dependent_local_candidates=['v03-local-unresolved_and_anomalies-0027-01','v03-local-unresolved_and_anomalies-0027-02'],
              unaffected=['不改公告原文、分卷冻结包、原notes/read_at/reader或原批次SHA。','743主说等保住十小时后再正式分给抹，是当时分配承诺，不能单独冒充系统禁装备规则。','749两国器最终保有与743仍在争夺的阶段均保留，不把早期装备等同无追杀/无掉落。','同一旧句的历史批次、备份与正式原记录均保持；未来由root审核保存优先overlay，读者引用这些旧字段时显式先读该纠正层。'],
              schema_note='只提供原文件/字段/原串与建议优先解读；不是已应用的全书合并schema，不代签primary。')
target=H/'priority-corrections-proposal.json';target.write_text(json.dumps(proposal,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
md=['# 狮王盾“内／后”优先纠正层提案','','仅提案，正式库与冻结包未改。', '',correction,'', '实际归属：primary原读卷3尾；本裁定者定向复核范围见JSON。','']
for i,item in enumerate(items,1):
    path=item.get('json_path',item.get('json_path_within_row'))
    where='JSONL '+str(item['jsonl_index'])+' / ' if 'jsonl_index' in item else ''
    md += [f'## {i}. '+item['file'],'',where+'.'.join(map(str,path)),'','原：'+item['before'],'','拟优先：'+item['proposed_after'],'','原读者：'+str(item['original_research_reader']),'']
md+=['## 原文定位','','740 L57978与744 L58220均写“10小时内”；743 L58116仍余9h17、L58148主先允保住后给、L58158—71因撤退需要先交/补怒/实用。749最终保有是后一个阶段。','', '## 保留边界','','旧notes、分卷研究、批次与SHA不覆盖；这份提案须root核源/审阅后另存显式优先纠正层。','']
(H/'priority-corrections-proposal.md').write_text('\n'.join(md),encoding='utf-8')
assert all(sha(ROOT/item['file'])==item['input_sha256'] for item in items)
print(json.dumps(dict(affected_fields=len(items),proposal_sha256=sha(target),formal_and_frozen_unchanged=True),ensure_ascii=False))
