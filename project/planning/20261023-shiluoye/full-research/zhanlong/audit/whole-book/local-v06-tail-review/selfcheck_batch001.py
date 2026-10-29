import json,pathlib,hashlib
from save_tail_manual import Q,read,write,sha
p=Q/'adjudications-local-v06-tail-batch001.json';rows=read(p)
before=json.loads(json.dumps(rows[8],ensure_ascii=False))
rows[8]['rationale']='1263托交之后，1266林的中位飞升系统与本人回城状态确证取冬格成功。东1262已飞、1263得托格后，林在1266确以该链完成飞升，后续1281约东等五神同赴探寻、1290四友实际分款，又有东在凡界活动的后证，足答安全出境；不把1265提前概括的后来玩家组队写成本章东已相聚。无须另造寄存UI或把主背包被清除的鲁/空间格套在林格上。'
rows[8]['later_chapters']=[1262,1263,1264,1266,1281,1290]
allnotes={}
for f in (Q.parents[5]/'writing-vault/library/reports/zhanlong').glob('vol??-chapter-notes.jsonl'):
 for s in f.read_text(encoding='utf-8').splitlines():
  n=json.loads(s);allnotes[int(n['chapter_id'].split('-')[1])]=(f,n)
# 使用保存器相同的已读正式notes来源格式。
from save_tail_manual import F,ROOT
allnotes={}
for f in F.glob('vol??-chapter-notes.jsonl'):
 for s in f.read_text(encoding='utf-8').splitlines():
  n=json.loads(s);allnotes[int(n['chapter_id'].split('-')[1])]=(f,n)
ev=[]
for k in rows[8]['later_chapters']:
 f,n=allnotes[k];ev.append(dict(source_id=n['source_id'],revision=n['revision'],chapter_id=n['chapter_id'],start_line=n['start_line'],end_line=n['end_line'],claim_kind='fact',evidence_access='完整正式四栏派生；不转移原文实读归属',material_path=str(f.relative_to(ROOT)).replace('\\','/'),material_sha256=sha(f),source_reader=n.get('reader')))
rows[8]['later_evidence']=ev
write(Q/'batch001-pre-delivery-selfcheck-delta.json',dict(reason='交付前自核撤1265相聚误指，改按林系统及东后续实际凡界活动；尚未交primary签收。',before=before,after=rows[8]))
write(p,rows)
md=['# 《斩龙》卷六尾199候选终评草稿','独占原序[200:399]，本批assigned offset 0—19；待primary逐项主审。','']
for x in rows:md += [f"- **{x['candidate_id']}** · {x['status']} / {x['audit_domain']}",f"  原题：{x['title']}",f"  终评：{x['rationale']}",f"  后证raw：{', '.join(map(str,x['later_chapters']))}；派生保原reader。",'']
p.with_suffix('.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
st=read(Q/'reader-state.json');st['batches'][0]['sha256']=sha(p);write(Q/'reader-state.json',st);print(sha(p))
