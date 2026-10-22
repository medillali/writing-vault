"""从已审计研究生成时间推进图片的 SVG；PNG 由配套浏览器渲染器生成。"""
from pathlib import Path
from collections import Counter
from functools import lru_cache
import hashlib
import html
import json
import math
import re

HERE = Path(__file__).resolve().parent
VAULT = HERE.parents[2]
OUT = HERE / 'reading/plot/images'
SID = 'src-9ff09c395734410b856f77c77a652834'
GRAPH_PATH = VAULT / 'library/sources' / SID / 'plot-graph.json'
G = json.loads(GRAPH_PATH.read_text(encoding='utf-8'))
SYN = json.loads((HERE / 'book-synthesis.json').read_text(encoding='utf-8'))
NODES = {n['id']: n for n in G['nodes']}
EDGES = {e['id']: e for e in G['edges']}
VOLUMES = sorted((n for n in G['nodes'] if n['kind'] == 'volume'), key=lambda n: n['narrative_order'])
THREADS = [t for t in G['threads'] if t['id'].startswith('book-') and t['kind'] == 'hidden']
INK, MUTED, BLUE, PURPLE = '#172b46', '#51637a', '#2563a6', '#7850b5'
GREEN, AMBER, RED = '#087f65', '#a5650b', '#bf3b42'
STATE = {'resolved': ('已回收', GREEN, '#e6f5ef'), 'partial': ('部分回收', AMBER, '#fff3dc'), 'open': ('未回收', RED, '#fcecef')}
REL = {'cause': ('因果', '#147d8b'), 'setup': ('铺垫', PURPLE), 'reveal': ('揭示', '#a5650b'),
       'misdirection': ('误导', '#bf3b75'), 'reversal': ('转折', '#c05c25'), 'echo': ('呼应', '#537aa0'), 'payoff': ('回收', GREEN)}
CLAIM = {'fact': '事实', 'inference': '研究推断', 'synthesis': '研究综合', 'plan': '计划'}
SHORT = [
    '获得魂能与同伴，抢劫引发围捕', '记忆与宝藏扩充资源，娜娜进入队伍', '雷神败亡，救赎之魂促成去留选择',
    '建立家园，圣骑追踪使身份暴露', '救援与伤亡后北行，黑龙进化', '黑大觉醒，天使被封，原萝茜苏醒',
    '掌握元力，重订同伴与自由的边界', '神骑冲突后，强制转生氓族', '领地扩张，批量赋魂造成透支',
    '噬魂制傀儡，航海遭遇双层封印', '海皇夺躯失败，龙岛战争展开', '龙墓解封，先知受约；治理压力扩大',
    '黑龙被放逐，旧驻地遭袭失守', '获得记忆传承，回归时活尸计划待裁决', '暂禁活尸阵，帝国遗产与达罗亚出现',
    '同族保护者夺体，并毁己民供能', '夺体逆转，假旗崩解，红月开启', '子民归来；黑龙投入本源，后记醒返',
]
GAPS = {
    'sunken-undead-kingdom': '旧沼泽古国消失的完整因由仍缺',
    'tank-battle-soul': '战意是否服从、最终如何处置未明',
    'christine-identity': '本体脱封及后记个人去向未明',
    'th-rode-music': '旧次逃生方式与准确转生时点未答',
    'rosy-angel-identity': '记忆整合与最终生活未明',
    'desert-bones-and-mourning-soul': '起始之夜完整过程仍未讲完',
    'aroyo-memory-and-mang-clan': '氓族知晓真实死因后的反应未展示',
    'church-institution-and-angel-agency': '教皇结局与新制度执行过程未展示',
    'roge-soul-and-prayer': '祈愿与凝魂之间的确切因果未答',
    'soul-devourer-weapon-and-puppets': '完整流转链与全部傀儡权限未明',
    'forest-tree-and-dwarf-faith': '本源转移与政治后果未完全交代',
    'church-false-flag-and-cleansing-army': '操盘者、执行者及目的已明确；污名另计',
    'niruda-split-personhood-and-divinity': '两灵格后记去向与原天使人格未明',
    'source-consciousness-and-world-freedom': '内部胜负过程与最终权限未展示',
    'memory-and-power': '知识可继承，力量与掌握程度仍有限制',
}


