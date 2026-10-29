"""已实际读1108—1110派生笔记后，更新未签旧草稿的明确后态。"""
import json,copy
from pathlib import Path
B=Path(__file__).parent/'zhanlong';P=B/'audit/whole-book'
def read(q):return json.loads(q.read_text(encoding='utf-8'))
s=read(B/'source.json');cs={int(c['chapter_id'][3:]):c for c in s['chapters']}
updates={
 'v01-question-v01-q-rolin':('answered','559NPC武悼天王确实守城，572护伤罗林，588以一敌三君重伤被救并自责；589交青萝照顾，1108流霜明确报告身体完全重塑，主亲见锻炉NPC冉闵，1109又实为主炼戒。罗林背叛及列异魔君王否定其忠誓；不把NPC守誓付出混成同名玩家老K，也不以新身体洗掉旧重伤。',[559,572,588,589,1108,1109]),
 'v01-thread-t-reincarnation':('answered','178—179救魂实复生、209有条件留守后，559守城/572护伤罗林、588抗三君而重伤，589托青萝照顾，1108明身体完全重塑并主亲见锻炉NPC，1109实际炼成王戒。誓言经行为检验且伤后恢复有专门后证；罗林背誓另失败，NPC冉闵和玩家老K不得合并。',[178,179,559,572,588,589,1108,1109]),
 'v01-thread-t-mocha':('partial','915抹茶实际夺城杀友、916舞揭身份/林释亲缘；946方谈爱主属方推，956主修正非强逼交城，960堂妹线索后仍需本人行动。1086为爱追寻本人认薛柔/抹茶/小妖，1109跨服正式回斩任长老，1356参与订婚；旧动作弱需重估，不等所有关心皆假或责任被爱赦免。早合同与指定圣魂盾仍无独立全结证。',[915,916,946,956,960,1086,1109,1356,1386]),
}
deltas=[];dest=P/'history-v01-pre-sign';dest.mkdir(exist_ok=True)
for name in ['adjudications-history-v01-batch001.json','adjudications-history-v01-batch002.json']:
 p=P/name;raw=p.read_bytes();rows=read(p);changed=False
 for row in rows:
  if row['candidate_id'] not in updates:continue
  before=copy.deepcopy(row);status,rationale,nums=updates[row['candidate_id']]
  row.update(status=status,rationale=rationale,later_chapters=nums,later_evidence=[{k:s[k] for k in ['source_id','revision']}|{k:cs[n][k] for k in ['chapter_id','start_line','end_line']}|{'claim_kind':'inference'} for n in nums])
  deltas.append(dict(file=name,candidate_id=row['candidate_id'],before=before,after=copy.deepcopy(row)));changed=True
 if changed:
  assert not (dest/name).exists();(dest/name).write_bytes(raw);p.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert len(deltas)==3
(P/'history-v01-pre-sign-corrections.json').write_text(json.dumps({'reviewer':'primary','basis':'实际读1108—1110后补上NPC冉闵重塑与炼戒，1086/1109替换错指1090的本人认名/回会后证；全未签稿，保before。','changes':deltas},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('CORRECTED',len(deltas))
