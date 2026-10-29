from character_arc_common import *
p=A/'reader3-character-arcs-part07.json';m=p.with_suffix('.md');before=p.read_bytes();mbefore=m.read_bytes();x=json.loads(before);r=x['characters'][4]
oldi=r['initial_comparison_stage'];oldt=r['terminal_state'];olde=deepcopy(r['evidence'])
r['initial_comparison_stage']='899以前为偏将军，朝会实际擢为上将并任炎龙新统帅，接续徐翊死后的军权；与守御林的龙硎为独立人物，不能因检索命中“斩龙忠烈营”造其早期龙城履历。'
r['terminal_state']='978明确死亡。源1288命中“龙忠”实为“斩龙忠烈营”词内，并非人物提名或复生后证；未见本人恢复。'
r['evidence']=[e for e in r['evidence'] if e['chapter_id']!='ch-0649']
delta=[{'path':'/characters/4/initial_comparison_stage','before':oldi,'after':r['initial_comparison_stage']},{'path':'/characters/4/terminal_state','before':oldt,'after':r['terminal_state']},{'path':'/characters/4/evidence','before':olde,'after':r['evidence']}]
(P/'character-part07-selfcheck-before.json').write_bytes(before);(P/'character-part07-selfcheck-before.md').write_bytes(mbefore)
dump(p,x);md=mbefore.decode('utf-8').replace(oldi,r['initial_comparison_stage']).replace(oldt,r['terminal_state']);md=md.replace('ch-0649 L51642—51701；','');m.write_bytes(md.encode('utf-8'))
dump(P/'character-part07-selfcheck-delta.json',{'reason':'交primary之前原文全读649/899/1288，修正精确词内误命中，未受审组不沿错。','before_sha256':hashlib.sha256(before).hexdigest(),'after_sha256':sha(p),'md_after_sha256':sha(m),'delta':delta})
v=P/'character-arcs-part07-validation.json';receipt=json.loads(v.read_text(encoding='utf-8'));receipt.update(sha256=sha(p),md_sha256=sha(m),source_refs=sum(len(r['evidence']) for r in x['characters']));dump(v,receipt)
st=P/'character-arc-reader-state.json';s=json.loads(st.read_text(encoding='utf-8'));s['groups'][-1]=receipt;dump(st,s)
print(json.dumps(receipt,ensure_ascii=False))
