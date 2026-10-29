import json,copy,hashlib
from audit_evidence import H,evidence
out=[]
for filename,cid in [('character-arcs-part05.json','character-arc-63'),('character-arcs-part08.json','character-arc-93')]:
 p=H/filename;obj=json.loads(p.read_text(encoding='utf-8'));before=next(x for x in obj['characters'] if x['audit_id']==cid);after=copy.deepcopy(before)
 if cid.endswith('63'):
  after['terminal_state']='末仍索阵营军官、1504活并实际收留奥。斩龙剑物链已有1299心然转述：拾荒者被紫妍杀、剑到卡琳；1455卡献冰明确。没有雪薇亲自追回/转交的镜头，不以物链报告冒认她的追回功。'
  after['evidence_boundaries']='雪薇不是卡琳同一军官；1299杀拾荒者与剑到卡琳为心然对陆说明，1458同称拾荒者再现场被冰杀，机制未交代，不编两人或额外复活。旧游戏史只人物回忆；后活不证明早战未伤。'
 else:
  after['key_decisions']='1258收钱/被拒索吻后遭逼问带路，陆依承诺放走→1273灰影抢雪薇斩龙剑由陆识别→1299心然转述他被紫妍杀、剑到卡琳→1458同称拾荒者血眼撞冰断鲜血结界，被冰领域焰化尘。'
  after['terminal_state']='1299已有被紫妍杀的角色报告，1458又有同称人物再现并被冰杀的现场；两层均保留，未给再现机制，不自行造第二拾荒者或一次未写复活。1458死亡明确。'
  after['evidence_boundaries']='1273身份为陆识而非系统复核；1299心然明确补转述物链，不能写全书没有说明，也不等雪薇亲追回。陆猜卡琳授意偷剑后自止，不当已证幕后；1458受圣控制仍陆判断。'
 after['evidence']=evidence([int(e['chapter_id'][3:]) for e in before['evidence']]+[1299])
 out.append(dict(path=filename,input_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),audit_id=cid,changed_fields=[k for k in before if before[k]!=after[k]],before=before,after=after))
x=dict(status='proposal_pending_primary_review_no_signed_group_modified',reason='本人BEGIN-END全文复读1299 L103488—103544，L103511—15已有心然转述紫妍杀拾荒/剑到卡琳及陆自止幕后猜测，须与1458实景并存。',changes=out)
(H/'character-scavenger-report-layer-proposal.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print([(r['path'],r['input_sha256']) for r in out])
