"""录入第六集审查确认的跨集变化，所有关系有双端来源。"""
import json
from pathlib import Path

p=Path(__file__).parent
config=json.loads((p/'cross-input.json').read_text(encoding='utf-8'))
def ev(ch,a,b):return {'chapter_id':f'ch-{ch:04d}','start_line':a,'end_line':b}
def edge(key,src,dst,kind,label,tracks,refs,claim='inference'):
    return {'id':key,'from':src,'to':dst,'kind':kind,'label':label,'claim_kind':claim,'tracking_keys':tracks,'evidence':refs}
new=[
 edge('cross-children-02','v04-e06','v06-e01','payoff','对泰戈的特殊反应发展为黑大主动开口和控制断开；骨架原主仍未确认',['children-consciousness'],[ev(40,5042,5087),ev(41,5088,5115),ev(57,6963,7008)]),
 edge('cross-angel-01','v05-e03','v06-e06','reversal','借体降临的强敌被群体控制后封印本源；封印不等于杀灭',['rosy-angel-identity'],[ev(47,5773,5815),ev(64,7861,7897)],'fact'),
 edge('cross-angel-02','v05-e03','v06-e09','reveal','降临者采用萝茜名字的疑问回收为天使与原残灵分离；原萝茜补魂醒来仍失忆',['rosy-angel-identity'],[ev(47,5813,5815),ev(66,8177,8214)],'fact'),
 edge('cross-mark-02','v05-e04','v06-e06','payoff','北行寻找印记源头后，斯科特确认自己散播印记；龙墓假设未成立',['red-moon-destination'],[ev(48,5876,5941),ev(64,7881,7897)],'fact'),
 edge('cross-desert-01','v05-e08','v06-e07','reveal','沙下骨骸得到斯科特的远古战争解释，史诗有起始边界；战因胜负仍未明',['desert-bones-and-mourning-soul'],[ev(55,6847,6869),ev(65,7945,7968)]),
 edge('cross-roder-02','v05-e05','v06-e07','payoff','音乐家随队后的安魂琴歌产生战力之外的集体价值；亡妻现状未因此解决',['roder-song-and-wife','blackdragon-autonomy-and-companionship'],[ev(51,6335,6388),ev(65,8048,8081)]),
 edge('cross-identity-news-01','v05-e01','v06-e02','cause','幸存者带回的不死身份情报引起疾风、同盟及教会不同应对',['god-knight-pursuit'],[ev(45,5540,5568),ev(58,7110,7145),ev(59,7200,7226)],'fact'),
 edge('cross-tank-02','v03-e03','v05-e09','reveal','再压回体内的战魂仍未炼化，神圣伤只造成共同压制而非根除',['tank-battle-soul'],[ev(29,3514,3515),ev(46,5623,5632)],'fact'),
]
existing={e['id']:e for e in config['edges']}
existing.update({e['id']:e for e in new})
config['edges']=list(existing.values())
(p/'cross-input.json').write_text(json.dumps(config,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
r=json.loads((p/'vol06.json').read_text(encoding='utf-8'))
for c in r['characters']:
    if c['name']=='斯科特':
        c['aliases']=[]
        if '亡灵圣者' not in c['summary']:c['summary']='被称为亡灵圣者的'+c['summary']
(p/'vol06.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Added audited cross-volume edges; preserved entity distinction.')
