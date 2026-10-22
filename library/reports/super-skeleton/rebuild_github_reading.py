"""从既有研究主档生成GitHub阅读副本；不更改卡片、图、笔记或历史。"""
from pathlib import Path
from collections import Counter
import hashlib
import html
import json
import re

HERE = Path(__file__).resolve().parent
VAULT = HERE.parents[2]
OUT = HERE / 'reading'
SID = 'src-9ff09c395734410b856f77c77a652834'
LABELS = {
    'summary': '概述', 'name': '姓名', 'aliases': '别名', 'goal': '目标',
    'conflict': '矛盾与限制', 'arc_change': '人物变化', 'coverage_note': '覆盖与结局边界',
    'identity_notes': '身份辨析', 'knowledge_limits': '认知边界', 'relationships': '人物关系',
    'opening_observations': '开篇观察', 'volume_history': '分集变化', 'evidence': '证据定位',
    'applicability': '适用场景', 'choice': '行动与选择', 'consequence': '后果',
    'failure_mode': '失效条件', 'limits': '使用边界', 'obstacle': '障碍',
    'state_change': '状态变化', 'volume': '所属集数', 'why_it_works': '为何有效', 'steps': '操作步骤',
    'observer': '观察者', 'belief': '当时认知', 'state': '认知状态', 'claim_kind': '判断类型',
    'contradiction': '内在矛盾', 'decision_pattern': '决策方式', 'knowledge_boundary': '认知边界',
    'unknowns': '当时未解问题', 'arc_in_sample': '样段中的变化', 'confirmed': '已确认信息',
    'misbeliefs': '误认与误判', 'relationship': '人物关系',
}
FIELD_ORDER = ['summary', 'name', 'aliases', 'volume', 'coverage_note', 'identity_notes', 'goal',
               'obstacle', 'conflict', 'choice', 'consequence', 'state_change', 'arc_change',
               'relationships', 'knowledge_limits', 'steps', 'why_it_works', 'applicability',
               'failure_mode', 'limits', 'volume_history', 'opening_observations']
CLAIMS = {'fact': '原文事实', 'inference': '研究推断', 'synthesis': '抽象综合', 'plan': '计划'}
STATES = {'open': '未回收', 'partial': '部分回收', 'resolved': '已回收', 'abandoned': '已放弃', 'unknown': '未确认'}
KINDS = {'character': ('characters', '人物卡'), 'scene': ('scenes', '场景卡'), 'pattern': ('patterns', '机制卡')}
RELATIONS = {'cause': '因果', 'setup': '铺垫', 'reveal': '揭示', 'misdirection': '误导', 'reversal': '转折', 'echo': '呼应', 'payoff': '回收'}
written = []


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def text(value):
    value = html.escape(str(value), quote=False)
    return re.sub(r'([\\`*\[\]])', r'\\\1', value)


def cell(value):
    return text(value).replace('|', '&#124;').replace('\n', '<br>')


def save(path, lines):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('\n'.join(lines).rstrip() + '\n', encoding='utf-8')
    written.append(path)


def evidence(items):
    rows = ['| 章节 | 行号 | 判断类型 |', '|---|---|---|']
    for e in items:
        cid = e.get('chapter_id', '')
        c = chapters.get(cid, {})
        span = f"{e['start_line']}–{e['end_line']}" if 'start_line' in e else '章节范围'
        rows.append(f"| {cell(cid + ' ' + c.get('title', ''))} | {span} | {CLAIMS.get(e.get('claim_kind'), '随所在研究条目')} |")
    return rows + ['']


