"""沿用《超级骷髅兵》的字体测量、配色和SVG卡片规范；不读取其小说数据。"""
from pathlib import Path
from functools import lru_cache
import html, math, re
INK, MUTED, BLUE, PURPLE = '#172b46', '#51637a', '#2563a6', '#7850b5'
GREEN, AMBER, RED = '#087f65', '#a5650b', '#bf3b42'
STATE = {'resolved': ('已回收', GREEN, '#e6f5ef'), 'partial': ('部分回收', AMBER, '#fff3dc'), 'open': ('未回收', RED, '#fcecef')}
REL = {'cause': ('因果', '#147d8b'), 'setup': ('铺垫', PURPLE), 'reveal': ('揭示', '#a5650b'),
       'misdirection': ('误导', '#bf3b75'), 'reversal': ('转折', '#c05c25'), 'echo': ('呼应', '#537aa0'), 'payoff': ('回收', GREEN)}
CLAIM = {'fact': '事实', 'inference': '研究推断', 'synthesis': '研究综合', 'plan': '计划'}
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


STATE.update({'unknown':('原文未明',AMBER,'#fff3dc'),'abandoned':('明确中断',RED,'#fcecef')})
REL['sequence']=('阅读衔接',BLUE)
CLAIM['reading_order']='阅读顺序，非因果'
def title(t):return t['title']
def vol(n):return n['stage_number']
def evidence(n):return '；'.join(f"{e['chapter_id']} L{e['start_line']}–{e['end_line']}" for e in n.get('evidence',[]))
def conclusion(t):return t['resolution_note']
