from pathlib import Path
import json,hashlib,copy,sys
sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent;A=H.parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
p=A/'character-arcs-part02.json';m=p.with_suffix('.md');d=json.loads(p.read_text(encoding='utf-8'));assert sha(p)=='1beb29e39d3e3de9a4a6168fa3c1a89217af561c2c479f03854bae7ce0a0922c'
b=H/'corrections/character02-time-proposal';b.mkdir(parents=True,exist_ok=False)
for x in [p,m,A/'character-arcs-part02-validation.json']:(b/x.name).write_bytes(x.read_bytes())
old=d['characters'][1]['terminal_state'];new=old.replace('1357沈母由拒绝到签署授权，1359队友祭墓','1359沈母由拒绝到签署授权，1357队友祭墓');assert new!=old
sid=d['source_id'];rev=d['revision']
out=dict(status='proposal_pending_primary_not_applied',scope='仅005 terminal_state中祭墓与签约两raw时点互换；已交JSON/MD原字节尚未变',input_sha256={p.name:sha(p),m.name:sha(m)},changes=[dict(path=['characters',1,'terminal_state'],before=old,proposed_after=new)],source_check=dict(actual_reviewer='zongheng_vol05_full',attribution='本次实际逐行完整再读raw1357/1358/1359全部索引行L97621—97823，原首次全文归属不变；primary已独立读并指出时点。',evidence=[dict(source_id=sid,revision=rev,chapter_id='ch-1357',start_line=97667,end_line=97676,claim_kind='fact'),dict(source_id=sid,revision=rev,chapter_id='ch-1359',start_line=97757,end_line=97807,claim_kind='fact')]),crosscheck004=dict(status='no_change_needed',business=dict(chapter_id='ch-1358',start_line=97682,end_line=97689,result='薛柔本人确认兹爵营业执照已办'),relationship=dict(chapter_id='ch-1358',start_line=97703,end_line=97710,result='薛景自称副盟、方本人明说很喜欢阿景正在交往、薛景回应；004原句raw正确'),limits='不以印刷章1350替raw1358，不改004或005其他文学字段/证据。'))
q=A/'character-arcs-part02-time-correction-proposal.json';q.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
q.with_suffix('.md').write_text('# 人物02时点最小提案\n\n待primary批准；原组和MD原字节未改，旧字节另存。\n\n005 terminal_state before：'+old+'\n\nafter：'+new+'\n\nraw1357 L97667—76祭墓；raw1359 L97757仍拒，L97805—07签并交协议。004自核raw1358 L97687—89执照、L97703—10副盟/交往均正确，保原句。\n',encoding='utf-8')
print(json.dumps(dict(proposal_sha256=sha(q),md_sha256=sha(q.with_suffix('.md')),changes=out['changes'],original_json_unchanged=sha(p)==out['input_sha256'][p.name],original_md_unchanged=sha(m)==out['input_sha256'][m.name]),ensure_ascii=False,indent=2))
