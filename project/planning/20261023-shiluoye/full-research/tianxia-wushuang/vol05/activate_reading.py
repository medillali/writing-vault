"""依主代理本轮明确启动消息启用本代理卷五→卷七；不读取正文。"""
import json
from pathlib import Path
P=Path(__file__).resolve().parent.parent
ref='primary NEW_TASK：纵横已正式发布验收；明确授权启动天下无双卷五→卷七全文阅读与九维交付，无需逐卷批准。'
for v in [5,7]:
 d=P/f'vol{v:02}'
 for name in ['assignment.json','reader-state.json']:
  p=d/name;x=json.loads(p.read_text(encoding='utf-8'))
  assert not x.get('completed_chapter_ids',[])
  x.update(reading_authorized=True,metadata_only=False,start_authorization_reference=ref)
  if name=='reader-state.json':x['status']='reading' if v==5 else 'authorized_awaiting_vol05_completion'
  p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('已启用卷五，卷七按序等待；未读取正文。')