def render_value(key, value, level=2):
    label = LABELS.get(key, key)
    lines = ['#' * min(level, 6) + ' ' + label, '']
    if key == 'evidence' and isinstance(value, list):
        return lines + evidence(value) if value else lines + ['未另列证据。', '']
    if key == 'volume_history':
        for item in value:
            lines += [f"### 第{item.get('volume', '?')}集", '']
            for k, v in item.items():
                if k != 'volume':
                    lines += render_value(k, v, 4)
        return lines
    if isinstance(value, dict):
        for k, v in value.items():
            lines += render_value(k, v, level + 1)
    elif isinstance(value, list):
        if not value:
            lines += ['未另列。', '']
        elif all(not isinstance(v, (dict, list)) for v in value):
            lines += ['- ' + text(v) for v in value] + ['']
        else:
            for i, v in enumerate(value, 1):
                lines += [f"{'#' * min(level + 1, 6)} 条目{i}", '']
                if isinstance(v, dict):
                    for k, val in v.items():
                        lines += render_value(k, val, level + 2)
                else:
                    lines += [text(v), '']
    else:
        lines += [text(value) if value not in ('', None) else '未填写。', '']
    return lines


def node_page(node_id):
    node = by_id[node_id]
    while node.get('parent_id') and node['kind'] != 'volume':
        node = by_id[node['parent_id']]
    return node['id'] + '.md' if node['kind'] == 'volume' else 'README.md'


def node_link(node_id, prefix=''):
    return f"[{text(by_id[node_id]['title'])}]({prefix}{node_page(node_id)})"


def diagram(nodes, edges, structural=False):
    ids = {n['id']: f'n{i}' for i, n in enumerate(nodes)}
    lines = ['```mermaid', 'flowchart LR']
    for n in nodes:
        label = html.escape(n['title'], quote=True).replace('\n', ' ')
        lines.append(f'  {ids[n["id"]]}["{label}"]')
    for edge in edges:
        if structural:
            lines.append(f"  {ids[edge['from']]} --> {ids[edge['to']]}")
        else:
            label = html.escape(RELATIONS.get(edge['kind'], edge['kind']), quote=True)
            lines.append(f"  {ids[edge['from']]} -. {label} .-> {ids[edge['to']]}")
    return lines + ['```', '']


def relations_table(edges, prefix=''):
    rows = ['| 起点 | 关系 | 终点 | 研究说明 |', '|---|---|---|---|']
    for e in edges:
        rows.append(f"| {node_link(e['from'], prefix)} | {RELATIONS.get(e['kind'], e['kind'])} | {node_link(e['to'], prefix)} | {cell(e.get('label', ''))} |")
    return rows + ['']


def make_cards():
    for card in cards:
        aid = card['asset_id']
        folder, name = KINDS[card['asset_type']]
        lines = [f"# {text(card['title'])}", '', f'[返回{name}目录](../{folder}.md) · [全书阅读首页](../README.md)', '',
                 f"类型：{name} · 版本：{card['revision']} · {'来源分析' if card['scope']=='source-analysis' else '可迁移机制'}", '',
                 f"审阅状态：{ {'draft': '研究草稿，待用户审阅', 'reviewed': '已审阅', 'approved': '已认可'}.get(card['review_status'], text(card['review_status']))} · 收藏：{'是' if card['favorite'] else '否'}", '']
        content = card['content']
        for key in [k for k in FIELD_ORDER if k in content] + [k for k in content if k not in FIELD_ORDER]:
            value = content[key]
            if key == 'opening_observations':
                lines += ['以下为最初开篇样段的历史观察；其中“未知”“未读”等表述描述当时范围，全书终点结论见本页前部。', '']
            lines += render_value(key, value)
        lines += ['## 全部引用定位', ''] + evidence(card['evidence'])
        lines += ['## 个人笔记', '', text(card.get('user_notes', '')) or '尚无个人笔记。', '']
        if card.get('derived_from'):
            lines += ['## 来源素材', '']
            for ref in card['derived_from']:
                target = next((a for a in cards if a['asset_id'] == ref['asset_id']), None)
                if target:
                    lines += [f"- [{text(target['title'])}]({target['asset_id']}.md)，采用版本{ref['revision']}。"]
                else:
                    lines += [f"- `{ref['asset_id']}`，采用版本{ref['revision']}。"]
            lines += ['']
        lines += ['## 记录信息', '', f"标签：{text('、'.join(card.get('tags', [])))}", '',
                  f"[JSON主档](../../../../{folder}/{aid}.json) · [版本历史](../../../../../history/assets/{aid}/)", '',
                  '本页是自动生成的阅读副本；持久笔记和收藏请通过资料库工具写入主档。']
        # 首版卡片还没有历史文件夹，避免提供不存在的导航。
        if not (VAULT / 'history/assets' / aid).exists():
            lines[-3] = f'[JSON主档](../../../../{folder}/{aid}.json)'
        save(OUT / 'cards' / (aid + '.md'), lines)
    for kind, (folder, name) in KINDS.items():
        group = sorted((c for c in cards if c['asset_type'] == kind), key=lambda c: (c['content'].get('volume', 0), c['title']))
        lines = [f'# {name}目录', '', '[全书阅读首页](README.md)', '', f'共{len(group)}张。点击标题阅读中文条目、分集变化及证据。', '', '| 卡片 | 概述 |', '|---|---|']
        lines += [f"| [{cell(c['title'])}](cards/{c['asset_id']}.md) | {cell(c['content']['summary'])} |" for c in group]
        save(OUT / (folder + '.md'), lines)


