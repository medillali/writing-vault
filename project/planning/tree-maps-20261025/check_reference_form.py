"""验收用户指定的分枝交汇形式，而非仅验收图片能否打开。"""
from pathlib import Path
from collections import Counter
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
root=Path(sys.argv[1])/'library/reports/two-books-full-20261025'
for book in ('zeidan','leveling'):
    folder=root/book
    source=json.loads((folder/'plot/graph.json').read_text(encoding='utf-8'))
    meta=json.loads((folder/'plot/whole-book/manifest.json').read_text(encoding='utf-8'))
    assert meta.get('layout',{}).get('engine')=='Graphviz dot', '旧图仍是研究阶段卡片网格，尚未采用参考图的关系布局'
    scenes={n['id'] for n in source['nodes'] if n['kind']=='scene'}
    assert set(meta['events'])==scenes, '场景必须全部保留且同一事件只画一次'
    assert len(meta['events'])==len(set(meta['events']))
    assert not any(n.startswith('stage-') or n=='story' for n in meta['positions']), '阶段目录不能充当剧情父节点'
    assert meta['forks'] and meta['junctions'] and meta['threads'], '需要真实分枝、共享交汇及暗线终态'
    model=json.loads((folder/'plot/topology.json').read_text(encoding='utf-8'))
    edges=model['edges']; pairs={(e['from'],e['to']) for e in edges if e['kind'] not in ('echo','sequence')}
    incoming=Counter(b for a,b in pairs); outgoing=Counter(a for a,b in pairs)
    assert set(meta['forks'])=={n for n in scenes if outgoing[n]>1}
    assert set(meta['junctions'])=={n for n in scenes if incoming[n]>1}, '阅读衔接线不能虚增交汇'
    assert all(e.get('evidence') for e in edges if e['kind']!='sequence')
    assert all(t['anchor'] in scenes and t['conclusion'] for t in meta['threads'])
    assert meta['reference']['book']=='超级骷髅兵'
    print(book, '形式与身份验收通过',len(scenes),'事件',len(meta['forks']),'分枝',len(meta['junctions']),'交汇')
