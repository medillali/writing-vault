from save_focus_manual import P,A,ROOT,read,write,sha
import copy
p=A/'focused-findings-part02.json';data=read(p);old=copy.deepcopy(data);proposal=read(P/'focus02-canglan-later-narration-proposal-v2.json');c=proposal['changes'][0];assert sha(p)==c['input_sha256']
ix=next(i for i,x in enumerate(data['findings']) if x['key']==c['key']);assert data['findings'][ix]==c['before'];after=copy.deepcopy(c['after'])
support=ROOT/'writing-vault/library/reports/zhanlong/audit/primary-rereads/canglan-1369-addendum.json';s=read(support)
e=after['evidence'][-1];assert e['chapter_id']=='ch-1369';e.update(access_level='derived-primary-independent-whole-chapter-reread',research_path=str(support.relative_to(ROOT)).replace('\\','/'),material_sha256=sha(support),source_reader='primary本轮1369整章独立复读；首次reader=zongheng_vol05_full不变',attribution_note='本代理实际完整读此addendum，不冒亲读1369原文；正式旧1369四栏没有吞魂两句，故该新主张由独立证明承担。')
data['findings'][ix]=after;write(P/'focus02-before-canglan-approved.json',old);write(p,data)
assert all(a==b for i,(a,b) in enumerate(zip(old['findings'],data['findings'])) if i!=ix)
delta={'primary_approval':'三字段已完整读批准；并要求仅新1369证据指正式primary全文复读证明','input_sha256':c['input_sha256'],'before':c['before'],'after':after,'other_seven_identical':True,'original_eight_refs_identical':c['before']['evidence']==after['evidence'][:-1],'after_sha256':sha(p),'support_sha256':sha(support)};write(P/'focus02-canglan-approved-merged-delta.json',delta)
md=p.with_suffix('.md');text=md.read_text(encoding='utf-8')
for k in ['conclusion','limits_and_counterevidence']:text=text.replace(c['before'][k],after[k])
text=text.replace(c['before']['stage_chain'][2],after['stage_chain'][2]).replace('ch-1350, ch-1370\n','ch-1350, ch-1370, ch-1369\n');md.write_text(text,encoding='utf-8')
print(sha(p));print(sha(P/'focus02-canglan-approved-merged-delta.json'));print(sha(support))