def make_plot():
    root = next(n for n in graph['nodes'] if n['kind'] == 'story')
    lines = ['# 主线树与暗线目录', '', '[全书阅读首页](../README.md) · [全部265条语义关系](relations.md)', '',
             '**[PC／手机剧情阅读器](reader.md)**：PC从阶段骨架进入局部图，手机沿事件卡片阅读；查看全部前因后果、进入支线并返回原位置。', '',
             '**[全书一张大树图](whole-book.md)**：163个事件、265条关系；支线另起、交汇后再分枝，暗线状态贴在对应枝端。', '',
             '[打开主线与暗线图片版](images.md)：全书阶段树、18集推进图、15条暗线时间图。PNG可直接保存，SVG可放大。', '',
             '蓝色主干按小说阅读进度推进；回叙与跨段聚合保留说明。跨集页面的回收状态采用全书终点复核结论。', '',
             '## 全书主线图片', '', '[PNG原尺寸](images/main-overview.png) · [SVG矢量图](images/main-overview.svg)', '',
             '![全书主线树](images/main-overview.png)', '']
    lines += ['## 按集阅读', ''] + [f"- [{text(n['title'])}]({n['id']}.md)" for n in volumes]
    lines += ['', '## 46条跨集剧情线', '', '| 剧情线 | 终点状态 | 核心问题 |', '|---|---|---|']
    for t in book_threads:
        lines += [f"| [{cell(t['title'])}](threads/{t['id']}.md) | {STATES[t['status']]} | {cell(t.get('question', ''))} |"]
    save(OUT / 'plot/README.md', lines)
    for volume in volumes:
        nodes = [n for n in graph['nodes'] if n['id'] == volume['id'] or n.get('parent_id') == volume['id']]
        ids = {n['id'] for n in nodes}
        edges = [e for e in graph['edges'] if e['from'] in ids and e['to'] in ids]
        num = int(volume['id'].split('-')[1])
        lines = [f"# {text(volume['title'])} · 剧情结构", '', f'[剧情目录](README.md) · [本集九维报告](../../vol{num:02d}.md)', '',
                 '## 主线时间与分支图片', '', f"[PNG原尺寸](images/{volume['id']}.png) · [SVG矢量图](images/{volume['id']}.svg) · [全书图片目录](images.md)", '',
                 f"![{text(volume['title'])}时间主干与分支](images/{volume['id']}.png)", '']
        lines += ['## 本集因果、伏笔与回收关系', ''] + relations_table(edges)
        lines += ['跨集联系见[全部语义关系](relations.md)与[跨集剧情线](README.md)。', '', '## 事件、人物与认知依据', '']
        for n in nodes:
            if n['id'] == volume['id']:
                continue
            lines += [f"### {text(n['title'])}", '', f"判断类型：{CLAIMS.get(n.get('claim_kind'), '未另标注')}", '', text(n.get('summary', '')), '']
            linked = [assets[c] for c in n.get('characters', []) if c in assets]
            if linked:
                lines += ['人物：' + '、'.join(f"[{text(c['content'].get('name', c['title']))}](../cards/{c['asset_id']}.md)" for c in linked), '']
            for k in n.get('knowledge', []):
                observer = assets.get(k['observer'], {}).get('content', {}).get('name', '读者' if k['observer'] == 'reader' else k['observer'])
                state = {'unknown': '未知', 'suspects': '怀疑', 'knows': '知道', 'misbelieves': '误以为'}.get(k['state'], k['state'])
                lines += [f"- {text(observer)}：{state}；{text(k['belief'])}", '']
            lines += evidence(n.get('evidence', []))
        lines += ['## 本集当时的剧情线判断', '', '这是分集历史判断，后续回收结果以跨集终点页为准。', '']
        for t in graph['threads']:
            if t['id'].startswith(f'v{num:02d}-'):
                lines += [f"### {text(t['title'])}", '', f"当时状态：{STATES[t['status']]}", '', text(t.get('question', '')), '', text(t.get('resolution_note', '')), '']
                final = next((b for b in book_threads if b.get('tracking_key') == t.get('tracking_key')), None)
                if final:
                    lines += [f"[查看全书终点判断](threads/{final['id']}.md)", '']
        save(OUT / 'plot' / (volume['id'] + '.md'), lines)
    lines = ['# 全部语义关系', '', '[剧情目录](README.md)', '', '265条关系按起点所在集排列；文本保留判断类型和章节行号，未把推断提升为事实。', '']
    for volume in volumes:
        edges = [e for e in graph['edges'] if node_page(e['from']) == volume['id'] + '.md']
        lines += ['## ' + text(volume['title']), '']
        for e in edges:
            lines += [f"### {text(e.get('label', e['id']))}", '', f"{node_link(e['from'])} → **{RELATIONS[e['kind']]}** → {node_link(e['to'])}", '',
                      f"判断类型：{CLAIMS.get(e.get('claim_kind'), '未另标注')}", ''] + evidence(e.get('evidence', []))
    save(OUT / 'plot/relations.md', lines)
    for t in book_threads:
        edges = [edges_by_id[e] for e in t['edge_ids']]
        nodes = sorted((by_id[n] for n in t['node_ids']), key=lambda n: n.get('narrative_order', 0))
        lines = [f"# {text(t['title'])}", '', '[剧情目录](../README.md) · [全书阅读首页](../../README.md)', '',
                 f"终点状态：**{STATES[t['status']]}**", '', '## 核心问题', '', text(t.get('question', '')), '',
                 '## 全书复核结论', '', text(t.get('resolution_note', '')), '']
        if t['kind'] == 'hidden':
            lines += ['## 暗线时间图片', '', '按主线阅读进度向下推进；分页保留关系编号与接续说明，每张均带全书终点状态。', '']
            for p in sorted((OUT / 'plot/images').glob(t['id'] + '-*.svg')):
                stem = p.stem
                lines += [f'[PNG原尺寸](../images/{stem}.png) · [SVG矢量图](../images/{stem}.svg)', '',
                          f'![{text(t["title"])}时间图](../images/{stem}.png)', '']
        lines += ['## 关联事件', '']
        lines += [f"- {node_link(n['id'], '../')}：{text(n.get('summary', ''))}" for n in nodes]
        lines += ['', '## 关系网络', '', '虚线展示因果、铺垫、误导、揭示与回收。每组至多6条关系；组间通过同名节点衔接，不新增时间顺序或因果。', '']
        for start in range(0, len(edges), 6):
            part = edges[start:start + 6]
            ids = {e[key] for e in part for key in ['from', 'to']}
            lines += [f'### 关系组{start // 6 + 1}', ''] + diagram([n for n in nodes if n['id'] in ids], part)
            lines += relations_table(part, '../')
        if not edges:
            lines += ['此线未单列关系边；保留事件及终点说明。', '']
        lines += ['逐条引用依据见[全部语义关系](../relations.md)及事件所在分集页。']
        save(OUT / 'plot/threads' / (t['id'] + '.md'), lines)


