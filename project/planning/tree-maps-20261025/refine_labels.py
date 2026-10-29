from pathlib import Path
import json,shutil
O=Path('.verify/tree-maps-20261025/library/reports/two-books-full-20261025')
notes={
'book-scar':'伤痕仅有自述与怀疑；飞刀技艺确证，师承细节及伤口解释仍未明。',
'book-aode-child':'解咒任务已完成；沃卡德复生、童灵与黑幽灵关系仍未明。',
'book-old-man':'老者身份及本命任务已确认；称名冲突、方盒与本命实体仍未明。',
'book-nightmare-space':'救援、索德牺牲与双门用途已兑现；全地图清尽与称名差异另计。',
'book-mine-necklace':'多方证词改写矿洞悲剧；首赠项链失而复得，长期记忆得到回应。',
'book-snail-candy':'标记计被反用，合作击杀兑现；糖果由争到合，真约战另有终局证据。',
'book-phoenix':'救援和复活确有实用；次数冲突、最终库存及保留末次的用途未明。',
'book-soul-ring':'只证实解开第一封；后续封印、人物身份与双戒纸解释仍未明。',
'book-shadowsand':'游戏追击告终，现实雇佣背景揭开；组织覆灭或现实受惩未获确证。',
'book-double-spy':'揭一人留一人传递假情报，围狂龙后逐天骑；圣剑是后续独立博弈。',
'book-taburet-oslinlan':'铭文重释旧情，诅咒与宽恕得到说明；终局亲见两人幸福相拥。',
'book-kamori-retrial':'归还头颅恢复证言，互证栽赃、惩凶并改史；战马承接临终托付。',
'book-demon-ring-politics':'夺舍解除、四附件成戒并升神器；七遗物钥匙传说及局部冲突另计。',
'book-arland-father':'后文明确认父，并安排现实重逢；不倒填早期心理或任意改规则。',
}
for f in ('zeidan','leveling'):
 p=O/f/'plot/curated-topology.json';d=json.loads(p.read_text(encoding='utf-8'))
 for t in d['threads']:
  if t['kind']=='hidden':t['display_note']=notes[t['id']]
 p.write_bytes((json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
shutil.copyfile('.planning/tree-maps-20261025/leveling-topology-审阅.md',O/'leveling/plot/拓扑审阅.md')
p=O/'tree_topology.py';s=p.read_text(encoding='utf-8').replace("p.GAPS={t['id']:t['resolution_note'] for t in data['threads']}","p.GAPS={t['id']:t.get('display_note',t['resolution_note']) for t in data['threads']}")
s=s.replace("'semantic_relations':len(structural)","'semantic_edges_total':sum(e['kind']!='sequence' for e in edges),'echo_relations':sum(e['kind']=='echo' for e in edges),'semantic_relations':len(structural)")
p.write_bytes(s.encode('utf-8'))
for f in ('zeidan','leveling'):
 p=O/f/'README.md';s=p.read_text(encoding='utf-8').replace('[剧情阅读器](plot/relations/index.html)','[分枝交汇树与证据](plot/whole-book/index.html)')
 p.write_bytes(s.encode('utf-8'))
p=O/'rebuild-full.py';s=p.read_text(encoding='utf-8').replace('plot/relations/index.html','plot/whole-book/index.html');p.write_bytes(s.encode('utf-8'))
print('终态框使用短注；完整结论和证据仍保留在侧栏。')
