"""验证整书签收拒绝同数量换义、错后证、漏项和已签组内容篡改。"""
import copy
import tempfile
import unittest
from pathlib import Path

from book_audit_common import AuditError, encode_json, sha
from record_primary_whole_book_review import check_batches, check_groups


class SignedReviewIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.stage = Path(self.temp.name)
        self.audit = self.stage / 'audit/whole-book'
        self.audit.mkdir(parents=True)
        self.rows = [dict(candidate_id='a', status='answered', rationale='任务确已执行',
                          audit_domain='quest-result', later_chapters=[8, 9, 8]),
                     dict(candidate_id='b', status='unknown', rationale='具名角色去向未明',
                          audit_domain='specific-person', later_chapters=[9])]
        self.write(self.audit / 'batch.json', self.rows)
        self.write(self.stage / 'primary-audit-review-progress.json', {
            'batches': [dict(path='batch.json', sha256=sha(self.audit / 'batch.json'),
                             candidate_ids=['a', 'b'], count=2)],
            'distinct_reviewed_candidate_ids': ['a', 'b'], 'distinct_reviewed_candidates': 2})
        self.package = dict(historical={'candidates': []}, local={'candidates': []})
        for kind, row in zip(('historical', 'local'), self.rows):
            assessment = {k: copy.deepcopy(row[k]) for k in ('status', 'rationale', 'audit_domain', 'later_chapters')}
            assessment['later_evidence'] = [{'chapter_id': f'ch-{n:04d}'} for n in sorted(set(row['later_chapters']))]
            self.package[kind]['candidates'].append(dict(candidate_id=row['candidate_id'], terminal_assessment=assessment))

    def write(self, path, value):
        path.write_bytes(encode_json(value))

    def test_same_count_swapped_meanings_rejected(self):
        changed = copy.deepcopy(self.package)
        first = changed['historical']['candidates'][0]['terminal_assessment']
        second = changed['local']['candidates'][0]['terminal_assessment']
        first['rationale'], second['rationale'] = second['rationale'], first['rationale']
        with self.assertRaises(AuditError):
            check_batches(self.stage, self.audit, changed)

    def test_changed_later_evidence_rejected(self):
        changed = copy.deepcopy(self.package)
        changed['local']['candidates'][0]['terminal_assessment']['later_evidence'] = [{'chapter_id': 'ch-0008'}]
        with self.assertRaises(AuditError):
            check_batches(self.stage, self.audit, changed)

    def test_missing_candidate_rejected(self):
        changed = copy.deepcopy(self.package)
        changed['local']['candidates'] = []
        with self.assertRaises(AuditError):
            check_batches(self.stage, self.audit, changed)

    def test_signed_file_changed_rejected(self):
        self.write(self.audit / 'batch.json', list(reversed(self.rows)))
        with self.assertRaises(AuditError):
            check_batches(self.stage, self.audit, self.package)

    def test_equivalent_deduplicated_evidence_allowed(self):
        batches, signed = check_batches(self.stage, self.audit, self.package)
        self.assertEqual((batches, set(signed)), (1, {'a', 'b'}))

    def test_changed_character_with_same_ids_rejected(self):
        groups, package = [], {}
        for section, id_field in [('characters', 'audit_id'), ('findings', 'key')]:
            rows = [{id_field: section + '-1', 'terminal_state': '有明确边界的原判断'}]
            path = self.audit / (section + '.json')
            self.write(path, {section: rows})
            groups.append(dict(path=path.name, sha256=sha(path), section=section,
                               id_field=id_field, reviewed_ids=[rows[0][id_field]], count=1))
            package[section] = {section: copy.deepcopy(rows)}
        self.write(self.stage / 'primary-research-group-review-progress.json', {'groups': groups})
        self.assertEqual(check_groups(self.stage, self.audit, package), 2)
        package['characters']['characters'][0]['terminal_state'] = '被总装者无声改写'
        with self.assertRaises(AuditError):
            check_groups(self.stage, self.audit, package)


if __name__ == '__main__':
    unittest.main()