def main():
    make_cards()
    make_plot()
    counts = Counter(c['asset_type'] for c in cards)
    lines = ['# 《超级骷髅兵》GitHub阅读版', '', '[资料库首页](../../../../README.md) · [研究总目录](../README.md)', '',
             '已完成18集、183章（含序章）的蒸馏与研究复核，以下页面可在GitHub直接阅读。事实、研究解释、可迁移方法和个人评价分别保留；研究草稿等待你的审阅。', '',
             '## 从这里开始', '', '| 内容 | 阅读入口 |', '|---|---|',
             '| PC分层看图、手机沿线阅读与原位返回 | [双端剧情阅读器](plot/reader.md) |',
             '| 一张大图贯穿全书主线与暗线 | [全书分枝交汇图](plot/whole-book.md) |',
             '| 主线树、暗线、未回收疑点的图片 | [图片阅读入口](plot/images.md) |',
             '| 全书九维综合、阶段及人物弧 | [全书综合报告](../book-synthesis.md) |',
             f"| {counts['character']}张人物卡 | [人物目录](characters.md) |",
             f"| {counts['scene']}张场景卡 | [场景目录](scenes.md) |",
             f"| {counts['pattern']}张机制卡 | [机制目录](patterns.md) |",
             '| 18集主线树、46条跨集剧情线 | [剧情与暗线目录](plot/README.md) |',
             '| 198项问题、89条历史修订复核 | [疑点账本](../question-ledger.md) |',
             '| 覆盖、资料保护与恢复验收 | [全书验收说明](../验收说明.md) |', '', '## 逐集九维研究', '',
             '| 集数 | 九维报告 | 剧情树 |', '|---|---|---|']
    for i, v in enumerate(volumes, 1):
        lines += [f"| {text(v['title'])} | [阅读报告](../vol{i:02d}.md) | [查看剧情树](plot/{v['id']}.md) |"]
    lines += ['', '## 阅读与维护', '',
              '- 原小说TXT保留在本机；页面提供研究内容和章节行号，不提供原文全文。',
              '- 卡片按中文字段展示；人物分集历史与全书终点补记均保留，旧判断不会冒充最终结论。',
              '- 剧情阅读器提供PC局部关系图、手机事件卡片和可携带的阅读进度；GitHub上的HTML文件需下载后在浏览器打开。',
              '- 主线与暗线同时提供PNG、SVG原图；完整文字、证据与Mermaid关系组保留。',
              '- 图片由`rebuild_plot_images.py`与`render_plot_images.cjs`生成，再运行本阅读页生成器。',
              '- 本目录由同级报告目录的`rebuild_github_reading.py`生成。修改主档后重新生成；个人笔记和收藏通过资料库工具保存。',
              '- 其他三本目前仅有开篇样段，Space尚未接入。', '',
              '[GitHub图表支持说明](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams)']
    save(OUT / 'README.md', lines)
    if (OUT / 'plot/images.md').exists():
        written.append(OUT / 'plot/images.md')
    if (OUT / 'plot/whole-book.md').exists():
        written.append(OUT / 'plot/whole-book.md')
    if (OUT / 'plot/reader.md').exists():
        written.append(OUT / 'plot/reader.md')
    manifest = {'source_id': SID, 'source_revision': source['revision'], 'cards': dict(counts), 'volumes': len(volumes),
                'nodes': len(graph['nodes']), 'relations': len(graph['edges']), 'book_threads': len(book_threads),
                'pages': {p.relative_to(OUT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in written}}
    (OUT / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in manifest.items() if k != 'pages'} | {'markdown_pages': len(written)}, ensure_ascii=False, indent=2))


source = read(VAULT / 'library/sources' / (SID + '.json'))
chapters = {c['chapter_id']: c for r in source['revisions'] if r['revision'] == source['revision'] for c in r['chapters']}
cards = [read(p) for folder, _ in KINDS.values() for p in sorted((VAULT / 'library' / folder).glob('*.json'))]
cards = [a for a in cards if any(e.get('source_id') == SID for e in a['evidence'])]
assets = {a['asset_id']: a for a in cards}
graph = read(VAULT / 'library/sources' / SID / 'plot-graph.json')
by_id = {n['id']: n for n in graph['nodes']}
edges_by_id = {e['id']: e for e in graph['edges']}
volumes = [n for n in graph['nodes'] if n['kind'] == 'volume']
book_threads = [t for t in graph['threads'] if t['id'].startswith('book-')]

if __name__ == '__main__':
    main()
