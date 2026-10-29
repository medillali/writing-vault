"""根据已执行的验收结果写收尾说明；不提前宣称远程重克隆通过。"""
import json
from pathlib import Path
from persist import ROOT,HERE,SID
from fictionlib.vault import Vault

def main():
    proof=json.loads((HERE/'fullbook-verification.json').read_text(encoding='utf-8'))
    browser=json.loads((HERE/'live-18-qa.json').read_text(encoding='utf-8'))
    package=json.loads((HERE/'review-package.json').read_text(encoding='utf-8'))
    applied=json.loads((HERE/'book-end-applied.json').read_text(encoding='utf-8'))
    assert proof['volumes']==18 and browser['volumes']==18 and package['browser_check']=='passed'
    vault=Vault(ROOT/'writing-vault')
    cards=[a for a in vault.search() if any(e.get('source_id')==SID for e in a.get('evidence',[]))]
    kinds={kind:sum(a['asset_type']==kind for a in cards) for kind in ['character','scene','pattern']}
    folder=vault.root/'library/reports/super-skeleton'
    ledger=json.loads((folder/'question-ledger.json').read_text(encoding='utf-8'))
    counts={s:sum(e['status']==s for e in ledger['entries']) for s in ['answered','partial','open','text-uncertain']}
    acceptance=f'''# 《超级骷髅兵》全书蒸馏验收

## 本轮成果

完成18集、183正文/序章、202索引段（另含18集标题、1章前说明）的实际顺序阅读、逐集九维分析、独立复核与入库。原始全文约1,161,225字符，引用采用同一来源修订的章节ID及行号。本轮研究卡{len(cards)}张：人物{kinds['character']}、场景{kinds['scene']}、机制{kinds['pattern']}；全库仍保留其他三书的18张开篇样段卡。

逐集九维项目{proof['nine_dimension_items']}项，全书综合另有九维分析、阶段与角色弧。剧情图{proof['graph_nodes']}节点、{proof['graph_edges']}关系，保留主线树、暗线网络、各集当时认知和最终累计状态。{len(ledger['entries'])}项原始问题均做整书复核：已回答{counts['answered']}、部分回答{counts['partial']}、未回收{counts['open']}、文本不确定{counts['text-uncertain']}。未回收与口径矛盾保留，不强补答案。

## 模块与验收状态

| 模块 | 子项 | 状态与证据 |
|---|---|---|
| 来源与覆盖 | 全文切分、修订、阅读记录 | 18/18集，202/202索引段；分集报告、reader日志与运行检查点一致 |
| 持久资料库 | 人物/场景/机制、版本历史 | 本轮扩充；{applied['character_cards_audited']}张人物完成终点审计，{applied['state_corrections']}张另有累计补记；人工备注、收藏和审阅状态保留 |
| 情节结构 | 主线树、语义关系、伏笔状态 | 无悬空引用；逐集与跨集关系可筛选；阶段解释保留，终点修订单独追加 |
| 审查入口 | 分集九维、全书综合、问题账本 | 1440px桌面和390px视口实际浏览器通过；搜索、类型/集数筛选、证据展开、图链接与网络视图通过；无脚本错误及远程请求 |
| 本地迁移 | 备份、恢复、离线审查包 | 全库卡片与图恢复一致；无原小说TXT仍可独立重建完全相同HTML；离线包解压后相对链接及浏览器通过 |
| Git保存 | 两个既有私有库、资料库提交 | 本轮研究资料推送writing-vault；最终SHA和重新克隆比对由提交后的本机验收记录给出 |
| ChatGPT衔接 | 文件工作包、Space/记忆 | 文件式工作包沿用已实现能力；Space未接入，GitHub保存不会自动写入记忆 |
| 文学审阅 | 事实、解释、抽象方法、用户偏好 | 研究草稿可供整书审查；结构验证不代替文学判断，未替用户收藏或批准风格规则 |

## 验收边界

本轮扩充研究数据及专用审查页，并修复全书大图被过度缩小的问题。工具回归与大图浏览器验证另附记录；研究数据已执行覆盖、证据、资料保护、图、真实浏览器、恢复与迁移检查。390px为本机浏览器视口验证，不声称手机实体设备验收。图文静态文件无服务器部署步骤。

`audit/`保留分集复核、读完记录、人物和线程审计；`validation/`保存本轮本地验收结果。原文仍仅在本机，未入Git或默认备份。其他三本仅为开篇样段，不将其称为全书蒸馏。

建议先看全书综合和审查重点，再看疑点账本及感兴趣的人物/场景；用户反馈再写入人工笔记或收藏，逐集原始研究不被覆盖。
'''
    (folder/'验收说明.md').write_text(acceptance,encoding='utf-8')
    validation=folder/'validation';validation.mkdir(exist_ok=True)
    for name in ['fullbook-verification.json','live-18-qa.json','book-end-applied.json','review-package.json','graph-readability-review.md','graph-code-review.md','tool-final-verification.json','tool-ci-final.json','ledger-final-sync.json']:
        (validation/name).write_text((HERE/name).read_text(encoding='utf-8'),encoding='utf-8')
    fixture=ROOT/'distill-novels/work/tests/readability-7OyqBX/passed.json'
    (validation/'graph-readability-fixture.json').write_text(fixture.read_text(encoding='utf-8'),encoding='utf-8')
    readme=f'''# 我的小说资料库

人物、场景、创作机制位于`library`，原创作品位于`books`。JSON为主档，`library/views`为生成的阅读副本，版本历史位于`history`。这是实际个人资料库，未混入演示素材。

## 当前可审查成果

- [《超级骷髅兵》全书审查入口](library/views/超级骷髅兵全书审查.html)：18集完整研究、九维分析、{len(cards)}张研究卡、主线树与暗线网络、全书综合和{len(ledger['entries'])}项疑点回收。
- [全书综合报告](library/reports/super-skeleton/book-synthesis.md)、[疑点账本](library/reports/super-skeleton/question-ledger.md)、[验收说明](library/reports/super-skeleton/验收说明.md)。HTML需下载到本机打开；GitHub网页可直接看Markdown。
- [四书开篇样段入口](library/views/四书实测.html)：保留原先开篇测试。《骷髅魔导师》《重生之贼行天下》《网游之纵横天下》尚未全书蒸馏。
- [卡片目录](library/views/index.md)：当前资料的Markdown副本。研究解释和用户评价分开；所有新研究仍待用户审阅，未自动收藏。

## 保存与恢复

私有资料库：[medillali/writing-vault](https://github.com/medillali/writing-vault)，`main`分支。独立私有工具库：[medillali/distill-novels](https://github.com/medillali/distill-novels)。保存卡片会维护历史，但不会自动进行Git提交；更新后校验、检查diff、按范围提交并推送。

换机将两个仓库克隆到相邻短目录，用工具的`scripts/library.py`读写资料。专用审查页可单独运行`library/reports/super-skeleton/rebuild_review.py`重建，无需原小说。图的重新生成需要工具库，已生成的图可直接离线打开。工作区`novel.cmd`只是本机入口，换机不依赖它。

全库ZIP备份保存研究主档与历史，离线审查ZIP提供直接阅读副本。审查页能筛选与查看，不能直接保存个人备注；持久编辑须通过资料库工具。原TXT仅在本机`private-sources`，不在Git历史或默认备份中；核对原文需要另行携带原书和一致修订。

检查点在`exchanges/runs`，新会话从既有来源和检查点接续，不能重建空库覆盖资料。Space尚未接入，GitHub保存不会自动写入ChatGPT记忆；文件工作包可用于双端衔接，新私库的连接访问范围仍需后续配置。
'''
    (vault.root/'README.md').write_text(readme,encoding='utf-8')
    print(json.dumps({'research_cards':len(cards),'kinds':kinds,'questions':counts,'written':['README.md','验收说明.md','validation']},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
