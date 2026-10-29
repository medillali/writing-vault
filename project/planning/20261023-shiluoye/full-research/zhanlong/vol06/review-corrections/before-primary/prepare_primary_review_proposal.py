"""只生成主审修订提案，不改任何冻结输入/输出/回执。"""
from pathlib import Path
import json,hashlib,copy,sys
sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).parent
def read(n):return json.loads((H/n).read_text(encoding='utf-8'))
def sha(n):return hashlib.sha256((H/n).read_bytes()).hexdigest()
manifest=read('freeze-manifest.json')
assert all(sha(n)==v for n,v in manifest['files'].items())
A=read('analysis.json');C=read('cards.json');G=read('graph.json')
def at(obj,path):
    for part in path:obj=obj[part]
    return obj
delta=[]
def change(file,path,after,reason,source=None):
    data={'analysis.json':A,'cards.json':C,'graph.json':G}[file]
    before=at(data,path)
    assert before!=after,(file,path)
    delta.append(dict(file=file,json_path=path,before=before,proposed_after=after,rationale=reason,source_basis=source or []))
def observation(oid):
    for dim,rows in A['dimensions'].items():
        for i,r in enumerate(rows):
            if r['id']==oid:return ['dimensions',dim,i]
    raise KeyError(oid)
def card(key):return next(i for i,c in enumerate(C) if c['origin_key'].endswith('/'+key))

rain_source=[dict(chapter_id='ch-1385',start_line=99582,end_line=99594,note='燕令布/盾甲遮引线，雨中炮仍发；兽骑速度快难瞄准/瞬杀'),dict(chapter_id='ch-1385',start_line=99607,end_line=99620,note='西门城墙被砸破，随后方共享59:59开幕倒计时')]
p=observation('v06-stateful-resources')
old=at(A,p+['facts',0,'text'])
change('analysis.json',p+['facts',0,'text'],old.replace('鬼城又因粮尽、炮潮受困。','鬼城又遭粮尽与炮引线受潮风险；防雨后炮仍能发射。'),'同义事实澄清：受潮是风险，不能写成已哑炮。',rain_source)
p=observation('v06-attrition-ladder')
change('analysis.json',p+['facts',0,'text'],'鬼城先墙高炮多，随后野战失利、墙损减员、马粮尽、三万取粮遭伏、哗变三千出城被杀；敌待雨进攻，但布与盾甲护引线后炮仍能发射。快兽难以瞄准或瞬杀，西城门城墙仍被砸破；外援再提供短时开口。','用先后事实代替“雨压炮→破城”的歧义因果链。',rain_source)
p=observation('v06-open-end-not-erasure')
change('analysis.json',p+['title'],'长期承诺由不同状态的再出现分步回收','将研究索引流程改为小说实际的承诺回收机制。')
change('analysis.json',p+['interpretation','text'],'职位正式授任、身体恢复、营业资格和授权签字的再次出现，使不同旧承诺分别获得可见回收；秦皇空棺、长老回赠与旧贪查仍留空缺，完成感因而是局部累积，并非一次全清。','保原facts/全部证据与未闭项，只把解释改成文学内容。')
change('analysis.json',p+['limits_and_counterevidence'],'本卷没有给出秦皇尸去向、回赠长老和旧贪查的完成场面；相似资源在别处再次出现，也不等于该项旧承诺已经兑现。','移除亲读边界/流程措辞，保小说内回收不充分的限制。')
p=observation('v06-source-interface-anomalies')
change('analysis.json',p+['title'],'命名与数值漂移增加连续阅读负担','把操作规范标题改为连续性实际效果，不把源差当优点。')
change('analysis.json',p+['interpretation','text'],'同一神尊的名字、神格品级与兵力口径变化，会使读者更难辨认实体、比较损益和追踪因果；后来明确的行动结果能限定部分理解，却不能消除所有字面歧义。','去研究方法口吻，说明对读者因果确定的影响。')
change('analysis.json',p+['limits_and_counterevidence'],'未获解释的命名和数值差异会削弱读者对同人、位阶与损失规模的确定判断；结局成功不能替这些差异补出唯一解释，它们仍是连续阅读的负担。','去“检查通过/待主审”流程，限定为文学局限。')
# 本条原facts把孙方霖约3000人出城混列成数量漂移，实际数量接口为祝海3万/景音说5万。
change('analysis.json',p+['facts',0,'text'],'同段空间神尊名乱码/异写、冬茗格中上位漂移；祝海三万禁军出队与随后景音所称五万禁军存在口径差。','同一待修观察内的数词澄清：三千是另一次孙方霖出城，不能当此源差。',[dict(chapter_id='ch-1383',start_line=99443,end_line=99456,note='祝海改带3万禁军并实际出北门'),dict(chapter_id='ch-1384',start_line=99501,end_line=99508,note='景音惜五万禁军')])
source=read('../source.json') if (H/'../source.json').exists() else None
for path,kind in [(p+['facts',0,'evidence'],'fact'),(p+['interpretation','evidence'],'synthesis'),(p+['evidence'],'synthesis')]:
    old=at(A,path);sample=old[0]
    extra=dict(source_id=sample['source_id'],revision=sample['revision'],chapter_id='ch-1383',start_line=99443,end_line=99456,claim_kind=kind)
    if extra not in old:change('analysis.json',path,old+[extra],'为三万出队增加精准证据，保已有证据不删。')