def esc(s):
    return html.escape(str(s), quote=True)


@lru_cache(maxsize=32)
def font(size, bold=False):
    # 本机用字体实测换行；其他机器可安装 Pillow 与微软雅黑或 Noto CJK。
    from PIL import ImageFont
    candidates = [Path('C:/Windows/Fonts') / ('msyhbd.ttc' if bold else 'msyh.ttc'),
                  Path('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc')]
    for p in candidates:
        if p.exists():
            return ImageFont.truetype(str(p), size)
    raise RuntimeError('请安装 Microsoft YaHei 或 Noto Sans CJK 字体后重新生成图片。')


def wrap(s, width, size=26, bold=False):
    lines = []
    for paragraph in str(s).split('\n'):
        line = ''
        # 不把章节编号、行号或英文字段拆成两行。
        for char in re.findall(r'[A-Za-z0-9][A-Za-z0-9_.:–/\-]*|.', paragraph):
            if line and font(size, bold).getlength(line + char) > width - 8:
                lines.append(line)
                line = char
            else:
                line += char
        lines.append(line)
    return lines


def text_height(s, width, size=26, bold=False):
    return len(wrap(s, width, size, bold)) * math.ceil(size * 1.48)


class SVG:
    def __init__(self, width=1600):
        self.w, self.parts = width, []

    def rect(self, x, y, w, h, fill='white', stroke='#d9e2ed', radius=14):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}"/>')

    def path(self, d, color=BLUE, width=3, dash='', arrow=False, opacity=1):
        marker = f' marker-end="url(#a{color[1:]})"' if arrow else ''
        self.parts.append(f'<path d="{d}" stroke="{color}" stroke-width="{width}" fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="{dash}" opacity="{opacity}"{marker}/>')

    def circle(self, x, y, r, fill=BLUE, stroke='white'):
        self.parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="3"/>')

    def text(self, x, y, s, width, size=26, color=INK, bold=False):
        yy = y
        for line in wrap(s, width, size, bold):
            self.parts.append(f'<text x="{x}" y="{yy + size}" font-size="{size}" font-weight="{700 if bold else 400}" fill="{color}" data-left="{x}" data-right="{x + width}" data-bottom="{yy + math.ceil(size * 1.48)}">{esc(line)}</text>')
            yy += math.ceil(size * 1.48)
        return yy

    def header(self, eyebrow, title, subtitle):
        self.rect(0, 0, self.w, 12, BLUE, BLUE, 0)
        self.text(64, 42, eyebrow, self.w - 128, 22, BLUE, True)
        y = self.text(64, 83, title, self.w - 128, 44, INK, True)
        y = self.text(64, y + 16, subtitle, self.w - 128, 24, MUTED)
        return y + 34

    def save(self, name, height, metadata):
        self.text(64, height - 64, '《超级骷髅兵》研究图 · 研究草稿待审阅 · 章节与行号可回查正文 · PNG / SVG', self.w - 128, 20, MUTED)
        colors = {BLUE, PURPLE, GREEN, AMBER, RED} | {c for _, c in REL.values()}
        defs = ''.join(f'<marker id="a{c[1:]}" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L8,4 L0,8 Z" fill="{c}"/></marker>' for c in sorted(colors))
        content = f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{height}" viewBox="0 0 {self.w} {height}" role="img"><title>{esc(metadata["title"])}</title><desc>按主线阅读进度排列，回收状态采用全书终点复核。</desc><defs>{defs}</defs><rect width="100%" height="100%" fill="#f4f7fc"/><g font-family="Microsoft YaHei, Noto Sans CJK SC, sans-serif">' + ''.join(self.parts) + '</g></svg>'
        (OUT / (name + '.svg')).write_text(content, encoding='utf-8')
        return {'file': name, 'width': self.w, 'height': height, **metadata}


