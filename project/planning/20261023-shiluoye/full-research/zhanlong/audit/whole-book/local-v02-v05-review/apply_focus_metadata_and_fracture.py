from save_focus_manual import P,A,read,write,sha
import copy
proposal=read(P/'focus-input-metadata-amendment-proposal.json');deltas=[]
for c in proposal['changes']:
 p=A/c['file'];before=read(p);after=copy.deepcopy(before);k='writing-vault/library/reports/zhanlong/vol06-handoff.md'
 assert after['formal_input_sha256'][k]==c['before'];after['formal_input_sha256'][k]=c['after'];assert before['findings']==after['findings']
 write(P/f"{p.stem}-before-formal-link-pin.json",before);write(p,after)
 deltas.append({'file':p.name,'before':c['before'],'after':c['after'],'finding_and_evidence_identical':True,'after_sha256':sha(p)})
write(P/'focus-input-metadata-applied-delta.json',{'primary_approval':'root核正式与stage仅末5个MD链接适配，批准顶层pin单独修；无文学变更','original_input_receipt_preserved':True,'changes':deltas})
p=A/'focused-findings-part01.json';before=read(p);after=copy.deepcopy(before);a=after['findings'][0]['stage_chain'][2];assert '1380断臂活' in a
after['findings'][0]['stage_chain'][2]=a.replace('1380断臂活','1380臂骨震断低垂仍活（非截肢）');write(P/'focus01-before-fracture-precision.json',before);write(p,after)
write(P/'focus01-fracture-precision-delta.json',{'primary_approval':'root原文全文1380 L99222—99289核L99230骨折后要求仅一处措辞收窄','before':before['findings'][0],'after':after['findings'][0],'other_seven_identical':before['findings'][1:]==after['findings'][1:],'other_top_level_identical':True,'after_sha256':sha(p)})
md=p.with_suffix('.md');md.write_text(md.read_text(encoding='utf-8').replace('1380断臂活','1380臂骨震断低垂仍活（非截肢）'),encoding='utf-8')
src=P/'manual_focus_part01.py';src.write_text(src.read_text(encoding='utf-8').replace('1380断臂活','1380臂骨震断低垂仍活（非截肢）'),encoding='utf-8')
old=read(P/'focus02-canglan-later-narration-proposal.json');old['changes'][0]['input_sha256']=sha(A/'focused-findings-part02.json');old['reason']+=' 输入base仅顶层正式handoff链接适配元数据更新，before/after文学对象逐值同上一提案。';write(P/'focus02-canglan-later-narration-proposal-v2.json',old)
for n in [1,2,3]:
 f=A/f'focused-findings-part{n:02d}.json';print(f.name,sha(f))
print('metadata delta',sha(P/'focus-input-metadata-applied-delta.json'));print('fracture delta',sha(P/'focus01-fracture-precision-delta.json'));print('canglan proposal v2',sha(P/'focus02-canglan-later-narration-proposal-v2.json'))
