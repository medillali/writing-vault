"""接续第十五集的裁决、晶体损失、圣器线索和权力调整。"""
import json
from pathlib import Path
p=Path(__file__).parent
cfg=json.loads((p/'cross-input.json').read_text(encoding='utf-8'))
reports={n:json.loads((p/f'vol{n:02d}.json').read_text(encoding='utf-8')) for n in range(1,16)}
def event(key):return next(e for e in reports[int(key[1:3])]['events'] if e['key']==key)
def edge(key,src,dst,kind,label,tracks,claim='inference'):
    return {'id':key,'from':src,'to':dst,'kind':kind,'label':label,'claim_kind':claim,'tracking_keys':tracks,'evidence':event(src)['evidence']+event(dst)['evidence']}
new=[
 edge('cross-corpse-plan-01','v14-e08','v15-e01','reversal','黑龙回归后暂时否决全城活尸计划，依据是时机与收益，并非宣布永久放弃或普遍人道原则',['seiyne-living-corpse-plan','blackdragon-autonomy-and-companionship'],'fact'),
 edge('cross-corpse-plan-02','v14-e08','v15-e08','echo','原先全城方案在红月转机中获得重新准备授权，仍未实际发动',['seiyne-living-corpse-plan','alliance-war-and-divine-power'],'fact'),
 edge('cross-crystal-loss-01','v12-e09','v15-e03','reversal','八晶体初觉醒后的武装成长伴随十七、十八冻碎损失，成长不能抹去个体存亡代价',['children-consciousness'],'fact'),
 edge('cross-prophet-control-02','v12-e05','v15-e04','payoff','先知自身完整魂约之后，黑龙进一步收走剩余三十六龙的魂约；保留其指挥职不等于解除主从限制',['dragon-soul-oath-and-prophet','undead-dragon-force-survival'],'fact'),
 edge('cross-relics-01','v13-e08','v15-e06','payoff','权杖和第三圣器的追索在海底遗迹推进，三器联系红月通道；见到彼端并不等于已实体抵达',['desert-bones-and-mourning-soul'],'fact'),
 edge('cross-legacy-use-01','v14-e02','v15-e06','payoff','继承的知识支持识别遗物和寻找旧帝国，使命接续仍不保证继承者理解全部隐情',['cutroman-legacy-and-mission','desert-bones-and-mourning-soul']),
 edge('cross-v15-church-agency','v13-e03','v15-e01','reveal','菲力普对放逐原因作自我说明，确认其重视黑龙对自身的利用价值',['church-institution-and-angel-agency'],'fact'),
 edge('cross-faith-02','v14-e09','v15-e07','reveal','后文进一步说明自然神本源借娜娜、分身留树；少女主体与神明仍须分开记录',['forest-tree-and-dwarf-faith','nana-protection'],'fact'),
]
new[-1]['evidence'].append({'chapter_id':'ch-0161','start_line':19708,'end_line':19725})
existing={e['id']:e for e in cfg['edges']};existing.update({e['id']:e for e in new});cfg['edges']=list(existing.values())
(p/'cross-input.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Volume 15 cross-volume relations recorded.')