def title(t):
    return t['title'].split(' · ')[-1]


def vol(n):
    return int(n['id'][1:3])


def evidence(n):
    entries = n.get('evidence', [])
    return '；'.join(f"{e['chapter_id']} L{e['start_line']}–{e['end_line']}" for e in entries)


def conclusion(t):
    return re.sub(r'^已入库至第\d+集；最近关联事件在第\d+集。最新状态审计在第\d+集。', '', t['resolution_note'])


def overview():
    s = SVG()
    y = s.header('01 / 全书主线树', '从求生到争取自由的世界', '主干沿第1—18集向下推进；右侧展开各集转折。阶段划分与短说明属于研究整理。')
    ranges = [(1, 3), (4, 6), (7, 9), (10, 12), (13, 15), (16, 17), (18, 18)]
    prev = None
    for i, (stage, (lo, hi)) in enumerate(zip(SYN['stages'], ranges), 1):
        st = stage['title'].split('：', 1)[1]
        th = text_height(st, 460, 30, True)
        sh = text_height(stage['summary'], 460, 23)
        h = max(134 + th + sh, (hi - lo + 1) * 116 + 20)
        cy = y + 45
        if prev is not None:
            s.path(f'M 95 {prev} L 95 {cy - 22}', width=5, arrow=True)
        s.circle(95, cy, 24)
        s.text(82, cy - 19, str(i), 36, 24, 'white', True)
        s.path(f'M 120 {cy} H 160', width=3)
        s.rect(160, y, 510, h - 24, '#eaf1fb', '#c5d6ed')
        yy = s.text(184, y + 20, f'第{lo:02d}—{hi:02d}集' if lo != hi else f'第{lo:02d}集', 460, 22, BLUE, True)
        yy = s.text(184, yy + 10, st, 460, 30, INK, True)
        s.text(184, yy + 18, stage['summary'], 460, 23, MUTED)
        for v in range(lo, hi + 1):
            by = y + (v - lo) * 116
            s.path(f'M 670 {cy} H 700 V {by + 47} H 734', width=2)
            s.rect(736, by, 800, 100)
            s.text(758, by + 8, VOLUMES[v-1]['title'], 750, 26, INK, True)
            s.text(758, by + 48, SHORT[v-1], 750, 23, MUTED)
        prev = cy
        y += h + 24
    s.rect(160, y, 1376, 132, '#fff3dc', '#eed8ad')
    s.text(184, y + 16, '结局已有生活与情感回收；机制和治理过程仍有空白', 1328, 28, AMBER, True)
    s.text(184, y + 64, '本源内部争夺、停战治理及若干配角去向未完整展示。详见暗线终点图；不把后记反推为所有问题已解决。', 1328, 24, INK)
    return s.save('main-overview', y + 232, {'title': '全书主线树', 'kind': 'overview', 'volume_ids': [v['id'] for v in VOLUMES]})


