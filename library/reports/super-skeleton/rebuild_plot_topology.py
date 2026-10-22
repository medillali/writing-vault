"""按真实关系生成多起点、分枝、共享交汇的全书图，不用集数构造父子树。"""
from pathlib import Path
from collections import Counter
import hashlib
import json
import math
import sys
sys.dont_write_bytecode = True
import rebuild_plot_images as p

HERE = Path(__file__).resolve().parent
OUT = HERE/'reading/plot/whole-book'
CORE = 'book-37dd82abc178'
TEAL, JUNCTION = '#147d8b', '#b86a23'
NW, HEADER, PAD = 366, 510, 90
ns = p.NODES
events = sorted((n for n in p.G['nodes'] if n['kind']=='event'), key=lambda n:n['narrative_order'])
threads = sorted((t for t in p.G['threads'] if t['id'].startswith('book-')),
                 key=lambda t:(min(ns[n]['narrative_order'] for n in t['node_ids']),t['id']))
ts = {t['id']:t for t in threads}
hidden = [t for t in threads if t['kind']=='hidden']
hno = {t['id']:i+1 for i,t in enumerate(hidden)}
core_nodes, core_edges = set(ts[CORE]['node_ids']), set(ts[CORE]['edge_ids'])
hidden_edges = {eid for t in hidden for eid in t['edge_ids']}
edges = list(p.G['edges'])
# 主题呼应仍展示并可点选，不用它代替剧情推进来决定层级。
structural = [e for e in edges if e['kind']!='echo']
# 同一对事件可以同时有因果和揭示；交汇路数按不同来路计，不重复数语义边。
pairs = {(e['from'],e['to']) for e in structural}
incoming, outgoing = Counter(b for a,b in pairs), Counter(a for a,b in pairs)
roots = [n['id'] for n in events if not incoming[n['id']]]
forks = [n['id'] for n in events if outgoing[n['id']]>1]
junctions = [n['id'] for n in events if incoming[n['id']]>1]
TIME_LABELS = {'v09-e05':'跨段聚合','v14-e04':'缺席期回叙','v14-e05':'缺席期补叙',
               'v14-e06':'缺席期回叙','v17-e05':'神史回叙'}


def size(n):
    if n['id'] in hno:
        return NW, 95+p.text_height(p.title(n),NW-40,26,True)+p.text_height(p.GAPS[n['tracking_key']],NW-40,23)
    return NW, 83+p.text_height(n['title'],NW-40,29,True)


def endpoint(t):
    return max(t['node_ids'],key=lambda nid:ns[nid]['narrative_order'])


