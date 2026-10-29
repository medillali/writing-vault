"""记录卷四全部研究的主审及定点修订核验；不冒称主审全文复读。"""
import json,hashlib
from pathlib import Path
from check_volume import load_and_check
B=Path(__file__).parent;book='tianxia-wushuang';d=B/book/'vol04'
src,spec,_,a,c,g,_,r=load_and_check(book,4)
for eid in ['e-geometry-training-feit-cost','e-siege-wall-mirror-counter','e-sealing-contract-beastking-rebirth']:assert next(e for e in g['edges'] if e['id']==eid)['kind']=='setup'
obs=next(x for x in a['dimensions']['characters'] if x['id']=='v04-distributed-work')
assert all(any(e['chapter_id']=='ch-0699' and e['start_line']==58857 for e in obs[p]['evidence']) for p in ['fact','inference','mechanism'])
assert any(e['chapter_id']=='ch-0699' for e in obs['evidence'])
small=next(x for x in c if x['origin_key'].endswith('/character/xiaoman'));assert '水云谣' not in json.dumps(small,ensure_ascii=False)
review=dict(volume=4,reviewer='primary',status='reviewed_for_library_import',user_approval=False,
scope='主审完整45九维/30人物50场景12机制/60节点45边22线/37问题；源全文阅读归分卷读者，primary定向完整重读725—726并核0699单行，非声称独立全文复读。',
corrections_verified=['3条前后阶段关系收窄setup，未凭相邻时序建立直接因果。','distributed-work矿工月光石补0699 L58857，保乱月独立人。','漂亮小蛮不并水云谣；零度冰点为人/焚琴煮鹤为会。','心如日月725系统已真死，不能用此前阶段活态盖终稿。','暗月本次90%NPC恢复例外；达达魂融狼不同蒙川肉身复活。','六转第二全服第一战士；楼车李斗残活与斗后来实死分开；维760被换存769才实杀。','有限复号保部分字段但神泣仍耗，何单独退让不代表三人协议。','黑海已结/暗月再围仅3h雪银召骑，未骑名/胜负/十级；所有源金额星级舰数漂移保留。'],
preflight=r,remaining=['按卷序待卷三先正式保存后再导4。','研究draft/无用户认可，不导原创canon。'],input_sha256={n:hashlib.sha256((d/n).read_bytes()).hexdigest() for n in ['analysis.json','cards.json','graph.json','read-log.json','chapter-notes.jsonl','reader-state.json']})
(B/book/'review-vol04.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('review-vol04 passed; six hashes pinned; pending prior-volume import')
