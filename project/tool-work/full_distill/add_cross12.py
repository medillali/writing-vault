"""录入第十二集的继承、远征完成与新意识。"""
import json
from pathlib import Path
p=Path(__file__).parent
cfg=json.loads((p/'cross-input.json').read_text(encoding='utf-8'))
reports={n:json.loads((p/f'vol{n:02d}.json').read_text(encoding='utf-8')) for n in range(1,13)}
def event(key):return next(e for e in reports[int(key[1:3])]['events'] if e['key']==key)
def edge(key,src,dst,kind,label,tracks,claim='inference'):
    return {'id':key,'from':src,'to':dst,'kind':kind,'label':label,'claim_kind':claim,'tracking_keys':tracks,'evidence':event(src)['evidence']+event(dst)['evidence']}
new=[
 edge('cross-dragon-prayer-01','v11-e09','v12-e01','reveal','祈祷白光揭为拿不列斯转出元力与记忆，帝勒获得能力并自主退战，拿本源仍沉睡',['dragon-bloodline-and-confinement'],'fact'),
 edge('cross-rosy-memory-01','v10-e09','v12-e02','payoff','分身借体后的记忆变化在萝茜醒来时得到局部说明，新生活经验主导并夹异源碎忆，三实体不合并',['rosy-angel-identity'],'fact'),
 edge('cross-expedition-03','v11-e09','v12-e03','payoff','岛上冲突最终伴随取得安息石和毁峰重损，取物成功不等于击败龙皇或保全队伍',['dragon-tomb-expedition'],'fact'),
 edge('cross-prophet-03','v09-e03','v12-e04','reveal','早先效忠承诺在交付宝物时显出分身半魂漏洞，控制范围并非黑龙最初所想',['dragon-soul-oath-and-prophet'],'fact'),
 edge('cross-crystal-awakening-01','v11-e03','v12-e09','payoff','海皇战后接受分流的金属骨后来呈晶体并有八具初觉醒；海皇本源是否为觉醒机制仍属人物推测',['children-consciousness'],'fact'),
 edge('cross-emperor-skill-03','v11-e07','v12-e08','payoff','黑大的自主战法之后，黑大黑二进一步承担赐魂与指挥，八个旧孩子仍没有自主意识',['children-consciousness'],'fact'),
 edge('cross-church-agency-04','v11-e05','v12-e07','reveal','菲力普对工具制度的解释扩展到备用身体来源与机构盲区，了解一层安排不代表掌握教会全局',['church-institution-and-angel-agency']),
]
existing={e['id']:e for e in cfg['edges']};existing.update({e['id']:e for e in new});cfg['edges']=list(existing.values())
(p/'cross-input.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Volume 12 cross-volume relations recorded.')
