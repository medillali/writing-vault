"""签名前依据866、1169、1413新读后证，保留并纠正两项过早的未回收判断。"""
import hashlib
import json
from pathlib import Path

base = Path(__file__).parent/'tianxia-wushuang/audit/whole-book/local-v05-primary-review'
out = base/'adjudications-local-v05-part05.json'
before = base/'primary-before/adjudications-local-v05-part05-before-terminal-receipts.json'
assert not before.exists()
before.parent.mkdir(exist_ok=True)
before.write_bytes(out.read_bytes())
decisions_path = base/'decisions-v05-part05.json'
rows = json.loads(decisions_path.read_text(encoding='utf-8'))
replacement = {
 'v05-local-local_historical_questions-045-02': ['answered','return-to-guild-explicitly-confirmed-later','837开放返门后月仍离开；1413叙述明确“月光石重回古剑之后”且讲众人让装/法攻次连，已是归队后证。1314救出与正式归队分层，未展示单独入会系统不等她始终未返，不补虚构点击镜头。',[837,1413]],
 'v05-local-local_historical_questions-053-01': ['answered','specific-spear-later-possession-and-use','845交连保管并拟赠何，866陆与连/明月明确何已拿七星琉璃枪，1169原文L94329何实际持枪输出，足证本物后来交到并使用。具体递交场面省略，不因缺一幕仍判未回收，也不拿另一面特兰盾替此枪。',[845,866,1169]],
}
changed = []
for index, row in enumerate(rows):
    if row[0] in replacement:
        changed.append(row[0])
        rows[index] = [row[0], *replacement[row[0]]]
assert set(changed) == set(replacement)
(base/'primary-before/decisions-v05-part05-before-terminal-receipts.json').write_bytes(decisions_path.read_bytes())
decisions_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
# 由原构建器重新核验全部后证已读记录；输出旧版本另存，不把过时结论留在活动批。
out.unlink()
print(json.dumps({'corrections': changed, 'before_sha256': hashlib.sha256(before.read_bytes()).hexdigest()}, ensure_ascii=False))