i=card('li-xiaoyao');old=C[i]['content']['constraints']
change('cards.json',[i,'content','constraints'],old.replace('NPC不可复','NPC军不能按玩家方式掉级返场'),'收窄为当前NPC军返场限制，兼容流/佩其他复苏机制。')
i=card('frost');old=C[i]['content']['stage_change']
after=old.replace('留百龙骑守关','允留百名龙骑协防，未另演全部到场')
assert after!=old
change('cards.json',[i,'content','stage_change'],after,'1386流的措辞是将会留下，不是百骑已完成驻防清册。',[dict(chapter_id='ch-1386',start_line=99695,end_line=99700)])
for j,r in enumerate(A['character_states']):
    if r['origin_key']==C[i]['origin_key']:change('analysis.json',['character_states',j,'stage_change'],after,'同步同一人物阶段状态。')
i=card('xue-rou');old=C[i]['content']['relationship_directions'];after=['薛景：妹妹，薛柔为姐姐' if v=='薛景：姐姐' else v for v in old]
change('cards.json',[i,'content','relationship_directions'],after,'关系方向写清主宾。')
i=card('rain-and-split');ct=C[i]['content']
change('cards.json',[i,'content','obstacle'],'雨中引线受潮风险/遮雨布少/兽骑快/西墙破','与实际炮仍可开火分开。',rain_source)
rain_summary='防雨后重炮仍可发射，但快兽难以瞄准或瞬杀，西城墙仍被砸破；方共享开幕倒计时，4万玩家开始袭皇营掩护NPC撤退。'
for field in ['summary','consequence','state_change']:change('cards.json',[i,'content',field],rain_summary,'保开炮事实，并将“倒计时到”澄清为共享倒计时已开始，非已经归零。',rain_source)
j=next(j for j,r in enumerate(G['nodes']) if r['id']=='zl-v06-rain-and-split')
change('graph.json',['nodes',j,'summary'],rain_summary,'同步来源场景节点，不新造雨停炮因果边。',rain_source)
for eid in ['zl-v06-e-soul-army-canglan-soul','zl-v06-e-lanse-loss-upper-god']:
    j=next(j for j,r in enumerate(G['edges']) if r['id']==eid)
    assert G['edges'][j]['kind']=='setup'
    change('graph.json',['edges',j,'kind'],'echo','这是同主题/后果的呼应而非已经建立的情节伏笔；label/证据保持。')

