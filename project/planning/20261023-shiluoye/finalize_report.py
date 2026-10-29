"""汇总本批真实验收结果，不将排队任务标记为完成。"""
import pathlib,json,shutil
root=pathlib.Path(__file__).resolve().parents[2]
work=root/'.planning/20261023-shiluoye';vault=root/'writing-vault';dest=vault/'library/reports/collection'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
validation=read(dest/'validation.json');first=read(work/'zongheng-tianxia/import-result.json')
assert validation['vault']['valid'] and not validation['broken_local_links']
shutil.copyfile(work/'collection-review.md',dest/'迁移审查.md')
for number in [1,2]:
    review=work/f'vol{number:02d}-review.md'
    if review.exists():shutil.copyfile(review,dest/f'卷{number}研究复核.md')
review2=dest/'卷2研究复核.md'
if review2.exists():
    with review2.open('a',encoding='utf-8') as file:
        file.write('\n## 主代理补充核对\n\n另全文复读第68、77章：有限信任、不要告知凌雪的边界及任务交付均有正文支持；修正冰茶由复活预言复活后脱战回城，以及凌雪仅第一件狂风装备耐久低于10%的范围。第69章9860元标为按4.93元/金乘2000金计算，正文称近一万。该复读未增加覆盖章数。正式库的图标识符按节点、边、线索字段分别映射，保留状态枚举和阶段事实；结构合并后通过全库校验。\n')
counts=dict(first['counts']);second_path=work/'zongheng-tianxia-vol02/import-result.json'
completed=49;volume_text='卷一';next_chapter=50
if second_path.exists():
    second=read(second_path);completed=second['cumulative_read_chapters'];volume_text='前两卷';next_chapter=101
    for kind,count in second['counts'].items():counts[kind]=counts.get(kind,0)+count
text=f'''# 本批整理与验收记录

日期：2026-10-23。当前总体状态：**统一管理完成本批落地；三部失落叶全书蒸馏仍在推进中。**

## 已落实的内容

| 范围 | 本批状态 | 证据与入口 |
|---|---|---|
| 单一正式资料库 | 继续使用writing-vault；共8本来源 | [总目录](README.md) |
| 三本输入与身份 | 全文已建索引；纵横复用内容相同的既有source_id；原文件不改写 | [输入核验](input-audit.json) |
| 创作顺序 | 纵横天下→天下无双→斩龙；以作者访谈为依据 | [顺序及配置](catalog-config.json) |
| 纵横分卷研究 | {volume_text}第1—{completed}章连续全文阅读，分卷九维报告、人物{counts['character']}、场景{counts['scene']}、机制{counts['pattern']}、主暗线图已入库 | [分卷专题](../zongheng-tianxia/README.md) |
| 旧贼胆迁移 | 463章首轮研究继承；183份人物材料、109场景、69剧情线；60候选独立保留 | [贼胆](../zeidan/README.md)、[迁移审查](迁移审查.md) |
| 其他旧成果 | 保留贼行天下、超级骷髅兵、骷髅魔导师；未重置用户字段 | [总目录](README.md) |
| 阅读续接 | 纵横下一起点第{next_chapter}章；天下无双、斩龙依序待读；练级专家序章＋前12章另有已读检查点 | [管理规则](管理规则.md) |

新卷中的原文事实、主角估计、研究解释和迁移条件分别记录。第30章的击杀/物品获取与任务失败并存；第49章巫师之心尚未交付，后续状态以新章节实证更新。图只覆盖已读范围。读完一卷不等于该卷最后新接任务已经解决。人物数量为分卷观察材料数量，不是去重人数。

## 验证结果

- 正式库结构校验：{validation['vault']}。
- {validation['reading_unit_segments_exactly_once']}个原索引片段恰好映射一次；合章、重复章号及正文误识别段保留。
- {validation['checkpoint_partition_verified']}份检查点的完成/待完成集合无交叉、正文及序章无遗漏；个别既有检查点不计章前介绍，单独记入机器结果的checkpoint_nonbody_exclusions。
- 本批范围检查{validation['checked_local_links']}个本地Markdown链接，失效{len(validation['broken_local_links'])}个。
- 《贼胆》迁入9份原JSON/JSONL哈希一致；292张卡旧字段保留；2,039处原文链接映射正确，40处无行号文字标签已补精确行号。
- 数据级检查与证据范围检查不等于逐条文学解释已被用户认可。全库没有改成“已审阅”。

机器结果见[validation.json](validation.json)。备份与实际恢复的结果由归档结束后单独生成的 `backup-verification.json` 记录；备份排除原小说全文、可重建阅读视图与Git内部文件。恢复验证针对研究主档及其引用结构，不代表原文已随包备份。

## 仍待推进

《纵横天下》第{next_chapter}章起尚待继续，后两书依序推进；不能称三本全书已蒸馏完成。跨作者机制入口仅使用目前已有证据，不把后来作品未读内容写成风格演进结论。用户对研究的取舍与审美评价尚待填写。

本批失落叶研究与统一目录已保存在本地，本任务未执行Git提交或推送。另一个蜗牛双书任务已有它自己范围的Git同步记录，不将该结果扩张为本批全库已同步。未执行Space写入或记忆同步，也未安排后台任务。备份的最终回执在归档完成后写入，因此回执自身不在该归档内。
'''
(dest/'本批验收.md').write_text(text,encoding='utf-8')
print('wrote 本批验收.md and 迁移审查.md')
