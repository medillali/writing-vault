"""录入第十集回收，保留武器权限与人物身份的边界。"""
import json
from pathlib import Path
p=Path(__file__).parent
cfg=json.loads((p/'cross-input.json').read_text(encoding='utf-8'))
reports={n:json.loads((p/f'vol{n:02d}.json').read_text(encoding='utf-8')) for n in range(1,11)}
def event(key):return next(e for e in reports[int(key[1:3])]['events'] if e['key']==key)
def edge(key,src,dst,kind,label,tracks,claim='inference'):
    return {'id':key,'from':src,'to':dst,'kind':kind,'label':label,'claim_kind':claim,'tracking_keys':tracks,'evidence':event(src)['evidence']+event(dst)['evidence']}
new=[
 edge('cross-taige-02','v09-e04','v10-e01','payoff','苏醒时发现的泰戈变化由刀火测试与问答进一步确认，特殊变异原因仍是研究者解释',['taige-soul-repair'],'fact'),
 edge('cross-emperor-skill-01','v09-e07','v10-e03','payoff','黑龙通过实践掌握的意控能力进一步进入教学，黑大和黑二参与练习，不扩为十孩全会',['children-consciousness'],'fact'),
 edge('cross-knight-03','v09-e06','v10-e04','reversal','雷奥所持噬魂因同源亲和未能伤害黑龙灵魂，刺杀反转为雷奥死亡及同形傀儡生成，教皇动机仍未明',['god-knight-pursuit','soul-devourer-weapon-and-puppets'],'fact'),
 edge('cross-expedition-01','v09-e03','v10-e06','payoff','暂不定时的龙岛承诺进入夺船启航阶段，旅程两月仅至中继岛，不等于取得安息石',['dragon-tomb-expedition','dragon-soul-oath-and-prophet'],'fact'),
 edge('cross-christine-01','v09-e08','v10-e08','reveal','萝茜的新使命后来显出观察黑龙视野的联系用途，角色与读者获知的时点分别保留',['christine-identity','rosy-angel-identity'],'fact'),
 edge('cross-christine-02','v02-e08','v10-e09','reveal','早期女神自称在私人视角和菲力普独立识认下获得更强证据；不据神性推定全部历史自述真实',['christine-identity']),
 edge('cross-tank-04','v09-e09','v10-e02','payoff','取得身体指令权限的战魂在伏击战中被调用，仍会受克制和自行脱离，不能视作意志已驯服',['tank-battle-soul']),
 edge('cross-coercion-01','v08-e07','v10-e06','echo','两次以转生和魂约组织行动均包含强迫，后来获得人力不抹去当时的拒绝权缺失',['blackdragon-autonomy-and-companionship'],'synthesis'),
]
next(e for e in new if e['id']=='cross-christine-02')['evidence']+=event('v10-e08')['evidence']
existing={e['id']:e for e in cfg['edges']};existing.update({e['id']:e for e in new});cfg['edges']=list(existing.values())
(p/'cross-input.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Volume 10 cross-volume relations recorded.')
