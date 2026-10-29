from pathlib import Path
import json,hashlib,copy,sys
sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent;A=H.parent;R=Path('C:/Users/Administrator/Documents/ChatGPT/Novel');old=A/'character-arcs-part03-wang-identity-evidence-supplement-proposal.json';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();h=lambda x:hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
assert sha(old)=='cff301c27eaca067956e55b4e6deae6de2920b6be08f97f603d3df267f76e59e';d=json.loads(old.read_text(encoding='utf-8'));out=copy.deepcopy(d);mat='writing-vault/library/reports/zhanlong/audit/priority-corrections-wang-identity.json';msha='f1eb93aeb09d4dd5b1ee542610b0e4a734b224da6520a10bd758686352b79f0e';assert sha(R/mat)==msha
changes=[]
for i,e in enumerate(out['append_exact_objects']):
 for k,val in [('research_path',mat),('research_sha256',msha)]:changes.append(dict(path=['append_exact_objects',i,k],before=e[k],proposed_after=val));e[k]=val
probe=copy.deepcopy(out)
for i,e in enumerate(probe['append_exact_objects']):
 e['research_path']=d['append_exact_objects'][i]['research_path'];e['research_sha256']=d['append_exact_objects'][i]['research_sha256']
assert probe==d
rows=json.loads((A/'character-arcs-part03.json').read_text(encoding='utf-8'))['characters'][3]['evidence'];after=[e for e in rows if e['chapter_id']!='ch-0500']+out['append_exact_objects'];out['result_evidence_array_sha256']=h(after);out['status']='material_metadata_revision_pending_primary_not_applied';out['previous_supplement_sha256']=sha(old);out['metadata_only_delta']=changes;out['material_role_explanation']='正式优先层是primary核源回执，research_path只为回执材料包，不冒原文内容；原文仍由固定SID/rev及章行定位，接读等级与actual_reader不改，不把私人TXT要求打包。'
q=A/'character-arcs-part03-wang-identity-evidence-material-proposal.json';q.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');q.with_suffix('.md').write_text('# 010新增四ref研究材料元数据修订\n\n保原cff提案JSON/MD字节，旧已签人物不改。仅四个新ref各将research_path/research_sha256换为正式王身份核源回执 '+mat+' SHA '+msha+'；原SID/rev/章行/actual_reader/接读等级/身份用途不变，另23原ref与四文学不动。回执不是原文内容本身。\n',encoding='utf-8');print(json.dumps(dict(proposal_sha256=sha(q),md_sha256=sha(q.with_suffix('.md')),changes=changes,other_ref_fields_unchanged=probe==d),ensure_ascii=False,indent=2))
