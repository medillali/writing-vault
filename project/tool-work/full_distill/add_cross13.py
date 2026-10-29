"""录入第十三集的身份揭示、关系对照和放逐转折。"""
import json
from pathlib import Path
p=Path(__file__).parent
cfg=json.loads((p/'cross-input.json').read_text(encoding='utf-8'))
reports={n:json.loads((p/f'vol{n:02d}.json').read_text(encoding='utf-8')) for n in range(1,14)}
def event(key):return next(e for e in reports[int(key[1:3])]['events'] if e['key']==key)
def edge(key,src,dst,kind,label,tracks,claim='inference'):
    return {'id':key,'from':src,'to':dst,'kind':kind,'label':label,'claim_kind':claim,'tracking_keys':tracks,'evidence':event(src)['evidence']+event(dst)['evidence']}
new=[
 edge('cross-forest-01','v10-e05','v13-e02','reveal','以惩罚与恩赐逼取信仰的巨树确认为自然神，合作出现不抹去其先前强迫行为',['forest-tree-and-dwarf-faith'],'fact'),
 edge('cross-church-agency-03','v11-e05','v13-e03','reveal','猎犬比喻背后的自我保存目的发展为扶植敌对势力，强制放逐并非征得黑龙同意的救援',['church-institution-and-angel-agency'],'fact'),
 edge('cross-nana-03','v11-e04','v13-e02','payoff','克丽丝向娜娜求助后进入双神共同传承安排，已选定与开始准备不等于完成仪式或解除封印',['nana-protection','christine-identity'],'fact'),
 edge('cross-friendship-01','v10-e06','v13-e05','echo','夺船时的杀转与拘魂，同异界无约束互助并置，显示主角关系选择存在差异而非已经普遍尊重自由',['blackdragon-autonomy-and-companionship'],'synthesis'),
 edge('cross-empire-history-01','v11-e04','v13-e08','reveal','海蛇腹中遗物留下的古国问题，进一步获得皇冠、权杖与永恒之眼的追索方向；帝国消失原因仍未回答',['desert-bones-and-mourning-soul']),
 edge('cross-dragon-loss-01','v12-e05','v13-e06','reversal','取石破封后获得的龙群遭遇天使袭击，72无智龙覆灭而36有智龙保留；这是远征完成后的新代价',['dragon-tomb-expedition','undead-dragon-force-survival'],'fact'),
 edge('cross-prophet-friendship-01','v12-e05','v13-e05','echo','先知被逼交出完整魂约，金龙则与黑龙交换无约束烙印；依存与平等关系的条件不同',['blackdragon-autonomy-and-companionship'],'synthesis'),
 edge('cross-swamp-visitor-01','v12-e09','v13-e01','payoff','来者悬念由沼泽边矮人与追兵的交战接续，托雷所载预录消息进一步解释神的邀请',['swamp-approaching-lives']),
]
new[-1]['evidence'].append({'chapter_id':'ch-0130','start_line':16406,'end_line':16419})
update={'key':'swamp-approaching-lives','volume':13,'title':'沼泽新来者的身份与邀请','kind':'subplot','status':'resolved',
        'question':'第12集末靠近沼泽的生物是谁、当次来意为何？',
        'resolution_note':'开篇接续托雷矮人一行与追兵在沼泽边的交战；黑龙介入后出现自然神预录邀请。只关闭当次来访悬念，合作真实目的由自然神线继续追踪。',
        'evidence':[{'chapter_id':'ch-0130','start_line':16406,'end_line':16419},*event('v13-e01')['evidence']]}
updates={(u['key'],u['volume']):u for u in cfg.get('state_updates',[])};updates[(update['key'],13)]=update;cfg['state_updates']=list(updates.values())
existing={e['id']:e for e in cfg['edges']};existing.update({e['id']:e for e in new});cfg['edges']=list(existing.values())
(p/'cross-input.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Volume 13 cross-volume relations recorded.')
