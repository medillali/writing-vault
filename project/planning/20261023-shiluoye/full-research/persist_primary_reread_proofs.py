"""保存既已实际完成的主审复核记录，不生成或扩大正文覆盖。"""
from pathlib import Path
import hashlib, json
B = Path(__file__).resolve().parent
S = B/'zhanlong'
R = B.parents[2]
source = json.loads((S/'source.json').read_text(encoding='utf-8'))
index = {c['chapter_id']:c for c in source['chapters']}
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def digest(data): return hashlib.sha256(data).hexdigest()
def write_new_or_same(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists(): assert path.read_bytes() == data, str(path)
    else: path.write_bytes(data)
facts = {
    743: ['公告十小时内可争夺，不是十小时后才能给；尚余9h17时主提前交抹盾，并借神将膝增加怒量，群狮120怒实际施放。', '最初主许自己先守十小时与危机中提前让盾分时，不能据提前交付制造装备规则违规。'],
    981: ['当章生日者为宋寒；主拍卖买匕并告知领用，不等后续明确实装。', '薛柔署名纸和XTS钥匙由宋亲收，车位置为纸述，未演亲自提车。'],
    1041: ['主实际摘花鞠躬并看佩儿碑；帝命迁柩、准帝王礼，工匠已动工。', '这足以回应早期立碑存在，不把1034会猎湖旁另一碑的主猜测并成同一处已证。'],
    1110: ['旧神将战膝由倾浅代收准备转李牧，不能记为李牧已实穿。', '薛柔归队后收旧装备的交接与个人恋爱结果分开。'],
    1181: ['问剑五千万成交星辰之戒并实际戴上，扣5%后四千七百五十万到主账户，林与东城各实收1584万。', '取得、佩戴与坠星辰450%实测是不同证据，不能由成交补技能测试。'],
    1182: ['持续建设和等级目标按当章实际状态保存，不能从未来目标直接倒写工程已全成。', '此章已完整复读，复读与原团队全文覆盖重叠，不产生额外唯一章节。'],
    1183: ['新建龙谷有系统100%完成通知，建设从规划进入实成状态。', '完成工程与各条龙逐名封格不等同。'],
    1194: ['龙谷生态和龙神殿已形成，不能继续记作仅有设想。', '主第三次入天界仍未取得神格认可，不能将1264失败或1272后成提前写到此时。'],
    1386: ['鬼城败退中五十万NPC返不足十八万，与返千人以下的玩家分群统计；御林七万、天穹三万为各自后态。', '三日后镇天关四十万兵和两千余炮已实建；傲天新版本二十四小时后、KILLS南京行程仍为未来。', '白墨颜数字角色三日后实际上线发言，雷的记忆载体仍电话方案，不能当现实肉身复活。']
}
full = []
for raw, rows in facts.items():
    cid = f'ch-{raw:04d}'; ch = index[cid]
    full.append(dict(chapter_id=cid, start_line=ch['start_line'], end_line=ch['end_line'],
                     full_text_read=True, facts=rows))
partials = [
    (181,16175,16201,'问剑邀河南洛阳、让太师爷领教，主口头应而心中不想；1163—1165后赴北辰家另有后证。'),
    (528,42760,42830,'李牧死于剑锋寒；林先被问剑控制再受弓法集火而死；主本人由系统记问剑杀。'),
    (530,42940,42963,'初版王域所有友方目标句式里的自身可指各受益目标，不足判仅佩戴者回血。'),
    (541,43770,43784,'初版王域实际群回已演；此处不等1109强化参数。'),
    (740,57970,57980,'公告十小时内争夺限制，不是等十小时之后才准交付。'),
    (744,58210,58224,'抹茶在提前交盾后实际参与盾技和战斗，保与743连续。'),
    (1109,81317,81329,'强化王域条文和队友释义分渠道保留，强化数值不倒灌530初版。'),
    (1174,85717,85727,'五千龙城铁骑实集；主回顾归功流霜杀罗林及旧友心理，不覆盖833系统问剑末刀。')
]
parts=[]
for raw,a,z,note in partials:
    cid=f'ch-{raw:04d}'; ch=index[cid]
    assert ch['start_line'] <= a <= z <= ch['end_line']
    parts.append(dict(chapter_id=cid,start_line=a,end_line=z,full_text_read=False,note=note))
note = dict(source_id=source['source_id'],revision=source['revision'],reader='primary',
    complete_book=False, count_as_additional_unique_coverage=False, original_first_reader_unchanged=True,
    method='仅登记前述会话内已经实际显示全文或限定原行片段后的手写复核；程序只检查来源章界，不代替阅读。',
    full_chapter_rereads=full, partial_source_rereads=parts,
    derived_rereads=[dict(chapter_ids=['ch-1163','ch-1164','ch-1165'],reader='primary',
        method='完整四栏派生笔记复读，原文读者仍reader4',full_text_read=False,
        fact='实际赴河南、接机、进入北辰家拜北辰观和实练火甲；后证回应早拜访邀请，不必要求旧地名再次逐字出现。')])
stage=S/'primary-additional-rereads-20261026.json'
data=(json.dumps(note,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
write_new_or_same(stage,data)
files = [S/n for n in ['primary-source-crosschecks.json','primary-focused-rereads.json',
    'primary-wuhan-reread.json','primary-528-reread.json','primary-additional-rereads-20261026.json']]
files += sorted((S/'primary-ending-reread').glob('*.json'))
dest=R/'writing-vault/library/reports/zhanlong/audit/primary-rereads'
records=[]
for p in files:
    value=read(p)
    if 'source_id' in value: assert value['source_id']==source['source_id']
    if 'revision' in value: assert value['revision']==source['revision']
    rel=p.relative_to(S); content=p.read_bytes();write_new_or_same(dest/rel,content)
    records.append(dict(path=rel.as_posix(),sha256=digest(content),bytes=len(content)))
manifest=dict(status='existing-actual-reread-proofs-preserved',reader='primary',files=records,
    full_book_personal_reread=False,unique_coverage_added=0,
    boundary='仅保存重叠复读证明，不改变首次分工署名，不等全书审计通过或完整资料库备份。')
write_new_or_same(dest/'manifest.json',(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
print(json.dumps(dict(status=manifest['status'],files=len(records),unique_coverage_added=0),ensure_ascii=False))
