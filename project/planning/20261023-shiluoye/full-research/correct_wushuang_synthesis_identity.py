"""主审实际核源后定向修正综合的一条继承误读，保旧版和其余35条逐值不变。"""
from pathlib import Path
import copy, datetime, hashlib, json, sys
sys.stdout.reconfigure(encoding='utf-8')
B=Path(__file__).resolve().parent; ROOT=B.parents[2]
S=B/'tianxia-wushuang'; D=ROOT/'writing-vault/library/reports/tianxia-wushuang'
read=lambda p: json.loads(p.read_text(encoding='utf-8'))
sha=lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
snapshot=D/'audit/synthesis-revisions/before-identity-guild-field-fix'
assert not snapshot.exists(),'一次修订已开始，不能重跑覆盖快照'
draft=read(S/'book-synthesis-draft.json'); before=copy.deepcopy(draft)
row=draft['dimensions']['continuity'][0]
assert row['id']=='wushuang-book-continuity-01'
wrong='卷6：吻痕/谁与争锋至少各三服职业实体，'
correct='卷6：1098同ID三项均为吻痕：中国165刺客、美国192战士和无籍199荷兰战士；其中谁与争锋是中国吻痕所属公会名，1209巴西212剑师另以谁与争锋为角色ID，不能混字段或造出中美同名谁。'
assert row['fact_summary'].count(wrong)==1
md=(S/'book-synthesis-draft.md').read_text(encoding='utf-8')
assert md.count(wrong)==1
files=[S/'book-synthesis-draft.json',S/'book-synthesis-draft.md',S/'primary-synthesis-review.json',D/'book-synthesis.json',D/'book-synthesis.md',D/'audit/book-synthesis-review.json',D/'ACCEPTANCE.json',D/'ACCEPTANCE.md']
snapshots={}
for i,p in enumerate(files):
    q=snapshot/f'{i:02d}-{p.name}';q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(p.read_bytes())
    snapshots[p.relative_to(ROOT).as_posix()]={'snapshot':q.relative_to(D).as_posix(),'sha256':sha(p)}
identity_record='1098的官方查找列出吻痕三同ID，谁与争锋仅为中国吻痕的公会字段；1209角色ID谁与争锋属于巴西212剑术宗师、锋芒盟主。旧研究给后者造中美同名玩家，属于派生读者误配，已撤回；不是小说新增实体或源文矛盾。'
source=read(S/'source.json')
ev=[dict(source_id=source['source_id'],revision=source['revision'],chapter_id=f'ch-{n:04d}',start_line=a,end_line=z,claim_kind='fact') for n,a,z in [(1098,88904,88909),(1209,97115,97121)]]
upstream=row['supporting_observations'][5]
assert upstream['volume']==6 and upstream['observation_id']=='v06-identity-separation'
correction=dict(status='primary-source-verified-correction',error_class='derived-research-guild-name-and-role-id-field-confusion',before_fact_summary=row['fact_summary'],corrected_identity=identity_record,evidence=ev,reviewer='primary',user_approval=False,actual_source_read_scope='root此前已BEGIN-END完整原章1098及1209；本次重读已发表36条综合的全部顶层文学语义时发现尚未同步的一处派生摘要。',retained_historical_upstream=dict(material_path=upstream['material_path'],json_pointer=upstream['json_pointer'],quoted_observation=upstream['reported_observation'],policy='原reported_observation是旧读者误读的来源历史，不作为当前小说事实；原正式卷六不就地改写。'))
row['fact_summary']=row['fact_summary'].replace(wrong,correct)
row['post_audit_source_correction']=copy.deepcopy(correction)
for dim,rows in before['dimensions'].items():
    for i,old in enumerate(rows):
        if (dim,i)!=('continuity',0):assert draft['dimensions'][dim][i]==old
assert row['supporting_observations']==before['dimensions']['continuity'][0]['supporting_observations']
draft['validation']['direct_primary_identity_rechecks']=2
draft['validation']['historical_inherited_quotation_correction']='continuity[0].post_audit_source_correction优先于保留的卷六旧引用误读；原继承2626定位统计不改。'
md=md.replace(wrong,correct)
md+='\n\n## 终审后的身份字段更正\n\n1098三同ID属于吻痕；谁与争锋在该处为公会名，1209另为巴西玩家角色名。卷六旧reported_observation作为误读历史保留，不能采用其中捏造的中美同名谁。当前综合已核源撤回此误配，其余35条综合未改；人物全弧与问题终点评定已先行正确保存。\n\n[完整更正、原文定位与旧版快照](audit/synthesis-identity-correction.md)。\n'
write(S/'book-synthesis-draft.json',draft)
(S/'book-synthesis-draft.md').write_text(md,encoding='utf-8')
review=read(S/'primary-synthesis-review.json')
review['corrections_verified'].append(dict(dimension='continuity',index_zero_based=0,field='fact_summary',before=wrong,after=correct,reason=identity_record))
review['original_source_rechecks']+=['root已完整原章1098：L88904—88909三同ID都是吻痕，谁与争锋为公会。','root已完整原章1209：L97115—97121巴西角色ID谁与争锋；不是另一中美同名者名单。']
review['input_sha256']={name:sha(S/name) for name in ['book-synthesis-draft.json','book-synthesis-draft.md']}
review['post_terminal_audit_amendment']='已逐项主审完整36条顶层文学语义，定向修1条身份摘要并保其余35逐值不变；冻结终点四包/原卷/卡图不改。'
write(S/'primary-synthesis-review.json',review)
report=dict(**correction,source_id=source['source_id'],revision=source['revision'],amended_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),changed_synthesis_observation_id=row['id'],after_fact_summary=row['fact_summary'],other_35_observations_equal=True,original_upstream_quotation_preserved=True,before_snapshots=snapshots,formal_terminal_audit_changed=False)
for dest in [S/'audit',D/'audit']:
    write(dest/'synthesis-identity-correction.json',report)
    (dest/'synthesis-identity-correction.md').write_text('# 综合身份字段核源更正\n\n当前解释：'+identity_record+'\n\n直接原文：raw1098 L88904—88909、raw1209 L97115—97121。root已分别BEGIN-END全文核读；这次补齐的是综合摘要，未新增团队阅读覆盖。\n\n此前两项终点评定和人物107已正确保存，本次同步综合第continuity01条；保留旧版与旧上游引用作为读者误读的来源历史。其余35条逐值未改，原卷六、卡片、图及已冻结整书四包不改。用户评价仍draft。\n\n[完整前后与快照清单](synthesis-identity-correction.json) · [当前综合](../book-synthesis.md) · [正确人物全弧](../character-arcs.md)\n',encoding='utf-8')
print(json.dumps({'status':'targeted-synthesis-correction-ready-for-republication','other_35_equal':True,'snapshot_files':len(snapshots),'new_draft_sha256':sha(S/'book-synthesis-draft.json'),'new_review_sha256':sha(S/'primary-synthesis-review.json')},ensure_ascii=False))