def hidden_overview(group, page, total):
    s = SVG(1900)
    y = s.header('02 / 暗线沿主线时间展开', f'暗线时间总览 · {page}/{total}', '从左到右：第1—18集。圆点是已有事件；曲线连接同一暗线；虚线尾巴仅表示疑问仍悬置。')
    start, step = 550, 61
    for i in range(18):
        x = start + i * step
        s.text(x - 15, y, f'{i+1:02d}', 52, 24, BLUE, True)
        s.path(f'M {x} {y + 96} V {y + 136 + len(group) * 174}', '#dce4ef', 1)
    s.text(1665, y, '全书终点', 160, 24, MUTED, True)
    for lo, hi, label in [(1,3,'求生与同伴'),(4,6,'照护与觉醒'),(7,9,'自由与领地'),(10,12,'海皇与龙岛'),(13,15,'放逐与遗产'),(16,17,'夺体/假旗'),(18,18,'本源')]:
        x = start + (lo - 1) * step - 24
        width = (hi-lo+1)*step-6 if lo != hi else step+6
        s.rect(x, y + 44, width, 44, '#eaf1fb', '#d0def0', 8)
        s.text(x+6, y + 49, label, width-12, 20, BLUE, True)
    y += 118
    for t in group:
        label, color, fill = STATE[t['status']]
        s.rect(56, y, 1788, 150, 'white', '#e0e6ef')
        s.text(78, y + 16, title(t), 430, 27, INK, True)
        s.text(78, y + 94, GAPS[t['tracking_key']], 1445, 22, MUTED)
        nums = sorted({vol(NODES[n]) for n in t['node_ids']})
        points = [(start + (v - 1) * step, y + 45 + (6 if j % 2 else -6)) for j, v in enumerate(nums)]
        for (x1, y1), (x2, y2) in zip(points, points[1:]):
            s.path(f'M {x1} {y1} C {(x1+x2)/2} {y1-23} {(x1+x2)/2} {y2+23} {x2} {y2}', PURPLE, 3)
        for x, py in points:
            s.circle(x, py, 8, PURPLE)
        ex, ey = points[-1]
        s.path(f'M {ex+9} {ey} C {ex+30} {ey} 1600 {y+45} 1640 {y+45}', color, 3, '7 8' if t['status'] != 'resolved' else '', True)
        s.rect(1650, y + 18, 170, 58, fill, fill, 10)
        s.text(1668, y + 27, label, 140, 26, color, True)
        y += 174
    return s.save(f'hidden-overview-{page:02d}', y + 114, {'title': f'暗线时间总览 {page}', 'kind': 'hidden-overview', 'thread_ids': [t['id'] for t in group], 'states': {t['id']: t['status'] for t in group}})


def event_height(n):
    return 76 + text_height(n['title'], 742, 28, True) + text_height(n.get('summary', ''), 742, 24) + text_height(evidence(n), 742, 20)


