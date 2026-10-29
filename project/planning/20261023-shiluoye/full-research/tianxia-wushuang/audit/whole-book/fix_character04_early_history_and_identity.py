import copy,hashlib,json
from audit_evidence import H,evidence,render_characters
p=H/'character-arcs-part04.json';raw=p.read_bytes();assert hashlib.sha256(raw).hexdigest()=='7728c2958cb7c2d7208b42a5c41a8fc4a2ee2bbf94942d20c06c88df3c9e2636'
a=json.loads(raw);b=copy.deepcopy(a);by={x['audit_id']:x for x in b['characters']}
x=by['character-arc-51'];x['initial_comparison_stage']='轮椅独居的父亲，希望儿子工作住房稳定，早不知陆病情和电竞全史；陆母在陆十六岁时亡，214—215主现二十四、母已亡八年。'
x['key_decisions']='拒何接养老、存款愿赠/亲属借款→214—216何陪陆返乡并实际扫母墓，陆留父五万/退父赠资金→1338电话与童年事故梦部分呼应→1342父与三叔实到苏家餐住夜、1343送站→1591陆以五亿委托未来照料。'
x['evidence_boundaries']='无双214母祭日、215明确母已亡八年且陆何扫墓；母死因未给，陆十六岁参赛错过临终的自责不证明电竞致死。童年父车祸梦与父电话部分呼应，仍不把梦全部细节作客观重演。不得串入纵横母离家/另人扫墓限制。'
x=by['character-arc-57'];x['initial_comparison_stage']='1086以65级中国虚拟部部长现身，1087自承唐龙为堂弟并为其行为道歉；与唐龙是亲属说法下的不同人，不是同一官员改名。'
x['key_decisions']='1087本人道歉并跪求陆返中国，称弟停职调查/许问责，陆扶起但拒立即归→1487再以陌号机密电话召见→1498订票并许何林同行→1499真赴京/1500基地与徐等实见，转入唤醒心任务。'
x['evidence_boundaries']='唐龙堂弟关系由1087唐风本人说明；道歉、停职调查消息、未来辞职许诺、陆实际复籍分步骤，不能把跪求当当时已恢复全部权限。后北京主单门独入/何林在外等的知情范围仍分开。'
x['evidence']=evidence([int(e['chapter_id'][3:]) for e in x['evidence']]+[1086,1087])
x=by['character-arc-59'];x['name']='书生／丁书生（本书称谓）'
x['initial_comparison_stage']='本作称灵恸天王丁书生，771在月恒南方总部实际遇陆；772祭许岩墓揭其为昔年游戏老师，与何创会表姐为同一人由双方口述。'
x['key_decisions']='772认许岩师恩和何同源关系、许连夜飞纽约帮林恢复账号→774/776有限复号有后证而起飞过程未逐镜→1463接秦电话安慰/拟找冰兰→1500北京基地出现→1504催主告心现实→1609与清风破拟伏击高战士。'
x['evidence_boundaries']='本书源码丁舒升检索零、丁书生八处，其中771/772实际现身/本人称丁书生；因此不把前作规范实名当本书明确实名。前作丁舒升／轻狂书生仅在外部关联层保同一三部曲人物索引，不作本书新事件证据。秦电话/后台权限与安慰分别记，三人同床仍陆猜玩笑。'
x['external_identity_association']=dict(other_book='网游之纵横天下',other_book_canonical_name='丁舒升／轻狂书生',scope='本项目此前已核前作身份映射，独立于本书称谓；不把外作事实倒灌本书。',research_path='.planning/20261023-shiluoye/full-research/zongheng-tianxia/vol08/character-arc-audit-draft.json',other_book_audit_id='character-arc-01')
x['evidence']=evidence([int(e['chapter_id'][3:]) for e in x['evidence']]+[771,772,774,776])
x=by['character-arc-60'];x['name']='刘婉茹／林逸欣母亲';x['terminal_state']='775林现实见母苏醒已成；1595母刘婉茹明确具名并正常参加家聚晚餐。末完整病理全愈/对多方伴侣和婚姻的正式态度未给，不由家庭一次相见全清。'
x['evidence']=evidence([int(e['chapter_id'][3:]) for e in x['evidence']]+[1595])
assert sum(x!=y for x,y in zip(a['characters'],b['characters']))==4
(H/'reviewed-batches'/'character-arcs-part04-before-early-history-identity-delta.json').write_bytes(raw)
p.write_text(json.dumps(b,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');sha=hashlib.sha256(p.read_bytes()).hexdigest()
(H/'character04-early-history-identity-delta.json').write_text(json.dumps(dict(before_sha256=hashlib.sha256(raw).hexdigest(),after_sha256=sha,unchanged_other_characters=10,deltas=[dict(audit_id=x['audit_id'],before=x,after=y) for x,y in zip(a['characters'],b['characters']) if x!=y],source_checks=['完整读primary214/215/216四栏','完整读正式卷六1086/1087四栏','完整读正式卷四771/772四栏','完整读卷八1595四栏','本书丁舒升0/丁书生8定位；跨书名移独立外部关联']),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
render_characters('character-arcs-part04.md',b['characters'],b['title']);print(sha)
