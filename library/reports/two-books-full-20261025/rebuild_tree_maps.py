"""重建分枝交汇树与离线地图；展示拓扑不反写来源图、卡片或用户评价。"""
from pathlib import Path
from collections import Counter
import base64, hashlib, io, json, math, os, re, shutil, subprocess, sys
from PIL import Image
import tree_topology as tree
HERE=Path(__file__).resolve().parent
VAULT=HERE.parents[2]
REFERENCE=VAULT/'library/reports/super-skeleton'
NODE=Path.home()/'.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe'
MODULES=NODE.parent.parent/'node_modules'
BOOKS={'zeidan':('贼胆','z'),'leveling':('网游之练级专家','l')}
def sha(raw):return hashlib.sha256(raw).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def write(p,text):p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(text.encode('utf-8'))
def dump(p,value):write(p,json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def run_node(script,*args):
    subprocess.run([str(NODE),str(HERE/script),*map(str,args)],env={**os.environ,'NODE_PATH':str(MODULES)},check=True)
def build_model(folder):
    title,key=BOOKS[folder];D=HERE/folder
    g=read(D/'plot/graph.json');curated=read(D/'plot/curated-topology.json');source=read(HERE/'sources.json')[key]
    assert curated['source_id']==source['source_id']
    stages=sorted((n for n in g['nodes'] if n['kind']=='arc'),key=lambda n:n['narrative_order'])
    nodes=sorted((dict(n) for n in g['nodes'] if n['kind']=='scene'),key=lambda n:n['narrative_order'])
    ns={n['id']:n for n in nodes};counts=Counter()
    for n in nodes:
        stage=int(n['parent_id'].split('-')[-1]);counts[stage]+=1
        n.update(kind='event',source_node_id=n['id'],stage_number=stage,label_id=f'S{stage:02d}-E{counts[stage]:02d}')
    core=curated['core_event_ids'];assert len(core)==len(set(core)) and set(core)<=set(ns)
    assert core==sorted(core,key=lambda nid:ns[nid]['narrative_order'])
    chapters=source.get('all_chapters',source['units'])
    bounds=chapters if isinstance(chapters,dict) else {x.get('id',x.get('chapter_id',x.get('unit_id'))):x for x in chapters}
    def proof(items):
        assert items,'语义关系与暗线必须保留证据'
        result=[]
        for item in items:
            e={**item,'source_id':source['source_id'],'revision':source['revision'],'claim_kind':'inference'}
            assert e['chapter_id'] in bounds, e
            b=bounds[e['chapter_id']]
            assert b['start_line']<=e['start_line']<=e['end_line']<=b['end_line'],(e,b)
            result.append(e)
        return result
    edges=[];signatures=set()
    for item in curated['links']:
        assert item['from'] in ns and item['to'] in ns and item['from']!=item['to']
        assert item['kind'] in ('cause','setup','reveal','reversal','payoff','echo','misdirection')
        signature=(item['from'],item['to'],item['kind'],item['label']);assert signature not in signatures;signatures.add(signature)
        edges.append({**item,'id':'view-'+sha('|'.join(signature).encode())[:16],'claim_kind':'inference','evidence':proof(item['evidence'])})
    for a,b in zip(core,core[1:]):
        edges.append({'id':'read-'+sha((a+b).encode())[:16],'from':a,'to':b,'kind':'sequence','claim_kind':'reading_order','label':'主干阅读衔接：按首次获知位置组织，不代表因果，也不计入分枝或交汇。','evidence':[]})
    threads=[]
    for item in curated['threads']:
        t=dict(item);assert t['id'].startswith('book-') and t['id']!='book-main'
        assert len(t['node_ids'])>=2 and set(t['node_ids'])<=set(ns)
        t['node_ids']=sorted(set(t['node_ids']),key=lambda nid:ns[nid]['narrative_order'])
        t.update(edge_ids=[e['id'] for e in edges if e['kind']!='sequence' and e['from'] in t['node_ids'] and e['to'] in t['node_ids']],resolution_note=t['conclusion'],tracking_key=t['id'],evidence=proof(t['evidence']))
        threads.append(t)
    assert set(ns)<=set(core)|{nid for t in threads for nid in t['node_ids']},'有场景未归入整书线'
    main={'id':'book-main','title':curated['core_title'],'kind':'main','status':'resolved','node_ids':core,'edge_ids':[e['id'] for e in edges if e['from'] in core and e['to'] in core],
          'question':'主角的处境、能力与核心目标如何沿全书改变？','resolution_note':'蓝色突出核心成长进程；细点线只表示阅读衔接，具体因果及终局边界以各事件和暗线证据为准。','evidence':[]}
    model={'schema_version':1,'title':title,'source_id':source['source_id'],'source_revision':source['revision'],
           'source_graph_sha256':sha((D/'plot/graph.json').read_bytes()),'curation_sha256':sha((D/'plot/curated-topology.json').read_bytes()),
           'claim_kind':'inference','core_title':curated['core_title'],'nodes':nodes,'stages':stages,'edges':edges,'threads':[main,*threads],
           'boundary':'派生展示拓扑；来源图保持原样。研究阶段不是原著卷结构，阅读衔接不是因果。'}
    dump(D/'plot/topology.json',model)
    return model
def make_map(folder,model):
    D=HERE/folder;out=D/'plot/whole-book';target=D/'plot/map';meta=read(out/'manifest.json')
    Image.MAX_IMAGE_PIXELS=400_000_000
    raw=(out/'tree.png').read_bytes();im=Image.open(io.BytesIO(raw)).convert('RGB');width,height=im.size
    assert (width,height)==(meta['width'],meta['height'])
    hi=math.ceil(math.log2(max(width,height)));lo=hi-math.ceil(math.log2(max(width,height)/512));tiles={};checks=[]
    for level in range(lo,hi+1):
        factor=2**(hi-level);size=(math.ceil(width/factor),math.ceil(height/factor));scaled=im if level==hi else im.resize(size,Image.Resampling.LANCZOS)
        for x in range(math.ceil(size[0]/512)):
            for y in range(math.ceil(size[1]/512)):
                rect=(max(0,x*512-1),max(0,y*512-1),min(size[0],(x+1)*512+1),min(size[1],(y+1)*512+1))
                tile=scaled.crop(rect);buf=io.BytesIO();tile.save(buf,format='WEBP',lossless=True,method=4);payload=buf.getvalue()
                assert Image.open(io.BytesIO(payload)).convert('RGB').tobytes()==tile.tobytes()
                name=f'{level}/{x}/{y}';tiles[name]='data:image/webp;base64,'+base64.b64encode(payload).decode()
                checks.append({'key':name,'size':tile.size,'rect':rect,'sha256':sha(payload),'pixel_match':True})
    positions=meta['positions'];volumes=[]
    for stage in range(1,len(model['stages'])+1):
        first=next(n for n in model['nodes'] if n['stage_number']==stage)
        volumes.append({'number':stage,'event':first['id'],**positions[first['id']]})
    start=next(n for n in model['nodes'] if n['id'] in model['threads'][0]['node_ids'])
    data={'width':width,'height':height,'tile_size':512,'overlap':1,'min_level':lo,'max_level':hi,'tiles':tiles,'start':positions[start['id']],'volumes':volumes,
          'source_sha256':sha(raw),'svg':(out/'tree.svg').read_text(encoding='utf-8'),'png':'data:image/png;base64,'+base64.b64encode(raw).decode()}
    CODE=REFERENCE/'map';title=model['title']
    engine=re.sub(r'//# sourceMappingURL=.*','',(CODE/'vendor/openseadragon.min.js').read_text(encoding='utf-8'))
    engine='/* OpenSeadragon license\n'+(CODE/'vendor/LICENSE.txt').read_text(encoding='utf-8')+'\n*/\n'+engine
    template=(CODE/'template.html').read_text(encoding='utf-8').replace('超级骷髅兵',title).replace('定位到集数','定位到研究阶段').replace('定位到某一集','定位到研究阶段')
    template=template.replace('https://github.com/medillali/writing-vault/blob/main/library/reports/super-skeleton/reading/plot/map.md',f'https://github.com/medillali/writing-vault/blob/main/library/reports/two-books-full-20261025/{folder}/plot/README.md').replace('卡片与事件详情','树状图与事件证据')
    app=(CODE/'app.js').read_text(encoding='utf-8').replace('超级骷髅兵',title).replace("'第'+v.number+'集'","'第'+v.number+'研究阶段'")
    # 全图后立即点击可读大小，也必须定位开篇，不能沿用动画中途的旧中心。
    app=app.replace('viewer.viewport.goHome()','viewer.viewport.goHome(true)')
    for k,v in {'STYLE':(CODE/'style.css').read_text(encoding='utf-8'),'APP':app,'ENGINE':engine,'DATA':json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')}.items():template=template.replace(f'/* MAP_{k} */',v)
    write(target/'index.html',template);shutil.copyfile(out/'index.html',target/'cards.html')
    dump(target/'manifest.json',{'engine':'OpenSeadragon 6.1.1','tile_format':'WebP lossless','tiles':checks,'tile_count':len(checks),'full_resolution_tiles':sum(int(t['key'].split('/')[0])==hi for t in checks),
         'source_png_sha256':sha(raw),'source_svg_sha256':sha((out/'tree.svg').read_bytes()),'html_sha256':sha(template.encode()),'html_bytes':len(template.encode()),'pixel_verification':'全部图块逐片解码，与对应PNG层级矩形像素完全一致',
         'reference_template_sha256':sha((CODE/'template.html').read_bytes())})
    write(D/'plot/README.md',f'''# 《{title}》全书剧情树与地图

[打开可缩放地图](map/index.html) · [打开树状图与事件证据](whole-book/index.html) · [完整PNG](whole-book/tree.png) · [矢量SVG](whole-book/tree.svg)

![全书分枝与交汇](whole-book/tree-preview.png)

沿用《超级骷髅兵》的树状分枝与整图缩放形式：蓝色为核心主线，青色为旁枝，紫色为暗线，金色标记共享事件的交汇。同一事件只画一次；阶段只用于定位，不作为剧情父节点。

保留全书精选的{len(model['nodes'])}个场景；{meta['semantic_relations']}条推进语义关系与{meta['reading_links']}条主干阅读衔接分开。实线为因果，虚线为铺垫、揭示、转折或回收；蓝色细点线仅表示阅读顺序，不计入分枝或交汇。

全图有{len(meta['forks'])}个分枝点、{len(meta['junctions'])}个交汇点、{len(meta['threads'])}条暗线终态注记。点击事件、连线或剧情线可查看研究判断与章节行号；终局没有交代的结果仍标为未明。

地图可离线拖动、滚轮或双指缩放、小地图跳转、研究阶段定位、记住位置、下载PNG/SVG。浏览器直接打开HTML；GitHub网页展示下方图片与索引。

| 开篇分枝 | 共享交汇 |
|---|---|
| ![](map/opening.png) | ![](map/junction.png) |
| 中后段转折 | 终局边界 |
| ![](map/turning.png) | ![](map/ending.png) |

以上局部均截自同一张全图，不重新排版。完整逐章覆盖见[章节笔记](../chapter-notes.md)，结局边界见[终局核对](../ending-audit.md)。

展示拓扑是可审阅的研究解释：[人工核对配置](curated-topology.json)、[派生拓扑](topology.json)、[原研究图](graph.json)、[布局与身份清单](whole-book/manifest.json)。原来源图与卡片不因版式改变。
''')
def main():
    sys.stdout.reconfigure(encoding='utf-8')
    selected=[a for a in sys.argv[1:] if a in BOOKS] or list(BOOKS)
    models={f:build_model(f) for f in selected}
    for folder in selected:
        tree.configure(folder);tree.prepare();run_node('layout_tree.cjs',folder);tree.render()
    run_node('render_full.cjs',HERE,'svg',*selected)
    for folder in selected:make_map(folder,models[folder])
    run_node('render_full.cjs',HERE,'views',*selected)
if __name__=='__main__':main()
