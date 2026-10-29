import json,pathlib,collections
H=pathlib.Path(__file__).resolve().parent
def read(f):return json.loads((H/f).read_text(encoding='utf-8'))
def write(f,x):(H/f).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
C=read('cards.json');A=read('analysis.json');G=read('graph.json');N=[json.loads(x) for x in (H/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines()]
S=A['source_id'];R=A['revision'];P=S+'/full-20261025/vol03/'
def E(*ps):return [{'source_id':S,'revision':R,'chapter_id':N[p-101]['chapter_id'],'start_line':N[p-101]['start_line'],'end_line':N[p-101]['end_line']} for p in ps]
extra=[('linao','林傲（傲世狂人）','资本与复仇驱动的敌会首领，转职遭截、等级遭反守尸仍继续悬赏。','霸主地位、压倒雪月。','战术/情绪管理不足、依赖稻花香与盟友。','香受其指使但暗助书；王成为隐蔽资源；血饮互利又争执。','买转职窗口、结盟围谷、布悬赏，自己疑反伏不赴。','被杀回30余后重新练级；并未被彻底赶出主城。',[152,153,188,201,203,206,208]),('xueyin','血饮天下','敌盟组织者，以精锐、招募与宣传补足旧部归零损失。','壮大血饮、阻书首转、取得装备。','核心被复仇打回零、新人需培养；联盟脆弱。','招七星灯、格里高利、火之魄；与林傲结盟又争功；与天地临场谈战利。','剪辑不败视频、雇刺法、带500追书、谈判助天地。','多次失败仍有组织资源，威胁从人数转高手组合与情报。',[207,216,225,238,239,240,243,244])]
for id,title,summary,goal,limit,rel,decision,change,ps in extra:
 C.append({'asset_type':'character','scope':'source-analysis','title':title,'origin_key':P+'character/'+id,'tags':['作者:失落叶','作品:网游之纵横天下','卷三','人物阶段'],'content':{'summary':summary,'goals':[goal],'constraints':[limit],'relationship_directions':[rel],'decisions':[decision],'stage_change':change,'knowledge_boundary':'只据本卷阶段；追杀动机推测与敌方自述分开。'},'evidence':E(*ps),'user_notes':'','favorite':False,'review_status':'draft'})
G['knowledge'] += [{'node_id':'v03-disguise','observer':P+'character/xueyin','state':'misbelieves','belief':'看见书冲进怪群，笃定书已死并计划进洞捡剑；读者知道书正变身混杀。','evidence':E(240,241)},{'node_id':'v03-fox','observer':'reader','state':'knows','belief':'血饮以剪辑视频宣称七星灯不败，读者已看过书火联合胜的完整切磋。','evidence':E(215,216)}]
write('cards.json',C);write('graph.json',G)
A['characters']=[{'origin_key':c['origin_key'],**c['content'],'evidence':c['evidence']} for c in C if c['asset_type']=='character'];write('analysis.json',A)
