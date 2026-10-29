import hashlib,json,pathlib
H=pathlib.Path(__file__).resolve().parent;R=H.parents[5]
rows=[]
for v in range(1,9):
 p=R/f'writing-vault/library/reports/tianxia-wushuang/vol{v:02d}-analysis.json';d=json.loads(p.read_text(encoding='utf-8'));k=next(x for x in ['major_character_states','character_states','characters'] if x in d)
 rows.append(dict(volume=v,field=k,count=len(d[k]),indices_read=[0,len(d[k])],field_semantics_read_in_full=True,input_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),access_kind='formal-derived-interface-reading',not_novel_full_reread=True))
out=dict(status='all_eight_character_state_fields_read',reader='/root/zongheng_vol04_full',source_scope='仅各卷人物状态接口；本代理原文亲读卷五/七，不宣称亲读其他卷全文。',interfaces=rows,total=sum(x['count'] for x in rows))
(H/'character-interface-reading.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
log=H/'research-interface-read-log.json';d=json.loads(log.read_text(encoding='utf-8'));d['character_state_interfaces']=out;d['in_progress_fields']=[];log.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(out['total'])
