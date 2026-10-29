from save_tail_manual import Q,F,ROOT,read,write,sha
import json
p=Q/'adjudications-local-v06-tail-batch003.json';row=read(p)[1];after=json.loads(json.dumps(row,ensure_ascii=False))
after['status']='partial';after['rationale']='1280流霜拟再带兰取上位格，1295叙已再为兰斩得一枚上位格，故取得神格的提议已有后证，不能继续写全未回收。1295却未演兰炼完/系统高阶飞升，1296只明确兰实际驻凡书；1274子舒自述斩一帝与1295回述流杀两帝还有归属口径差。至终点缺的是兰是否实炼成上位及对应格的明确归属链，不是完全没有后续夺格。'
after['later_chapters']=[1274,1280,1295,1296,1386]
notes={int(n['chapter_id'].split('-')[1]):n for n in map(json.loads,(F/'vol06-chapter-notes.jsonl').read_text(encoding='utf-8').splitlines())}
ev=[];f=F/'vol06-chapter-notes.jsonl'
for k in after['later_chapters']:
 n=notes[k];ev.append(dict(source_id=n['source_id'],revision=n['revision'],chapter_id=n['chapter_id'],start_line=n['start_line'],end_line=n['end_line'],claim_kind='fact',evidence_access='完整正式四栏派生；不转移原文实读归属',material_path=str(f.relative_to(ROOT)).replace('\\','/'),material_sha256=sha(f),source_reader=n['reader']))
after['later_evidence']=ev
write(Q/'lan-upper-godhead-later1295-proposal.json',dict(status='proposal-not-applied',batch_sha256=sha(p),reason='下一批顺读1295发现已为兰取上位格的后证，须撤全未回收结论；未经primary核定不改已交批。',before=row,after=after,other_19_objects_unchanged=True));print(sha(Q/'lan-upper-godhead-later1295-proposal.json'))
