import copy,json
from save_manual_batch import P,F,read,write,sha
f=P/'adjudications-local-v05-batch013.json';rows=read(f);b=next(x for x in rows if x['candidate_id'].endswith('0167-01'));a=copy.deepcopy(b)
a['rationale']='1147三军前线已列、1149三军与炮真实撤保，1157守城成功；1169王正式令梁印转兵部侍郎/周宁即花枪复秋收统领，花本人收到系统，1146借战复职意图已有明确后证。1146二十龙借天翎获交易令但本次二十逐名到阵/伤亡账未独列，复合项只保该具体借军执行明细未详，不因任职已答代全军到阵。'
n=next(json.loads(s) for s in (F/'vol05-chapter-notes.jsonl').read_text(encoding='utf-8').splitlines() if json.loads(s)['chapter_id']=='ch-1169');e=copy.deepcopy(a['later_evidence'][0]);e.update(chapter_id=n['chapter_id'],start_line=n['start_line'],end_line=n['end_line']);a['later_chapters'].append(1169);a['later_evidence'].append(e)
p=P/'huaqing-office-after-defense-proposal.json';write(p,{'status':'proposal-pending-primary-review-not-applied','reason':'本轮完整补读1169王令与花本人系统回讯，补已交013任职直接后证；其余19和二十龙实际到战边界不变。','changes':[{'path':f.name,'candidate_id':b['candidate_id'],'input_sha256':sha(f),'before':b,'after':a,'scope':'仅0167-01理由及追加1169，保partial/domain/其余19'}]});print(sha(p))
