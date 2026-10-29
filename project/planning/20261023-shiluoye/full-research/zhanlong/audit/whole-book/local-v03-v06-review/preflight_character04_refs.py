"""首次交付前自核：去掉未支撑的548，补凫水实际技能出处，不触已交组。"""
from pathlib import Path
import json,hashlib,copy,sys
sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent;A=H.parent;R=Path('C:/Users/Administrator/Documents/ChatGPT/Novel');F=R/'writing-vault/library/reports/zhanlong';B=A.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=A/'character-arcs-part04.json';m=p.with_suffix('.md');v=A/'character-arcs-part04-validation.json';a=H/'character-authored-group04.json';before=load(p);b=H/'corrections/character04-unsubmitted-preflight';b.mkdir(parents=True,exist_ok=False)
for x in [p,m,v,a]:(b/x.name).write_bytes(x.read_bytes())
d=copy.deepcopy(before);auth=load(a);d['characters'][1]['key_decisions']=d['characters'][1]['key_decisions'].replace('602以后反魔壳','后来反魔壳');auth[1]['key_decisions']=d['characters'][1]['key_decisions']
chs={int(x['chapter_id'][3:]):x for x in load(B/'source.json')['chapters']}
def ref(n,vol):
 c=chs[n];q=F/f'vol{vol:02d}-cards.json';return dict(source_id=d['source_id'],revision=d['revision'],chapter_id=c['chapter_id'],start_line=c['start_line'],end_line=c['end_line'],claim_kind='fact',access_level='direct-initial-assigned-full-text' if 505<=n<=653 else 'derived-formal-character-and-handoff-interface',research_path=q.relative_to(R).as_posix(),research_sha256=sha(q))
d['characters'][1]['evidence'] += [ref(611,3),ref(614,3)];auth[1]['raw_refs'] += [611,614]
idx=next(i for i,x in enumerate(d['characters'][6]['evidence']) if x['chapter_id']=='ch-0548');d['characters'][6]['evidence'][idx]=ref(468,2);auth[6]['raw_refs']=[468 if n==548 else n for n in auth[6]['raw_refs']]
dump(p,d);dump(a,auth)
md=['# 《斩龙》人物弧终点评定第04组','','待primary逐项文学主审；这是各原读者材料的派生研究，不称一人全书原文重读。固定输入SHA与完整证据在同名JSON；之后总稿须与本组人物对象逐值一致。','']
for row in d['characters']:
 md+=['## '+row['audit_id']+' '+row['name'],'']
 for label,k in [('起点','initial_comparison_stage'),('关键选择','key_decisions'),('成本','costs'),('终点','terminal_state'),('证据边界','evidence_boundaries')]:md +=[label+'：'+row[k],'']
 md +=['来源：'+'；'.join(f"raw{int(e['chapter_id'][3:])} L{e['start_line']}—{e['end_line']}" for e in row['evidence']),'']
m.write_text('\n'.join(md)+'\n',encoding='utf-8');rec=load(v);rec.update(json_sha256=sha(p),md_sha256=sha(m),authored_sha256=sha(a),evidence_count=sum(len(x['evidence']) for x in d['characters']),additional_priority_input_sha256={k:x for k,x in d['formal_input_sha256'].items() if k.endswith(('dongcheng-kinship.json','fox-identity.json'))});dump(v,rec)
dump(A/'character-arcs-part04-preflight-delta.json',dict(scope='首次交付前自核，未交原稿精确字节保留',before_sha256=sha(b/p.name),after_sha256=sha(p),changes=['015 key_decisions去无证602起点，补611/614反魔实际出处','020 evidence误选548改为468近卫正式分盟'],source_notes='仅前期材料索引自核；原文覆盖归属不变'))
print(json.dumps(rec,ensure_ascii=False,indent=2))