authored=read('scene-transfer-proposals-authored.json')
scene_cards=[c for c in C if c['asset_type']=='scene']
assert len(authored)==len(scene_cards)==58
assert len({r['key'] for r in authored})==58
assert {r['key'] for r in authored}=={c['origin_key'].rsplit('/',1)[1] for c in scene_cards}
assert all(len({r[field] for r in authored})==58 for field in ['applicability','failure_mode'])
scene_proposals=[]
for r in authored:
    i=card(r['key']);c=C[i]
    scene_proposals.append(dict(origin_key=c['origin_key'],title=c['title'],before={f:c['content'][f] for f in ['applicability','failure_mode']},proposed_after={f:r[f] for f in ['applicability','failure_mode']},why_it_works_preserved=c['content']['why_it_works'],evidence_preserved=c['evidence']))
scene_doc=dict(status='proposal_only_not_applied',base_cards_sha256=sha('cards.json'),authorship='zongheng_vol05_full基于本人全卷实读逐场手写；脚本仅附旧字段/证据，不生成内容。',scope='只拟替换58场景的applicability/failure_mode；why_it_works、事实、来源及全部其他字段保留。',count=58,proposals=scene_proposals)
(H/'scene-transfer-proposals.json').write_text(json.dumps(scene_doc,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
md=['# 卷六58场景适用条件／失效边界提案','','仅提案，冻结卡图与原notes未动。每项两字段人工重写，why_it_works/证据保留。','']
for n,r in enumerate(scene_proposals,1):
    md+=['## '+str(n)+'. '+r['title'],'',r['origin_key'],'','适用条件：'+r['proposed_after']['applicability'],'','失效边界：'+r['proposed_after']['failure_mode'],'','保留 why_it_works：'+r['why_it_works_preserved'],'']
(H/'scene-transfer-proposals.md').write_text('\n'.join(md),encoding='utf-8')
proposal=dict(status='proposal_only_not_applied',base_freeze_sha256=sha('freeze-manifest.json'),base_files=manifest['files'],changes=delta,scene_fields_proposal='scene-transfer-proposals.json',synchronization_on_approval=['仅将批准字段应用到JSON，report对应同条文字、handoff流允留百骑同步。','同步build_artifacts.py/research_cards.py/research_interfaces.py及58场景手写数据的装配入口；不重造其他已审语义。','保旧freeze/validation回执另存，应用后串行校验并固定新SHA；原notes/state/log索引不动。'],unchanged='冻结文件当前全部哈希仍匹配；没有执行上述任何修改。')
(H/'primary-review-proposal.json').write_text(json.dumps(proposal,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
md=['# 卷六主审定向修订提案','','冻结输入不改，仅提出最小字段改动。完整before/proposed_after与路径见JSON。','', '原章1385已再次BEGIN—END全文核读，99582—99590布盾护引线后炮仍发；99594快兽难瞄/瞬杀；99607—99620西门破后才收到开幕倒计时。没有雨已停炮证据。','']
for n,r in enumerate(delta,1):md+=['## '+str(n)+'. '+r['file']+' / '+'.'.join(map(str,r['json_path'])),'','原：'+json.dumps(r['before'],ensure_ascii=False),'','拟：'+json.dumps(r['proposed_after'],ensure_ascii=False),'','理由：'+r['rationale'],'']
md+=['## 58场景另件','','[逐场适用条件与失败边界](scene-transfer-proposals.md)，只替换两字段，why_it_works和原来源保留。','']
(H/'primary-review-proposal.md').write_text('\n'.join(md),encoding='utf-8')
assert all(sha(n)==v for n,v in manifest['files'].items())
print(json.dumps(dict(changes=len(delta),scene_proposals=len(scene_proposals),frozen_files_unchanged=True,proposal_sha256=sha('primary-review-proposal.json'),scene_proposals_sha256=sha('scene-transfer-proposals.json')),ensure_ascii=False))
