# 私人小说生产入口

本轮交付可运行的本地工作台：**建书、人物卡、章节目录、任务包、正文回收、审稿返修、定稿与后章记忆。** Codex 负责规划与审稿，Antigravity 负责文字，用户验收重要取舍与最终正文。

## 直接启动

需要 Git 与 Python 3.10+，不需要付费 API、不需要 PowerShell、不需要 Node。

1. 在 HTX 的这个研究库中切换到本 PR 分支，或下载本分支源码 ZIP 并解压。已有未提交改动先保留，不覆盖旧工作副本。
2. 打开 `project/studio`，Windows 双击 **`start.cmd`**。
3. 浏览器打开 `http://127.0.0.1:19423`。建一部真实作品，从第一章开始；此处不会把虚构演示冒充你的作品。

跨平台可在研究库根目录运行：

```bash
python3 project/studio/launch.py
```

启动脚本先校验随附工具包，再将工具克隆到独立的版本目录并打开工作台。再次运行会复用相同版本，存在不符的提交或本地改动时会停止，避免覆盖。私人小说数据默认在 Windows `%LOCALAPPDATA%\NovelStudio` 或 Linux/WSL `~/.local/share/novel-studio`，与程序目录、研究库分开。

## 这次交付为什么带工具包

当前连接可以写 `writing-vault`，对 `distill-novels` 写入返回 GitHub 403；当前执行环境也没有另一个已登录的 Git 客户端。因此完整工具以 `distill-novels.bundle` 交付在本 PR 中，附 `toolkit.patch` 供逐行审阅。Bundle 包含完整 Git 历史与已验证功能提交，可离线克隆；不是只有方案文档，也不依赖尚未创建的远端工具分支。

`release.json` 记录精确提交与 SHA-256。工具库独立 PR 尚未创建；补齐该仓库写权限后，可把同一功能提交推送并发起 PR，无须重做开发。没有合并两个仓库的 main，也没有处理其他研究 PR。

## 使用与验收

- [完整上手说明](docs/私人小说工作台.md)：日常分工、Antigravity 提示、回收、备份恢复。
- [四种章节任务](docs/章节任务模板.md)：开书、开篇、常规章节、返修。
- [工具设计比较](docs/小说工具设计比较.md)：Pagekin、Novelcrafter、NovelAI、星月写作。
- [测试结果与限制](docs/工作台验收.md)：68 项测试与 DOM 实际交互通过，真实浏览器视觉验收尚未完成。

首个真实目标是开篇三章完整闭环，不再按审计轮数衡量产出。两个仓库目前公开，本 PR 仅包含通用工具、文档和虚构测试；真实原稿与备份留在私人目录。

用户已授权 dot 通过 HTX 连接 GitHub，但本会话没有可用 HTX 远程执行入口；不能把代码交付说成 HTX 已安装。此前 WSL 与 Windows 工作副本也不自动同步，选定一处私人主档后使用。

## 手动提取与核验

```bash
git clone -b codex/private-novel-studio-20261113 project/studio/distill-novels.bundle /path/to/new-studio-code
python3 /path/to/new-studio-code/scripts/studio.py serve --open --research-vault /path/to/writing-vault
```

新目录必须是空目录或不存在。也可运行 `python3 project/studio/launch.py --check-only --code-dir /path/to/new-studio-code` 只安装核验，不启动服务。资料库中的原小说全文不在本包中。
