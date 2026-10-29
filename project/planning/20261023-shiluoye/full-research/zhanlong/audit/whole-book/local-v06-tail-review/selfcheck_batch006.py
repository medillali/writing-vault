from save_tail_manual import Q,read,write,sha
p=Q/'adjudications-local-v06-tail-batch006.json';rows=read(p);before=dict(rows[19]);rows[19]['rationale']=rows[19]['rationale'].replace('其余掉落三星/五星部位','其余掉落五星铠腕/布鞋')
write(Q/'batch006-pre-delivery-selfcheck-delta.json',dict(reason='交付前自核去除误加三星等级；原1323四栏两项均五星',before=before,after=rows[19]));write(p,rows)
md=['# 《斩龙》卷六尾199候选终评草稿','本批offset100—119；待primary逐项主审。','']
for x in rows:md += [f"- **{x['candidate_id']}** · {x['status']} / {x['audit_domain']}",f"  原题：{x['title']}",f"  终评：{x['rationale']}",f"  后证raw：{', '.join(map(str,x['later_chapters']))}；派生保原reader。",'']
p.with_suffix('.md').write_text('\n'.join(md)+'\n',encoding='utf-8');s=read(Q/'reader-state.json');s['batches'][5]['sha256']=sha(p);write(Q/'reader-state.json',s);print(sha(p))
