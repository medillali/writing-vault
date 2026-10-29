"""录入第十一集的解封、代价与远征回收。"""
import json
from pathlib import Path
p=Path(__file__).parent
cfg=json.loads((p/'cross-input.json').read_text(encoding='utf-8'))
reports={n:json.loads((p/f'vol{n:02d}.json').read_text(encoding='utf-8')) for n in range(1,12)}
def event(key):return next(e for e in reports[int(key[1:3])]['events'] if e['key']==key)
def edge(key,src,dst,kind,label,tracks,claim='inference'):
    return {'id':key,'from':src,'to':dst,'kind':kind,'label':label,'claim_kind':claim,'tracking_keys':tracks,'evidence':event(src)['evidence']+event(dst)['evidence']}
new=[
 edge('cross-seal-01','v10-e09','v11-e01','payoff','外封破除后继续解除内部封印，海皇此时才真正获释',['sea-emperor-double-seal'],'fact'),
 edge('cross-christine-03','v10-e08','v11-e03','reveal','观察与教学的深层目的由独处叙述解释为求自身脱困；黑龙并不因此获得读者全部知识',['christine-identity'],'fact'),
 edge('cross-christine-04','v09-e08','v11-e04','reversal','先借萝茜保护并接近黑龙，黑龙拒援后转向娜娜求助；新请求尚未等于脱困成功',['christine-identity','nana-protection']),
 edge('cross-emperor-skill-02','v10-e03','v11-e07','payoff','教学与个体意识发展进入实战，黑大自主提出投枪，不代表其余八孩觉醒',['children-consciousness']),
 edge('cross-armament-02','v10-e04','v11-e02','reveal','已有神器和实体附能并非真正纯魂武装，海皇危机中十孩供力促成黑龙凝兵',['soul-devourer-weapon-and-puppets','desert-bones-and-mourning-soul']),
 edge('cross-expedition-02','v10-e06','v11-e06','payoff','中继岛之后终于登龙岛，现场政治和守卫改变取石行动，尚未取得安息石',['dragon-tomb-expedition'],'fact'),
 edge('cross-seabeast-01','v10-e07','v11-e04','payoff','海兽被杀后其躯体进一步被转生为远征资源，转生耗半魂而非无成本扩军',['dragon-tomb-expedition']),
 edge('cross-church-agency-02','v08-e06','v11-e05','reveal','菲力普独处展露的工具恐惧在对克罗斯的猎犬解释中进一步公开，听者动摇不等于已投效',['church-institution-and-angel-agency']),
]
existing={e['id']:e for e in cfg['edges']};existing.update({e['id']:e for e in new});cfg['edges']=list(existing.values())
(p/'cross-input.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Volume 11 cross-volume relations recorded.')
