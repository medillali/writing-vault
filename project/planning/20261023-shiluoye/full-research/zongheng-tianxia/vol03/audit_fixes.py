import json,pathlib
H=pathlib.Path(__file__).resolve().parent
def rd(f):return json.loads((H/f).read_text(encoding='utf-8'))
def wr(f,x):(H/f).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
C=rd('cards.json');A=rd('analysis.json');G=rd('graph.json');N=[json.loads(s) for s in (H/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines()]
S=A['source_id'];R=A['revision'];P=S+'/full-20261025/vol03/'
def E(*ps):return [{'source_id':S,'revision':R,'chapter_id':N[p-101]['chapter_id'],'start_line':N[p-101]['start_line'],'end_line':N[p-101]['end_line']} for p in ps]
group=next(x for x in C if x['origin_key']==P+'character/supporters');C.remove(group)
for id,title,summary,goal,limit,rel,dec,change,ps in [
 ('luoyu','落雨无声','沉默但稳定输出的职业弓箭手，资源倾斜滞后后终于获得承认。','参与团队并提升弓手能力。','装备相较核心较差，断魂由63掉57。','同事从信任其输出到主动集中资源；不是紫月的同一实体。','射翼根帮助制空；与月放风筝引怪，持续输出。','233章收75烈焰靴甲弓时71，流泪因被重视；后续装备落实待续核。',[169,202,232,233]),
 ('xiatian','夏天（去年夏天）','召唤师成员，操作有限但资源与宠物功能确实参与队伍。','参与共同生活、升级并获得认可。','宠狼受高怪压制，常被身体和笨拙笑话评价。','与紫月同住秦房；依赖书，与众人玩笑但有被贬低的不对称。','用移动承伤、转蓝给秦、宠狼牵制、向书通报豺谷围困。','从弱输出到可做有限辅助；244救援触发者之一，不夸成战术核心。',[117,189,190,235,243]),
 ('ziyue','紫月','刺客成员，经验不足但有练习和实战贡献。','进步、参与亲密共同体。','错误走位、误伤盟友、潜行路线可被熟悉者预判。','与夏天亲近；向书学步法，受众人调笑。','录步法学习、内赛被反隐、233补刀敌刺保护秦。','进步可见但不被研究者抬成与悲酥同级高手。',[144,180,189,233])]:
 C.append({'asset_type':'character','scope':'source-analysis','title':title,'origin_key':P+'character/'+id,'tags':['作者:失落叶','作品:网游之纵横天下','卷三','人物阶段'],'content':{'summary':summary,'goals':[goal],'constraints':[limit],'relationship_directions':[rel],'decisions':[dec],'stage_change':change,'knowledge_boundary':'最近明确状态以本卷证据为准，不从他人升级补造等级。'},'evidence':E(*ps),'user_notes':'','favorite':False,'review_status':'draft'})
qin=next(x for x in C if x['origin_key']==P+'character/qinyun');qin['content']['stage_change']='从被救者成为关键救援者；最近明确等级为正文236章榜单75级（ch-0237 L21061—21066），不能当作244卷末确数；持80链戒待用。';qin['evidence']+=E(236)
q2=next(x for x in A['dimensions']['continuity'] if x['id']=='q2');q2['fact']='50万建帮欠款正文181章再提，198实际支付；150万借款199交雪，之后未见归还。';q2['evidence']=E(181,198,199)
# 去掉仅以主题近似牵连的边，保留有具体工具与后果的关系。
G['edges']=[x for x in G['edges'] if x['id']!='v03-e2']
for t in G['threads']:t['edge_ids']=[x for x in t['edge_ids'] if x!='v03-e2']
knowledge=G.pop('knowledge',[])
for k in knowledge:
 nid=k.pop('node_id');next(x for x in G['nodes'] if x['id']==nid).setdefault('knowledge',[]).append(k)
mapping={'rebuild':['shusheng','lingxue'],'ronin':['shusheng','binglan'],'equipment_split':['shusheng','bingcha','qinyun'],'qin_rescue':['shusheng','qinyun','lingyue'],'token':['shusheng','daohuaxiang','lingyue'],'ghost':['shusheng','lingxue'],'anti_transfer':['shusheng','linao','daohuaxiang'],'earn_rep':['shusheng'],'final':['shusheng','lingxue','lingyue','qinyun','longhun','diyuhuo'],'shop':['shusheng','lingxue','lingyue','bingcha'],'reject_bet':['shusheng','lingxue','lingyue','lingtian','wangjunjie'],'retreat':['shusheng','longhun','gufen','lingyue'],'ice_failure':['shusheng','lingxue','qinyun'],'rescue_valley':['shusheng','lingxue','lingyue','qinyun','daohuaxiang','bingcha'],'countertrap':['shusheng','longhun','gufen','linao','xueyin','daohuaxiang'],'fox':['shusheng','qinyun','qixingdeng','diyuhuo'],'ice_cave':['shusheng','lingxue','qinyun'],'ice_queen':['shusheng','lingxue','lingyue','qinyun','bingcha'],'revenge_maids':['shusheng'],'tiger_shares':['shusheng','lingxue','lingyue','qinyun','bingcha','luoyu','xiatian','ziyue'],'promise':['shusheng','lingxue','bingcha'],'disguise':['shusheng','xueyin','lingxue','binglan'],'dragon_rescue':['shusheng','lingxue','lingyue','qinyun','xiatian','qixingdeng','xueyin']}
for n in G['nodes']:
 if n['kind']=='scene':
  sid=n['id'][4:];n['asset_origin_key']=n.pop('scene_origin_key');n['characters']=[P+'character/'+x for x in mapping[sid]]
for e in G['edges']:
 for endpoint in ('from','to'):
  evidence=next(n['evidence'] for n in G['nodes'] if n['id']==e[endpoint])
  e.setdefault('evidence',[]).extend(evidence)
 e['evidence']=list({(x['chapter_id'],x['start_line'],x['end_line']):x for x in e['evidence']}.values())
# 每个证据对象自身的判断类型：事件事实、人物阶段综合、机制抽象、解释与疑点分开。
def mark(obj,default):
 if isinstance(obj,dict):
  if all(k in obj for k in ('source_id','revision','chapter_id','start_line','end_line')):obj['claim_kind']=default
  for k,v in obj.items():
   if k!='claim_kind':mark(v,default)
 elif isinstance(obj,list):
  for v in obj:mark(v,default)
for c in C:mark(c,'synthesis' if c['asset_type'] in ('character','pattern') else 'fact')
for dim,observations in A['dimensions'].items():
 for o in observations:mark(o,'inference')
mark(A['unresolved_and_anomalies'],'inference')
for n in G['nodes']:
 mark(n,'inference' if n['kind']=='arc' else 'fact')
 for k in n.get('knowledge',[]):mark(k,'inference' if k['state'] in ('unknown','suspects') else 'fact')
mark(G['edges'],'inference');mark(G['threads'],'synthesis')
A['threads']=G['threads'];A['characters']=[{'origin_key':c['origin_key'],**c['content'],'evidence':c['evidence']} for c in C if c['asset_type']=='character'];A['transferable_mechanisms']=[{'origin_key':c['origin_key'],**c['content'],'evidence':c['evidence']} for c in C if c['asset_type']=='pattern']
for f,x in [('analysis.json',A),('cards.json',C),('graph.json',G)]:wr(f,x)
for f in ('report.md','handoff.md'):
 text=(H/f).read_text(encoding='utf-8').replace('共47张：15张独立人物、1张群体比较、23张场景、8张机制','共49张：18张独立人物、23张场景、8张机制').replace('20关系边','19关系边').replace('182再承诺50万','181再承诺50万').replace('182再提','181再提').replace('182章再提','181章再提').replace('243达到80不等已二转','241达到80不等已二转').replace('秦的80自然女神链及圣光戒','秦的80自然女神链及圣光戒')
 text=text.replace('卷末75附近','最近明确正文236章75，卷末精确级数不据推算')
 (H/f).write_text(text,encoding='utf-8')
