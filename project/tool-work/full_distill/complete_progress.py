"""远程重克隆通过后才关闭本轮全书执行检查项。"""
import json
from persist import ROOT,HERE

remote=json.loads((HERE/'remote-fullbook-verification.json').read_text(encoding='utf-8'))
local=json.loads((HERE/'fullbook-verification.json').read_text(encoding='utf-8'))
package=json.loads((HERE/'review-package.json').read_text(encoding='utf-8'))
tool=json.loads((HERE/'tool-final-verification.json').read_text(encoding='utf-8'))
assert remote['remote_private'] and remote['independent_html_rebuild_identical'] and package['browser_check']=='passed'
plan=ROOT/'task_plan.md'
text=plan.read_text(encoding='utf-8')
for label in ['全书复核跨集人物弧与伏笔回收，生成九维综合报告和审查清单。','验证覆盖、人工字段保护、图与页面、备份恢复和远程提交一致。']:
    text=text.replace('- [ ] '+label,'- [x] '+label)
text=text.replace('本轮正在完成《超级骷髅兵》全书九维蒸馏；其余三本全书和Space接入保留后续。','本轮已完成《超级骷髅兵》全书九维蒸馏及本地/私有远程验收，等待用户整书审查；其余三本全书和Space接入保留后续。')
text=text.replace('第18集提交848074e，最终综合另作提交',f'第18集提交848074e，最终综合提交{remote["commit"][:7]}')
plan.write_text(text,encoding='utf-8')
with (HERE/'progress.md').open('a',encoding='utf-8') as f:
    f.write(f'''\n\n## 全书交付验收已完成\n\n- 18集/183正文序章/202索引段；逐集九维{local['nine_dimension_items']}项，整书综合27项。\n- 104张人物卡逐项审计，27张累计补记；46条剧情线终点审计，198问及89修订完成复核。\n- 实际1440px/390px浏览器、离线包、无原文备份恢复和独立HTML重建通过。\n- 私人远程最终提交：{remote['commit']}；重新克隆{remote['tracked_files_verified']}个跟踪文件内容一致（Windows换行差异单独记载），原TXT不在库中。\n- 最终交付备份：backups/小说资料库-全书审查交付-20261022.zip；离线包：backups/超级骷髅兵-离线审查包-20261022-终审.zip。\n- 工具已修复大图可读性并通过53项核心测试及浏览器回归；私库提交{tool["commit"]}。其他三本保持开篇样段。用户收藏/风格规则尚待审阅，Space未接入。\n- 验收记录：fullbook-verification.json、live-18-qa.json、review-package.json、delivery-backup-verification.json、remote-fullbook-verification.json。\n''')
print('Completed local and private-remote delivery checkpoints.')
