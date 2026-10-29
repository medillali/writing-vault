"""把已主审的跨书比较接到正式综合与阶段证据，保用户取舍空白。"""
from pathlib import Path
import hashlib,json,re
B=Path(__file__).resolve().parent;R=B.parents[2];C=R/'writing-vault/library/reports/collection'
draft=B/'cross-book-comparison-draft.md';text=draft.read_text(encoding='utf-8')
text=text.replace('# 五部完整研究的写作问题比较草稿','# 五部小说的写作机制比较',1)
first=text.split('\n\n')[1]
text=text.replace(first,'本比较采用《纵横天下》《天下无双》《斩龙》的已主审全书九维综合，以及既有《贼胆》《练级专家》全书成果。《斩龙》人物全弧和整书最终验收仍在进行；比较只证明所列机制及其证据范围，不代替整书验收。蜗牛两书没有追认为本轮重新阅读。《超级骷髅兵》保留为既有标准与独立来源，不并入两位作者的风格演进论证。',1)
zl=json.loads((R/'writing-vault/library/reports/zhanlong/book-synthesis.json').read_text(encoding='utf-8'))
ids={row['id'] for rows in zl['dimensions'].values() for row in rows}
pairs=[['worldbuilding-01','continuity-01'],['worldbuilding-02','worldbuilding-03'],['characters-02','dialogue-02'],['characters-01','themes-01'],['characters-04','dialogue-03'],['plot-01','continuity-02'],['plot-03','worldbuilding-01'],['narrative-01','narrative-02','continuity-03']]
snail=['回报开启新的前置条件','个人自由由组织条款塑形','专业价值按任务验证','关系通过有成本的行动改变','先谈收益归属再兑现回报','目标成功与战斗胜负分别结算','把猜想写成有边界的试验','结局的交叉叙述：不能用一本补写另一本']
comp=R/'writing-vault/library/reports/two-books-full-20261025/COMPARISON.md';st=comp.read_text(encoding='utf-8')
scenes=[1,6,3,2,6,6,3,6]
sections=re.split(r'(?=^## [1-8]\. )',text,flags=re.M)
assert len(sections)==9
for n,part in enumerate(sections[1:],1):
    if n==8:part=part.split('## 使用与发布边界')[0].rstrip()+'\n'
    target_ids=['zhanlong-book-'+s for s in pairs[n-1]];assert set(target_ids)<=ids
    assert '## '+snail[n-1] in st
    anchor=snail[n-1].replace('：','').replace(' ','-')
    v=scenes[n-1];scene=R/f'writing-vault/library/reports/zhanlong/reading/plot/vol{v:02d}.md';assert scene.is_file()
    part+='\n核验入口：[纵横全书综合](../zongheng-tianxia/book-synthesis.md) · [无双全书综合](../tianxia-wushuang/book-synthesis.md) · [斩龙全书综合](../zhanlong/book-synthesis.md)（'+ '、'.join('`'+x+'`' for x in target_ids)+'） · [斩龙相关阶段场景](../zhanlong/reading/plot/vol'+f'{v:02d}'+'.md) · [蜗牛双书对应机制](../two-books-full-20261025/COMPARISON.md#'+anchor+')。\n'
    sections[n]=part
text=''.join(sections)
text+='''
## 怎样用于自己的书

先选一个当前要解决的问题，打开综合中的观察ID，再沿上游卷号、人物或场景核对source_id与章节行号。为自己的作品另写人物目标、资源和代价；保留的是可检验的因果关系，不搬用原作专名、关系组合和桥段。

| 层次 | 当前内容 | 后续记录位置 |
|---|---|---|
| 原作事实 | 各书来源、章节行号与阶段状态；同名人物仍按来源分开 | 原卡及逐章记录，纠正用独立优先层 |
| 研究解释 | 本文八类写作问题、机制、适用与失效条件 | 综合与比较报告，允许反证和修订 |
| 用户取舍 | 尚未填写，不自动把有效机制变成用户喜好 | 卡片用户笔记和试写反馈 |
| 原创方案 | 上述改造方向是候选，没有导入原创正典 | 用户自己的项目、试写与版本记录 |

[八来源统一目录](README.md) · [按问题检索机制](机制索引.md) · [蜗牛两书的来源与结局边界](../two-books-full-20261025/COMPARISON.md) · [超级骷髅兵独立研究](../super-skeleton/README.md)
'''
dest=C/'写作机制比较.md';assert not dest.exists()
dest.write_text(text,encoding='utf-8')
report=dict(status='cross-book-mechanism-comparison-published-for-research',comparisons=8,source_books=5,zhanlong_full_book_acceptance=False,user_taste_approved=False,draft_sha256=hashlib.sha256(draft.read_bytes()).hexdigest(),published_sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),source_synthesis_sha256=hashlib.sha256((R/'writing-vault/library/reports/zhanlong/book-synthesis.json').read_bytes()).hexdigest(),limits='正式来源支持机制比较；斩龙人物全弧/整书最终验收及全项目备份恢复仍另验。')
(C/'cross-book-comparison-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
