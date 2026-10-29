"""录入第七集独立审查后的跨集关系，复用两端已审证据。"""
import json
from pathlib import Path
p=Path(__file__).parent
cfg=json.loads((p/'cross-input.json').read_text(encoding='utf-8'))
reports={n:json.loads((p/f'vol{n:02d}.json').read_text(encoding='utf-8')) for n in range(1,8)}
def event(key):return next(e for e in reports[int(key[1:3])]['events'] if e['key']==key)
def edge(key,src,dst,kind,label,tracks,claim='inference'):
    refs=event(src)['evidence']+event(dst)['evidence']
    return {'id':key,'from':src,'to':dst,'kind':kind,'label':label,'claim_kind':claim,'tracking_keys':tracks,'evidence':refs}
new=[
 edge('cross-angel-03','v06-e06','v07-e05','payoff','封存天使后来成为元力知识来源；其遭吸收与原萝茜失忆后的经历分别记录',['rosy-angel-identity','desert-bones-and-mourning-soul'],'fact'),
 edge('cross-rosy-01','v06-e09','v07-e03','reveal','补魂失忆后仍有姓名触发的敌意，娜娜的关心使本次杀意退去；未证明完整恢复记忆',['rosy-angel-identity'],'fact'),
 edge('cross-history-01','v06-e07','v07-e05','reveal','斯科特承认先前隐瞒并补充古帝国史，已知历史的来源边界进一步收紧',['desert-bones-and-mourning-soul'],'fact'),
 edge('cross-knight-01','v06-e02','v07-e08','payoff','出岛的暗之神骑提供持续方位，追索在同盟败亡后转为出口拦截',['god-knight-pursuit'],'fact'),
 edge('cross-dragon-01','v05-e04','v07-e02','payoff','北行求力遇到曾预告的龙墓危险；损失使风险判断改变，但不重开已解决的印记源头疑问',['dragon-tomb-expedition']),
 edge('cross-armour-01','v06-e08','v07-e09','setup','已掌握的灵魂运用与武装支撑正面应战信心，战果留待下一集；不归因为本集金属化实验',['god-knight-pursuit']),
 edge('cross-autonomy-02','v06-e04','v07-e07','echo','对具体伙伴的关爱边界发展为明确的自由存在宣言；两次选择都未解除灵魂支配关系',['blackdragon-autonomy-and-companionship'],'synthesis'),
]
existing={e['id']:e for e in cfg['edges']}
existing.update({e['id']:e for e in new})
cfg['edges']=list(existing.values())
(p/'cross-input.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Volume 7 cross-volume relations recorded.')
