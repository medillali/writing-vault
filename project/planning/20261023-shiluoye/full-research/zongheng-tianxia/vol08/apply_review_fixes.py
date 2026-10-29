"""主代理文学审阅修订；不改原文与其他卷。"""
import json
from pathlib import Path
R=Path(__file__).parent
p=R/'build_artifacts.py';s=p.read_text(encoding='utf-8')
s=s.replace("question='灵儿身世/封印是否全回收？',status='unknown',answer='本卷末无明确总清，需前卷特别五六七交叉核，勿以陪伴结尾代替身世结案。'", "question='灵儿母史是否明述终结？',status='unknown',answer='第三封印前卷已解（卷七研究raw0922），本卷不再追加封印；未知仅指母史总清未在末卷明述，待前卷正式核，不称余封印未收。'")
p.write_text(s,encoding='utf-8')
p=R/'handoff.md';s=p.read_text(encoding='utf-8')
s=s.replace('raw1092干呕的怀孕玩笑当场解释慢性咽炎，不能做怀孕伏笔。','raw1092干呕由秦本人解释为慢性咽炎，恐孕为月的玩笑及主的担心；未见怀孕确证，也不能用人物解释当医学排除。')
s=s.replace('灵儿：末继续陪主，问爱冰兰。其身世/母印剩余封印是否全书已回收，本卷末未明总清；待主代理将卷五六七正式产物纳入审计，不以本卷不再提及断言全书遗漏。','灵儿：末继续陪主，问爱冰兰。第三封印在前卷已解（卷七既有研究raw0922），本卷不再追加封印；母史是否明述终结须前卷正式研究核，不把母史与已闭的三封印链混为一个问题。')
p.write_text(s,encoding='utf-8')
p=R/'report.md';s=p.read_text(encoding='utf-8').replace('灵儿剩余封印和母史全书是否总清','灵儿第三封印前卷已解，本卷未再明述的母史是否总清')
p.write_text(s,encoding='utf-8')
# 更正本阅读者原笔记与对应追加批次的过强排孕解释；保存阅读事实而非删读。
p=R/'chapter-notes.jsonl'
ns=[json.loads(x) for x in p.read_text(encoding='utf-8').splitlines()]
for n in ns:
 if n['chapter_id']=='ch-1092':
  n['facts']=[x.replace('韵当场说明慢性咽炎，非怀孕。','韵当场以慢性咽炎解释，未见怀孕确证或医学排除。') for x in n['facts']]
  n['state_changes']=[x.replace('秦韵非怀孕。','恐孕是人物话题，未见怀孕确证。') for x in n['state_changes']]
  fix='主代理审阅后回读L118992—119002：干呕由秦本人归于慢性咽炎，月以孕开玩笑、主担心；未见检测，不能把解释写成客观非孕确证。'
  if fix not in n['inferences']:n['inferences'].append(fix)
p.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in ns),encoding='utf-8')
for p in R.glob('batch-*.json'):
 a=json.loads(p.read_text(encoding='utf-8'));changed=False
 for n in a:
  if n.get('index')==1092:
   n['facts']=[x.replace('韵当场说明慢性咽炎，非怀孕。','韵当场以慢性咽炎解释，未见怀孕确证或医学排除。') for x in n['facts']]
   n['state_changes']=[x.replace('秦韵非怀孕。','恐孕是人物话题，未见怀孕确证。') for x in n['state_changes']]
   fix='主代理审阅后回读：干呕由秦本人解释为慢性咽炎，未见检测，不能确认医学排孕。'
   if fix not in n['inferences']:n['inferences'].append(fix)
   changed=True
 if changed:p.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
