"""只在planning临时目录内发布合成小样例，不向真实资料库写入。"""
import hashlib
import tempfile
import unittest
from pathlib import Path
from book_audit_common import BASE, AuditError, encode_json, preflight, read, sha
from publish_book_audit import generated, publish
from validate_book_audit import validate


class AuditPublicationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='audit-fixture-', dir=BASE)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.book = 'fixture-book'
        self.stage = self.root / 'staging'
        self.audit = self.stage / 'vol08'
        self.dest = self.root / 'writing-vault/library/reports' / self.book
        self.ev = dict(source_id='fixture-source', revision='fixture-revision', chapter_id='ch-0001',
                       start_line=1, end_line=2, claim_kind='fact', access_level='fixture-only')
        self.write(self.stage / 'source.json', dict(source_id='fixture-source', revision='fixture-revision',
                   chapters=[dict(chapter_id='ch-0001', start_line=1, end_line=20)]))
        self.write(self.dest / 'README.md', '# 既有综合与阅读\n\n[阅读](reading/README.md)\n')
        self.write(self.dest / 'reading/README.md', '# 既有阅读内容\n')
        self.graph = self.root / 'writing-vault/library/sources/fixture-source/plot-graph.json'
        self.write(self.graph, dict(revision=9, threads=[dict(id='v1-thread', status='open')]))
        self.write(self.root / 'writing-vault/library/views/plots/fixture-source/collected/index.html', '<html>fixture</html>')
        formal = {}
        for kind, value in [('analysis', {}), ('graph', {}), ('cards', {'review_status': 'draft', 'human_note': '保留'})]:
            path = self.dest / f'vol01-{kind}.json'
            self.write(path, value)
            formal[path.relative_to(self.root).as_posix()] = sha(path)
        inputs = [dict(volume=1, status='formal-library', open_questions=1, graph_threads=1,
                       analysis=next(x for x in formal if '-analysis.' in x),
                       graph=next(x for x in formal if '-graph.' in x))]
        for kind in ['analysis', 'graph']:
            inputs[0][kind + '_sha256'] = formal[inputs[0][kind]]
        def decision():
            return dict(status='unknown', rationale='合成样例未给结果', later_evidence=[self.ev],
                        audit_domain='fixture-domain', review_progress='reviewed-draft')
        history = [dict(candidate_id='q1', volume=1, entry_type='analysis.open_questions',
                        original_stage_status='open', title='合成问题', original_record={'question': 'x'},
                        original_evidence=[self.ev], terminal_assessment=decision()),
                   dict(candidate_id='t1', volume=1, entry_type='graph.threads',
                        original_stage_status='open', title='合成线程', original_record={'id': 'thread', 'status': 'open'},
                        original_evidence=[self.ev], terminal_assessment=decision())]
        arc = dict(audit_id='arc-01', name='样例人物', terminal_state='样例终点', evidence=[self.ev], review_status='draft')
        local = dict(candidate_id='l1', volume=1, original_field='issues', original_index=0,
                     original_evidence=[self.ev], terminal_assessment=decision())
        files = {
            'character-arc-audit-draft.json': {'characters': [arc]},
            'end-state-audit-draft.json': {'findings': [dict(key='f1', evidence=[self.ev], review_status='draft')]},
            'historical-question-pool.json': dict(candidates=history, inputs=inputs,
                                                 local_issue_records=[dict(volume=1, field='issues', original_records=[{}])]),
            'local-question-pool.json': {'candidates': [local]},
            'audit-validation.json': dict(character_arcs=1, focused_findings=1, historical_candidates=2,
                                         local_candidates=1, evidence_references_checked=8,
                                         pending_inputs=[], unadjudicated_candidates=0),
            'whole-book-audit-handoff.md': '# 样例交接\n',
            'provenance_fixture.py': '# 只存档，不执行\n',
        }
        for name in ['character-arc-audit-draft', 'end-state-audit-draft', 'historical-question-pool', 'local-question-pool']:
            files[name + '.md'] = '# 样例可读原稿\n'
        for name, value in files.items():
            self.write(self.audit / name, value)
        core = {}
        for name in ['analysis.json', 'cards.json', 'graph.json', 'read-log.json', 'chapter-notes.jsonl', 'reader-state.json']:
            self.write(self.audit / name, {})
            core[name] = sha(self.audit / name)
        self.manifest = dict(source_id='fixture-source', audit_sha256={n: sha(self.audit / n) for n in files},
                             formal_input_sha256=formal, frozen_volume08_hashes=core)
        self.write(self.audit / 'audit-freeze-manifest.json', self.manifest)
        self.write(self.stage / 'primary-whole-book-review.json', dict(status='reviewed_for_library_import',
                   reviewer='primary', fixture_only=True, freeze_manifest_sha256=sha(self.audit / 'audit-freeze-manifest.json')))

    def write(self, path, value):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(value.encode('utf-8') if isinstance(value, str) else encode_json(value))

    def context(self):
        return preflight(self.root, self.book, self.stage, 'vol08', self.stage / 'source.json', True)

    def test_publish_and_independent_validation(self):
        ctx = self.context()
        before = sha(self.graph)
        readme = (self.dest / 'README.md').read_bytes()
        files, stats, overlay = generated(ctx, {})
        result = publish(ctx, files, stats)
        self.assertEqual(result['status'], 'published-audit-validation-passed')
        self.assertEqual(sha(self.graph), before)
        self.assertTrue((self.dest / 'README.md').read_bytes().startswith(readme))
        self.assertEqual(read(self.dest / 'question-ledger.json')['not_a_merged_pool'], True)
        self.assertEqual(validate(self.root, self.book)['graph_threads'], 1)
        # 已发布包的独立验收不依赖原暂存目录。
        self.stage.rename(self.stage.with_name('staging-moved'))
        self.assertEqual(validate(self.root, self.book)['counts']['local'], 1)

    def test_missing_review_blocks_before_write(self):
        (self.stage / 'primary-whole-book-review.json').unlink()
        with self.assertRaises(AuditError):
            self.context()
        self.assertFalse((self.dest / 'audit').exists())

    def test_changed_review_manifest_blocks_before_write(self):
        self.write(self.stage / 'primary-whole-book-review.json', dict(status='reviewed_for_library_import', reviewer='primary', freeze_manifest_sha256='0' * 64))
        with self.assertRaises(AuditError):
            self.context()
        self.assertFalse((self.dest / 'audit').exists())

    def test_tampered_freeze_blocks(self):
        self.write(self.audit / 'character-arc-audit-draft.md', '变化')
        with self.assertRaises(AuditError):
            self.context()

    def test_path_traversal_blocks(self):
        from book_audit_common import contained
        with self.assertRaises(AuditError):
            contained(self.root, '../escape.json')

    def test_post_publication_tamper_detected(self):
        ctx = self.context()
        files, stats, _ = generated(ctx, {})
        publish(ctx, files, stats)
        self.write(self.dest / 'audit/whole-book/local-question-pool.json', {})
        with self.assertRaises(AuditError):
            validate(self.root, self.book)


if __name__ == '__main__':
    unittest.main(verbosity=2)