def prepare():
    OUT.mkdir(parents=True,exist_ok=True)
    nodes=[]
    for n in events+hidden:
        w,h=size(n)
        nodes.append({'name':n['id'],'attributes':{'width':w/72,'height':h/72}})
    links=[]
    for e in edges:
        forward=ns[e['from']]['narrative_order']<ns[e['to']]['narrative_order']
        links.append({'tail':e['from'],'head':e['to'],'attributes':{
            'id':e['id'],'constraint':forward and e['kind']!='echo',
            'weight':6 if e['id'] in core_edges and e['kind']!='echo' else (3 if e['kind']=='cause' else 1)}})
    for t in hidden:
        links.append({'tail':endpoint(t),'head':t['id'],'attributes':{'id':'state-'+t['id'],'weight':2}})
    # 只约束大致阅读进度，避免第18集的独立起点浮到开篇附近。
    # 不画时间链，也不以这些隐形约束生成剧情关系。
    ranks={}
    for n in events:
        prev=[ranks[e['from']]+1 for e in structural if e['to']==n['id'] and e['from'] in ranks]
        ranks[n['id']]=max([(p.vol(n)-1)*3]+prev)
    for t in hidden:ranks[t['id']]=ranks[endpoint(t)]+1
    subgraphs=[]
    for level in range(max(ranks.values())+1):
        anchor=f'_rank{level}'
        nodes.append({'name':anchor,'attributes':{'shape':'point','width':0,'height':0,'style':'invis'}})
        subgraphs.append({'name':f'r{level}','graphAttributes':{'rank':'same'},
                          'nodes':[{'name':anchor}]+[{'name':nid} for nid,r in ranks.items() if r==level]})
        if level:links.append({'tail':f'_rank{level-1}','head':anchor,'attributes':{'id':f'_order{level}','style':'invis','weight':0}})
    model={'directed':True,'graphAttributes':{'rankdir':'TB','nodesep':'.8','ranksep':'1.05','splines':'spline','outputorder':'edgesfirst'},
           'nodeAttributes':{'shape':'box','fixedsize':True,'label':''},'nodes':nodes,'edges':links,'subgraphs':subgraphs}
    (OUT/'layout-input.json').write_text(json.dumps(model,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('布局输入：163个事件、265条原始关系、15个暗线状态注记。')


class Map(p.SVG):
    def group(self,**attrs):
        self.parts.append('<g '+' '.join(f'{k.replace("_","-")}="{p.esc(v)}"' for k,v in attrs.items())+'>')
    def end(self):self.parts.append('</g>')
    def tooltip(self,s):self.parts.append('<title>'+p.esc(s)+'</title>')


def bounds(ids,positions):
    boxes=[positions[i] for i in ids]
    x=min(b['x'] for b in boxes);y=min(b['y'] for b in boxes)
    return {'x':x-35,'y':y-35,'width':max(b['x']+b['width'] for b in boxes)-x+70,
            'height':max(b['y']+b['height'] for b in boxes)-y+70}


def render():
    layout=json.loads((OUT/'layout.json').read_text(encoding='utf-8'))
    _,_,gw,gh=map(float,layout['bb'].split(','))
    width,height=math.ceil(gw+2*PAD),math.ceil(gh+HEADER+140)
    positions={}
    for n in layout['objects']:
        if n['name'] not in ns and n['name'] not in hno:continue
        x,y=map(float,n['pos'].split(','));w=float(n['width'])*72;h=float(n['height'])*72
        positions[n['name']]={'x':round(x-w/2+PAD,2),'y':round(gh-y-h/2+HEADER,2),
                              'width':round(w,2),'height':round(h,2),
                              'volume':p.vol(ns[n['name']]) if n['name'] in ns else None}
    assert set(positions)=={n['id'] for n in events+hidden}
    s=Map(width)
    s.rect(0,0,width,16,p.BLUE,p.BLUE,0)
    s.text(80,48,'《超级骷髅兵》 · 剧情分枝与交汇',width-160,82,p.INK,True)
    s.text(80,162,'从黑龙主线出发，旁支另起，在同一件事上相交，再继续分枝。',width-160,39,p.MUTED)
    s.text(80,230,f'163个事件 / {len(roots)}个图内起点 / {len(forks)}个分枝点 / {len(junctions)}个交汇点 / 15条暗线终点复核',width-160,32,p.INK)
    legend=[(p.BLUE,'蓝色 · 自由存在与同伴主线'),(TEAL,'青色 · 其他剧情枝线'),(p.PURPLE,'紫色 · 暗线关系'),(JUNCTION,'金色节点标记 · 多路交汇')]
    for i,(c,label) in enumerate(legend):
        x=80+i*850;s.path(f'M {x} 328 H {x+90}',c,7);s.text(x+112,300,label,700,28,c,True)
    s.text(80,365,'实线为因果，虚线为铺垫、揭示、转折或回收，细点线为主题呼应；只有接入同一事件框才算交汇，线条穿过不算。',width-160,27,p.MUTED)
    s.text(80,416,'整体沿阅读进度向下展开，集数只是事件标记；回叙在获知位置保留。状态框是第18集复核注记，不是新增剧情。',width-160,27,p.MUTED)
    links_meta=[]
    for el in sorted((e for e in layout['edges'] if not e['id'].startswith('_order')),key=lambda el: (0 if el['id'] in p.EDGES and p.EDGES[el['id']]['kind']=='echo' else 1)):
        eid=el['id'];state=eid.startswith('state-');e=p.EDGES.get(eid)
        if state:
            t=ts[eid[6:]];color=p.STATE[t['status']][1];stroke=2.5;dash='5 9';opacity=.8
        else:
            color=p.BLUE if eid in core_edges else p.PURPLE if eid in hidden_edges else TEAL
            stroke=5 if eid in core_edges else 3
            dash='' if e['kind']=='cause' else '2 11' if e['kind']=='echo' else '11 8'
            opacity=.33 if e['kind']=='echo' else .85
        s.group(id=eid,data_kind='annotation' if state else 'edge',data_from=endpoint(t) if state else e['from'],
                data_to=t['id'] if state else e['to'],data_relation='state' if state else e['kind'],
                tabindex=0 if not state else -1,role='button' if not state else 'group',
                aria_label='暗线终点注记' if state else p.REL[e['kind']][0]+'：'+e['label'])
        for draw in el.get('_draw_',[]):
            if draw['op'] not in ('b','B'):continue
            points=[(round(x+PAD,2),round(gh-y+HEADER,2)) for x,y in draw['points']]
            d='M '+','.join(map(str,points[0]))+' C '+' '.join(','.join(map(str,pt)) for pt in points[1:])
            s.parts.append(f'<path d="{d}" stroke="transparent" stroke-width="18" fill="none" pointer-events="stroke"/>')
            s.path(d,color,stroke,dash,not state,opacity)
        if e:s.tooltip(p.REL[e['kind']][0]+' · '+p.CLAIM[e['claim_kind']]+'\n'+e['label']+'\n'+p.evidence(e))
        s.end()
        links_meta.append({'id':eid,'from':endpoint(t) if state else e['from'],'to':t['id'] if state else e['to'],
                           'kind':'annotation' if state else e['kind'],'core':eid in core_edges})
    for n in events:
        nid=n['id'];b=positions[nid];x,y,w,h=(b[k] for k in ('x','y','width','height'))
        memberships=[t['id'] for t in threads if nid in t['node_ids']]
        darks=[hno[t] for t in memberships if t in hno]
        color=p.BLUE if nid in core_nodes else TEAL
        s.group(id=nid,data_kind='event',data_volume=p.vol(n),data_threads=','.join(memberships),
                data_junction=str(nid in junctions).lower(),data_root=str(nid in roots).lower(),
                tabindex=0,role='button',aria_label=n['title'])
        s.rect(x,y,w,h,'#edf4ff' if nid in core_nodes else 'white',color,18)
        mark='起点' if nid in roots else ('交汇 '+str(incoming[nid])+'路' if nid in junctions else '分枝' if nid in forks else '')
        s.text(x+18,y+12,f'{p.vol(n):02d}集 · {nid}',w-140,18,color)
        if mark:
            fill='#fff0df' if nid in junctions else '#e9f4f4'
            s.rect(x+w-123,y+9,108,30,fill,fill,8)
            s.text(x+w-113,y+10,mark,96,18,JUNCTION if nid in junctions else color,True)
        end=s.text(x+20,y+49,n['title'],w-40,29,p.INK,True)
        suffix=TIME_LABELS.get(nid) or ('暗线 '+ ' / '.join(f'{i:02}' for i in darks) if darks else p.CLAIM[n['claim_kind']])
        assert end<=y+h-30,(nid,end,y+h)
        s.text(x+20,y+h-29,suffix,w-40,18,p.PURPLE if darks else p.MUTED)
        s.tooltip(n['summary']+'\n'+p.evidence(n));s.end()
    for t in hidden:
        b=positions[t['id']];x,y,w,h=(b[k] for k in ('x','y','width','height'))
        label,color,fill=p.STATE[t['status']]
        s.group(id=t['id'],data_kind='thread',data_thread=hno[t['id']],tabindex=0,role='button',aria_label=p.title(t))
        s.rect(x,y,w,h,fill,color,22)
        yy=s.text(x+20,y+12,f'暗线 {hno[t["id"]]:02d} · {label}',w-40,23,color,True)
        yy=s.text(x+20,yy+8,p.title(t),w-40,26,p.INK,True)
        yy=s.text(x+20,yy+10,p.GAPS[t['tracking_key']],w-40,23,color)
        s.text(x+20,y+h-29,'全书终点复核 · 点击查看问题范围',w-40,17,p.MUTED)
        assert yy<=y+h-29,(t['id'],yy,y+h)
        s.tooltip(t['question']+'\n'+p.conclusion(t));s.end()
    s.text(80,height-92,'研究草稿待审阅 · 全部事件与原始关系可回查 · 交汇依据已有推进关系，起点不推断为绝对无前因 · 原文事实与研究推断分开保存',width-160,27,p.MUTED)
    colors={p.BLUE,p.PURPLE,TEAL,p.GREEN,p.AMBER,p.RED}
    defs=''.join(f'<marker id="a{c[1:]}" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L6,3 L0,6 Z" fill="{c}"/></marker>' for c in sorted(colors))
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" aria-label="超级骷髅兵多起点剧情树"><title>超级骷髅兵：分枝与交汇</title><defs>{defs}</defs><rect width="100%" height="100%" fill="#f7f9fc"/><g font-family="Microsoft YaHei, Noto Sans CJK SC, sans-serif">'+''.join(s.parts)+'</g></svg>'
    (OUT/'tree.svg').write_text(svg,encoding='utf-8')
    meta={'version':2,'width':width,'height':height,'selection':'全事件分枝交汇版','source_id':p.SID,
          'graph_sha256':hashlib.sha256(p.GRAPH_PATH.read_bytes()).hexdigest(),
          'events':[n['id'] for n in events],'edges':[e['id'] for e in edges],'positions':positions,'links':links_meta,
          'threads':[{'id':t['id'],'number':hno[t['id']],'status':t['status'],'anchor':endpoint(t),'conclusion':p.conclusion(t)} for t in hidden],
          'roots':roots,'forks':forks,'junctions':junctions,'core':CORE,'time_labels':TIME_LABELS,
          'volume_bounds':{str(v):bounds([n['id'] for n in events if p.vol(n)==v],positions) for v in range(1,19)},
          'thread_bounds':{t['id']:bounds(t['node_ids'],positions) for t in threads},
          'layout':{'engine':layout['engine'],'version':layout['version'],'direction':'按关系自上而下分枝；无集数父子结构',
                    'echo':'显示但不决定层级','back_references':'保留原方向，不强制为向下推进'},
          'states':dict(Counter(t['status'] for t in hidden))}
    (OUT/'manifest.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    observers={'reader':'读者'}
    for path in (p.VAULT/'library/characters').glob('*.json'):
        card=json.loads(path.read_text(encoding='utf-8'));observers[card['asset_id']]=card['content'].get('name',card['title'])
    data={'meta':meta,'nodes':{n['id']:n for n in events},'threads':ts,'volumes':p.VOLUMES,'edges':p.EDGES,'observers':observers}
    raw=json.dumps(data,ensure_ascii=False).replace('<','\\u003c')
    template=(HERE/'whole_book_viewer.html').read_text(encoding='utf-8')
    (OUT/'index.html').write_text(template.replace('<!-- TREE_SVG -->',svg).replace('/* TREE_DATA */',raw),encoding='utf-8')
    write_readme(meta)
    print(json.dumps({k:meta[k] for k in ('width','height','states')}))


def write_readme(meta):
    (HERE/'reading/plot/whole-book.md').write_text(f'''# 全书剧情树：分枝与交汇

[返回图片目录](images.md) · [全部事件与证据](README.md)

**从主线出发，支线可另起，在共享事件处汇合，再向后分枝。** 包含全书163个事件、265条已有关系、15条暗线终点复核；不再按集数排列成链式目录。

[完整PNG图片](whole-book/tree.png) · [SVG无损放大](whole-book/tree.svg) · [离线缩放页面](whole-book/index.html)

![多起点分枝与交汇总图](whole-book/tree-preview.png)

预览用于看形态；文字请打开原图放大。下载 `whole-book/index.html` 后用浏览器打开，可拖动、缩放、搜索，聚焦主线、任一支线、交汇点或未回收问题，点击事件和连线查看摘要与证据。页面自带所有内容，不需要网络；GitHub不运行仓库中的HTML。

- **蓝色**突出“自由存在与同伴关系”核心主线；青色为其他剧情关系；紫色为暗线关系。核心主线与暗线重合时优先蓝色，事件内保留暗线编号。
- **同一事件只画一次**。多条推进关系接入同一事件框，才标为交汇；线条交叉不表示剧情相交。全图有{len(meta['roots'])}个图内起点、{len(meta['forks'])}个分枝点、{len(meta['junctions'])}个交汇点。
- **实线**为因果，虚线为铺垫、揭示、转折或回收，细点线为主题呼应。265条关系均保留原方向和判断性质；点击连线可看类型。呼应与两条后置解释不强制决定向下层级。
- **集数只作位置提示**，不是父子层级。同一高度不表示同一天；回叙仍注明。图内起点不等于故事世界中绝对没有前因。
- **暗线状态贴在对应枝端**：1条已回收、11条部分回收、3条未回收。连接状态框的细虚线是注记；状态统一取第18集复核，不能将回收范围扩大到全部人物去向。

![放大示例：旁支接入共同事件](whole-book/tree-junction-preview.png)

原有49张分图继续保留供逐集、逐线查阅。源研究JSON、个人笔记和版本历史没有因这次布局改变。

重建：`rebuild_whole_book.py --prepare` → `layout_whole_book.cjs` → `rebuild_whole_book.py` → `render_whole_book.cjs`。布局使用 [Viz.js / Graphviz](https://viz-js.com/api/)，需要 `@viz-js/viz`（本次3.31.0）、Python/Pillow、中文字体和Node.js/Playwright。`VIZ_MODULE`可指定本地模块路径。布局输入、坐标与源图哈希见[清单](whole-book/manifest.json)。
''',encoding='utf-8')


if __name__=='__main__':
    prepare() if '--prepare' in sys.argv else render()
