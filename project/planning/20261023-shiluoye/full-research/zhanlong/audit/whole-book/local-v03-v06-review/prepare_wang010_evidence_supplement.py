from pathlib import Path
import json,hashlib,copy,sys
sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent;A=H.parent;R=Path('C:/Users/Administrator/Documents/ChatGPT/Novel');p=A/'character-arcs-part03.json';d=json.loads(p.read_text(encoding='utf-8'));old=d['characters'][3]['evidence'];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();h=lambda x:hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
assert sha(p)=='3832d4b45a17e90ce5388b6a713f003ddffc61e65bc12f3938f2f0327c0063f6'
remove=[e for e in old if e['chapter_id']=='ch-0500'];assert len(remove)==1;assert not any(e['chapter_id']=='ch-0499' for e in old);keep=[copy.deepcopy(e) for e in old if e['chapter_id']!='ch-0500'];assert len(old)==24 and len(keep)==23
src=f"writing-vault/private-sources/normalized/sources/{d['source_id']}/{d['revision']}.txt";assert sha(R/src)==d['revision']
adds=[]
for n,lo,hi in [(445,37035,37043),(499,40992,40992),(500,41038,41043),(1199,87375,87384)]:adds.append(dict(source_id=d['source_id'],revision=d['revision'],chapter_id=f'ch-{n:04d}',start_line=lo,end_line=hi,claim_kind='fact',access_level='targeted-original-source-identity-boundary-reread',actual_reader='zongheng_vol05_full',research_path=src,research_sha256=d['revision'],evidence_purpose='仅证明王将/王翦分体及500告白者为王将；不将王将恋情归给王翦。primary已独立核相同明确姓名段。'))
after=keep+adds
out=dict(status='supplement_proposal_pending_primary_not_applied',supersedes='仅替代priority-corrections-wang-identity-proposal.json内010 evidence的旧拟法；四文学提案保持584a5d原值',parent_proposal_sha256='584a5d0123215cc224a5deaf38d90c9fa1e6077220c370ebbf096a1077f261e8',input_json_sha256=sha(p),input_md_sha256=sha(p.with_suffix('.md')),target=['characters',3,'evidence'],correction_to_previous_description='原数组24条，仅有500没有499，前述去499/500描述不精确；真实只去掉500原全章1ref，保其余23条原对象，再加4条身份用途精准ref。',original_count=len(old),retained_count=len(keep),retained_original_objects_sha256=h(keep),remove_exact_objects=remove,append_exact_objects=adds,result_count=len(after),result_evidence_array_sha256=h(after),other_scope='010四文学新句按原584a5d提案；其余行/字段/wrapper逐值保留。MD只同步这四句和该行证据定位；尚未执行。')
q=A/'character-arcs-part03-wang-identity-evidence-supplement-proposal.json';q.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');md=['# 010王将身份证据补充提案','','原24条中仅500、无499；只移除原500全章1ref，保其余23对象逐值/顺序，再附4条精准身份边界证据。四文学新句仍按584a5d原提案，已签组不先改。','']
for e in adds:md+=['- '+e['chapter_id']+f' L{e["start_line"]}—{e["end_line"]}：'+e['evidence_purpose']]
md+=['','原JSON '+sha(p)+'；原MD '+sha(p.with_suffix('.md'))+'。结果27 refs。']
q.with_suffix('.md').write_text('\n'.join(md)+'\n',encoding='utf-8');print(json.dumps(dict(proposal_sha256=sha(q),md_sha256=sha(q.with_suffix('.md')),original_count=len(old),retained=len(keep),removed=remove,added=adds,result_count=len(after)),ensure_ascii=False,indent=2))
