from common import P,ROOT,dump,sha
import json,copy

old=P/'vol04-identity-two-issues-proposal.v2.json'
x=json.loads(old.read_text(encoding='utf-8'))
prior=copy.deepcopy(x['affected_fields'])
specs=[
('chr-db3efcc2697e551d88e12c1439e2bc6f.json','stage_change','899获炎龙新统职位；919等级称差单列，非一直留御林任相同官。'),
('chr-736d302e333e5484906b47dc0eb1a44f.json','stage_change','后炎龙统领换龙硎。'),
('chr-623eb778fd0255228d29785a5a75b4f1.json','relationships','火象国王百里伦复现异常不可她解释补完。'),
]
for name,key,needle in specs:
 p=ROOT/'writing-vault/library/characters'/name
 obj=json.loads(p.read_text(encoding='utf-8'))
 value=obj['content'][key]
 match=[r for r in prior if r['field'].endswith('/content/'+key) and r['before']==value]
 assert match,(name,key,value)
 r=copy.deepcopy(match[0]);r['path']=p.relative_to(ROOT).as_posix();r['sha256']=sha(p);r['field']='/content/'+key
 r['composition_note']='仅补正式canonical人物字段路径；建议内容与既有镜像逐值相同，未就地改卡。'
 x['affected_fields'].append(r)
assert x['affected_fields'][:57]==prior and len(prior)==57 and len(x['affected_fields'])==60
x['canonical_addition']='按primary要求，仅追加三个人物canonical字段及实际文件SHA；前57逐值不变。'
x['previous_proposal']={'path':old.relative_to(ROOT).as_posix(),'sha256':sha(old)}
f=P/'vol04-identity-two-issues-proposal.v3.json';assert not f.exists();dump(f,x)
ls=['# 卷四两处实体误读最小纠正提案 v3','','前57字段与v2逐值一致；仅增三个人物canonical路径，未修改任何冻结字段或正式卡。','',f'JSON SHA：{sha(f)}','']
for r in x['affected_fields']:
 ls += ['## '+r['path']+' '+r['field'],'',r['sha256'],'','旧：'+r['before'],'','新：'+r['after'],'',r['composition_note'],'','后证：'+'；'.join(f'{e["chapter_id"]} L{e["start_line"]}—{e["end_line"]}' for e in r['evidence']),'']
f.with_suffix('.md').write_text('\n'.join(ls),encoding='utf-8')
print(f.name,sha(f),len(x['affected_fields']))
