"""卷七旧逐章原子index456—475，末20条。"""
import json,pathlib,hashlib
H=pathlib.Path(__file__).resolve().parent
rows=[x for x in json.loads((H/'local-question-pool.json').read_text(encoding='utf-8'))['candidates'] if x['volume']==7]
J=[
('unknown','source-divine-tier-wording','苏伦1483面板初位神而1494主拿他作准神比较，未见作者专门改字；实际战与称谓分别存，不用回忆口吻降改旧面板。',[1483,1494]),
('answered','disguise-teleport-and-rescue','1496伪装先混入后活气穿帮、真实与林交手；1503亲见心活并用神石逆向传回七，奥明确1495轻踏已留印。后证才绑定伏笔，不在1495早判已显阵。',[1495,1496,1503]),
('answered','dragon-and-target-survival','1497飞银实入放逐/伤后活，1503心亲见并救，1504飞银最终活随回；不因1496挡林危机把飞银提前判死，也不补他具体出裂方法。',[1496,1497,1503,1504]),
('answered','teleport-preparation-payoff','1503神石逆阵真正带主心奥回百兽院，奥当面确认1495踏地留印；原动作的具体部署由后证落实，不是研究者凭一个轻踏自造预阵。',[1495,1496,1503]),
('partial','weakness-test-and-control-anomaly','1498血海实沾夜并系统攻速减，1502淬血匕为另一永久削弱；1503心活。1497狂神100%描述却MISS的特定原因仍未说明，不能假定夜当时无敌。',[1497,1498,1502,1503]),
('answered','later-boss-fate-and-real-identity','1502再遇夜/1503主心合杀，1500现实董身体与徐宁唤醒计划说明数据问题，1507—1508现实醒；1498夜离海非死，电话机密亦非当时已揭。',[1498,1500,1502,1503,1507,1508]),
('answered','logout-vs-world-crossing','主1498下线而奥飞银仍在放逐，1504三者才真实出炼狱回人界；上下线不构自动传队友跨世界，原限制由后证守住。',[1498,1501,1504]),
('answered','beijing-revelation-and-item-allocation','1500唐徐会揭心董身份/继续游戏带醒任务，1506青峰李/耀阳炎神斗/紫云凰蛋北、1511噬灵鞭周成交实用，物件不再统称包中未分。',[1499,1500,1506,1511]),
('answered','reporting-provenance','1499人界军势/烛战结盟来自何林李等转述，后1516—1519实际会战提供局部互证；后战不把主炼狱期间各场军调倒成亲见，来源边界已落实。',[1499,1516,1517,1518,1519]),
('partial','game-rescue-and-real-awakening','1503游戏心真救回，1507抓手发声后再闭、1508才真正睁眼；徐宁给人格/脑波解释为小说内技术说辞，完整科学过程未展示，不把游戏胜利等同即时临床全愈。',[1500,1503,1507,1508]),
('answered','age-and-research-boundary','1500徐明确董欣然17岁，阶段身份及照护关系照实记录；后继承/同住不据亲密玩笑补性行为，原研究边界已落实，非剧情任务待结。',[1500,1508,1509]),
('partial','captive-identity-and-princess-outcome','1503主亲见笼中确是心、合杀夜并破笼救，公主也冲出活；佯婚护族当场目的转战友但全族总体结局未显示，不能由她活补食人谷全幸存。',[1501,1502,1503]),
('unknown','tribe-fate-vs-enemy-threat','1502夜声称三万红龙灭谷是敌威胁，随行近千被杀为明确；1503公主活不证明老巢全族幸存，也无镜头确认全谷被灭，终点保总体未知。',[1502,1503]),
('partial','rescued-identity-kill-and-place-name','1503心明确现/主与心合杀夜，无单挑或系统独占末刀；红龙巢/火龙巢是同场源称谓差未专门纠字，不另造第二Boss或第二次救援。',[1502,1503]),
('answered','physical-awakening-sequence','1507现实抓手发声后闭眼、1508睁眼确认醒，独立于1503游戏救出与1504返人界；两阶段都有回执，不将1503当现实已醒。',[1503,1504,1507,1508]),
('unknown','unshown-tribe-fate','公主1503从坍洞冲出活，与食人谷全族未有画面是两层；后文未给该族完整生还/灭族结果，不能以救心圆满气氛代结。',[1503]),
('unknown','weapon-restoration-gap','心此前枪折与1502—1504又持龙骨枪都可记实景，但完整修复/重铸或另取同名武器过程未示；不擅补主修枪或神力自动复原。',[1459,1502,1503,1504]),
('answered','fear-explained-and-real-acceptance','1506心亲说怕现实醒后没有主，1507唤醒安排/1508实际睁眼同住接受照护，解释哭因并推进接受现实；不能说1504已完整答应，亦不把哭等同不愿生还。',[1504,1506,1507,1508]),
('unknown','companion-full-restoration','奥1504活返并被紫罗兰收留休养是实回执，七日神力全恢复/腿伤全愈未有独立后证；不因主游戏救援结束就算她代价全部清零。',[1492,1493,1504]),
('partial','remaining-purgatory-threats','1504林受伤败退且裂关，五王巨兽仍活、其他境域未全清；末卷没有林纳全军终灭或再袭实景，1600地震是论坛旧事非重出。现存威胁与未来反扑未示分开，不补世界永久和平。',[1504,1600]),
]
assert len(J)==20
out=[dict(candidate_id=rows[i+456]['candidate_id'],status=s,audit_domain=d,rationale=r,later_chapters=e) for i,(s,d,r,e) in enumerate(J)]
p=H/'adjudications-local-v07-part08.json';p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
md=['# 卷七旧逐章原子08（index456—475，末20可主审）','','游戏带回与现实唤醒分段，17岁人物只记身份和照护；未明族群/奥恢复和剩余炼狱仍保限制。','']
for x in out:
 row=next(r for r in rows if r['candidate_id']==x['candidate_id']);md += [f"## {x['candidate_id']} {row['title']}",'',f"{x['status']} / {x['audit_domain']}：{x['rationale']}",'','后证raw：'+', '.join(map(str,x['later_chapters'])),'']
(H/'local-v07-reviewed-part08.md').write_text('\n'.join(md),encoding='utf-8')
print(len(out),hashlib.sha256(p.read_bytes()).hexdigest())
