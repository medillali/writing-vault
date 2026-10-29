from build_full import *
import shutil
coverage=load(O/'coverage.json');assert set(coverage)=={'z','l'}
bs={k:batches(k) for k in BOOK};units={k:{u['ordinal']:u for b in bb for u in b['units']} for k,bb in bs.items()}
def E(k,*ords):return evidence(k,unique([e for n in ords for e in units[k][n]['evidence']]),'synthesis')
COMPARISONS=[
('competence-with-gaps','能力与认知缺口并存','萧御把真实手部经验转为游戏技能，仍必须练习步调、时机和完成度。','萧翎生产强而战斗常识弱，漏接职业任务甚至造成开篇困境。','给人物一项可用专长，同时让他在另一项关键知识上有可被纠正的不足。','不要以一个领域的天才代替所有领域能力。','backstab-lab','gargoyle-birth',[6,7,8,9],[2,16,44,46]),
('reward-adds-frontier','回报开启新的前置条件','满熟练却缺技能费，委托能提前升级但带任务责任；闲置钥匙以后才遇锁箱。','早拿泰坦之心仍需鉴定、材料、导师与工艺，取得不等于能使用。','把奖励拆成拥有、理解、制造、运用四种状态，让新资源继续提出可选择的问题。','前置门槛须改变行动，不能只用拖延字数。','open-box-is-not-loot','l-b07-clock',[10,128,299,318,319],[5,9,220,319,320]),
('hypothesis-then-test','把猜想写成有边界的试验','反手背刺、短动作、嗅觉反制都经历失败、观察与改动；安抚增偷率仍只猜测。','永动机从构想到技能齐备再分级实测，四只怪不能维持就保留上限。','记录假设、测试条件、观察结果、未排除解释，再决定是否扩大使用。','一次巧合成功不能升级成全局规则。','shift-the-mark','perpetual-test',[7,8,9,91,98,278,316],[33,72,82,86]),
('environment-as-rule','环境与敌方行为共同提供解法','鱼群食伤同类、幽灵峡谷白雾时序、斯卡守箱职责可被观察后反用。','能源巨偶耗尽、镜像虚无后的虚弱和冰窖生活痕迹将战斗转为规则问题。','先展示稳定行为，再让角色付代价验证，最后重组可用条件。','环境解法不能在终局凭空出现。','bind-guardian-by-duty','l-b08-mirror',[19,24,318,319],[309,332,333,345,346]),
('opponent-keeps-agency','对手保持学习与反制能力','云义挡三连突击，萧御承受重伤后脱离，双方明确平局。','无炎七胜仍输双系控制，狂龙新天神技能破解旧地刺经验。','让对手根据已见信息调整，使主角的旧强项产生新的缺口。','用对手忽然失智证明升级会破坏长期竞争。','yunyi-has-grown','l-scene-wuyan-boundary',[119,120,308,309,310],[178,179,180,297]),
('specialists-have-domains','专业价值按任务验证','风神擅扛巨怪却难抓灵活斯卡，风隐侦察强而不必PK最强。','无炎有操作需资源支持，夜落的药剂与治疗者的时机不能被法伤替代。','让同一人物在不同问题里有不同排名，团队通过组合而非总战力成立。','不能为突出主角而让所有专业角色失去本职能力。','specialists-not-one-ranking','l-b-s03',[313,314,315,317],[106,179,188,195,205]),
('two-victory-metrics','公开战果与隐藏进度分开','蜗牛看似没打赢却已给全员上粉；角色按血量评估而读者知道准备目标。','敌法杖与戒指信息逐层曝光，范露娜被击败仍把夺舍引导推进。','同场至少明确两方真正想推进的状态，让小动作在回看时有意义。','没有事前动作证据的布局容易成为事后解释。','marking-false-loss','strength-deadline',[275,276,277,278],[58,60,118,121,122,126]),
('success-and-cost-separate','目标成功与战斗胜负分别结算','援凤以主角死亡换复活时间，骨龙夺宝又由公会牺牲人手救尸。','森林龙危机仍有九人存活，起搏器救回治疗才得到重整再战机会。','先写清任务目标，再分别核算人命、时间、资源、装备和组织代价。','不要用最终收益抹掉别人已经承担的损失。','raid-loot-and-rescue-cost','l-b08-resurrection',[286,287,304,305],[334,337]),
('relationships-are-actions','关系通过有成本的行动改变','卫风殿后、返援、与旧友决裂才建立有限信任；授艺后仍各自独行。','牧琳赔偿解团、救情敌，花舞自有积蓄并自由离队，关系有职业和经济条件。','给关系变化一个可见选择与具体损失，同时保留双方边界。','感恩、同住或沉默不自动等于永久追随和恋爱同意。','teaching-proved-by-old-rival','l-b06-wolves',[295,296,297,298,299],[129,300,306,324,340]),
('ownership-before-reward','先谈收益归属再兑现回报','糖果与萧御按约分史诗肩和技能书，并给参与者补偿。','魔力源泉先经团员同意，才由输出者个人绑定；雇佣合同还规定险情的战利品份额。','区分持有、借用、公共贡献、个人所有权，让对话真的改变分配。','自动把稀有奖品给主角会使此前合作规则失去意义。','loot-settlement-game','l-scene-shared-prize',[279,280],[105,118,129,185,186]),
('objects-change-meaning','物件随新信息改变意义','友情项链先被低估，后安抚、招魂与故事关系不断回用；早期母亲哺血故事重新接回巫妖王线。','塔布雷特杖铭文和卡莫里头颅，让掉落物与任务物转为对另一人的证词和托付。','为同一物件设计功能、关系、历史三层信息，后层重释而不抹掉前层。','只追加更高数值而不改变选择，物件就缺少叙事寿命。','open-box-is-not-loot','pendant-sun-payoff',[48,138,139,151,320],[136,137,165,168,171,172]),
('institutions-shape-freedom','个人自由由组织条款塑形','独行高手借风野公会的资源、侦察与救援扩大战术，合作按互利而非无条件义气运作。','天狂拒吞并而签独立投资，又用分配、训练与库存吸引人才，队伍自由需要具体制度。','把角色想保留的自主权写成能谈判、能违约、能承担代价的条款。','忽略组织托底会把个人成果写成无成本奇迹。','raid-loot-and-rescue-cost','l-b-s05',[265,302,305,313],[147,188,212,213,233,353,363])
]
v=Cached(V);shared=[];data=[]
def find_scene(k,key):
 found=[(b,s) for b in bs[k] for s in b['scenes'] if s['key']==key]
 # 第一条使用早段身体技艺机制，若早期命名不同则以明确章节对应场景为准。
 if k=='z' and key=='body-skill-experiment' and not found:found=[(b,s) for b in bs[k] for s in b['scenes'] if b['unit_start']==1 and any(e['chapter_id'] in ['ch-0008','ch-0009','ch-0010'] for e in s['evidence'])][:1]
 assert len(found)==1,(k,key,len(found));b,s=found[0];aid=ident('scn',k,'scene/'+b['stage_id']+'/'+s['key']);return v.get_asset(aid)
