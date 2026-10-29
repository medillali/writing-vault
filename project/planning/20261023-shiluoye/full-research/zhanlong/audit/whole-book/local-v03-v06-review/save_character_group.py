"""仅装配本人手写人物弧与固定来源，已交组不覆写。"""
from pathlib import Path
import json,hashlib,sys,datetime
sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent;A=H.parent;R=Path('C:/Users/Administrator/Documents/ChatGPT/Novel');F=R/'writing-vault/library/reports/zhanlong';B=A.parents[1]
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
g=int(sys.argv[1]);authored=load(H/f'character-authored-group{g:02d}.json');p=A/f'character-arcs-part{g:02d}.json';assert not p.exists()
source=load(B/'source.json');ch={int(c['chapter_id'][3:]):c for c in source['chapters']}
inputs=load(A/'character-arc-input-manifest.json')['sha256'].copy()
kin=F/'audit/priority-corrections-dongcheng-kinship.json';assert sha(kin)=='90760c6c4926e9dc6047fc4c82119d61155dfc47857ae7cc954dc073b03c7e85';inputs[kin.relative_to(R).as_posix()]=sha(kin)
if g>=4:
 fox=F/'audit/priority-corrections-fox-identity.json';assert sha(fox)=='b3773c8687b85a34f8051e925c08974aec274663919c7c2de90d273e236fcb02';inputs[fox.relative_to(R).as_posix()]=sha(fox)
if g>=7:
 wang=F/'audit/priority-corrections-wang-identity.json';assert sha(wang)=='f1eb93aeb09d4dd5b1ee542610b0e4a734b224da6520a10bd758686352b79f0e';inputs[wang.relative_to(R).as_posix()]=sha(wang)
for rel,s in inputs.items():assert sha(R/rel)==s,(rel,s)
def volume(n):return next(v for v,end in enumerate([251,504,753,968,1179,1386],1) if n<=end)
rows=[]
for old in authored:
 row={k:v for k,v in old.items() if k not in ['raw_refs','evidence_overrides']};refs=[]
 for n in old['raw_refs']:
  c=ch[n];v=volume(n);path=F/f'vol{v:02d}-cards.json'
  access='direct-initial-assigned-full-text' if 505<=n<=653 or 1180<=n<=1386 else 'derived-formal-character-and-handoff-interface'
  if n==139:access='targeted-full-indexed-chapter-reread';path=kin
  if row['audit_id']=='character-arc-047' and n in [445,499,500,1199]:access='direct-source-identity-boundary-check';path=wang
  lo,hi=c['start_line'],c['end_line']
  if row['audit_id']=='character-arc-047' and n in [445,499,500,1199]:lo,hi={445:(37035,37043),499:(40992,40992),500:(41038,41043),1199:(87375,87384)}[n]
  if g==8:
   path=F/f'vol{v:02d}-chapter-notes.jsonl'
   access='direct-initial-assigned-full-text-and-current-note-check' if 1180<=n<=1386 else 'derived-formal-complete-four-column-row'
   override=old.get('evidence_overrides',{}).get(str(n),{})
   lo,hi=override.get('start_line',lo),override.get('end_line',hi)
   access=override.get('access_level',access)
  refs.append(dict(source_id=source['source_id'],revision=source['revision'],chapter_id=c['chapter_id'],start_line=lo,end_line=hi,claim_kind='fact',access_level=access,research_path=path.relative_to(R).as_posix(),research_sha256=sha(path)))
 row.update(evidence=refs,actual_reviewer='zongheng_vol05_full',review_status='draft',reading_attribution='本人原始全文为卷三505—653及卷六1180—1386；卷三654—753为primary，卷1/2/4/5按原reader。其他卷在本次实际完整接读所列人物接口/交接和必要原文定位后派生，不冒个人全书原文重读；139另本次整章核收养链。')
 rows.append(row)
 assert all(row[k] for k in ['audit_id','name','initial_comparison_stage','key_decisions','costs','terminal_state','evidence_boundaries','evidence'])
out=dict(status='stable_group_draft_pending_primary_review',scope='《斩龙》六卷人物终点派生审计稳定分组；交付后冻结，未经primary批准不改已交组。',source_id=source['source_id'],revision=source['revision'],group_number=g,actual_reviewer='zongheng_vol05_full',formal_input_sha256=inputs,characters=rows)
dump(p,out)
md=[f'# 《斩龙》人物弧终点评定第{g:02d}组','','待primary逐项文学主审；这是各原读者材料的派生研究，不称一人全书原文重读。固定输入SHA与完整证据在同名JSON；之后总稿须与本组人物对象逐值一致。','']
for row in rows:
 md += ['## '+row['audit_id']+' '+row['name'],'']
 for label,k in [('起点','initial_comparison_stage'),('关键选择','key_decisions'),('成本','costs'),('终点','terminal_state'),('证据边界','evidence_boundaries')]:md += [label+'：'+row[k],'']
 md += ['来源：'+'；'.join(f"raw{int(e['chapter_id'][3:])} L{e['start_line']}—{e['end_line']}" for e in row['evidence']),'']
p.with_suffix('.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
receipt=dict(status='structure_and_source_bounds_checked_not_semantic_approval',group=g,count=len(rows),audit_ids=[x['audit_id'] for x in rows],json_sha256=sha(p),md_sha256=sha(p.with_suffix('.md')),input_manifest_sha256=sha(A/'character-arc-input-manifest.json'),additional_priority_input_sha256={k:s for k,s in inputs.items() if k.endswith(('dongcheng-kinship.json','fox-identity.json','wang-identity.json'))},authored_sha256=sha(H/f'character-authored-group{g:02d}.json'),evidence_count=sum(len(x['evidence']) for x in rows),notes_and_formal_unchanged=True)
dump(A/f'character-arcs-part{g:02d}-validation.json',receipt);print(json.dumps(receipt,ensure_ascii=False,indent=2))
