from synthesis_common import *
p=P/'synthesis-worldbuilding.json';m=p.with_suffix('.md')
before=p.read_bytes();bm=m.read_bytes();a=json.loads(before)
assert sha(p)=='4b3d0b4f78d09a1a5c72be59f4ff69a4a9f10879603880045fca2606c3482646'
(P/'synthesis-worldbuilding-before-material-delta.json').write_bytes(before)
(P/'synthesis-worldbuilding-before-material-delta.md').write_bytes(bm)
old=a['rows'][1]['fact_summary'];assert old.count('百炼铁')==1
a['rows'][1]['fact_summary']=old.replace('百炼铁','100份麒麟铁')
dump(p,a)
oldmd=bm.decode('utf-8');assert oldmd.count('百炼铁')==1
m.write_text(oldmd.replace('百炼铁','100份麒麟铁'),encoding='utf-8')
check=json.loads(before);check['rows'][1]['fact_summary']=a['rows'][1]['fact_summary'];assert check==a
delta={'approval':'primary指定仅fact_summary材料名修正；其余逐值相同','before_json_sha256':hashlib.sha256(before).hexdigest(),'before_md_sha256':hashlib.sha256(bm).hexdigest(),'after_json_sha256':sha(p),'after_md_sha256':sha(m),'changes':[{'json_pointer':'/rows/1/fact_summary','before':old,'after':a['rows'][1]['fact_summary'],'evidence':[ref(257,22394,22418),ref(258,22424,22449)]}],'unchanged_rows':[0,2,3]}
dump(P/'synthesis-worldbuilding-material-delta.json',delta)
print(json.dumps(delta,ensure_ascii=False))
