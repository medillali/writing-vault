"""应用primary明确批准的三项炼魂后证及一项1369定位；其余逐值不变。"""
from pathlib import Path
import json,hashlib,shutil,collections
H=Path(__file__).resolve().parent;A=H.parent
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=A/'adjudications-local-v06-batch007.json';assert sha(p)=='5b1141b9e02e28e76521c71fe3588f7a7d52e853d96bc99b7e85cea8c8bffb9b'
before=load(p);after=json.loads(json.dumps(before));proposal=load(H/'batch007-mirror-evidence-proposal.json')
backup=H/'corrections'/'batch007-approved-mirror-and-source';backup.mkdir(parents=True,exist_ok=False)
for f in [p,p.with_suffix('.md'),H/'adjudications-local-v06-batch007-validation.json',H/'v06-batch007-source-check.json']:
 shutil.copy2(f,backup/f.name)
allowed={}
for change in proposal['changes']:
 r=next(x for x in after if x['candidate_id']==change['candidate_id'])
 for k,v in change['proposed_after'].items():r[k]=v
 allowed[r['candidate_id']]=change['allowed_fields']
r=next(x for x in after if x['candidate_id']=='v06-local-chapter_unresolved_index-0038-01')
e=next(e for e in r['later_evidence'] if e['chapter_id']=='ch-1369')
e.update(start_line=98452,end_line=98455,research_path='writing-vault/library/reports/zhanlong/audit/primary-rereads/canglan-1369-addendum.json',research_sha256='daaaa7afc722444c2f8584a31ed18b92fb3111bcb63d561711463fe826fd0a67',research_reader='primary',research_reading_scope='primary实际全文复读；本裁定者本次只核相关源段，不冒其全文归属')
allowed[r['candidate_id']]=['later_evidence']
changes=[]
for b,a in zip(before,after):
 assert b['candidate_id']==a['candidate_id']
 diff=[k for k in a if a[k]!=b[k]]
 assert set(diff)==set(allowed.get(a['candidate_id'],[])),(a['candidate_id'],diff)
 if diff:changes.append(dict(candidate_id=a['candidate_id'],fields=diff,before={k:b[k] for k in diff},after={k:a[k] for k in diff}))
assert len(changes)==4
dump(p,after)
md=['# 卷6本地候选终评第007批','','人工终评20项，待primary逐项主审；不改原池/冻结卷。原题与原记录完整保存在同名JSON。','']
for r in after:
 md+=['## '+r['candidate_id'],'','原子题：'+r['title'],'','终点：'+r['status']+' / '+r['audit_domain'],'',r['rationale'],'','证据：'+'；'.join(f"raw{int(e['chapter_id'][3:])} L{e['start_line']}—{e['end_line']} ({e['claim_kind']})" for e in r['later_evidence']),'']
p.with_suffix('.md').write_text('\n'.join(md),encoding='utf-8')
receipt=load(H/'adjudications-local-v06-batch007-validation.json');receipt.update(sha256=sha(p),approved_delta_applied=True,unchanged_objects=16,all_unlisted_fields_equal=True)
dump(H/'adjudications-local-v06-batch007-validation.json',receipt)
check=load(H/'v06-batch007-source-check.json');check['approved_correction']='1240/1241实际炼魂军回收：新增本次完整notes接读及L89944—90004定向源；1369 L98452—55按primary addendum精确定位，保原全文归属。';check['full_derived_notes_read_this_batch'] += [1240,1241];check['targeted_source_ranges_read'] += [[89944,90004],[98449,98456]];check['research_source']=dict(path=e['research_path'],sha256=e['research_sha256'],reader='primary');dump(H/'v06-batch007-source-check.json',check)
delta=dict(status='applied_explicit_primary_approval',before_sha256=sha(backup/p.name),after_sha256=sha(p),proposal_sha256=sha(H/'batch007-mirror-evidence-proposal.json'),approved_by='primary',actual_editor='zongheng_vol05_full',unchanged_objects=16,unlisted_fields_identical=True,changes=changes)
dump(H/'batch007-approved-delta.json',delta)
print(json.dumps(dict(batch_sha256=sha(p),delta_sha256=sha(H/'batch007-approved-delta.json'),changed_objects=4,unchanged_objects=16)))
