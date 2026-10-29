"""卷八完整语义审阅及唯一超证措辞纠正后的签收。"""
import hashlib,json
from pathlib import Path
from check_volume import load_and_check

B=Path(__file__).parent;book='tianxia-wushuang';d=B/book/'vol08'
source,spec,_,analysis,cards,graph,_,preflight=load_and_check(book,8)
target=next(c for c in cards if c['origin_key'].endswith('/scene/tianhuang'))
for field in ['summary','outcome','state_change']:
    assert '未见性交易履行证据' in target['content'][field]
assert '未见性交易履行证据' in next(n for n in graph['nodes'] if n['id']=='w08-tianhuang')['summary']
assert '性交易未履行' not in json.dumps([analysis,cards,graph],ensure_ascii=False)
assert preflight['cards']=={'character':35,'scene':36,'pattern':10}
review=dict(volume=8,reviewer='primary',status='reviewed_for_library_import',user_approval=False,
    scope='primary逐项主审36九维/12源疑/35角色状态/10迁移机制，35人物36场景10机制卡，45节点28边13线程与19知识记录；primary亲读前68片并完整读后35条派生笔记及实际复读1608/1609，不冒认一人亲读全105片。',
    corrections_verified=['天荒场景及图/报告由肯定未履行改未见履行证据，未知不作否定事实。','1527索菲娅发起护送、苏菲是受援方，回查原文两人不同。','赤龙臂1592录像转述补后段使用，保交还动作未直接展示。','强暗示陆林生还恢复与明确赴美治疗、临床根治未知分层；何末疗仍蒙纱。','最终四城征服/英雄城保/两城废弃、魂归正式分盟和伪徽分开。','神装借一月与二队冠军杯分别有回执，具体最终击烛和系统MVP未知。'],
    semantic_review_document='review-wushuang-vol08.md',preflight=preflight,
    remaining=['按卷六、七、八顺序保存；整书综合与终点审计另验。','研究草稿不是用户个人风格或审美已认可；斩龙和整库备份恢复仍待继续。'],
    input_sha256={n:hashlib.sha256((d/n).read_bytes()).hexdigest() for n in ['analysis.json','cards.json','graph.json','read-log.json','chapter-notes.jsonl','reader-state.json']})
(B/book/'review-vol08.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'review':'vol08-primary-passed-six-hashes-pinned','preflight':preflight},ensure_ascii=False))
