"""录入第八集跨集伏笔与回收，区分同类主题和事实关联。"""
import json
from pathlib import Path
p=Path(__file__).parent
cfg=json.loads((p/'cross-input.json').read_text(encoding='utf-8'))
reports={n:json.loads((p/f'vol{n:02d}.json').read_text(encoding='utf-8')) for n in range(1,9)}
def event(key):return next(e for e in reports[int(key[1:3])]['events'] if e['key']==key)
def edge(key,src,dst,kind,label,tracks,claim='inference'):
    return {'id':key,'from':src,'to':dst,'kind':kind,'label':label,'claim_kind':claim,'tracking_keys':tracks,'evidence':event(src)['evidence']+event(dst)['evidence']}
new=[
 edge('cross-cliffhanger-01','v07-e09','v08-e01','payoff','上集盾墙冲撞前的悬停在本集战斗中兑现；雷奥救主教并灭口使胜负之外再生身份问题',['god-knight-pursuit'],'fact'),
 edge('cross-armour-02','v06-e08','v08-e01','payoff','此前制作后尚待实测的战装在圣力攻击中得到验证；能量仍消耗，不扩展为所有单位均免疫',['desert-bones-and-mourning-soul'],'fact'),
 edge('cross-rosy-02','v07-e03','v08-e08','setup','与娜娜建立的新关系进一步成为接触克丽丝的渠道，旧人格和记忆仍未恢复',['rosy-angel-identity','christine-identity']),
 edge('cross-aroyo-01','v01-e03','v08-e05','payoff','早期吞噬阿罗约留下的记忆在氓族相遇时产生亲近与识别，也让被隐瞒的旧杀戮进入联盟关系',['memory-and-power','aroyo-memory-and-mang-clan'],'fact'),
 edge('cross-altar-01','v02-e01','v08-e09','payoff','曾观察到活性的古祭坛回到主线，经修复后首批限载启动；本集结尾还不能确认全族转生成功',['sunken-undead-kingdom','transformation-altar-and-mang-survival'],'fact'),
 edge('cross-tuk-01','v01-e07','v08-e09','setup','早期提供沼泽与祭坛信息的图克，面对新启动景象显出熟悉感；守护使命的来源仍未揭',['tuk-and-the-transformation-altar']),
 edge('cross-autonomy-03','v07-e07','v08-e07','echo','自由存在的宣言与强迫族群接受死亡/运魂安排形成价值冲突；这是主题对照，不声称宣言导致屠杀',['blackdragon-autonomy-and-companionship'],'synthesis'),
]
existing={e['id']:e for e in cfg['edges']};existing.update({e['id']:e for e in new})
cfg['edges']=list(existing.values())
(p/'cross-input.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Volume 8 cross-volume relations recorded.')