def timeline(name, heading, nodes, edges, thread=None, page=1, total=1):
    """时间主干与关系旁路分开画；旁路编号在图后给出完整语义。"""
    s = SVG(1700)
    y = s.header('03 / 按主线进度查看事件与分支' if thread is None else '04 / 一条暗线的埋设、揭示与终点',
                 heading, '蓝色主干：阅读顺序；彩色旁路：已有语义关系。回叙与跨段聚合保留原标注，不能当作同一时点。')
    if thread:
        label, color, fill = STATE[thread['status']]
        h = text_height(thread['question'], 1270, 26) + 30
        s.rect(64, y, 1572, h, fill, fill)
        s.text(86, y + 14, label + ' · 全书终点', 270, 24, color, True)
        s.text(360, y + 14, thread['question'], 1250, 26)
        y += h + 26
    top = y
    positions, heights = {}, {}
    for n in nodes:
        h = event_height(n)
        positions[n['id']], heights[n['id']] = y, h
        y += h + 40
    bottom = y
    # 时间骨架在事件卡片之外，避免把相邻事件误标为因果。
    s.path(f'M 114 {top + 42} V {bottom - 36}', BLUE, 4, arrow=True)
    inside = [e for e in edges if e['from'] in positions and e['to'] in positions]
    # 关系按起点排序并复用不相交通道，所有语义保持原始方向。
    lanes, badges = [], []
    edge_number = {e['id']: i + 1 for i, e in enumerate(edges)}
    for e in sorted(inside, key=lambda e: (min(positions[e['from']], positions[e['to']]), e['id'])):
        a, b = positions[e['from']] + 45, positions[e['to']] + 45
        lo, hi = sorted((a, b))
        lane = next((i for i, end in enumerate(lanes) if end < lo - 20), len(lanes))
        if lane == len(lanes):
            lanes.append(hi)
        else:
            lanes[lane] = hi
        x = 1060 + lane * 55
        if x > 1600:
            raise ValueError(f'{name}: 关系通道过密，请缩小分页')
        kind, color = REL[e['kind']]
        s.path(f'M 984 {a} C {x} {a} {x} {a} {x} {a+18} L {x} {b-18 if b>a else b+18} Q {x} {b} 992 {b}', color, 2.5, '' if e['kind']=='cause' else '6 5', True, .85)
        # 编号放在独立通道旁，完整关系说明在下方；不缩小文字。
        mid = (a+b)/2
        badges.append((x, mid, edge_number[e['id']], color))
    for x, mid, number, color in badges:
        s.rect(x - 20, mid - 17, 42, 34, 'white', color, 8)
        s.text(x - 13, mid - 16, str(number), 34, 20, color, True)
    for i, n in enumerate(nodes):
        ny, h = positions[n['id']], heights[n['id']]
        s.circle(114, ny + 45, 11)
        s.text(64, ny + 68, f'{vol(n):02d}集', 94, 22, BLUE, True)
        s.path(f'M 126 {ny+45} H 186', BLUE, 2)
        s.rect(188, ny, 796, h)
        yy = s.text(212, ny + 14, n['id'] + ' · ' + CLAIM.get(n.get('claim_kind'), '研究记录'), 742, 20, BLUE)
        yy = s.text(212, yy + 6, n['title'], 742, 28, INK, True)
        yy = s.text(212, yy + 10, n.get('summary', ''), 742, 24, MUTED)
        s.text(212, yy + 12, evidence(n), 742, 20, MUTED)
    y = bottom + 8
    if edges:
        y = s.text(64, y, '旁路关系说明 · 编号对应图中连线', 1572, 28, INK, True) + 18
        for e in edges:
            kind, color = REL[e['kind']]
            outside = e['from'] not in positions or e['to'] not in positions
            text = f"{edge_number[e['id']]:02d}  {kind} · {CLAIM.get(e.get('claim_kind'), '研究记录')} · {e['from']} → {e['to']}" + ('〔跨页接续〕' if outside else '')
            y = s.text(84, y, text, 1518, 23, color, True)
            y = s.text(84, y + 4, e['label'], 1518, 23, MUTED) + 14
    if thread:
        label, color, fill = STATE[thread['status']]
        summary = conclusion(thread)
        h = 110 + text_height(summary, 1518, 25)
        s.rect(64, y + 20, 1572, h, fill, fill)
        yy = s.text(88, y + 40, f'{label} · 终点边界（第18集复核）', 1518, 28, color, True)
        s.text(88, yy + 16, summary, 1518, 25)
        y += h + 40
        if page < total:
            y = s.text(64, y, f'继续下一张：{page+1}/{total}。跨页边仅在起点页列出；终点结论在各页重复，便于单独保存。', 1572, 23, BLUE) + 14
    return s.save(name, y + 104, {'title': heading, 'kind': 'thread' if thread else 'volume', 'node_ids': [n['id'] for n in nodes],
                  'edge_ids': [e['id'] for e in edges], 'drawn_edge_ids': [e['id'] for e in inside],
                  'thread_id': thread['id'] if thread else None, 'status': thread['status'] if thread else None, 'page': page, 'total': total})


