"""一次性移植既有参考图的绘制层，产出可独立维护的参数化生成器。"""
from pathlib import Path
import re
ROOT=Path('.verify/tree-maps-20261025/library/reports')
REF=ROOT/'super-skeleton'; OUT=ROOT/'two-books-full-20261025'
def write(name,text):
    (OUT/name).write_bytes(text.encode('utf-8'))
raw=(REF/'rebuild_plot_images.py').read_text(encoding='utf-8')
style='''"""沿用《超级骷髅兵》的字体测量、配色和SVG卡片规范；不读取其小说数据。"""\nfrom pathlib import Path\nfrom functools import lru_cache\nimport html, math, re\n'''+raw[raw.index("INK, MUTED, BLUE"):raw.index('SHORT =')]+raw[raw.index('def esc('):raw.index('    def header(')]
style+= '''\nSTATE.update({'unknown':('原文未明',AMBER,'#fff3dc'),'abandoned':('明确中断',RED,'#fcecef')})
REL['sequence']=('阅读衔接',BLUE)
CLAIM['reading_order']='阅读顺序，非因果'
def title(t):return t['title']
def vol(n):return n['stage_number']
def evidence(n):return '；'.join(f"{e['chapter_id']} L{e['start_line']}–{e['end_line']}" for e in n.get('evidence',[]))
def conclusion(t):return t['resolution_note']
'''
write('tree_style.py',style)
raw=(REF/'rebuild_plot_topology.py').read_text(encoding='utf-8')
raw=raw.replace('import rebuild_plot_images as p','import tree_style as p')
a=raw.index('HERE ='); b=raw.index('\ndef size(')
config='''HERE = Path(__file__).resolve().parent
TEAL, JUNCTION = '#147d8b', '#b86a23'
NW, HEADER, PAD = 366, 510, 90

def configure(folder):
    global OUT, CORE, ns, events, threads, ts, hidden, hno, core_nodes, core_edges, hidden_edges, edges, structural, pairs, incoming, outgoing, roots, forks, junctions, TIME_LABELS
    data=json.loads((HERE/folder/'plot/topology.json').read_text(encoding='utf-8'))
    p.G=data; p.NODES={n['id']:n for n in data['nodes']}; p.EDGES={e['id']:e for e in data['edges']}
    p.VAULT=HERE.parents[2];p.SID=data['source_id'];p.VOLUMES=data['stages'];p.TITLE=data['title'];p.CORE_TITLE=data['core_title']
    p.GRAPH_PATH=HERE/folder/'plot/graph.json';p.GAPS={t['id']:t['resolution_note'] for t in data['threads']}
    OUT=HERE/folder/'plot/whole-book';CORE='book-main';ns=p.NODES
    events=sorted(data['nodes'],key=lambda n:n['narrative_order']);threads=data['threads'];ts={t['id']:t for t in threads}
    hidden=[t for t in threads if t['kind']=='hidden'];hno={t['id']:i+1 for i,t in enumerate(hidden)}
    core_nodes=set(ts[CORE]['node_ids']);core_edges=set(ts[CORE]['edge_ids'])
    hidden_edges={eid for t in hidden for eid in t['edge_ids']};edges=data['edges']
    # 阅读衔接只组织主干，不参与语义分枝与交汇的计数。
    structural=[e for e in edges if e['kind'] not in ('echo','sequence')]
    pairs={(e['from'],e['to']) for e in structural};incoming=Counter(b for a,b in pairs);outgoing=Counter(a for a,b in pairs)
    roots=[n['id'] for n in events if not incoming[n['id']]];forks=[n['id'] for n in events if outgoing[n['id']]>1];junctions=[n['id'] for n in events if incoming[n['id']]>1]
    TIME_LABELS={}
'''
raw=raw[:a]+config+raw[b:]
raw=raw.replace("p.GAPS[n['tracking_key']]","p.GAPS[n['id']]")
# 阅读衔接参与版式，研究阶段只约束大致获知进度。
raw=raw.replace("for e in structural if e['to']==n['id']", "for e in edges if e['kind']!='echo' and e['to']==n['id']")
raw=raw.replace('(p.vol(n)-1)*3','(p.vol(n)-1)*2')
raw=raw.replace("print('布局输入：163个事件、265条原始关系、15个暗线状态注记。')","print(f'布局输入：{len(events)}个事件、{len(structural)}条语义关系、{len(hidden)}个暗线终态。')")
raw=raw.replace("'《超级骷髅兵》 · 剧情分枝与交汇'","f'《{p.TITLE}》 · 剧情分枝与交汇'")
raw=raw.replace("'从黑龙主线出发，旁支另起，在同一件事上相交，再继续分枝。'","f'从“{p.CORE_TITLE}”出发，旁支另起，在共享事件处交汇，再继续分枝。'")
raw=raw.replace("f'163个事件 / {len(roots)}个图内起点 / {len(forks)}个分枝点 / {len(junctions)}个交汇点 / 15条暗线终点复核'","f'{len(events)}个事件 / {len(roots)}个图内起点 / {len(forks)}个分枝点 / {len(junctions)}个交汇点 / {len(hidden)}条暗线终点复核'")
raw=raw.replace("'蓝色 · 自由存在与同伴主线'","'蓝色 · 核心成长主线'")
raw=raw.replace("'实线为因果，虚线为铺垫、揭示、转折或回收，细点线为主题呼应；只有接入同一事件框才算交汇，线条穿过不算。'","'实线为因果，虚线为铺垫、揭示、转折或回收；蓝色细点线仅为主干阅读衔接，不代表因果，也不计入交汇。'")
raw=raw.replace("'整体沿阅读进度向下展开，集数只是事件标记；回叙在获知位置保留。状态框是第18集复核注记，不是新增剧情。'","'整体沿阅读进度向下展开，研究阶段只是位置提示；同一事件只画一次。暗线状态框取全书终点复核，不是新增剧情。'")
raw=raw.replace("stroke=5 if eid in core_edges else 3","stroke=2.5 if e['kind']=='sequence' else 5 if eid in core_edges else 3")
raw=raw.replace("else '2 11' if e['kind']=='echo'","else '2 11' if e['kind'] in ('echo','sequence')")
raw=raw.replace("opacity=.33 if e['kind']=='echo' else .85","opacity=.4 if e['kind'] in ('echo','sequence') else .85")
raw=raw.replace("f'{p.vol(n):02d}集 · {nid}'","f'阶段{p.vol(n):02d} · {n[\"label_id\"]}'")
raw=raw.replace("p.GAPS[t['tracking_key']]","p.GAPS[t['id']]")
raw=raw.replace('aria-label="超级骷髅兵多起点剧情树"><title>超级骷髅兵：分枝与交汇</title>', 'aria-label="{p.esc(p.TITLE)}多起点剧情树"><title>{p.esc(p.TITLE)}：分枝与交汇</title>')
raw=raw.replace("'selection':'全事件分枝交汇版'","'selection':'全事件分枝交汇版','title':p.TITLE,'stages':len(p.VOLUMES),'reference':{'book':'超级骷髅兵','form':'蓝色主干、青色枝线、紫色暗线、共享交汇、枝端终态；同版式离线地图'},'semantic_relations':len(structural),'reading_links':sum(e['kind']=='sequence' for e in edges)")
raw=raw.replace('for v in range(1,19)', 'for v in range(1,len(p.VOLUMES)+1)')
raw=raw.replace("'direction':'按关系自上而下分枝；无集数父子结构'", "'direction':'按关系自上而下分枝；无阶段父子结构','sequence':'蓝色细点线为主干阅读衔接，非因果，不计交汇'")
raw=raw.replace("(HERE/'whole_book_viewer.html')", "(HERE/'tree-viewer.html')")
raw=raw.replace("template.replace('<!-- TREE_SVG -->',svg)","template.replace('BOOK_TITLE',p.TITLE).replace('<!-- TREE_SVG -->',svg)")
raw=raw.replace('    write_readme(meta)','    return meta')
raw=raw[:raw.index('\ndef write_readme(')]
raw=raw.replace(".write_text(svg,encoding='utf-8')", ".write_bytes(svg.encode('utf-8'))")
raw=raw.replace(".write_text(template.replace", ".write_text(template.replace")
write('tree_topology.py',raw)
viewer=(REF/'whole_book_viewer.html').read_text(encoding='utf-8').replace('超级骷髅兵','BOOK_TITLE').replace('跳到某一集','跳到研究阶段').replace('集数仅为标记','研究阶段仅为标记')
viewer=viewer.replace("echo:'呼应'","echo:'呼应',misdirection:'误导',sequence:'阅读衔接（非因果）'")
viewer=viewer.replace("open:'未回收'","open:'未回收',unknown:'原文未明',abandoned:'明确中断'")
viewer=viewer.replace("'14条待回收暗线：11条部分回收、3条未回收；点击状态框展开整条线'", "data.meta.threads.filter(t=>t.status!=='resolved').length+'条待回收或未明暗线；状态以各枝端注记为准，点击展开整条线'")
viewer=viewer.replace("t.question+'\\n\\n'+t.resolution_note);", "t.question+'\\n\\n'+t.resolution_note,evidence(t.evidence));")
viewer=viewer.replace("Math.max(.025,scale)","Math.max(.005,scale)")
viewer=viewer.replace("Math.max(.025,Math.min", "Math.max(.005,Math.min")
write('tree-viewer.html',viewer)
print('已移植参考绘图层和阅读器；原参考文件未改动。')
