"""仅序列化逐项手写终评；不作关键词或模板语义判断。"""
import json,hashlib,collections
from pathlib import Path
P=Path(__file__).parent;A=P.parent;B=A.parent.parent;ROOT=B.parents[3]
POOL=json.loads((A/'local-question-pool.json').read_text(encoding='utf-8'))
S=json.loads((B/'source.json').read_text(encoding='utf-8'));CH={int(c['chapter_id'].split('-')[1]):c for c in S['chapters']}
def dump(path,x):path.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
stable_fields=['candidate_id','volume','original_path','original_field','original_index','atomic_index','original_record','title','original_evidence']
scope=[{k:c[k] for k in stable_fields} for c in POOL['candidates'] if c['volume'] in [1,4]]
sp=P/'scope-freeze.json'
if not sp.exists():dump(sp,scope)
else:assert json.loads(sp.read_text(encoding='utf-8'))==scope,'原记录或稳定清单变化，须先核root'
def evidence(nums):return [{'source_id':S['source_id'],'revision':S['revision'],'chapter_id':CH[n]['chapter_id'],'start_line':CH[n]['start_line'],'end_line':CH[n]['end_line'],'claim_kind':'fact'} for n in dict.fromkeys(nums)]
def batch(volume,number,start,manual,access):
 cs=[c for c in scope if c['volume']==volume];selected=cs[start-1:start-1+len(manual)];assert 1<=len(manual)<=20
 assert [x[0] for x in manual]==[c['candidate_id'] for c in selected]
 rows=[]
 for c,(cid,status,domain,reason,nums) in zip(selected,manual):
  assert status in ['answered','partial','unknown','unrecovered'] and reason and nums
  rows.append({'candidate_id':cid,'original_question':c['title'],'original_record':c['original_record'],'original_location':{k:c[k] for k in ['volume','original_path','original_field','original_index','atomic_index']},'status':status,'audit_domain':domain,'rationale':reason,'later_chapters':list(dict.fromkeys(nums)),'later_evidence':evidence(nums),'actual_reviewer':'/root/zongheng_vol03_full','source_attribution':{'early_source':'本代理卷1前150片亲读/primary尾100片实际全文且本代理完整派生读笔记；卷4本人全部亲读。','later_source':access,'boundary':'后证查询为最终正式派生研究/原四栏或另记定向原文，不冒个人全书全文阅读。'}})
 f=A/f'adjudications-local-v{volume:02d}-batch{number:03d}.json';assert not f.exists(),'冻结批不可覆写'
 dump(f,rows)
 lines=[f'# 斩龙局部卷{volume}第{number}批（待primary逐项主审）','',f'冻结顺序{start}—{start+len(rows)-1}；原题/原记录未改。','',access,'']
 for i,r in enumerate(rows,start):
  lines += [f'## {i} {r["candidate_id"]}','','原题：'+r['original_question'],'',r['status']+' / '+r['audit_domain']+'：'+r['rationale'],'','后证：'+'；'.join(f'{e["chapter_id"]} L{e["start_line"]}—{e["end_line"]}' for e in r['later_evidence']),'']
 f.with_suffix('.md').write_text('\n'.join(lines),encoding='utf-8')
 receipt={'file':f.name,'sha256':sha(f),'count':len(rows),'start_onebased_offset':start,'end_onebased_offset':start+len(rows)-1,'scope_freeze_sha256':sha(sp),'status':'frozen-awaiting-primary','counts':dict(collections.Counter(r['status'] for r in rows))}
 dump(P/f'v{volume:02d}-batch{number:03d}-receipt.json',receipt)
 state=P/'reader-state.json';st=json.loads(state.read_text(encoding='utf-8')) if state.exists() else {'scope_total':840,'completed_candidate_ids':[],'v01_next_onebased_offset':1,'v04_next_onebased_offset':1,'batches':[],'synthesis_status':'not-started-awaiting-local-adjudication'}
 assert not(set(st['completed_candidate_ids']) & set(r['candidate_id'] for r in rows))
 st['completed_candidate_ids'] += [r['candidate_id'] for r in rows];st[f'v{volume:02d}_next_onebased_offset']=start+len(rows);st['batches'].append(receipt);dump(state,st)
 print(json.dumps(receipt,ensure_ascii=False))
