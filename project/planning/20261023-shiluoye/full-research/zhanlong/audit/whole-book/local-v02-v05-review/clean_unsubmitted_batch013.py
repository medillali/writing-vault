from save_manual_batch import P,F,read,write,sha
import json
f=P/'adjudications-local-v02-batch013.json';x=read(f);o=x[10];old=o['rationale'];new='396林说正和东城忙神秘大礼；466近卫军及林盟主徽记实际出现，467问剑揭其秘密募兵，468三千近卫救战/主正式确认为分盟，469—470两女入主盟与副位实成。将秘密组织筹备到交付援军视为大礼的叙事兑现是跨段衔接判断，非拿反向龙吻礼代账；原文未再逐字把礼物标签贴回军队，事实与这一解释层分开。'
o.update(status='answered',audit_domain='foreshadowing-payoff',rationale=new,later_chapters=[396,466,467,468,469,470]); notes={}
ff=F/'vol02-chapter-notes.jsonl'
for line in ff.read_text(encoding='utf-8').splitlines():
 if line.strip():
  n=json.loads(line);notes[int(n['chapter_id'].split('-')[1])]=n
o['later_evidence']=[]
for k in o['later_chapters']:
 n=notes[k];o['later_evidence'].append(dict(source_id=n['source_id'],revision=n['revision'],chapter_id=n['chapter_id'],start_line=n['start_line'],end_line=n['end_line'],claim_kind='fact',evidence_access='本轮定向BEGIN-END原文复读' if k in [396,466,467,468] else '正式四栏派生已完整读取，保原reader',material_path='writing-vault/library/reports/zhanlong/vol02-chapter-notes.jsonl',material_sha256=sha(ff),source_reader=n['reader']))
write(f,x);md=f.with_suffix('.md');s=md.read_text(encoding='utf-8').replace(old,new).replace(f"**{o['candidate_id']}** · partial / relationship-receipt",f"**{o['candidate_id']}** · answered / foreshadowing-payoff").replace('证据raw：396, 416, 418, 469, 470；','证据raw：396, 466, 467, 468, 469, 470；');md.write_text(s,encoding='utf-8')
state=read(P/'reader-state.json');state['submitted_batches'][-1]['sha256']=sha(f);write(P/'reader-state.json',state)
write(P/'history/batch013-unsubmitted-gift-clarification.json',dict(status='unsubmitted-self-check-before-primary-notification',candidate_id=o['candidate_id'],before_rationale=old,after=o,meaning='未提交前补定向原文，未触此前已送块；与原手写入口不同处以此受控自核记录为准。'))
print(sha(f))
