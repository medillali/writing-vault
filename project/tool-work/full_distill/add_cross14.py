"""接续第十四集的归途、代理治理与传承代价。"""
import json
from pathlib import Path
p=Path(__file__).parent
cfg=json.loads((p/'cross-input.json').read_text(encoding='utf-8'))
reports={n:json.loads((p/f'vol{n:02d}.json').read_text(encoding='utf-8')) for n in range(1,15)}
def event(key):return next(e for e in reports[int(key[1:3])]['events'] if e['key']==key)
def edge(key,src,dst,kind,label,tracks,claim='inference'):
    return {'id':key,'from':src,'to':dst,'kind':kind,'label':label,'claim_kind':claim,'tracking_keys':tracks,'evidence':event(src)['evidence']+event(dst)['evidence']}
new=[
 edge('cross-return-01','v13-e03','v14-e09','payoff','强制放逐导致的失联以实体返场和魂链恢复收束，会议危机仍待处置',['death-world-return'],'fact'),
 edge('cross-training-01','v13-e09','v14-e01','payoff','入阵后的实际训练在七月回溯中提升感应与分控，能力提升须与后续记忆传承分开',['desert-bones-and-mourning-soul'],'fact'),
 edge('cross-mission-cost-01','v13-e07','v14-e02','reversal','守候使命的霍夫曼因漏带黑龙而遭君王分身灭魂，传承体系显露强制与暴力代价',['desert-bones-and-mourning-soul','cutroman-legacy-and-mission'],'fact'),
 edge('cross-friendship-02','v13-e05','v14-e03','payoff','无约束互助烙印支持金龙应邀随行；同行不等于改为主从魂约',['blackdragon-autonomy-and-companionship'],'fact'),
 edge('cross-state-building-01','v12-e06','v14-e05','payoff','夺取沙里克的计划由缺席期回叙补明，财政工程扩张同时伴随统治者秘密转生',['blackdragon-territory-and-industry'],'fact'),
 edge('cross-faith-01','v13-e02','v14-e05','payoff','传承安排之后娜娜承担信仰媒介作用，但此处不能据此宣布双神传承全部完成',['forest-tree-and-dwarf-faith','nana-protection'],'fact'),
 edge('cross-v14-autonomy','v07-e07','v14-e08','echo','早期重订伙伴边界与后期代理者提出全城活尸计划相对照，组织扩大后授权问题再次出现',['blackdragon-autonomy-and-companionship','seiyne-living-corpse-plan'],'synthesis'),
]
existing={e['id']:e for e in cfg['edges']};existing.update({e['id']:e for e in new});cfg['edges']=list(existing.values())
(p/'cross-input.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Volume 14 cross-volume relations recorded.')
