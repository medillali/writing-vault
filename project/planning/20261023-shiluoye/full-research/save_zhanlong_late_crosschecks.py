"""记录本轮确已执行的定向复读，不扩大团队唯一全文覆盖。"""
from pathlib import Path
import datetime, hashlib, json
B = Path(__file__).resolve().parent
R = B.parents[2]
source = json.loads((B / 'zhanlong/source.json').read_text(encoding='utf-8'))
chapters = {c['chapter_id']: c for c in source['chapters']}
rows = []
for n, full, start, end, reason in [
    (938, True, 70223, 70277, 'L70230罗嗣已分得半矿所制物资；纠正仅有比例而未见执行的漏后证。'),
    (1240, True, 89895, 89961, '武魂后改称炼魂，百万军与问剑魂面板已经出现。'),
    (1241, True, 89962, 90011, '问剑魂/方歌阙魂真实作战，本体同时在场；同义漏配撤回。'),
    (1295, True, 93676, 93734, 'L93721为兰蔻再斩上位格已有后证，炼成仍未演。'),
    (1374, True, 98779, 98838, '核实御林14万、秋收10万为不同军队。'),
    (975, False, 72491, 72509, 'L72503特赦军团上限至20万，授权与实编分开。'),
    (1221, False, 88760, 88766, '全副本通关与S7三带二计划分时。'),
    (1266, False, 91586, 91631, '235级87%为主角；东城月已回补给并在东桥相聚。'),
    (1192, False, 86860, 86869, '燕请求举荐燕本人替百里宁，不是荐百里宁。'),
    (1234, False, 89535, 89546, '燕战时代理任命。'),
    (1244, False, 90159, 90170, '燕正式长风统领及徽章。'),
]:
    cid = f'ch-{n:04d}'
    c = chapters[cid]
    assert c['start_line'] <= start <= end <= c['end_line']
    assert not full or (start == c['start_line'] and end == c['end_line'])
    rows.append(dict(chapter_id=cid, start_line=start, end_line=end, full_text_read=full, reason=reason))
record = dict(source_id=source['source_id'], revision=source['revision'], actual_reader='primary',
              recorded_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
              scope='实际工具输出逐行阅读后的补充核源记录，不由本脚本产生阅读。原各卷全文读者保持不变。',
              additional_unique_chapters=0, reads=rows, user_approval=False)
dest = R / 'writing-vault/library/reports/zhanlong/audit/primary-rereads/late-crosschecks-20261026.json'
assert not dest.exists()
dest.write_text(json.dumps(record, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps(dict(full_chapter_rereads=sum(r['full_text_read'] for r in rows), limited_rereads=sum(not r['full_text_read'] for r in rows),
                      additional_unique_chapters=0, sha256=hashlib.sha256(dest.read_bytes()).hexdigest()), ensure_ascii=False))
