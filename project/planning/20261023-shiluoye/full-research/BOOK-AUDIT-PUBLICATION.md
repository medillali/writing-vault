# 全书审计发布与验收脚本

本次仅准备辅助脚本并在planning隔离样例内验证；未运行真实资料库发布。`publish_book_audit.py`默认只读。正式发布只接受已经存在的真实主审凭据，不生成或补填审批。

## 《网游之纵横天下》执行

从Novel工作区根目录使用cmd运行。解释器路径为本机已验证的Python：

```bat
%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe .planning\20261023-shiluoye\full-research\publish_book_audit.py --reviewed --dry-run
%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe .planning\20261023-shiluoye\full-research\publish_book_audit.py --reviewed
%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe .planning\20261023-shiluoye\full-research\validate_book_audit.py --output writing-vault\library\reports\zongheng-tianxia\audit\whole-book\publication-validation.json
```

首行是只读预检；第二行是唯一正式发布步骤；第三行独立核验已发布副本，不依赖暂存目录，保存独立验收回执。若只需输出结果可省去`--output`。不带`--reviewed`时始终只读，即使已有主审凭据也不发布。

主审凭据默认读取`zongheng-tianxia/primary-whole-book-review.json`，冻结清单读取该本书暂存根下的`vol08/audit-freeze-manifest.json`。要求`status=reviewed_for_library_import`、`reviewer=primary`且`freeze_manifest_sha256`与当前清单一致；有`source_id`时核对一致。未增加新的文学审阅门槛。

## 发布范围

- 全部冻结审计JSON/MD原字节复制到本书正式`audit/whole-book/`，保留48人物弧、27聚焦项、105历史项、404原子项的独立schema与用户draft。
- 冻结清单中的辅助脚本只存档在`provenance/`；6份冻结卷末核心也存档以供脱离暂存目录验SHA。不会执行旧生成器。
- 真实主审凭据原样复制；另生成发布回执、人物身份索引、终点线程叠加。89图线程与16独立历史问题分别映射，不把105项全算作图线程。
- 本书根新增`question-ledger.md/json`、`character-arcs.md`。问题JSON仅索引两池，MD列各池终点枚举、原始条目类型与审计领域计数。
- 本书README与`reading/README.md`只追加带边界标记的导航块，使用执行时实时内容为base。`reading/plot/terminal-audit.md`连接独立终点对照。原导航字节备份在`provenance/previous-navigation/`。
- 不修改分卷包、正式图、卡片、人工字段或用户评价。发布前后核查它们的SHA。丁舒升/轻狂书生/丁书生有姓名层级；龙神称号组与血吼不自动合并；CGL邱华同名不自动合并。

README、reading/README及新入口完整SHA保存在发布回执中。发布后不要运行会覆盖这些导航的重建命令；后续验收状态可另写独立验收文档或检查点。相同冻结版本重复运行时先独立验收，成功则不重复写；已有不同冻结版本时脚本不覆盖，需另行设计保留旧版的迁移。

发布先完成只读检查与内容准备，再写独立临时目录，核对未变化后落正式子目录并接入导航；导航失败则恢复原导航并保留失败包。不会递归删除旧资料。发布和独立验收均不提交或推送Git。

## 校验范围与当前证据

只读预检核验当前51项冻结SHA（21审计文件、24正式输入、6卷末核心），来源修订/章节行范围/claim_kind、唯一标识、完整条数、原问题表示、终点枚举、未决输入及原图线程状态。3998条证据是定位检查数，不等于3998条独立文学事实。

独立验收逐项检查发布副本SHA、当前正式输入与保留文件SHA、两池计数、身份索引、原卷末与终点叠加对应、用户draft及可读链接可达性。它不重新评判主代理已经签收的文学解释。

隔离测试：`test_book_audit_scripts.py`，6项覆盖正常发布及脱离暂存目录独立验收、缺主审、主审清单不匹配、冻结内容篡改、路径越界和发布后篡改。样例仅写在本目录的临时子目录，并不伪造真实本书凭据。Windows临时目录使用短名称，已修复260字符路径边界。

## 书二/三适配

`--book tianxia-wushuang`或`--book zhanlong`选择正式本书目录；`--staging`指定各书暂存根；`--audit-subdir`指定实际末卷审计子目录；`--source-index`可覆盖默认的`staging/source.json`。`--root`仅在工作区位置变化时设置。独立验收使用同一个`--root`与`--book`，不需要暂存路径。

当前发布器消费已审4包schema：`character-arc-audit-draft.json`的`characters`、`end-state-audit-draft.json`的`findings`，以及两问题池的`candidates`，并使用冻结清单中的`audit_sha256`、`formal_input_sha256`、`frozen_volume08_hashes`。最后一键是现有末卷冻结字段名称；若后两书冻结采用其他键名，应先明确字段映射再适配，不把末卷编号或本书条数硬套到其他书。计数与证据数均从各书冻结验证实际核对，不使用48/27/105/404作为通用常量。

`--identity-profile`可指定各书明确姓名层级和冲突规则的JSON，参考本目录`zongheng-audit-identity-profile.json`。不传时后两书使用保守逐条索引，绝不复用纵横的人名规则或自动合并别名。必须先有各书实际主审凭据；本脚本不授权阅读后续书，也不把建档当已读或审计通过。
