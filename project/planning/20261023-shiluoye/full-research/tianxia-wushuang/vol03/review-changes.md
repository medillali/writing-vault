# 卷三主审修订差异

本轮仅修本卷草稿及生成辅助脚本，不改逐章真实阅读归属或正式资料库。修订后378片/376正文覆盖保持一致，未借后文补本卷结算。

| 具体字段 | 改动与依据 |
|---|---|
| `cards scene/tournament.content.choice`、`analysis.dimensions.pacing[3].fact`、`graph e-blade.label` | 按古剑视角统一半决赛2:1胜烛、决赛1:2负雪银；不改变胜负与冠军归属。 |
| `cards scene/dragonblade.content.choice/outcome/evidence` | 完整复读raw0363、0367—0368。0363 L33274—33283捕寒冰狐经验使陆100并触发武神；0368 L33619明确杀紫域后100→105，L33663—33680偷天自带降需20并105实穿；L33696—33701为靴/杖另镶简易，靴实际穿。补入0363/0368证据，不再把两个升级时点合写。 |
| `graph e-identity.label` | 战地第一分盟改战天第一分盟；550—551面对面互认和援军归属保持。 |
| `graph e-promotion.kind/label/evidence` | `cause`改`setup`，补500。表达寒刃任务恢复条件与501实际交付，502另付费学技，不以章节先后本身建立直接因果。 |
| `graph e-recooking.to/label` | 从第三城赌约`promise`改实际检验产能的`valley`；保制作/分药/五转门槛与604—605壁垒锋线，明确不是每位五转都由药促成。 |
| `graph e-acceptance`及线程引用 | 删除小蛮入盟→第三城赌约错误因果。八人真实入主盟仍完整保留在小蛮人物卡/场景与招募线程。 |
| `graph t-growth.node_ids` | 补`tournament`和`coldblade`，分别确为新装实用与导师任务条件；不机械加入第三城赌约。 |
| `graph t-business.node_ids/stage_note` | 补`sponsor`，合同只提供预期收入，雨立方真正出资另记。 |
| `graph t-recruit.node_ids/stage_note` | 补`nine`，书扇来自九龙并实际交吕；删除已删`e-acceptance`引用，不把赌约塞入招募线。 |
| `graph t-war.node_ids/stage_note` | 补`tigeralchemy`、`earth`，分别为青虎产能和掠夺技能在本战真实调用；成员包含边两端且具语义。 |
| `graph entry.knowledge` | 金石判断拆为先`misbelieves`金币、后`knows`只是金石并引怪，两条均531；保留误信窗口但不把已纠正判断写成终态。 |
| `handoff.md`、`report.md`、`validation.json` | 交接补精确成长时点；图计数更新为40节点/24边/14线程/16知识状态，刷新8文件哈希。 |

已实际执行：`find_thread_outside.py tianxia-wushuang 3` 无越成员输出；`check_volume.py tianxia-wushuang 3` 完整通过，65卡（23人物/32场景/10机制）、2956证据引用、40节点/24边/14线程。该检查只验证覆盖、定位与图结构，文学稿仍为draft，未获用户风格批准。正式导入与钉SHA由主代理负责。
