"""即时纠正手写笔记中的重复榜单草稿词，不改变原文/覆盖。"""
from pathlib import Path
P=Path(__file__).parent
before='前十主东方法叶林花问慕简舞（按原顺主东方法应原列表为主/苍月/方/叶/苍瞳/花/问/慕/简/舞）'
after='前十依次逍遥自在/苍月/方歌阙/叶来/苍瞳/花枪一壶酒/问剑/慕萱/简简单单/林小舞'
for name in ('batch015.json','chapter-notes.jsonl'):
    p=P/name;t=p.read_text(encoding='utf-8');assert t.count(before)==1;p.write_text(t.replace(before,after),encoding='utf-8')
print('0807 rank transcription repaired; coverage unchanged')
