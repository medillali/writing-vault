import json,pathlib
H=pathlib.Path(__file__).resolve().parent
p=H/'research-interface-read-log.json';d=json.loads(p.read_text(encoding='utf-8'))
d['completed_fields']=[dict(volume=v,interface='analysis.open_questions plus graph.threads original records',range=[0,n],complete=True) for v,n in enumerate([18,26,14,22,43,26,52,13],1)]
d['completed_fields'] += [dict(volume=8,interface='analysis.character_states',range=[0,35],complete=True)]
d['completed_fields'] += [dict(volume=8,interface='chapter-notes full four-column derived research',range=[0,105],complete=True)]
d['completed_fields'] += [dict(volume=6,interface='analysis.character_states',range=[0,48],complete=True),dict(volume=6,interface='chapter-notes full four-column derived research',range=[0,12],complete=False),dict(volume=6,interface='chapter-notes full four-column derived research',range=[135,144],complete=False),dict(volume=6,interface='chapter-notes full four-column derived research',range=[212,215],complete=False)]
d['completed_fields'] += [dict(volume=7,interface='chapter-notes full four-column research reread',range=[2,211],complete=True),dict(volume=7,interface='local candidates complete original records and atomic titles',range=[0,476],complete=True)]
d['in_progress_fields']=[dict(volume=7,interface='analysis.major_character_states',range=[0,12],complete=False,next_index=12)]
d['targeted_interfaces']=[dict(path='cross-volume-focused-review.json',scope='20 findings plus all attribution and source locators read in full')]
for ch,lo,hi,purpose in [(1295,103170,103249,'九君王杀奖与龙心SS交付分开'),(1389,110229,110303,'核无火麒麟实骑镜头，明确实骑后证在1407'),(1427,112979,113051,'明确弓复活例外与吕布衣持隐龙扇'),(1440,114038,114109,'作者明确纠阳坐骑墨麒麟为笔误'),(1471,116504,116588,'缴械15秒与非缴械15秒轮换')]:
 d['targeted_interfaces'].append(dict(volume=7,interface='novel full chapter reread',chapter_id=f'ch-{ch:04}',start_line=lo,end_line=hi,purpose=purpose+'；此前本人已全读，不新增整卷实读计数'))
d['mechanical_scope_supplement']='卷一/三/八notes未明串已另追加1291原子，保全不等本代理已读或已判。'
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
