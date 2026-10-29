from synthesis_common import *
p=B/'book-synthesis-draft.json';m=p.with_suffix('.md');pb=p.read_bytes();mb=m.read_bytes();a=json.loads(pb)
assert sha(p)=='ad82b17b9c7fd0fc165eb0f653cc231eb144f4b630f0449b77b771796941e21d'
(P/'synthesis-before-dependency-role-refinement.json').write_bytes(pb);(P/'synthesis-before-dependency-role-refinement.md').write_bytes(mb)
removed=[x for x in a['current_priority_reading'] if x['path'].endswith('-proposal.json')]
assert len(removed)==3
a['current_priority_reading']=[x for x in a['current_priority_reading'] if not x['path'].endswith('-proposal.json')]
for g in a['upstream_documents']:
 if g['volume']=='current-priority-reading':
  g['volume']='priority-reading-and-proof-archive'
  for doc in g['documents']:
   if doc['path'].endswith('-proposal.json'):
    doc['kind']='archived-proposal-not-current-interpretation';doc['reading_boundary']='仅保提案归档指纹；当前解释采用同名不带-proposal且已批准的独立层，不将提案重复计为当前纠正。'
a['dependency_role_note']='当前优先层只含已批准独立纠正与卷二两剑更正；三份proposal保作历史依赖指纹，不作为优先解释或额外逻辑问题。'
dump(p,a)
mdnew=mb
for x in removed:
 line=f'- {x["path"]} · SHA `{x["sha256"]}`\n'.encode('utf-8');assert mdnew.count(line)==1;mdnew=mdnew.replace(line,b'')
m.write_bytes(mdnew)
manifest=json.loads((P/'synthesis-final-assembly-validation.json').read_text(encoding='utf-8'));manifest['json_sha256']=sha(p);manifest['md_sha256']=sha(m);manifest['dependency_role_refinement']='仅区分已批准优先层与三份历史proposal；36条及九组逐值未改。';dump(P/'synthesis-final-assembly-validation.json',manifest)
dump(P/'synthesis-dependency-role-refinement-delta.json',{'before_json_sha256':hashlib.sha256(pb).hexdigest(),'before_md_sha256':hashlib.sha256(mb).hexdigest(),'after_json_sha256':sha(p),'after_md_sha256':sha(m),'removed_from_current_priority_only':removed,'all_36_rows_unchanged':json.loads(pb)['dimensions']==a['dimensions'],'upstream_documents_still_pinned':68})
print(sha(p),sha(m))
