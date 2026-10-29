"""发布导航必须区分全量研究与尚未重整的剧情树。"""
from pathlib import Path
P=Path(__file__).resolve().parent/'catalog-stage/书库'
for title in ['网游之天下无双','斩龙']:
    text=(P/'按书名'/title/'README.md').read_text(encoding='utf-8')
    assert '全量研究已保存' in text
    assert '开篇研究和建档不标成全书完成' not in text, title+'被错误回退为开篇研究'
    assert '全书剧情树仍待重整' in text
text=(P/'按书名/网游之纵横天下/README.md').read_text(encoding='utf-8')
assert '47位人物主档' in text and '完整人物库' in text
print('导航范围与最新人物/地图入口正确')
