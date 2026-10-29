"""主代理完整回读1305后的定向修订，保旧正式稿及原笔记。"""
from pathlib import Path
import copy,hashlib,json,sys
B=Path(__file__).resolve().parent;R=B.parents[2];D=B/'tianxia-wushuang/vol07';F=R/'writing-vault/library/reports/tianxia-wushuang'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(D/'analysis.json')=='48dad166ecb2d4ef9d2dfb3f578634f4e3589524b07f750685e8678e9ef72889'
assert sha(D/'chapter-notes.jsonl')=='5fcedf147fb7d937a9fc0ac329fb04925b70d4e61aa04e83cbb39f131b8be10a'
a=read(D/'analysis.json');x=next(x for x in a['unresolved_and_anomalies'] if x['id']=='v07-a-assassin-duration');old=copy.deepcopy(x)
s=read(B/'tianxia-wushuang/source.json')
def evidence(cid):
 c=next(c for c in s['chapters'] if c['chapter_id']==cid)
 return dict(source_id=s['source_id'],revision=s['revision'],chapter_id=cid,start_line=c['start_line'],end_line=c['end_line'],claim_kind='fact')
x.update(description='血盟分盟规模口径：1300乱月称全会十几个分盟，1305知无不言称四大长老每人掌管十几个分盟。',handling='两处均为分盟数量而非分钟时长；保不同说话者及规模口径差，未明是否重叠管理/统计时点不同，不造隐藏分盟。',evidence=[evidence('ch-1300'),evidence('ch-1305')])
history=F/'audit/research-corrections/v07-analysis-before-raw1305.json';history.parent.mkdir(parents=True,exist_ok=True)
assert not history.exists();history.write_bytes((F/'vol07-analysis.json').read_bytes())
correction=dict(reviewer='primary',kind='research-misreading-correction',user_approval=False,
 old_stage_analysis_sha256=sha(D/'analysis.json'),old_formal_analysis_sha256=sha(history),old_record=old,new_record=x,
 primary_original_reading='raw1305 L103912—103990全文BEGIN/END实际复读；另定向raw1300 L103613及1305 L103968均明确分盟。',
 original_notes_preserved_sha256=sha(D/'chapter-notes.jsonl'),scope='只改集中异常一条及报告纠错注；历史逐章问题保原记录，终点另说明原研究误读不等原文时长冲突。')
(D/'primary-corrections.json').write_text(json.dumps(correction,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(D/'analysis.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
with (D/'report.md').open('a',encoding='utf-8') as f:
 f.write('\n\n## 原文回读后的研究纠错\n\n原集中异常将“十几个分盟”误读成“十几分钟”，属于研究摘要错误，不能列为原文战斗耗时矛盾。raw1300 L103613为乱月称全会十几个分盟，raw1305 L103968为知无不言称各长老十几个分盟；应保两来源的规模口径差，不补隐藏分盟或精确总量。primary已实际全文复读1305；211逐章原笔记不重写，旧分析另存修订档。见[定向纠正记录](primary-corrections.json)。\n')
with (B/'review-wushuang-vol07.md').open('a',encoding='utf-8') as f:f.write('\n\n补充核源纠正：primary实际全文回读raw1305，确认分盟非分钟；唯一集中异常已改规模口径、补1300证据，旧正式分析留audit/research-corrections版本。其余研究/原笔记不变，后续签收和全书依赖SHA必须刷新。\n')
sys.stdout.reconfigure(encoding='utf-8');print(json.dumps({'correction':x,'stage_analysis_sha256':sha(D/'analysis.json'),'old_formal_snapshot':str(history)},ensure_ascii=False))
