"""钉卷三主审；阶段阅读与最终状态分开。"""
import json,hashlib
from pathlib import Path
from check_volume import load_and_check
B=Path(__file__).parent;d=B/'tianxia-wushuang'/'vol03'
_,_,_,a,c,g,_,r=load_and_check('tianxia-wushuang',3)
s=next(x for x in c if x['origin_key'].endswith('/scene/dragonblade'))
assert '升105' in s['content']['choice'] and '升100' in s['content']['choice']
assert '1:2负' in next(x for x in c if x['origin_key'].endswith('/scene/tournament'))['content']['choice']
assert not any(e['id']=='w03-e-acceptance' for e in g['edges'])
assert next(e for e in g['edges'] if e['id']=='w03-e-promotion')['kind']=='setup'
assert next(e for e in g['edges'] if e['id']=='w03-e-recooking')['to']=='w03-valley'
assert '战地' not in next(e for e in g['edges'] if e['id']=='w03-e-identity')['label']
review=dict(volume=3,reviewer='primary',status='reviewed_for_library_import',user_approval=False,
 scope='主审完整36九维、23人物32场景10机制、40节点24边14线程16知识与10源异常；分卷读者全文亲读归属保留，主审未声称独立全文复读。',
 corrections_verified=['决赛古剑视角1:2负雪银，官方赛果与主观末秒让步并存。','捕狐升100武神与紫域后105实穿偷天/镶简易靴分开；读者完整复读363/367/368。','e-promotion收为setup；小蛮入盟不伪连第三城赌约；灵烹实用指谷战。','线程成员只补有语义实际作用节点；战天名称修正；金石误信及后续确认分开。','三婶十万L44853定点核查：实际受款为三婶，照父用途不写父亲直接收款。','寒刃活逃/骨毁与NPC复活例外分开；死者再在场、CD/声望/奖励/套数异常保源。','九龙诸人真死、末刀与分装独立、KOF新胜不撤1:4败及第三城约。','卷末双线未终结，斗死斧在乱包，青虎未返，未借后卷回填。'],
 preflight=r,remaining=['研究draft，未获用户风格认可；不得导原创canon。'],
 input_sha256={n:hashlib.sha256((d/n).read_bytes()).hexdigest() for n in ['analysis.json','cards.json','graph.json','read-log.json','chapter-notes.jsonl','reader-state.json']})
(d.parent/'review-vol03.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('review-vol03 passed; six hashes pinned')
