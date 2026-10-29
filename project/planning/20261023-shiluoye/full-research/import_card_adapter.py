"""研究包到现有资料库的无损字段适配；不修改已冻结研究输入。"""
import copy
from fictionlib.vault import ASSET_FIELDS,SERVER_FIELDS
def adapt_card(raw):
 card=copy.deepcopy(raw)
 if 'claim_kind' in card:
  claim=card.pop('claim_kind')
  content=card.setdefault('content',{})
  if 'claim_kind' in content and content['claim_kind']!=claim:
   raise ValueError('顶层与内容的claim_kind冲突，须重新主审')
  content['claim_kind']=claim
 unknown=set(card)-ASSET_FIELDS-SERVER_FIELDS
 if unknown:raise ValueError('未知研究卡字段: '+', '.join(sorted(unknown)))
 return card