for key,title,ztext,ltext,control,risk,zscene,lscene,zords,lords in COMPARISONS:
 a,z=find_scene('z',zscene),find_scene('l',lscene);refs=[{'asset_id':x['asset_id'],'revision':x['revision']} for x in [a,z]];es=E('z',*zords)+E('l',*lords);aid=ident('pat','shared',key);path=V/v._asset_path(aid)
 content={'summary':control,'zeidan_implementation':ztext,'leveling_implementation':ltext,'applicability':control,'failure_mode':risk,'exercise':'在自己的题材里更换目标、资源、关系和环境，只保留这一条机制；写后记录选择是否清晰、代价是否兑现、读者实际反馈。','status':'跨书研究候选，尚非用户审定风格或原创正典。'}
 x=v.put_asset({'asset_id':aid,'asset_type':'pattern','scope':'reusable-pattern','origin_key':'two-full-books-20261025/'+key,'title':title,'tags':['双书全书比较','原创机制候选','待审阅'],'content':content,'evidence':es,'derived_from':refs,'user_notes':'','favorite':False,'review_status':'draft'},base_revision=load(path)['revision'] if path.exists() else None,generated=True);shared.append({'asset_id':aid,'revision':x['revision'],'type':'pattern','title':title});data.append({'key':key,'title':title,**content,'evidence':es,'derived_from':refs})
