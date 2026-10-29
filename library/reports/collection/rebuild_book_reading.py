"""依据正式主档重建单书中文阅读页；不读取小说TXT，不改变研究和用户字段。"""
from pathlib import Path
from collections import Counter
import hashlib
import html
import json
import re
import sys

HERE = Path(__file__).resolve().parent
VAULT = HERE.parents[2]
KINDS = {'character': ('characters', '人物卡'), 'scene': ('scenes', '场景卡'), 'pattern': ('patterns', '机制卡')}
LABELS = {
    'summary': '概述', 'name': '姓名', 'aliases': '别名', 'volume': '所属卷',
    'goal': '目标', 'goals': '目标', 'obstacle': '障碍', 'constraints': '限制',
    'conflict': '矛盾与限制', 'choice': '行动与选择', 'decisions': '重要决策',
    'consequence': '后果', 'state_change': '状态变化', 'arc_change': '人物变化',
    'relationships': '人物关系', 'relationship_direction': '关系方向',
    'knowledge_limits': '认知边界', 'knowledge_boundary': '认知边界',
    'steps': '因果步骤', 'causal_steps': '因果步骤', 'why_it_works': '为何有效',
    'applicability': '适用条件', 'failure_mode': '失效条件', 'limits': '使用边界',
    'originality_transform': '原创转换', 'coverage_note': '覆盖边界',
    'fact': '原文事实', 'facts': '原文事实', 'inference': '研究推断',
    'inferences': '研究推断', 'stage_state': '阶段状态', 'evidence': '证据定位',
    'unknowns': '未决问题', 'unresolved': '未决问题', 'identity_notes': '身份辨析',
    'observer': '观察者', 'belief': '当时认知', 'state': '认知状态',
    'claim_kind': '判断类型', 'decision_pattern': '决策方式',
    'relationship_directions': '关系方向', 'key_decisions': '重要决策',
    'stage_changes': '阶段变化', 'stage_change': '阶段变化',
    'fact_scope': '事实与解释边界', 'knowledge': '人物与读者认知',
    'not_user_style_rule': '尚非用户风格规则', 'literary_limits': '文学取舍与边界',
    'limitations': '限制', 'directional_relationships': '关系方向', 'change': '阶段变化',
    'voice_and_evidence_boundary': '声音与证据边界', 'failure_conditions': '失效条件',
    'core_original_chapter': '原书核心章号', 'transfer_question': '迁移时要回答的问题',
    'content': '当时认知内容', 'stage_note': '卷末阶段说明',
}
CLAIMS = {'fact': '原文事实', 'inference': '研究推断', 'synthesis': '抽象综合', 'plan': '计划'}
STATES = {'open': '未回收', 'partial': '部分回收', 'resolved': '已回收', 'abandoned': '已放弃', 'unknown': '未确认'}
RELATIONS = {'cause': '因果', 'setup': '铺垫', 'reveal': '揭示', 'misdirection': '误导', 'reversal': '转折', 'echo': '呼应', 'payoff': '回收'}


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def text(value):
    return re.sub(r'([\\`*\[\]])', r'\\\1', html.escape(str(value), quote=False))


def cell(value):
    return text(value).replace('|', '&#124;').replace('\n', '<br>')


