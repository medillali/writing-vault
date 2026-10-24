"""验收用户指定的分枝交汇形式，而非仅验收图片能否打开。"""
from pathlib import Path
from collections import Counter
import json, sys, hashlib
sys.stdout.reconfigure(encoding='utf-8')
root=(Path(sys.argv[1])/'library/reports/two-books-full-20261025') if len(sys.argv)>1 else Path(__file__).resolve().parent
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
    by_id={n['id']:n for n in model['nodes']}
    for node in source['nodes']:
        if node['kind']!='scene':continue
        assert by_id[node['id']]['source_node_id']==node['id']
        assert all(by_id[node['id']][k]==v for k,v in node.items() if k!='kind'), '原场景的身份、摘要、机制或来源发生变化'
    edges=model['edges']; pairs={(e['from'],e['to']) for e in edges if e['kind'] not in ('echo','sequence')}
    incoming=Counter(b for a,b in pairs); outgoing=Counter(a for a,b in pairs)
    assert set(meta['forks'])=={n for n in scenes if outgoing[n]>1}
    assert set(meta['junctions'])=={n for n in scenes if incoming[n]>1}, '阅读衔接线不能虚增交汇'
    assert all(e.get('evidence') for e in edges if e['kind']!='sequence')
    assert all(t['anchor'] in scenes and t['conclusion'] for t in meta['threads'])
    assert meta['reference']['book']=='超级骷髅兵'
    print(book, '形式与身份验收通过',len(scenes),'事件',len(meta['forks']),'分枝',len(meta['junctions']),'交汇')

    def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
    assert meta['graph_sha256']==sha(folder/'plot/graph.json')
    mm=json.loads((folder/'plot/map/manifest.json').read_text(encoding='utf-8'))
    assert mm['source_png_sha256']==sha(folder/'plot/whole-book/tree.png')
    assert mm['source_svg_sha256']==sha(folder/'plot/whole-book/tree.svg')
    assert mm['html_sha256']==sha(folder/'plot/map/index.html')
    assert all(t['pixel_match'] for t in mm['tiles'])
    assert (folder/'plot/map/cards.html').read_bytes()==(folder/'plot/whole-book/index.html').read_bytes()
    from PIL import Image
    Image.MAX_IMAGE_PIXELS=400_000_000
    previews=json.loads((folder/'plot/map/previews.json').read_text(encoding='utf-8'))
    with Image.open(folder/'plot/whole-book/tree.png') as image:
        for c in previews['crops']:
            rect=(c['left'],c['top'],c['left']+c['width'],c['top']+c['height'])
            with Image.open(folder/('plot/map/'+c['name']+'.png')) as crop:
                assert crop.convert('RGB').tobytes()==image.crop(rect).convert('RGB').tobytes(),'局部预览必须裁自同一全图'
    geometry=json.loads((folder/'validation/diagram-layout.json').read_text(encoding='utf-8'))
    assert all(not geometry[k] for k in ('overflow','overlaps','pierced','outsideCards'))
    browser=json.loads((folder/'validation/browser.json').read_text(encoding='utf-8'))
    assert browser['valid'] and browser['javascript_errors']==0 and browser['offline_external_requests']==0
    assert browser['widths']==[360,390,768,1280,1600]
    print(book,'图像哈希、瓦片、同图入口和离线交互回执一致')