dump(O/'shared-asset-manifest.json',shared);dump(O/'comparison.json',data)
body='# 双书全书比较：怎样转成自己的写作能力\n\n共同作者不等于统一可套用的风格。以下比较建立在两书全部阅读单元上，提取中性的创作控制，并列适用边界；个人评价仍待用户填写。\n\n'
for x in data:
 body+='## '+x['title']+'\n\n《贼胆》：'+x['zeidan_implementation']+'\n\n《网游之练级专家》：'+x['leveling_implementation']+'\n\n可试的控制：'+x['summary']+'\n\n失效条件：'+x['failure_mode']+'\n\n来源：'+'；'.join(f'`{e["source_id"]}` / {e["chapter_id"]} L{e["start_line"]}–{e["end_line"]}' for e in x['evidence'])+'\n\n'
body+='## 区别与选择\n\n《贼胆》较多让身体动作、临场观察和独行警戒成为近距离驱动力，现实贫困又把职业收入与自尊相连；《练级专家》更长地展开生产工艺、团队分工、制度与公会资源，将个体成长推向组织领导。两者都以旧信息重组产生战术回报，却不必在原创中保留网游的数字外壳。\n\n最终大战与同名人物的交叉登场可作两书各自叙述的比较证据，资料库仍以source_id分开记录。书中专名、人物关系配置、独特道具和桥段不会自动并成用户世界观。爱情、强者叙事及对普通人的评价应单独审阅，机制奏效也不代表其价值立场值得采纳。\n'
body+='''
## 结局的交叉叙述：不能用一本补写另一本

| 项目 | 《贼胆》本书写出的结果 | 《网游之练级专家》本书写出的结果 |
|---|---|---|
| 最终决斗 | 萧翎先倒地，萧御剩11%生命；萧翎复起后明确认输。叙述同时说明萧御保留的下位神属性构成优势。 | 最后一场约战停在开战前，明确把胜负留给读者。该书自身没有给出胜者。 |
| 神力结算 | 沃顿肉身先被另一支队伍击毁，分身甲变弱；萧御完成击杀并保留下位神神格。 | 团队击败沃顿后临时神力被回收，诸神成为凡人，并非全部永久死亡。 |
| 现实终点 | 萧御、赵岚馨与小雨登机起飞；没有继续写抵达后的婚礼。 | 萧翎已抵达新星，与四位女子重逢；现实父亲与游戏身份的联系得到确认。 |

这是同一共享事件在两书中的揭晓差异，不应把《贼胆》的决斗结果伪装成《练级专家》本书已经回收的答案。角色卡仍以来源分开；跨书比较单独标记外部证据。可迁移的控制是：先决定每部作品承诺回答什么，再选择结果揭晓、限知停笔或开放结尾，并让读者能够辨认边界。

《贼胆》证据：`src-2d8a13f33737429da512e5cc9e839712` / ch-0463 L28695–28737；ch-0464 L28864–28877、L28883–28893。逐章定位见[贼胆索引](zeidan/chapter-index.md#ch-0464)。

《练级专家》证据：`src-359a2bd5a60747038b12a7ba483a5f80` / ch-0387 L23139–23145；结局其余证据见[练级专家终态审计](leveling/ending-audit.md)。
'''
write(O/'COMPARISON.md',body)
for k in BOOK:
 s=S[k];v.checkpoint({'run_id':f'run-full-two-books-20261025-{k}','source_id':s['source_id'],'source_revision':s['revision'],'completed_chapters':[c['chapter_id'] for c in s['chapters']],'pending_chapters':[],'dimensions':list(DIM),'state':'full-source-read-and-distilled','actual_reading_units':len(s['units']),'front_matter':'章前书目信息已核对，不算剧情阅读单元','report':f'library/reports/two-books-full-20261025/{FOLDER[k]}/README.md','reading_basis':'bounded-full-source-reading-with-per-unit-notes','terminal_question_audit':True,'user_review_status':'pending','notes':'本次完整阅读与九维研究覆盖全书；旧试读、旧迁移检查点保留历史，不再代表当前最大覆盖。未创建原创项目。'})