def build(slug):
    config = read(HERE / 'catalog-config.json')
    sid, book = next((sid, b) for sid, b in config['books'].items() if b['slug'] == slug)
    source = read(VAULT / 'library/sources' / (sid + '.json'))
    revision = source['revision']
    chapters = {c['chapter_id']: c for r in source['revisions'] if r['revision'] == revision for c in r['chapters']}
    evidence_sources = {(sid, revision): (book['title'], chapters)}
    base = HERE.parent / slug
    out = base / 'reading'
    written = []

    def save(path, lines):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('\n'.join(lines).rstrip() + '\n', encoding='utf-8')
        written.append(path)

    def evidence(items):
        lines = ['| 来源与章节 | 行号 | 判断类型 |', '|---|---|---|']
        for e in items:
            span = f"{e['start_line']}—{e['end_line']}" if 'start_line' in e else '章节范围'
            key = (e.get('source_id', sid), e.get('revision', revision))
            if key not in evidence_sources:
                record = read(VAULT / 'library/sources' / (key[0] + '.json'))
                indexed = {c['chapter_id']: c for r in record['revisions'] if r['revision'] == key[1] for c in r['chapters']}
                evidence_sources[key] = (config['books'].get(key[0], {}).get('title', key[0]), indexed)
            title, indexed = evidence_sources[key]
            label = title + ' · ' + e.get('chapter_id', '') + ' ' + indexed.get(e.get('chapter_id'), {}).get('title', '')
            lines.append(f"| {cell(label)} | {span} | {CLAIMS.get(e.get('claim_kind'), '随所在条目')} |")
        return lines + ['']

    def value_lines(key, value, level=2):
        lines = ['#' * min(level, 6) + ' ' + LABELS.get(key, key), '']
        if key == 'evidence' and isinstance(value, list):
            return lines + evidence(value)
        if isinstance(value, dict):
            for k, v in value.items():
                lines += value_lines(k, v, level + 1)
        elif isinstance(value, list):
            if all(not isinstance(v, (dict, list)) for v in value):
                lines += ['- ' + text(v) for v in value] + [''] if value else ['未另列。', '']
            else:
                for i, item in enumerate(value, 1):
                    if isinstance(item, dict):
                        lines += ['#' * min(level + 1, 6) + f' 条目{i}', '']
                        for k, v in item.items():
                            lines += value_lines(k, v, level + 2)
                    else:
                        lines += [text(item), '']
        else:
            lines += [text(value) if value not in ('', None) else '未填写。', '']
        return lines

    cards = []
    for folder, _ in KINDS.values():
        for path in sorted((VAULT / 'library' / folder).glob('*.json')):
            card = read(path)
            if any(e.get('source_id') == sid for e in card.get('evidence', [])):
                cards.append(card)
    assets = {a['asset_id']: a for a in cards}
    counts = Counter(c['asset_type'] for c in cards)
    for card in cards:
        folder, name = KINDS[card['asset_type']]
        aid = card['asset_id']
        review = {'draft': '研究草稿，待用户审阅', 'reviewed': '已审阅', 'approved': '已认可'}.get(card['review_status'], card['review_status'])
        lines = ['# ' + text(card['title']), '', f'[返回{name}目录](../{folder}.md) · [本书阅读首页](../README.md)', '',
                 f"类型：{name} · 版本：{card['revision']} · {'来源分析' if card['scope'] == 'source-analysis' else '可迁移机制'}", '',
                 f"审阅状态：{text(review)} · 收藏：{'是' if card['favorite'] else '否'}", '']
        for key, value in card['content'].items():
            lines += value_lines(key, value)
        lines += ['## 全部引用定位', ''] + evidence(card.get('evidence', []))
        if card.get('derived_from'):
            lines += ['## 采用的来源素材版本', '']
            for ref in card['derived_from']:
                target = assets.get(ref['asset_id'])
                label = text(target['title']) if target else ref['asset_id']
                link = f"[{label}]({ref['asset_id']}.md)" if target else f"`{label}`"
                lines += [f"- {link}，采用版本{ref['revision']}；当前卡页面显示其当前版本。"]
            lines += ['']
        lines += ['## 个人笔记', '', text(card.get('user_notes', '')) or '尚无个人笔记。', '',
                  '标签：' + text('、'.join(card.get('tags', []))), '',
                  f'[JSON主档](../../../../{folder}/{aid}.json)', '',
                  '本页为主档的阅读副本。个人笔记、收藏与审阅状态通过资料库接口保存；分卷研究不是用户已认可的写作规则。']
        save(out / 'cards' / (aid + '.md'), lines)
    for kind, (folder, name) in KINDS.items():
        group = sorted((a for a in cards if a['asset_type'] == kind), key=lambda a: (str(a['content'].get('volume', '')), a['title']))
        lines = [f'# 《{book["title"]}》{name}目录', '', '[本书阅读首页](README.md)', '',
                 f'共{len(group)}张阶段卡。相同人物在不同卷的卡片保留各阶段认知，不按卡数计算独立人物。', '',
                 '| 卡片 | 概述 |', '|---|---|']
        lines += [f"| [{cell(a['title'])}](cards/{a['asset_id']}.md) | {cell(a['content']['summary'])} |" for a in group]
        save(out / (folder + '.md'), lines)

    volumes = []
    for path in sorted(base.glob('vol[0-9][0-9]-graph.json')):
        prefix = path.name.split('-')[0]
        graph = read(path)
        volumes.append(prefix)
        lines = ['# ' + text(graph['title']), '', f'[本书阅读首页](../README.md) · [本卷九维报告](../../{prefix}.md)', '',
                 '以下是本卷当时的事件、认知与剧情线状态；不能将其视为后卷或全书终点结论。', '', '## 事件与认知', '']
        for node in graph['nodes']:
            lines += ['### ' + text(node['title']), '', f"判断类型：{CLAIMS.get(node.get('claim_kind'), '随所在条目')}", '', text(node.get('summary', '')), '']
            people = [assets[c] for c in node.get('characters', []) if c in assets]
            if people:
                lines += ['人物：' + '、'.join(f"[{text(c['title'])}](../cards/{c['asset_id']}.md)" for c in people), '']
            for key in ['knowledge']:
                if node.get(key):
                    lines += value_lines(key, node[key], 4)
            lines += evidence(node.get('evidence', []))
        by_id = {n['id']: n for n in graph['nodes']}
        lines += ['## 因果、铺垫与回收', '']
        for edge in graph['edges']:
            lines += ['### ' + text(edge.get('label', edge['id'])), '',
                      text(by_id[edge['from']]['title']) + ' → **' + RELATIONS.get(edge['kind'], edge['kind']) + '** → ' + text(by_id[edge['to']]['title']), '',
                      f"判断类型：{CLAIMS.get(edge.get('claim_kind'), '随所在条目')}", ''] + evidence(edge.get('evidence', []))
        lines += ['## 本卷末剧情线状态', '']
        for thread in graph['threads']:
            lines += ['### ' + text(thread['title']), '', '状态：' + STATES[thread['status']], '', text(thread.get('question', '')), '']
            for key in ['stage_note', 'resolution_note']:
                if thread.get(key):lines += [text(thread[key]), '']
            if thread.get('resolution_evidence'):
                lines += evidence(thread['resolution_evidence'])
            elif thread.get('evidence'):
                lines += evidence(thread['evidence'])
        save(out / 'plot' / (prefix + '.md'), lines)

    checkpoint_path = VAULT / 'exchanges/runs' / ('run-deep-zongheng-tianxia-20261023.json' if slug == 'zongheng-tianxia' else f'run-deep-{slug}-20261025.json')
    checkpoint = read(checkpoint_path) if checkpoint_path.exists() else {}
    covered = len(checkpoint.get('completed_chapters', []))
    lines = [f'# 《{book["title"]}》研究阅读入口', '', '[本书研究总览](../README.md) · [多书资料目录](../../collection/README.md)', '',
             f'正式保存{len(volumes)}卷，检查点覆盖{covered}/{len(chapters)}个原索引片段；原索引含章前说明，正文阅读单元统计见多书目录。', '',
             '卡片、逐卷解释与终点审计分别保存；实际完成范围以正式检查点和验收记录为准。', '',
             f"- [人物卡：{counts['character']}张](characters.md)",
             f"- [场景卡：{counts['scene']}张](scenes.md)",
             f"- [机制卡：{counts['pattern']}张](patterns.md)", '',
             '| 卷 | 九维报告 | 剧情与证据 | 阅读日志 |', '|---|---|---|---|']
    for prefix in volumes:
        lines += [f'| {prefix} | [报告](../{prefix}.md) | [阶段结构](plot/{prefix}.md) | [实读范围](../{prefix}-read-log.json) |']
    for filename, label in [('book-synthesis.md', '全书综合'), ('question-ledger.md', '疑点账本'), ('验收说明.md', '验收说明')]:
        if (base / filename).exists():
            lines += ['', f'[{label}](../{filename})']
    lines += ['', '原文独立保管；本页不含原小说全文。生成阅读副本不代表Git已推送或Space、记忆已同步。', '',
              '从资料库根目录运行 `python library/reports/collection/rebuild_book_reading.py ' + slug + '` 可根据主档重建本目录。']
    save(out / 'README.md', lines)
    manifest = {'source_id': sid, 'source_revision': revision, 'cards': dict(counts), 'formal_volumes': volumes,
                'checkpoint_indexed_segments': covered,
                'pages': {p.relative_to(out).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in written}}
    (out / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return {k: v for k, v in manifest.items() if k != 'pages'} | {'markdown_pages': len(written)}


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    print(json.dumps(build(sys.argv[1]), ensure_ascii=False))
