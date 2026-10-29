from pathlib import Path
import json,shutil
R=Path(__file__).resolve().parents[2];V=R/'.verify/two-books';O=V/'library/reports/two-books-20261023'
mapping=json.loads((O/'validation/identity-reconciliation.json').read_text(encoding='utf-8'))['source_id_map']
for old,new in mapping.items():
 src=V/f'private-sources/normalized/sources/{old}';dst=V/f'private-sources/normalized/sources/{new}'
 if src.exists() and not dst.exists():shutil.copytree(src,dst)
for p in [O/'README.md',V/'START-HERE.md',V/'RESEARCH-QUEUE.md']:
 s=p.read_text(encoding='utf-8').replace('另迁入292张旧研究卡','另复用并核验292张旧研究卡')
 p.write_text(s,encoding='utf-8')
with (O/'README.md').open('a',encoding='utf-8') as f:f.write('\n并行入库已做身份对齐：两书使用长期库已有来源编号，292张旧卡复用既有ID和人工字段。本批不另建重复来源；详见[身份对齐记录](validation/identity-reconciliation.json)。\n')
with (V/'START-HERE.md').open('a',encoding='utf-8') as f:f.write('\n其他作品的跨书目录由同库的 `library/reports/collection/README.md` 维护；各书的实际覆盖以对应检查点为准。本页的双书成果可与该目录共存。\n')
p=O/'acceptance.md';s=p.read_text(encoding='utf-8')
s=s.replace('新增两书独立身份','复用两书既有身份').replace('迁移463章记录、292张卡','核验463章记录、复用292张卡').replace('等待本批提交推送','待最终远程回读').replace('人工字段与基线已有改动保留','复用292张卡的字段与版本保持一致')
s+='\n## 并行成果整合\n\n先前隔离快照 `6e430f2` 使用临时来源ID；最终内容已按相同原文哈希统一到长期库身份，并复用并行任务已经迁入的292张旧卡。旧快照ZIP保留为历史恢复点，正式接续使用当前Git版本和长期库。重新生成了机制工作包，确保ID变化后的基线哈希有效。\n'
p.write_text(s,encoding='utf-8')
with (R/'.planning/two-books-20261023/progress.md').open('a',encoding='utf-8') as f:f.write('\n- 推送main遇到非快进：另一个任务已提交地图并登记相同来源。隔离分支合并6099fa8后按文本哈希统一来源ID，复用292张已存在旧卡，保留其版本和用户字段。重新导出工作包；全库565卡/6来源/6图验证通过。最终合入只列举本批文件，不暂存其他任务的修改。\n')
print('normalized paths restored; reconciliation documented')
