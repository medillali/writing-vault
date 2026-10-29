"""卷五全部研究主审与定向修改回执。"""
import json,hashlib
from pathlib import Path
from check_volume import load_and_check
B=Path(__file__).parent;book='tianxia-wushuang';d=B/book/'vol05'
_,_,_,a,c,g,_,r=load_and_check(book,5)
assert next(e for e in g['edges'] if e['id']=='v05-e09')['kind']=='echo'
yun=next(x for x in c if x['origin_key'].endswith('/character/yun'))
assert '国王第五子' in json.dumps(yun,ensure_ascii=False) and '神隐王子玛法奥之子' not in json.dumps(a,ensure_ascii=False)
review=dict(volume=5,reviewer='primary',status='reviewed_for_library_import',user_approval=False,
scope='primary完整主审45九维/46人物51场景12机制/59节点51边14线/29问题25源异常；全文归分卷读者，primary定向全文重读0875 L72237—72293，不冒称独立全文复读265章。',
corrections_verified=['云栈·玛法奥自身是神隐城国王第五子，非所谓王子玛法奥之子；卡琳好友由本人述。','e09井与石化对策比较改echo，不凭不同技能使用写铺垫兑现。','奥先死魂散/头分离，后净魂+血制剂复体成无头新阶段；云无心但有呼吸续命不是完全死复。','苏母亡体尚存反证烧灰，不足证明卡兰斯全部历史无责；剑圣已实际死/外援未救及时。','世界古剑3:0为大分三人各2:1，青兽半3:2/0.07秒比赛判不是网络延时；两冠/MVP与本末国战MVP奖未展开分开。','李杀柏丽但系统记主杀郡主并列，主承毁约杀父/任务成功不消人际负债。','谷古剑五万归零由北报+具名共享末战分层，不补晴空雪具体死法，不扩大全部友盟16万。','唐25%营收归城只是被拒提案、剥CGL中国玩家资格通缉由系统实际执行，非现实国籍或现实司法判决。','孵幼神龙本卷未100/不能骑，千骑换千法未交，林藏事/返苏及补偿重练未结；后卷不会倒灌。'],
preflight=r,remaining=['按卷序3/4先正式保存再导5；研究仍draft/无用户认可。','正式保存卷末快照不等全书终点审计，三书项目继续。'],input_sha256={n:hashlib.sha256((d/n).read_bytes()).hexdigest() for n in ['analysis.json','cards.json','graph.json','read-log.json','chapter-notes.jsonl','reader-state.json']})
(B/book/'review-vol05.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('review-vol05 passed; six hashes pinned; pending prior-volume import')