def generate():
    OUT.mkdir(parents=True, exist_ok=True)
    images = [overview()]
    ordered = sorted(THREADS, key=lambda t: (min(NODES[n]['narrative_order'] for n in t['node_ids']), t['id']))
    for i in range(0, len(ordered), 8):
        images.append(hidden_overview(ordered[i:i+8], i//8+1, math.ceil(len(ordered)/8)))
    for v in VOLUMES:
        ns = sorted((n for n in G['nodes'] if n.get('parent_id')==v['id']), key=lambda n: n['narrative_order'])
        ids = {n['id'] for n in ns}
        es = [e for e in G['edges'] if e['from'] in ids and e['to'] in ids]
        images.append(timeline(v['id'], v['title'] + ' · 时间主干与分支', ns, es))
    for t in ordered:
        es = [EDGES[e] for e in t['edge_ids']]
        ids = set(t['node_ids']) | {e[k] for e in es for k in ('from', 'to')}
        ns = sorted((NODES[n] for n in ids), key=lambda n: n['narrative_order'])
        count = math.ceil(len(ns)/7)
        for i in range(count):
            part = ns[i*7:(i+1)*7]
            pids = {n['id'] for n in part}
            pe = [e for e in es if e['from'] in pids]
            images.append(timeline(f"{t['id']}-{i+1:02d}", f'{title(t)} · {i+1}/{count}', part, pe, t, i+1, count))
    manifest = {'source_id': SID, 'graph_sha256': hashlib.sha256(GRAPH_PATH.read_bytes()).hexdigest(),
                'synthesis_sha256': hashlib.sha256((HERE/'book-synthesis.json').read_bytes()).hexdigest(),
                'time_axis': 'narrative_order; 回叙和跨段事件保留源说明', 'hidden_states': dict(Counter(t['status'] for t in THREADS)),
                'images': images}
    (OUT/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    make_index(images, ordered)
    print(json.dumps({'svg_images': len(images), 'volumes': len(VOLUMES), 'hidden_threads':len(THREADS), 'max_height':max(i['height'] for i in images)}, ensure_ascii=False))


def image_links(im):
    n = im['file']
    return [f"### {im['title']}", '', f'[PNG原尺寸](images/{n}.png) · [SVG矢量图](images/{n}.svg)', '', f"![{im['title']}](images/{n}.png)", '']


def make_index(images, ordered):
    lines = ['# 主线与暗线图片版', '', '[全书阅读首页](../README.md) · [剧情与证据目录](README.md)', '',
             '**[全书一张大树图](whole-book.md)**：多起点分枝、共享事件交汇；包含全部163个事件与15条暗线终点状态。下面保留原有分图。', '',
             '沿小说第1—18集推进。图片可直接保存；点击PNG可查看原尺寸，SVG可继续放大。蓝色主干是阅读顺序，彩色旁路才表示已有语义关系。回叙、旧史和跨段聚合保留标记。', '',
             f'共{len(images)}张图片：全书主线树、18集时间主干与分支、2张暗线总览、15条暗线分页详图。', '',
             '**暗线终点：1条已回收，11条部分回收，3条未回收。** 状态针对每条线的问题范围；终点文字写明已知与缺口。空白时间的虚线不表示持续发生事件。', '']
    for im in images[:3]:
        lines += image_links(im)
    lines += ['## 18集主线图片', '', '| 集数 | 图片与依据 |', '|---|---|']
    for v in VOLUMES:
        lines += [f"| {v['title']} | [PNG](images/{v['id']}.png) · [SVG](images/{v['id']}.svg) · [事件与证据]({v['id']}.md) |"]
    lines += ['', '## 15条暗线图片', '', '| 暗线 | 终点状态 | 图片与依据 |', '|---|---|---|']
    for t in ordered:
        ims = [i for i in images if i.get('thread_id')==t['id']]
        links = ' · '.join(f"[图{i['page']}](images/{i['file']}.png)" for i in ims)
        lines += [f"| {title(t)} | {STATE[t['status']][0]} | {links} · [完整图文](threads/{t['id']}.md) |"]
    lines += ['', '图片摘要由既有研究主档生成，完整关系、认知边界与章节行号保留在图文页。人物卡、研究JSON、个人笔记与版本历史仍是原记录。', '',
              '重建：先运行报告目录的 `rebuild_plot_images.py`，再用 `render_plot_images.cjs` 生成PNG，最后运行 `rebuild_github_reading.py` 更新页面。需要 Python/Pillow、中文字体及 Node.js/Playwright 浏览器。']
    (OUT.parent/'images.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')


if __name__ == '__main__':
    generate()
