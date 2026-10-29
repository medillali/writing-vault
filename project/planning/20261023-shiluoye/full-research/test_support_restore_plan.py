"""实际31个入口附件的隔离还原与拒绝覆盖检查。"""
import json,shutil,tempfile,unittest
from pathlib import Path
from prepare_support_restore_plan import regenerate
B=Path(__file__).resolve().parent;V=B.parents[2]/'writing-vault'
class SupportRestoreTest(unittest.TestCase):
 def test_actual_support_and_conflict(self):
  base=B/'qa-temporary';base.mkdir(exist_ok=True)
  with tempfile.TemporaryDirectory(prefix='support-restore-',dir=base) as name:
   root=Path(name).resolve();self.assertTrue(root.is_relative_to(base.resolve()))
   src=V/'library/reports/collection/qa';dest=root/'library/reports/collection/qa'
   shutil.copytree(src/'support-snapshots',dest/'support-snapshots')
   shutil.copy2(src/'support-restore-plan.json',dest/'support-restore-plan.json')
   plan=json.loads((dest/'support-restore-plan.json').read_text(encoding='utf-8'))
   result=regenerate(root);self.assertEqual(result['verified_files'],len(plan['entries']))
   for e in plan['entries']:self.assertEqual((root/e['path']).read_bytes(),(V/e['path']).read_bytes())
   (root/'START-HERE.md').write_text('conflicting-user-note',encoding='utf-8')
   with self.assertRaises(AssertionError):regenerate(root)
   self.assertEqual((root/'START-HERE.md').read_text(encoding='utf-8'),'conflicting-user-note')
   plan['entries'][0]['path']='../escape.md'
   (dest/'support-restore-plan.json').write_text(json.dumps(plan),encoding='utf-8')
   with self.assertRaises(AssertionError):regenerate(root)
if __name__=='__main__':unittest.main()
