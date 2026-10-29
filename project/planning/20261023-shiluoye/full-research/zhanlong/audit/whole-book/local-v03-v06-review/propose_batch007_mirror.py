"""只生成三项遗漏炼魂后证的最小提案，不改已交批。"""
from pathlib import Path
import json,hashlib
H=Path(__file__).resolve().parent;A=H.parent
p=A/'adjudications-local-v06-batch007.json'
rows=json.loads(p.read_text(encoding='utf-8'))
texts={
'v06-local-chapter_unresolved_index-0028-01':'1210残1400由巨龙载走，1212叙战死玩家已经复活，唐琦已亲述自己及问剑被炼火杀；各会逐人是否全灭及逐人24小时上线清册未给。武魂并非只留预测：1240实际百万炼魂来攻，问剑魂等级加10/全属性加100%且保技能；1241真问与队友杀问魂，真方告自身18秒无敌供主杀方魂。玩家本体与受炼影子并存，不是原玩家自愿叛阵；成军实战子题已答，保逐人清册未详。',
'v06-local-chapter_unresolved_index-0031-01':'佩1214亲见、1349本魂复苏可答身体/意志，1212明确战死玩家已经复活。武魂1240改以炼魂名出现百万军，具名问剑魂加10级/全属性加100%，1241问本体合队杀自身魂、方本体告18秒无敌助主杀方魂，已有镜像实战回收。逐人24小时上线清册仍未列，不能将本体复活与镜像作战合成同一人叛变，也不再写军队仅预测。',
'v06-local-chapter_unresolved_index-0032-01':'佩1214亲见而1349原魂恢复，1219副本维护实开、1220已刷到S3，1221再明S4—7全通；1212战死玩家已复，1240—41百万炼魂及问/方具名魂实际交战，已知子题不留假pending。两龙骑及两龙尸是1211流霜所报、子舒称多半佩，未独证具体凶手；皎月尚差一件后的具名获法/升级回执未补，逐人24h清册也未列，不能拿总体复活补每人时表。'
}
changes=[]
for row in rows:
 if row['candidate_id'] not in texts:continue
 after=json.loads(json.dumps(row));after['rationale']=texts[row['candidate_id']]
 for n,s,e in [(1240,89944,89959),(1241,89963,90004)]:
  after['later_chapters'].append(n)
  after['later_evidence'].append(dict(source_id=row['later_evidence'][0]['source_id'],revision=row['later_evidence'][0]['revision'],chapter_id=f'ch-{n:04d}',start_line=s,end_line=e,claim_kind='fact'))
 if row['candidate_id'].endswith('0032-01'):
  after['later_chapters'].append(1221)
  after['later_evidence'].append(dict(source_id=row['later_evidence'][0]['source_id'],revision=row['later_evidence'][0]['revision'],chapter_id='ch-1221',start_line=88760,end_line=88766,claim_kind='fact'))
 changes.append(dict(candidate_id=row['candidate_id'],allowed_fields=['rationale','later_chapters','later_evidence'],before={k:row[k] for k in ['rationale','later_chapters','later_evidence']},proposed_after={k:after[k] for k in ['rationale','later_chapters','later_evidence']}))
out=dict(status='proposal_pending_primary',reason='当前批把武魂与后续炼魂同义后证漏配，派生研究纠错，非源文未回收',input_file=p.name,input_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),actual_reviewer='zongheng_vol05_full',source_check='本次完整接读1240/1241本人原notes，实际定向源L89944—90004；非全章再次全文声明',changes=changes)
q=H/'batch007-mirror-evidence-proposal.json';q.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(hashlib.sha256(q.read_bytes()).hexdigest())
