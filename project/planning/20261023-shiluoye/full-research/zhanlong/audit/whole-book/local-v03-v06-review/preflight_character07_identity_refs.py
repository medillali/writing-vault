from pathlib import Path
import json,hashlib,sys
sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent;A=H.parent;p=A/'character-arcs-part07.json';m=p.with_suffix('.md');v=A/'character-arcs-part07-validation.json';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
b=H/'corrections/character07-unsubmitted-identity-ref-preflight';b.mkdir(parents=True,exist_ok=False)
for q in [p,m,v]:(b/q.name).write_bytes(q.read_bytes())
d=json.loads(p.read_text(encoding='utf-8'));row=d['characters'][-1];assert row['audit_id']=='character-arc-047';changes=[]
for e in row['evidence']:
 n=int(e['chapter_id'][3:])
 if n in [445,499,500,1199]:
  lo,hi={445:(37035,37043),499:(40992,40992),500:(41038,41043),1199:(87375,87384)}[n];changes.append(dict(chapter_id=e['chapter_id'],before=[e['start_line'],e['end_line']],after=[lo,hi]));e['start_line']=lo;e['end_line']=hi
dump(p,d);md=['# 《斩龙》人物弧终点评定第07组','','待primary逐项文学主审；这是各原读者材料的派生研究，不称一人全书原文重读。固定输入SHA与完整证据在同名JSON；之后总稿须与本组人物对象逐值一致。','']
for row in d['characters']:
 md+=['## '+row['audit_id']+' '+row['name'],'']
 for label,k in [('起点','initial_comparison_stage'),('关键选择','key_decisions'),('成本','costs'),('终点','terminal_state'),('证据边界','evidence_boundaries')]:md +=[label+'：'+row[k],'']
 md +=['来源：'+'；'.join(f"raw{int(e['chapter_id'][3:])} L{e['start_line']}—{e['end_line']}" for e in row['evidence']),'']
m.write_text('\n'.join(md)+'\n',encoding='utf-8');rec=json.loads(v.read_text(encoding='utf-8'));rec['json_sha256']=sha(p);rec['md_sha256']=sha(m);rec['additional_priority_input_sha256']={k:s for k,s in d['formal_input_sha256'].items() if k.endswith(('dongcheng-kinship.json','fox-identity.json','wang-identity.json'))};dump(v,rec);dump(A/'character-arcs-part07-preflight-delta.json',dict(scope='首次交付前把047身份四ref收窄至实际核读定位；文学字段全保',changes=changes,old_json_sha256=sha(b/p.name),new_json_sha256=sha(p)));print(json.dumps(rec,ensure_ascii=False,indent=2))
