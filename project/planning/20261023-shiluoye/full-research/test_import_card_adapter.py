"""实际卷八卡的研究字段需保留且能通过主档字段边界。"""
import copy,json,sys,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
sys.path.insert(0,str(B.parents[2]/'distill-novels/scripts'))
from fictionlib.vault import ASSET_FIELDS,SERVER_FIELDS
from import_card_adapter import adapt_card
class AdapterTest(unittest.TestCase):
 def test_actual_volume8_preserves_claim_and_raw(self):
  raw=json.loads((B/'tianxia-wushuang/vol08/cards.json').read_text(encoding='utf-8'))
  before=copy.deepcopy(raw)
  for c in raw:
   adapted=adapt_card(c)
   self.assertFalse(set(adapted)-ASSET_FIELDS-SERVER_FIELDS)
   self.assertEqual(adapted['content']['claim_kind'],c['claim_kind'])
   self.assertEqual(adapted['evidence'],c['evidence'])
  self.assertEqual(raw,before)
 def test_unknown_field_is_rejected(self):
  with self.assertRaises(ValueError):adapt_card({'unrecognized':42})
if __name__=='__main__':unittest.main()
