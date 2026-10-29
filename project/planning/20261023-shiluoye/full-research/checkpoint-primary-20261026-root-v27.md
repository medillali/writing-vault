# 主审续接 v27

本任务继续到三书整体验收、统一管理、全新完整备份与实际隔离恢复；不在单卷/单书里程碑结束。v26和后续上下文中的旧数均被当前签账代替。

- 当前实际签入2582候选/135批：历史232全；local2350/2462。卷4根审至017（340/373），卷6前007（140/200），尾009（180/199）。剩112 = 卷4 33 + 卷6前60 + 尾19。分工不变：reader3卷4末后36综合；reader5卷6前段至200后人物分组；reader4尾段至399。
- 24重点3组仍原SHA cbafcb…/c21c99…/b76044…，总稿38aeea…；未签人物或36综合。六卷、全文已正式读完；ZL整书未验收，勿误报。
- 燕荐3字段已正式外置priority-corrections-yan-recommendation.json/md，原件不动。combined现在100字段记录/6逻辑问题，SHA829548507f2346a9384af96ac740cccaafd1cca2a7e9d205b22f40f4bde696cb。原97版a60…字节保formal audit/material-history/a60….json；manifest按原path+SHA解析。verify_zhanlong_focused_final.py已支持且实际通过24/220refs，签组不改。config、ZL总览、readingREADME、RESEARCH-QUEUE已补第五纠正入口；catalog重建8来源2844卡activeZL。
- tail003兰神格：根实际全文读1295，L93721确为兰斩格。批准0101-01 unrecovered→partial，取得已成/炼成未明并保1274子舒/1295流施为差。current90b7db7a1d25d7c5b07540ef7a5b17f37e2be6c7529e4e5250adba8fffa43be7；原b97f字节及delta存tail-review；根完整20新批读签。
- 卷4b016原e70曾签；根实际全文重读938，L70230罗嗣半矿实交/分2000多枚龙晶炮（语境炮弹），批准0163-01/0164-01 partial→answered，仅status/rationale/later_chapters/later_evidence改，保927追加938。current73704c15d8d0e6f5b79829ce8d14a280e238ccdf8ec737b9e02314f0880c0bb5。根完整重读新20；verify_zhanlong_halfmine_revision.py独立精确2项/其余18重放通过。reader3-review保存原e70及旧主审签账primary-progress-before-halfmine-resign.json（b6acbe…），后正常重新签入，无ID新增。
- 根实际全文读1374，御林14万实出、秋收10万；前批014秋收十万并无冲突。不要混御林和秋收。
- 卷6b007镜像修订：原5b114…中3条错称武魂只预测，根全文读1240/1241（L89947具名问魂；89954全属+100/技能保；89976合力杀问魂；89980—94方魂实战/真方告18s；90006退百万魂），另定向1221 L88760—66确认全副本已通。批准0028-01/0031-01/0032-01仅理由和后证补1240/41（0032补1221），status partial保。0038-01理由1369叙述原ref止98448错，改98452—55，指正式canglan-1369-addendum.json SHAdaaaa7…和真实primary全文归属。四项after51e9…已根完整20重读且独立精确重放通过，余16逐值相等。
- 根额外将b007两旧分类名unrealized/unseen改与已审实战理由一致：0028→rescued-survivors-and-unitemized-return-roster；0031→person-recovered-and-mirror-battle-realized。仅audit_domain，before51e快照+primary-batch007-final-revision.json存local-v03-v06-review。最终已签SHA88be5c924eec92b7a14540c2b28357b56ba3a8d65431c838e4e283e056a32038。勿重跑guarded verify_and_label_zhanlong_mirror_revision.py（已应用）。reader5已通知不覆写。
- 根扫已签候选武魂/镜像在新007前无命中；reader5扫自身全部v03与v06前7仅真需改3条，扫描回执已存，不把检索当阅读。
- 合池脚本新增保source_attribution的结构化署名；新增测试先实际KeyError失败再修，7/7通过。仍默认只读，--apply须2694全已签；当前未合池。
- 尚无ZL最终四包冻结编译器；旧WS assembler不可直接照抄115/30/4130。需全签两池后merge，人物/重点逐值等已签分组；末卷是vol06，legacy key frozen_volume08_hashes可显式说明沿旧接口用vol06 snapshots。
- 还需归档所有研究引用的path+SHA材料以脱离.planning恢复，不改已签对象；旧priority历史已经解决一个实际版本漂移案例。
- 发布顺序注意：先正式36综合及本书导航文案定稿，再audit publisher捕获原导航SHA；审计发布后勿在audit标记之外改README原内容，否则独立校验会失效。最终accept只改检查点/验收与catalog。
- 终点未做：人物全弧、36综合，合池/冻结/整书主审凭据、publish/独立验收、跨书比较正式稿/8源真状态、fresh fullbackup与actualisolatedrestore。ZH/WS已验收SHA保持前checkpoint。无Git/Space/远程/记忆写入。
