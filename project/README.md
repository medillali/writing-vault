# 项目框架、执行资料与跨端交接

[当前状态](CURRENT-STATE.md) · [跨端续接提示](CROSS-END-PROMPT.md) · [协作规则](../COLLABORATION.md)

- workspace/：原Novel父目录的创作框架、工作台和命令入口快照。
- planning/：各轮执行计划、阅读研究稿、审计与验证记录。它们按当时状态保留，不覆盖正式主档或最新检查点。
- tool-work/：工具work目录中有研究价值的full_distill与review工作稿；演示、依赖包和测试恢复副本不混入。
- exports/：既有对话交接包；正式可信基线仍保留于exchanges/outbox。
- sync/：本次归档清单、发布检查及远端核验回执。

根目录的library/和exchanges/runs/仍为当前研究主档与范围依据。旧脚本依赖原工作区布局，不要在本目录直接整批重跑。