v.build_views()
write(O/'APPLICATION-WORKFLOW.md','''# 后续创作的内容管理

方案A是每次把研究复制到新的Markdown目录，检索容易起步，但人物身份、版本和人工评价容易分叉。方案B继续用现有JSON资料库作主档，Markdown与HTML作阅读副本，Git保存修订。本次沿用方案B；既有卡片、旧贼胆研究和其他书不迁移、不改编号，迁移成本为零。

来源事实与解释位于source-analysis；抽象机制位于reusable-pattern；只有用户实际启动的原创项目才能进入original-project。当前没有替用户创建假作品。书中人物、物件与关系是研究对象，不会直接成为新作正典。

## 查找与评价

在Novel工作区的命令提示符执行：

```bat
novel.cmd search --query 信息 --type scene
novel.cmd search --tag 原创机制候选 --type pattern
novel.cmd checkpoint-show --id run-full-two-books-20261025-z
novel.cmd checkpoint-show --id run-full-two-books-20261025-l
```

从本包人物、场景、机制目录取得asset_id，再用asset-show阅读完整主档。评价填写user_notes、favorite、review_status；人工评价通过asset-put保存时必须携带当前base-revision。以后模型生成更新继续使用--generated，避免覆盖人工字段。

## 把机制用于自己的作品

先选一个机制和一张场景卡，说明自己为什么想试、准备改变哪些前提；更换专名、人物关系、资源形态与事件次序。写完检验角色有没有真实选择、结果有没有改变下一步。只有真实的读者反馈才能标reader-observation，个人判断仍是editorial-judgment。

用户确定作品后，用project-create创建实际项目；project-use固定引用asset_id与revision，升级引用必须明确进行。用户作品的正典只写入original-project，不回填到来源卡。usage-add记录具体改造、观察和反馈，形成学习—试写—反馈—再选择的循环。

## 保存与恢复

每批先核章节覆盖、证据、伏笔终态与原创边界，再限定路径提交私有资料库。工具Git和资料Git仍为两个独立仓库；本次只新增资料，不改生产工具。原书和规范化全文在private-sources，另有本地私有备份，不进资料库Git。编辑不自动等于提交，提交不自动等于推送；实际远程回读与恢复验收放validation。

JSON主档和固定修订是权威；HTML、SVG、PNG与Markdown可重建。sources.json不含机器原文路径，research保存人工阅读后的批次数据；rebuild-full.py重建卡片和分段阅读页，render_full.py复用既有地图生成器。全书综合JSON与终态审计保留研究判断，不靠词频自动生成。
''')
rows=[]
for k in ['z','l']:
 c=coverage[k];rows.append(f'| 《{BOOK[k]}》 | {c["actual_reading_units"]} | {c["stages"]} | {c["cards"]["character"]} | {c["cards"]["scene"]} | {c["cards"]["pattern"]} | [{BOOK[k]}]({FOLDER[k]}/README.md) |')
