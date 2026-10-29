"""录入第九集的既有伏笔回收与阶段状态；不提前使用第十集。"""
import json
from pathlib import Path
p=Path(__file__).parent
cfg=json.loads((p/'cross-input.json').read_text(encoding='utf-8'))
reports={n:json.loads((p/f'vol{n:02d}.json').read_text(encoding='utf-8')) for n in range(1,10)}
def event(key):return next(e for e in reports[int(key[1:3])]['events'] if e['key']==key)
def edge(key,src,dst,kind,label,tracks,claim='inference'):
    return {'id':key,'from':src,'to':dst,'kind':kind,'label':label,'claim_kind':claim,'tracking_keys':tracks,'evidence':event(src)['evidence']+event(dst)['evidence']}
new=[
 edge('cross-altar-02','v08-e09','v09-e01','payoff','祭坛启动后的声音与图克守护来源得到解释，混合灵魂的分批转生完成；知识继承不等于力量或原人格直接替换',['tuk-and-the-transformation-altar','sunken-undead-kingdom','transformation-altar-and-mang-survival'],'fact'),
 edge('cross-prophet-01','v07-e04','v09-e03','reveal','先知披露本名、分身和先前隐瞒，并提高筹码使拒绝转为有条件承诺；尚未实际取回安息石',['dragon-soul-oath-and-prophet','dragon-tomb-expedition'],'fact'),
 edge('cross-tank-03','v05-e09','v09-e09','payoff','先前不能炼化的战魂再次脱困后出现身体权限控制，独立战意仍反抗；内患只获有限进展',['tank-battle-soul'],'fact'),
 edge('cross-rosy-03','v08-e08','v09-e08','payoff','接触克丽丝后产生保护黑龙的新使命，萝茜行动履行使命但不认旧友；不据使命本身确认克丽丝神性',['rosy-angel-identity','christine-identity'],'fact'),
 edge('cross-industry-01','v07-e01','v09-e02','cause','人工金属化进入扩张阶段后受钢材供给与单人产能限制，促成城中采购和贸易谈判',['blackdragon-territory-and-industry'],'fact'),
 edge('cross-hero-01','v05-e07','v09-e05','echo','两次私人取利与公共救援结果重叠，见证和组织传播分别塑造英雄形象；不是同一宣传活动',['soul-consumption-ethics','alliance-war-and-divine-power'],'synthesis'),
 edge('cross-knight-02','v08-e06','v09-e06','setup','撤回总部的雷奥获得噬魂，先前离开的追兵转成新武器威胁；本集尚未交锋',['god-knight-pursuit'],'fact'),
 edge('cross-taige-01','v06-e01','v09-e04','reveal','转生后的泰戈继续经历沉睡与苏醒，身体变化有表现，修魂解释来自斯科特而具体能力仍待检验',['taige-soul-repair']),
]
existing={e['id']:e for e in cfg['edges']};existing.update({e['id']:e for e in new});cfg['edges']=list(existing.values())
update={'key':'transformation-altar-and-mang-survival','volume':9,'title':'氓族与骑士灵魂转生后的存续','kind':'main','status':'partial',
 'question':'已完成转生者如何适应存在形式，其人格与意愿将如何延续？',
 'resolution_note':'本集三千余混合灵魂完成分批转生，并非全都是氓族。存续结果已明确，弱魂适应、威逼忠誓和自主性问题仍保留；不能用后来成功倒推早先强制行为获得同意。',
 'evidence':event('v09-e01')['evidence']}
updates={(u['key'],u['volume']):u for u in cfg.get('state_updates',[])};updates[(update['key'],9)]=update;cfg['state_updates']=list(updates.values())
(p/'cross-input.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Volume 9 cross-volume relations recorded.')
