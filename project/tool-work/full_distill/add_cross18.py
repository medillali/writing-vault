"""连接终卷的回归、知识应用、音乐战果与价值选择。"""
import json
from pathlib import Path
p=Path(__file__).parent
cfg=json.loads((p/'cross-input.json').read_text(encoding='utf-8'))
reports={n:json.loads((p/f'vol{n:02d}.json').read_text(encoding='utf-8')) for n in range(1,19)}
def event(key):return next(e for e in reports[int(key[1:3])]['events'] if e['key']==key)
def edge(key,src,dst,kind,label,tracks,claim='fact'):
    return {'id':key,'from':src,'to':dst,'kind':kind,'label':label,'claim_kind':claim,'tracking_keys':tracks,'evidence':event(src)['evidence']+event(dst)['evidence']}
new=[
 edge('cross-v18-return','v17-e09','v18-e01','payoff','红月通道开启接续为哈力与子民灵魂跨界归来，并非把被放逐的物理大陆搬回',['desert-bones-and-mourning-soul']),
 edge('cross-v18-dragon-people','v12-e01','v18-e02','reveal','帝勒带族退离后的去向得到补叙：贫荒促使迁往深渊，侵略后不足两千返归；不能据此补全每位族人的命运',['dragon-bloodline-and-confinement']),
 edge('cross-v18-gun','v16-e01','v18-e05','reveal','雷奥恢复神智后续出送枪机缘的布局说明：教皇借他送枪，为黑龙布置机缘，不等雷奥知晓全部计划',['soul-devourer-weapon-and-puppets','god-knight-pursuit']),
 edge('cross-v18-memory-practice','v14-e02','v18-e04','payoff','切罗曼尔传承的知识在投影反追、时间干扰与跨界行动中转为应用；记忆继承不等原力量和人格复活',['cutroman-legacy-and-mission','memory-and-power']),
 edge('cross-v18-music','v15-e02','v18-e06','payoff','音乐教学形成乐团，安魂稳军与雷霆清场取得实际战果；乐师有伤亡，杀敌同时给本源供能，不能当全场战争已胜',['music-magic-and-ordinary-specialists','roder-song-and-wife']),
 edge('cross-v18-source','v17-e05','v18-e07','reveal','旧帝国与神祇历史接续为切里莫制造本源并被反噬；旧宇宙起源的口述尚未讲完，已证死亡与未证传说分别保留',['desert-bones-and-mourning-soul','source-consciousness-and-world-freedom']),
 edge('cross-v18-ethics','v16-e07','v18-e08','echo','达罗亚毁己民取能与黑龙要求减少所有种族死亡、托付子民形成价值对照；这一选择不抹去黑龙阵营此前杀戮责任',['soul-consumption-ethics','blackdragon-autonomy-and-companionship'],'synthesis'),
 edge('cross-v18-children','v17-e06','v18-e08','echo','大二主动救同类之后，黑龙把君王烙印交哈力保子民，主体选择与保护责任相连；其余孩子是否觉醒仍未知',['children-consciousness','blackdragon-autonomy-and-companionship'],'synthesis'),
 edge('cross-v18-divinity','v17-e09','v18-e08','payoff','曾重掌公正神格的女灵格最终主动赠格并疲惫离去，教皇另一人格的寿命后果并未同时得到交代',['niruda-split-personhood-and-divinity','church-institution-and-angel-agency']),
 edge('cross-v18-nana','v16-e04','v18-e09','payoff','双神传承与自然神控制的代价之后，后记确认娜娜成长并保青春；未据此补写正式成神或克丽丝本体解封',['nana-protection','forest-tree-and-dwarf-faith']),
 edge('cross-v18-home','v12-e06','v18-e09','echo','旧领地供应与治理困难在后记自由城市生活中获得方向性回应，具体停战和制度过程仍被省略',['blackdragon-territory-and-industry','blackdragon-autonomy-and-companionship'],'synthesis'),
]
existing={e['id']:e for e in cfg['edges']}
for e in new:
    if e['id'] in existing:assert (existing[e['id']]['from'],existing[e['id']]['to'])==(e['from'],e['to'])
existing.update({e['id']:e for e in new});cfg['edges']=list(existing.values())
(p/'cross-input.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Volume 18 cross-volume relations recorded.')