write(O/'README.md','# 双书完整蒸馏与创作资料入口\n\n两书均按《超级骷髅兵》的层次完成全文阅读、分段九维、人物阶段档案、场景因果卡、机制、全书综合、剧情图及终态核对。研究判断仍待用户审阅。\n\n| 作品 | 实读单元 | 九维阶段 | 人物档案 | 场景 | 机制 | 入口 |\n|---|---:|---:|---:|---:|---:|---|\n'+'\n'.join(rows)+'\n\n《贼胆》保留重号，463个正文单元；《练级专家》387个实际阅读单元含序章及合章，不能按末章印刷数字直接统计。章前简介另核书目信息。人物按来源内姓名聚合阶段快照，数量不含旧贼胆183份阶段记录；旧研究仍保留。\n\n- [跨书比较与12项原创机制候选](COMPARISON.md)\n- [创作、评价、版本与Git操作](APPLICATION-WORKFLOW.md)\n- [验收与证据边界](ACCEPTANCE.md)\n- [上一轮开篇试读与旧研究迁移](../two-books-20261023/README.md)\n- [超级骷髅兵既有阅读入口](../super-skeleton/reading/README.md)\n\nHTML下载后离线打开，Markdown可直接在私有GitHub阅读；原书全文不上传。终态账本保留已回收、部分回收、原文异常与刻意留白，早期推测不会自动变成最终事实。')
write(O/'ACCEPTANCE.md','''# 双书全书验收说明

全文覆盖由逐单元阅读笔记、来源修订与正式检查点共同证明；检索回执只说明取出了文本，索引和文件存在不代表读完。每阶段有完整九维，证据指向既有来源ID与规范化文本行号。合章、重号与误识别片段按已审核阅读映射处理。

人物、场景、机制通过现有资料库API保存；派生机制固定场景版本，生成更新保护人工笔记、收藏与审阅状态。全书图保存结构归属与独立关系边，结构相邻不自动等于因果。问题账保留各阶段历史，并按结局逐键更新终态；没有把预测当结果、计划当完成、人物误认当事实。

分段报告、全书综合与卡片提供不同阅读尺度；全书地图复用超级骷髅兵既有OpenSeadragon离线界面，并提供PNG/SVG。浏览器验收覆盖地图定位、缩放、节点证据、筛选、手机宽度和离线零外部请求；几何校验检查卡片、文字和关系穿越。结果见两书validation。

全库原验证器检查来源、版本、证据行界、卡片派生和图结构；本批另查链接、完整阅读单元、终态映射和长段原文重合。证据范围有效不证明每条文学解释无误，用户审阅仍未完成。原文异常和未解处有专门账本，没有擅自修补原书。

本次在独立目录生成，最后只复制和提交本批路径；失落叶任务的已有修改按指纹保护。工具生产代码与原创作品均未新增。原文留本机，Git仅保存研究概括、定位和生成的阅读产物。远程提交和本地备份恢复分别以validation/save-and-restore.json为凭；其他任务未提交状态不包含在本次Git快照备份内。
''')
path=V/'START-HERE.md';text=path.read_text(encoding='utf-8');text=text.replace('- **[贼胆＋网游之练级专家：本批研究](library/reports/two-books-20261023/README.md)**：旧研究迁移、开篇九维细读、人物/场景/机制卡及续读位置。','- **[贼胆＋网游之练级专家：完整蒸馏](library/reports/two-books-full-20261025/README.md)**：两书全文、九维、人物/场景/机制、全书图与结局核对；旧试读和迁移记录保留历史。')
write(path,text+'\n双书最新检查点是`run-full-two-books-20261025-z`与`run-full-two-books-20261025-l`。RESEARCH-QUEUE中的旧试读条目保留原时间语境，当前最大覆盖以这两个完整检查点为准。')
path=V/'AGENTS.md';text=path.read_text(encoding='utf-8');text=text.replace('- 双书入口：`library/reports/two-books-20261023/README.md`。贼胆463章旧研究是迁移成果，本次只回读1–10章；练级专家本次读序章与1–12章。不能把索引或迁移标成新增全文阅读。','- 双书最新完整入口：`library/reports/two-books-full-20261025/README.md`。2026-10-25已实际读完贼胆463正文单元与练级专家387阅读单元（含序章、合章），完成分段九维和终态问题复核。旧试读与贼胆迁移成果保留历史，不要重复建库；研究解释仍待用户审阅。')
write(path,text)
path=V/'CONTENT-GUIDE.md';text=path.read_text(encoding='utf-8');write(path,text+'\n## 双书完整研究\n\n2026-10-25完整成果见[双书总入口](library/reports/two-books-full-20261025/README.md)，实际创作检索、评价与固定版本引用见[后续操作](library/reports/two-books-full-20261025/APPLICATION-WORKFLOW.md)。原来开篇试读与迁移检查点作为历史保留，最新覆盖以全书检查点为准。')
dump(P/'shared-result.json',{'new_shared_patterns':len(shared),'ids':[a['asset_id'] for a in shared]});print('总入口、跨书机制、完整检查点与管理说明已保存',len(shared))
