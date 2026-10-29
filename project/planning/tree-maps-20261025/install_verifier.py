from pathlib import Path
p=Path('.planning/tree-maps-20261025/check_reference_form.py');s=p.read_text(encoding='utf-8')
s=s.replace("root=Path(sys.argv[1])/'library/reports/two-books-full-20261025'","root=(Path(sys.argv[1])/'library/reports/two-books-full-20261025') if len(sys.argv)>1 else Path(__file__).resolve().parent")
s=s.replace('import json, sys','import json, sys, hashlib')
s += '''
    def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
    assert meta['graph_sha256']==sha(folder/'plot/graph.json')
    mm=json.loads((folder/'plot/map/manifest.json').read_text(encoding='utf-8'))
    assert mm['source_png_sha256']==sha(folder/'plot/whole-book/tree.png')
    assert mm['source_svg_sha256']==sha(folder/'plot/whole-book/tree.svg')
    assert mm['html_sha256']==sha(folder/'plot/map/index.html')
    assert all(t['pixel_match'] for t in mm['tiles'])
    assert (folder/'plot/map/cards.html').read_bytes()==(folder/'plot/whole-book/index.html').read_bytes()
    geometry=json.loads((folder/'validation/diagram-layout.json').read_text(encoding='utf-8'))
    assert all(not geometry[k] for k in ('overflow','overlaps','pierced','outsideCards'))
    browser=json.loads((folder/'validation/browser.json').read_text(encoding='utf-8'))
    assert browser['valid'] and browser['javascript_errors']==0 and browser['offline_external_requests']==0
    assert browser['widths']==[360,390,768,1280,1600]
    print(book,'图像哈希、瓦片、同图入口和离线交互回执一致')
'''
Path('.verify/tree-maps-20261025/library/reports/two-books-full-20261025/verify_tree_maps.py').write_bytes(s.encode('utf-8'))
