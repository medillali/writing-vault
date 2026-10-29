import copy,json
from save_manual_batch import P,F,read,write,sha
f=P/'adjudications-local-v05-batch012.json';rows=read(f);b=rows[-1];a=copy.deepcopy(b)
a['rationale']='1134四将全血契成并跟青萝练，补1133仅韩落地确认；子舒讲价后主另许一万弹/精晶运炼为新约。1145韩明确大量弹几乎每日运龙城，持续互供已实际履行；但1134特定新增一万的批次/精确交总数未独列，不以旧五千或后弹充足硬认该数量已齐。1137末魂到手/1138升级已成，复合项只保数量层未详。'
n=next(json.loads(s) for s in (F/'vol05-chapter-notes.jsonl').read_text(encoding='utf-8').splitlines() if json.loads(s)['chapter_id']=='ch-1145');e=copy.deepcopy(a['later_evidence'][0]);e.update(chapter_id=n['chapter_id'],start_line=n['start_line'],end_line=n['end_line']);a['later_chapters'].append(1145);a['later_evidence'].append(e)
p=P/'continuous-ammunition-performance-proposal.json';write(p,{'status':'proposal-pending-primary-review-not-applied','reason':'本轮补读1145韩持续供弹回执，防已交前组看似全无履约后证；不改partial与特定数量边界。','changes':[{'path':f.name,'candidate_id':b['candidate_id'],'input_sha256':sha(f),'before':b,'after':a,'scope':'仅0154-01理由及追加1145，status/domain/其余19不变'}]});print(sha(p))
