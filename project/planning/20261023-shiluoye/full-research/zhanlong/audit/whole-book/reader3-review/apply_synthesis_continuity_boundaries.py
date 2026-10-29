from synthesis_common import *
q=json.loads((P/'synthesis-continuity-two-boundaries-proposal.json').read_text(encoding='utf-8'))
p=P/'synthesis-continuity.json';m=p.with_suffix('.md');pb=p.read_bytes();mb=m.read_bytes();a=json.loads(pb)
assert sha(p)==q['input_sha256'] and a['rows'][0]==q['before']
for suffix,content in [('.json',pb),('.md',mb)]:
 f=P/f'synthesis-continuity-before-approved-boundaries{suffix}';assert not f.exists();f.write_bytes(content)
a['rows'][0]=q['after'];check=json.loads(pb);check['rows'][0]=q['after'];assert check==a
mdnew=mb.replace(q['before']['fact_summary'].encode('utf-8'),q['after']['fact_summary'].encode('utf-8'));assert mdnew!=mb
nl=b'\r\n' if b'\r\n' in mdnew else b'\n';marker=('## '+a['rows'][1]['title']).encode('utf-8');assert mdnew.count(marker)==1
boundary=q['after']['supporting_observations'][3]['reported_fact_boundary']
insert=('派生事实边界（卷3支持栏）：'+boundary['text']+' 定位：ch-0740 L57970—57980；ch-0743 L58114—58186；ch-0749。优先纠正：priority-corrections-lion-shield.json，SHA '+q['after']['priority_corrections'][-1]['sha256']+'。').encode('utf-8')+nl+nl
mdnew=mdnew.replace(marker,insert+marker);assert b'\r\r\n' not in mdnew
dump(p,a);m.write_bytes(mdnew)
out={'approval':'primary批准4aba提案，仅列3路径','proposal_sha256':sha(P/'synthesis-continuity-two-boundaries-proposal.json'),'before_json_sha256':hashlib.sha256(pb).hexdigest(),'before_md_sha256':hashlib.sha256(mb).hexdigest(),'after_json_sha256':sha(p),'after_md_sha256':sha(m),'changed_fields':q['changed_fields'],'before':q['before'],'after':q['after'],'all_other_values_unchanged':True}
dump(P/'synthesis-continuity-approved-boundaries-delta.json',out);print(json.dumps({k:v for k,v in out.items() if k not in ['before','after']},ensure_ascii=False))
