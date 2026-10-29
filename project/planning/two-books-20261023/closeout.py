from pathlib import Path
import subprocess,json,shutil
R=Path(__file__).resolve().parents[2];V=R/'.verify/two-books';L=R/'writing-vault';P=R/'.planning/two-books-20261023'
rel='library/reports/two-books-20261023/validation/batch-validate.json';shutil.copy2(V/rel,L/rel)
p=P/'task_plan.md';p.write_text(p.read_text(encoding='utf-8').replace('- [ ]','- [x]'),encoding='utf-8')
with (P/'progress.md').open('a',encoding='utf-8') as f:f.write('\n- 完成：真实长期库合入29张新卡，复用292张旧卡与两个既有来源ID；纠正练级专家索引并同步队列。内容提交8d0cb62已推送并通过GitHub递归树2190文件哈希核验。最终精确Git备份已恢复至新目录并再次全库校验565卡/6来源/6图；原书独立本机备份核对通过。\n')
readme=R/'backups/README-two-books-20261023.md'
readme.write_text('# 双书备份选择\n\n使用 `writing-vault-two-books-canonical-exact-8d0cb62.zip`：最终统一身份后的研究，2190文件逐一核对Git blob，恢复库验证通过。原文用 `two-books-canonical-originals-20261023.zip`，两书字节哈希均通过。\n\n较早的writing-vault-two-books-20261023.zip是临时身份的历史快照，不能直接覆盖当前库。文件writing-vault-two-books-canonical-8d0cb62.zip受本机autocrlf影响，没有通过逐字节Git blob核验；保留作排错材料，不用作最终恢复入口。\n\n先恢复到新目录，继续以writing-vault当前main及检查点为准。Git不包含原书。\n',encoding='utf-8')
print('验收记录与任务计划已更新')
