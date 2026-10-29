"""记录主代理卷一全文阅读后的文学复核和结构校验；不表示用户认可。"""
import json,hashlib
from pathlib import Path
from check_volume import load_and_check
BASE=Path(__file__).resolve().parent
book='tianxia-wushuang';d=BASE/book/'vol01'
result=load_and_check(book,1)[-1]
(d/'validation.json').write_text(json.dumps({**result,'reader':'primary','unresolved_truncations':0,'semantic_review':'primary reviewed after own full-text reading','user_approval':False},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
review=dict(volume=1,reviewer='primary',status='reviewed_for_library_import',user_approval=False,
 scope='primary实际阅读全文raw0002—0092（90正文+卷标题）；书首raw1另记。复核36九维、20人物/26场景/9机制、32节点22边10线，原文事实/解释/角色话语分层。',
 corrections_verified=[
 '鬼不死盾受174回35不反推未明示的技能等级；地穴盾到92实持，85只是赠与待48。',
 '50谢礼只开交易无明确成交，明月十金未付款；89四级药给付与成交语境不充独立扣款收据。',
 '何假死由十三受命编造；90明月现实确认与何尚未确认分开，陆自称死一昼夜不当医学证明。',
 '尸斑冰毒/阳光/延迟只按小说自述与系统检测叙述管理，不当现实医学；一月研究未成。',
 '心然SSS约定未完成；北冥入游戏工作室已成、现实半月后来苏尚未，乾坤书仅提出、深红王未死。',
 '林圣灵/月瞳/戮风与破碎无双分时揭示，首会为中国第一非擅扩全球；多人合击与最后击杀不混。',
 '匿名二卖雇主血骷髅的占利与君子自述并列；原文性别/外貌评价不转用户审美规则。',
 '89已明示降级不卸仍可用50剑和不卸修理，关闭此前未知，不将真实后补解释列永恒矛盾。',
 '来源金额、蒜数量、职业/物名、重复升级、原文缺句与时钟差保留；图线程只连接成员节点，无把同主题当直接因果。'],
 preflight=result,remaining=['本卷完成不等全书；继续卷二，然后依分工完成全部8卷与全书九维/人物弧/全问题终点审计。','所有研究仍draft，未自动收藏/认可/导入原创canon。'],
 input_sha256={n:hashlib.sha256((d/n).read_bytes()).hexdigest() for n in ['analysis.json','cards.json','graph.json','read-log.json','chapter-notes.jsonl','reader-state.json']})
(BASE/book/'review-vol01.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('review-vol01: passed; six hashes pinned; user approval false')
