"""接续第十六集的主体恢复、夺体反转和未发动法阵。"""
import json
from pathlib import Path
p=Path(__file__).parent
cfg=json.loads((p/'cross-input.json').read_text(encoding='utf-8'))
reports={n:json.loads((p/f'vol{n:02d}.json').read_text(encoding='utf-8')) for n in range(1,17)}
def event(key):return next(e for e in reports[int(key[1:3])]['events'] if e['key']==key)
def edge(key,src,dst,kind,label,tracks,claim='inference'):
    return {'id':key,'from':src,'to':dst,'kind':kind,'label':label,'claim_kind':claim,'tracking_keys':tracks,'evidence':event(src)['evidence']+event(dst)['evidence']}
new=[
 edge('cross-v16-redmoon','v15-e09','v16-e01','reveal','红月聚合后的宣告被解释为达罗亚借信徒传力强降；向菲力普说切里莫之名并非二者同一人的证据',['desert-bones-and-mourning-soul'],'fact'),
 edge('cross-v16-puppet','v10-e04','v16-e01','reveal','噬魂枪的无意识傀儡阶段出现新进展：雷奥因吞魂进化并恢复神智；后来的恢复不能倒填此前意识状态',['soul-devourer-weapon-and-puppets','god-knight-pursuit'],'fact'),
 edge('cross-v16-angel-agency','v15-e01','v16-e02','payoff','菲力普对自身价值的重视进一步落实为临阵逃离，弗里昂的拒逃构成另一个选择',['church-institution-and-angel-agency'],'fact'),
 edge('cross-v16-corpse-limit','v15-e08','v16-e06','payoff','此前最后关头才启阵的限制在主角再次失联时被援引，塞茵祭魂阵仍未发动',['seiyne-living-corpse-plan','dragon-soul-oath-and-prophet'],'fact'),
 edge('cross-v16-two-inheritances','v13-e02','v16-e04','payoff','双神传承安排获得后文叙述确认，但媒介娜娜的意愿、神明本源与成神仍是不同问题',['nana-protection','christine-identity'],'fact'),
 edge('cross-v16-nature-cost','v15-e07','v16-e04','reversal','合作中的自然神以暗害旧长老保障神谕，娜娜的亲见与质问揭开维系联盟的代价',['forest-tree-and-dwarf-faith','nana-protection'],'fact'),
 edge('cross-v16-cutroman-death','v14-e02','v16-e02','reveal','君王遗产线补明切罗曼尔被两神植入光明神格、因持续信仰供能消融而亡的机制',['cutroman-legacy-and-mission'],'fact'),
 edge('cross-v16-betrayal','v15-e06','v16-e05','reversal','寻回旧帝国的共同方向被达罗亚用来骗取信任，黑龙随后遭封魂夺体；同族并不保证利益一致',['desert-bones-and-mourning-soul','daro-possession-crisis'],'fact'),
 edge('cross-v16-consumption','v06-e07','v16-e07','echo','早期围绕异族危险与吞魂的争论，到毁掉忠诚子民取能时呈现具体权力代价；不能以同族求存理由抹去被牺牲者意愿',['soul-consumption-ethics'],'synthesis'),
]
new[-1]['evidence'].append({'chapter_id':'ch-0065','start_line':8018,'end_line':8036})
existing={e['id']:e for e in cfg['edges']}
for e in new:
    if e['id'] in existing:assert (existing[e['id']]['from'],existing[e['id']]['to'])==(e['from'],e['to'])
existing.update({e['id']:e for e in new});cfg['edges']=list(existing.values())
(p/'cross-input.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Volume 16 cross-volume relations recorded.')
