import pathlib,json,hashlib,sys
sys.stdout.reconfigure(encoding='utf-8');H=pathlib.Path(__file__).resolve().parent
read=lambda p:json.loads(p.read_text(encoding='utf-8'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
archive=H/'reviewed-batches';archive.mkdir(exist_ok=True)
old=H/'adjudications-history-08.json';target=archive/'adjudications-history-08-primary-reviewed-v1.json'
assert not target.exists();target.write_bytes(old.read_bytes())
d=read(old)
x=next(x for x in d if x['candidate_id']=='v08-thread-012')
x['rationale']='霜云首夜五胜后主队缺席最终淘汰；后记李承风实持WEL世界冠军杯，故不能沿用早期仍参赛待定。此处只据持杯结果，不凭1609补全二队参赛名单或未展示赛程；最终击烛具体对局、系统MVP及借装归还没有展开。李把唯一MVP归陆是人物评价，不替系统公告。'
old.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(H/'reviewed-batch-ledger.json').write_text(json.dumps(dict(status='partial_groups_under_primary_review_not_final_acceptance',groups=[dict(group='history-vol08-13',primary_feedback='primary已逐项读并通过13条；thread012建议只写李持WEL冠军杯以免补全赛程，现已收窄。',reviewed_original_path=target.relative_to(H).as_posix(),reviewed_original_sha256=sha(target),narrowed_path=old.name,narrowed_sha256=sha(old),formal_input_manifest='input-inventory.json',formal_input_manifest_sha256=sha(H/'input-inventory.json'))]),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(archived_reviewed_sha256=sha(target),narrowed_sha256=sha(old)),ensure_ascii=False))
