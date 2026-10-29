from save_focus_manual import P,A,F,ROOT,read,write,sha
key='writing-vault/library/reports/zhanlong/vol06-handoff.md';inv=read(P/'focus-input-metadata-investigation.json');assert len(inv['mismatches'])==1
old=inv['mismatches'][0]['expected'];new=sha(ROOT/key)
changes=[]
for num in [1,2,3]:
 p=A/f'focused-findings-part{num:02d}.json';x=read(p);assert x['formal_input_sha256'][key]==old
 changes.append({'file':p.name,'input_sha256':sha(p),'field':f'/formal_input_sha256/{key}','before':old,'after':new,'scope':'仅顶层单一正式handoff元数据指纹；findings及evidence全部逐值不变'})
write(P/'focus-input-metadata-amendment-proposal.json',{'status':'proposal-pending-primary-confirmation-not-applied','reason':'40正式输入实际重核唯一vol06-handoff变；当前formal与stage文字差仅正式链接适配，不把旧23e9错称stage（stage实际5b224d）。原input-receipt不改，保旧指纹。','basis_path':key,'current_formal_sha256':new,'investigation_sha256':sha(P/'focus-input-metadata-investigation.json'),'changes':changes});print(sha(P/'focus-input-metadata-amendment-proposal.json'))
