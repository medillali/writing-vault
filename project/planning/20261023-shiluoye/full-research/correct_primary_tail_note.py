"""纠正主代理自己的误记，不改小说或其他阅读者笔记。"""
from pathlib import Path
root=Path(__file__).resolve().parent/'zongheng-tianxia/vol07-primary-tail'
old='敌狂战称手提长枪后写长剑等称谓细节不补统一武器史。'
new='敌狂战武器用一杆长剑的量词异常，未出现先持枪再换剑的明确过程，不造武器矛盾。'
for name in ['batch-0967-0968.json','chapter-notes.jsonl']:
    p=root/name;s=p.read_text(encoding='utf-8');assert s.count(old)==1
    p.write_text(s.replace(old,new),encoding='utf-8')
print('primary manual note corrected in batch and ledger')
