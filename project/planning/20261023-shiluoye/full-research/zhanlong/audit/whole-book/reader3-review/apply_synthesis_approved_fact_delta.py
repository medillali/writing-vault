from synthesis_common import *
proposal=json.loads((P/'synthesis-three-facts-selfcheck-proposal.json').read_text(encoding='utf-8'))
all_delta=[]
for dim in ['characters','themes','plot']:
 p=P/f'synthesis-{dim}.json';md=p.with_suffix('.md');pb=p.read_bytes();mb=md.read_bytes();a=json.loads(pb);old=json.loads(pb)
 for suffix,content in [('.json',pb),('.md',mb)]:
  f=P/f'synthesis-{dim}-before-approved-selfcheck{suffix}';assert not f.exists();f.write_bytes(content)
 changes=[c for c in proposal['changes'] if c['file']==str(p.relative_to(ROOT)).replace('\\','/')]
 mdnew=mb
 for c in changes:
  assert sha(p)==c['input_sha256'];i=int(c['json_pointer'].split('/')[2]);key=c['json_pointer'].split('/')[-1]
  assert a['rows'][i][key]==c['before'];a['rows'][i][key]=c['after'];needle=c['before'].encode('utf-8');assert mdnew.count(needle)==1;mdnew=mdnew.replace(needle,c['after'].encode('utf-8'))
 if dim=='characters':
  su=a['rows'][1]['supporting_observations'];j=next(i for i,x in enumerate(su) if x['volume']==6)
  boundary={'claim_kind':'fact','text':'1384仅见李命方歌阙到府取镇国刀向流霜求援；1385方回报流霜将来并给倒计时，未独演方实际取物或持刀。原reported_fact按冻结上游字面保留，不将其动作强度用于本综合结论。','evidence':[ref(1384,99517,99520),ref(1385,99614,99620)]}
  assert 'reported_fact_boundary' not in su[j];su[j]['reported_fact_boundary']=boundary
  pointer=f'/rows/1/supporting_observations/{j}/reported_fact_boundary'
  changes.append({'json_pointer':pointer,'before_key_present':False,'after':boundary,'reason':'root已审焦点纠正，保reported_fact原字面，仅新增明确边界'})
  nl=b'\r\n' if b'\r\n' in mdnew else b'\n';needle=('## '+a['rows'][2]['title']).encode('utf-8');assert mdnew.count(needle)==1
  insert=('派生事实边界（卷6支持栏）：'+boundary['text']+' 定位：ch-1384 L99517—99520；ch-1385 L99614—99620。').encode('utf-8')+nl+nl
  mdnew=mdnew.replace(needle,insert+needle)
  old['rows'][1]['supporting_observations'][j]['reported_fact_boundary']=boundary
 for c in changes:
  if 'before' in c:
   i=int(c['json_pointer'].split('/')[2]);old['rows'][i][c['json_pointer'].split('/')[-1]]=c['after']
 assert a==old
 dump(p,a);md.write_bytes(mdnew);assert b'\r\r\n' not in mdnew
 all_delta.append({'dimension':dim,'before_json_sha256':hashlib.sha256(pb).hexdigest(),'before_md_sha256':hashlib.sha256(mb).hexdigest(),'after_json_sha256':sha(p),'after_md_sha256':sha(md),'changes':changes,'all_other_values_unchanged':True})
out={'approval':'primary明确批准三fact_summary+characters02支持栏新增边界','proposal_sha256':sha(P/'synthesis-three-facts-selfcheck-proposal.json'),'changes_by_file':all_delta,'actual_source_rereads':proposal['new_actual_original_rereads']+[{'chapter_id':CH[n]['chapter_id'],'start_line':CH[n]['start_line'],'end_line':CH[n]['end_line'],'full_text_read':True,'actual_reader':'/root/zongheng_vol03_full','unique_coverage_increment':0} for n in [1384,1385]]}
dump(P/'synthesis-approved-selfcheck-combined-delta.json',out)
print(json.dumps([{'dimension':x['dimension'],'json_sha256':x['after_json_sha256'],'md_sha256':x['after_md_sha256']} for x in all_delta],ensure_ascii=False))
