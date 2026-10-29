"""检查本轮之前的卡片和人工字段没有被生成研究覆盖。"""
import pathlib,json,hashlib,datetime
base=pathlib.Path(__file__).resolve().parent
root=pathlib.Path(__file__).resolve().parents[3]
vault=root/'writing-vault'
baseline=json.loads((base/'baseline.json').read_text(encoding='utf-8'))
missing=[];manual_changed=[];content_changed=[]
for aid,old in baseline['assets'].items():
    path=vault/old['path']
    if not path.exists():
        missing.append(aid);continue
    raw=path.read_bytes();record=json.loads(raw)
    if any(record.get(key)!=old.get(key) for key in ('user_notes','favorite','review_status')):
        manual_changed.append(aid)
    if hashlib.sha256(raw).hexdigest()!=old['sha256']:
        content_changed.append(aid)
result={
 'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'baseline_assets':len(baseline['assets']),
 'missing':missing,'manual_fields_changed':manual_changed,'preexisting_content_changed':content_changed,
 'status':'passed' if not (missing or manual_changed or content_changed) else 'needs_review',
 'scope':'仅验证本轮前主档及人工字段保护，不代替新研究内容质量审查。'
}
dest=vault/'library/reports/collection/baseline-protection.json'
dest.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='scope'}))
assert not missing and not manual_changed and not content_changed
