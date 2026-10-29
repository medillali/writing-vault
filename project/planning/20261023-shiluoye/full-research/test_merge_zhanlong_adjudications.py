"""在隔离小样例上验证合池的完整性边界，不构造真实阅读凭据。"""
from pathlib import Path
import copy, hashlib, importlib.util, json, tempfile, unittest
B = Path(__file__).parent

class MergeTests(unittest.TestCase):
    def setUp(self):
        module = B / 'merge_zhanlong_adjudications.py'
        self.assertTrue(module.exists(), '缺少保护原问题与已签集合的合池功能')
        spec = importlib.util.spec_from_file_location('merge_zhanlong_test', module)
        self.m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.m)
        self.tmp = tempfile.TemporaryDirectory(prefix='zm-', dir=B)
        self.addCleanup(self.tmp.cleanup)
        self.a = Path(self.tmp.name)
        self.progress = self.a / 'signed.json'
        self.source = dict(source_id='src-test', revision='a'*64, chapters=[dict(chapter_id='ch-0001', start_line=1, end_line=10)])
        self.originals = {}
        self.rows = []
        for kind, cid in [('historical', 'h1'), ('local', 'l1')]:
            candidate = dict(candidate_id=cid, title=cid, original_record={'raw': ['不可改']}, terminal_assessment={'status':'unknown','review_progress':'pending-manual-adjudication'})
            pool = dict(source_id='src-test', pending_inputs=[], candidates=[candidate])
            self.originals[kind] = copy.deepcopy(pool)
            self.write(self.a / f'{kind}-question-pool.json', pool)
            self.rows.append(dict(candidate_id=cid, title=cid, status='partial', audit_domain='test', rationale='只判已证部分', later_chapters=[1], actual_reviewer='fixture-reader', reading_attribution='隔离样例，不是实际阅读', later_evidence=[dict(source_id='src-test', revision='a'*64, chapter_id='ch-0001', start_line=3, end_line=4, claim_kind='fact', source_reader='original-reader', evidence_access='derived-only')]))
        self.batch = self.a / 'nested/batch.json'
        self.sign()

    def write(self, path, data):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

    def sign(self):
        self.write(self.batch, self.rows)
        self.write(self.progress, dict(batches=[dict(path='nested/batch.json', sha256=hashlib.sha256(self.batch.read_bytes()).hexdigest(), candidate_ids=[r['candidate_id'] for r in self.rows], count=len(self.rows))], distinct_reviewed_candidate_ids=sorted({r['candidate_id'] for r in self.rows}), distinct_reviewed_candidates=len({r['candidate_id'] for r in self.rows})))

    def test_preserve_originals_and_precise_evidence_attribution(self):
        outputs, report = self.m.prepare_merge(self.a, self.progress, self.source)
        self.assertEqual(report['candidates'], 2)
        for kind, old in self.originals.items():
            final = outputs[kind]['candidates'][0]
            self.assertEqual({k:v for k,v in final.items() if k!='terminal_assessment'}, {k:v for k,v in old['candidates'][0].items() if k!='terminal_assessment'})
            signed = next(r for r in self.rows if r['candidate_id']==final['candidate_id'])
            self.assertEqual(final['terminal_assessment']['later_evidence'], signed['later_evidence'])
            self.assertEqual(json.loads((self.a / f'{kind}-question-pool.json').read_text(encoding='utf-8')), old)

    def test_reject_incomplete_signed_set(self):
        self.rows.pop()
        self.sign()
        with self.assertRaisesRegex(ValueError, '未全部签收'):
            self.m.prepare_merge(self.a, self.progress, self.source)

    def test_preserve_structured_source_attribution(self):
        self.rows[0]['source_attribution'] = dict(early_source='初读归原读者', later_source='仅派生复核', boundary='不增加全文覆盖')
        self.sign()
        outputs, _ = self.m.prepare_merge(self.a, self.progress, self.source)
        self.assertEqual(outputs['historical']['candidates'][0]['terminal_assessment']['source_attribution'], self.rows[0]['source_attribution'])

    def test_reject_changed_signed_bytes(self):
        self.batch.write_text(self.batch.read_text(encoding='utf-8')+' ', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'SHA'):
            self.m.prepare_merge(self.a, self.progress, self.source)

    def test_reject_duplicate_ids(self):
        self.rows.append(copy.deepcopy(self.rows[0]))
        self.sign()
        with self.assertRaisesRegex(ValueError, '重复'):
            self.m.prepare_merge(self.a, self.progress, self.source)

    def test_reject_out_of_range_evidence(self):
        self.rows[0]['later_evidence'][0]['end_line'] = 11
        self.sign()
        with self.assertRaisesRegex(ValueError, '证据'):
            self.m.prepare_merge(self.a, self.progress, self.source)

    def test_reject_path_escape(self):
        progress = json.loads(self.progress.read_text(encoding='utf-8'))
        progress['batches'][0]['path'] = '../escape.json'
        self.write(self.progress, progress)
        with self.assertRaisesRegex(ValueError, '越界'):
            self.m.prepare_merge(self.a, self.progress, self.source)

if __name__ == '__main__':
    unittest.main()
