"""按本卷CGL原文纠正原名；走版本API并保留原稿与人工字段。"""
import pathlib,json,copy,hashlib,sys
base=pathlib.Path(__file__).resolve().parent;root=base.parents[2]
sys.path.insert(0,str(root/'distill-novels/scripts'))
from fictionlib.vault import Vault
from fictionlib.storage import atomic_write,json_text
from check_volume import load_and_check
sys.stdout.reconfigure(encoding='utf-8')
sid='src-2a13958390274509b2af019f6b12d981';rev='2c541951301de981c755ebf4001bf3ec909d1e7d44314e14fa8af51751849a52'
stage=base/'zongheng-tianxia/vol07';formal=root/'writing-vault/library/reports/zongheng-tianxia'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
origin=sid+'/full-20261025/vol07/character/shusheng';cards=read(stage/'cards.json')
card=next(c for c in cards if c['origin_key']==origin)
title='轻狂书生（丁舒升；丁书生为误称或招呼名）'
card['title']=title
card['content']['identity_notes']='本卷CGL榜raw0966 L106934明确原名丁舒升；raw0935招呼牌写丁书生。误称或招呼名与游戏ID不另建人物。'
e={'source_id':sid,'revision':rev,'chapter_id':'ch-0966','start_line':106934,'end_line':106934,'claim_kind':'fact'}
if e not in card['evidence']:card['evidence'].append(e)
atomic_write(stage/'cards.json',json_text(cards))
analysis=read(stage/'analysis.json')
entry=next(c for c in analysis['characters'] if c['origin_key']==origin)
entry.update(title=title,evidence=copy.deepcopy(card['evidence']))
atomic_write(stage/'analysis.json',json_text(analysis))
preflight=load_and_check('zongheng-tianxia',7)[-1]
v=Vault(root/'writing-vault');old=v.get_asset('chr-7e3ed60ab784569798bab060b3148adb')
payload=copy.deepcopy(card);payload['asset_id']=old['asset_id']
record=v.put_asset(payload,old['revision'],generated=True)
assert all(record.get(k)==old.get(k) for k in ['user_notes','favorite','review_status'])
assert record['asset_id']==old['asset_id']
formal_cards=read(formal/'vol07-cards.json')
formal_cards=[record if c['asset_id']==record['asset_id'] else c for c in formal_cards]
atomic_write(formal/'vol07-cards.json',json_text(formal_cards))
for filename in ['vol07-asset-map.json','vol07-analysis.json']:
    data=read(formal/filename)
    if isinstance(data,list):rows=data
    else:
        rows=data['imported_assets']
        entry=next(c for c in data['characters'] if c['origin_key']==origin)
        entry.update(title=title,evidence=copy.deepcopy(card['evidence']))
    for row in rows:
        if row['asset_id']==record['asset_id']:row.update(title=title,revision=record['revision'])
    atomic_write(formal/filename,json_text(data))
path=base/'zongheng-tianxia/review-vol07.json';review=read(path)
old_review=formal/'audit/review-vol07-before-identity.json'
if not old_review.exists():atomic_write(old_review,json_text(review))
fix='姓名复核：原名丁舒升由raw0004 L166与本卷raw0966 L106934明确；丁书生作为误称/招呼名保留。卷七该卡通过generated API升版，人工字段与旧版本保留。'
if fix not in review['corrections_verified']:review['corrections_verified'].append(fix)
review['preflight']=preflight
review['input_sha256']={n:hashlib.sha256((stage/n).read_bytes()).hexdigest() for n in review['input_sha256']}
atomic_write(path,json_text(review));atomic_write(formal/'audit/review-vol07.json',json_text(review))
receipt={'asset_id':record['asset_id'],'previous_revision':old['revision'],'revision':record['revision'],'manual_fields_preserved':True,'source_evidence':e,'preflight':preflight,'scope':'仅修本轮新卷七卡与其导出快照；旧开篇及旧分卷主档未改写'}
atomic_write(formal/'audit/identity-correction.json',json_text(receipt))
print(json.dumps(receipt,ensure_ascii=False))
