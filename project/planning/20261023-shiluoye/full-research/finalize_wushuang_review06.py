"""卷六全量语义审阅与定向原文复核后的主代理签收。"""
import hashlib,json
from pathlib import Path
from check_volume import load_and_check

B=Path(__file__).parent;book='tianxia-wushuang';d=B/book/'vol06'
source,spec,_,a,c,g,_,r=load_and_check(book,6)
def card(suffix):return next(x for x in c if x['origin_key'].endswith(suffix))
assert r['cards']=={'character':48,'scene':61,'pattern':15}
wild=card('/scene/wild-city');assert '归泪所在野性王座' in wild['content']['summary']
assert '归泪所在野性王座' in next(n for n in g['nodes'] if n['id']=='wild-city')['summary']
assert '明宇断臂' in card('/scene/kalan-rescue')['content']['obstacle']
assert '弓交易' not in json.dumps(card('/character/sansheng'),ensure_ascii=False)
assert '售林' not in json.dumps(card('/character/sansheng'),ensure_ascii=False)
assert next(n for n in g['nodes'] if n['id']=='three-souls')['knowledge'][0]['state']=='misbelieves'
dim={x['id']:x for rows in a['dimensions'].values() for x in rows}
assert '己亡479002' in dim['v06-attrition-does-not-disappear']['fact']['text']
assert '1239' in dim['v06-promises-not-results']['fact']['text']
assert '嘶风封印水晶' in dim['v06-objects-change-functions']['fact']['text']
review=dict(volume=6,reviewer='primary',status='reviewed_for_library_import',user_approval=False,
    scope='primary逐项主审45九维、48角色状态、60集中问题、235逐章未决、4得失；48人物61场景15机制卡、72节点56边26线程与全部内嵌知识记录。primary亲读尾60原文、完整读前175派生四栏笔记；不冒称独读全235片。',
    semantic_review_document='review-wushuang-vol06.md',
    corrections_verified=['原文1173全文回读：飞炎领地归野性王座，烛未阻泪，琥杀烛后被烛龙将领杀；保护伞另线。','吻提整编/陆提保护伞名，1199陆仍盟主，1219吻已盟主各保时点。','1262艾蕾拉掉弓由林向七人队买，不归三生；已删误归。','卡兰先明宇断臂后米偷袭断腿，卡琳止血未全愈。','艾误信林浅真悔、1265背约反证；misbelieves明确belief。','1183己亡479002与杀敌7828831分开；水晶名/热沙实际结算/逐籍定位/生死谷规则/十万取魂补偿已核修。','primary回读0089明文降级不卸原装备可续穿，225盾在221使用不列矛盾，原始初判保留另作纠正。','游戏资格恢复不作现实国籍；卷末斯特活/心重伤/SS未结；后卷不能倒灌。'],
    preflight=r,remaining=['按卷序正式导入；全书终点审计和综合另验，用户评价保持draft。'],
    input_sha256={n:hashlib.sha256((d/n).read_bytes()).hexdigest() for n in ['analysis.json','cards.json','graph.json','read-log.json','chapter-notes.jsonl','reader-state.json']})
(B/book/'review-vol06.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'review':'vol06-primary-passed-six-hashes-pinned','preflight':r},ensure_ascii=False))
