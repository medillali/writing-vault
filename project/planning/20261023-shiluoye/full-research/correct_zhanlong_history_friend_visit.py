"""主审补同家族实际访问后证，不以地名精确检索无命中抹事件。"""
from pathlib import Path
import json,copy,sys
sys.stdout.reconfigure(encoding='utf-8')
B=Path(__file__).parent/'zhanlong';A=B/'audit/whole-book';p=A/'adjudications-history-v01-batch001.json'
S=json.loads((B/'source.json').read_text(encoding='utf-8'));C={int(c['chapter_id'][3:]):c for c in S['chapters']}
rows=json.loads(p.read_text(encoding='utf-8'));idx=next(i for i,r in enumerate(rows) if r['candidate_id']=='v01-question-v01-q-friend-invitations');before=copy.deepcopy(rows[idx])
out=A/'primary-friend-visit-correction';assert not out.exists();out.mkdir();(out/p.name).write_bytes(p.read_bytes())
r=rows[idx];r['status']='answered';r['rationale']='318实际抵西溪、319五人买票游园，湿地实游已有回收；1163主与林东/林成实际赴河南由问剑等接机，1164进北辰家见北辰观学心眼、1165实练火甲，家族做客/领教祖辈功夫也有明确后证。181原邀称河南洛阳、主口允心里畏不愿去，不据后来地名缺同词仍称从未实访；也不补精确原定次日、单独挑战或城市路程细节。生活邀约有实际行动回收，不把每句随口玩笑造契约。'
for n in [181,1163,1164,1165]:
 if n not in r['later_chapters']:
  r['later_chapters'].append(n);r['later_evidence'].append({k:S[k] for k in ['source_id','revision']}|{k:C[n][k] for k in ['chapter_id','start_line','end_line']}|{'claim_kind':'inference'})
(out/'delta.json').write_text(json.dumps(dict(candidate_id=r['candidate_id'],before=before,after=r,reading='root本轮实际原文181 L16175—16201部分与1163—65完整派生四栏；不冒原文全章复读'),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(r,ensure_ascii=False))
