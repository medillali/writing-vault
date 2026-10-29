"""接续第十七集的夺体回收、假旗控制与双灵格揭示。"""
import json
from pathlib import Path
p=Path(__file__).parent
cfg=json.loads((p/'cross-input.json').read_text(encoding='utf-8'))
reports={n:json.loads((p/f'vol{n:02d}.json').read_text(encoding='utf-8')) for n in range(1,18)}
def event(key):return next(e for e in reports[int(key[1:3])]['events'] if e['key']==key)
def edge(key,src,dst,kind,label,tracks,claim='inference'):
    return {'id':key,'from':src,'to':dst,'kind':kind,'label':label,'claim_kind':claim,'tracking_keys':tracks,'evidence':event(src)['evidence']+event(dst)['evidence']}
new=[
 edge('cross-v17-false-flag','v16-e09','v17-e01','payoff','秘密不死献祭的后果落实为安德鲁与光之神骑转生、奉命冒用黑龙名义；转生没有使他们成为黑龙真实部属',['church-institution-and-angel-agency','church-false-flag-and-cleansing-army'],'fact'),
 edge('cross-v17-chaos','v16-e08','v17-e02','payoff','混沌之灵的悬念由形成过程、战技传授和反吞神格接续，黑龙此次夺体危机解除',['daro-possession-crisis','desert-bones-and-mourning-soul'],'fact'),
 edge('cross-v17-history','v15-e07','v17-e05','reveal','先前缺席君王与三主神的推测得到向读者展开的历史说明；黑龙此时并未同步获得全部历史',['desert-bones-and-mourning-soul','niruda-split-personhood-and-divinity'],'fact'),
 edge('cross-v17-knight','v14-e03','v17-e07','reversal','曾按位面职责放行黑龙的光之神骑，后执行私令成为假旗统帅并被黑龙吞魂，职务与当前选择并不等同',['god-knight-pursuit','church-institution-and-angel-agency'],'fact'),
 edge('cross-v17-prophet-control','v15-e04','v17-e03','payoff','收走先知私兵魂约形成后续组织制衡，但其平民杀戮仍发生，权力受限不等于道德问题解决',['dragon-soul-oath-and-prophet'],'fact'),
 edge('cross-v17-war','v16-e06','v17-e03','payoff','收复里斯特及扩军之后，同盟领土光复；后续继续入侵与假旗危机须另计，不能当战争已彻底结束',['alliance-war-and-divine-power'],'fact'),
 edge('cross-v17-children','v12-e08','v17-e06','echo','承担赋魂工作后的大二在战场违先知命令救同类，工具能力与独立价值选择形成不同层次的成长',['children-consciousness','blackdragon-autonomy-and-companionship'],'synthesis'),
 edge('cross-v17-divine-control','v16-e04','v17-e09','echo','自然神控制神谕与尼鲁达双灵格经营恐惧信仰相互映照，均把群体信仰转为可调动的权力资源，具体责任和人格仍各自独立',['forest-tree-and-dwarf-faith','church-institution-and-angel-agency'],'synthesis'),
]
existing={e['id']:e for e in cfg['edges']}
for e in new:
    if e['id'] in existing:assert (existing[e['id']]['from'],existing[e['id']]['to'])==(e['from'],e['to'])
existing.update({e['id']:e for e in new});cfg['edges']=list(existing.values())
(p/'cross-input.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Volume 17 cross-volume relations recorded.')
