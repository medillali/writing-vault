from save_focus_manual import A,P,read,write,sha
import copy
p=A/'focused-findings-part03.json';old=read(p);new=copy.deepcopy(old);b=old['findings'][1];a=new['findings'][1]
z='方持镇国刀找霜后强开幕有前因';assert z in a['stage_chain'][2];a['stage_chain'][2]=a['stage_chain'][2].replace(z,'1384主令方取镇国刀求霜；1385方报霜将强开幕，求援有前因')
assert old['findings'][0]==new['findings'][0] and old['findings'][2:]==new['findings'][2:]
write(P/'focus03-before-rescue-channel.json',old);write(p,new)
write(P/'focus03-rescue-channel-delta.json',{'primary_approval':'root核1384/1385后明确要求，只将求援命令/方后来报告按实际渠道记，不冒方实取刀镜头','before':b,'after':a,'other_seven_identical':True,'evidence_identical':b['evidence']==a['evidence'],'after_sha256':sha(p)})
md=p.with_suffix('.md');md.write_text(md.read_text(encoding='utf-8').replace(z,'1384主令方取镇国刀求霜；1385方报霜将强开幕，求援有前因'),encoding='utf-8')
src=P/'manual_focus_part03.py';src.write_text(src.read_text(encoding='utf-8').replace(z,'1384主令方取镇国刀求霜；1385方报霜将强开幕，求援有前因'),encoding='utf-8')
print(sha(p));print(sha(P/'focus03-rescue-channel-delta.json'))
