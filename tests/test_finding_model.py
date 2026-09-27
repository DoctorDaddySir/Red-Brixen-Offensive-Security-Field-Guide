"""Versioned detail migration, validation and rendering with synthetic findings."""
import copy
import json
from pathlib import Path
import sqlite3
import sys
import unittest
from unittest.mock import patch

import test_rb_exports as export_fixture
from rb_finding_model import decode, empty_details, init_details, read_details, save_details, validate


class FindingModelTests(unittest.TestCase):
    def setUp(self):
        self.fixture = export_fixture.ExportTests()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.db = self.fixture.db
        init_details(self.db)

    def populated(self):
        doc = empty_details()
        for key, value in doc.items():
            if isinstance(value, str):
                doc[key] = 'PRIVATE ' + key + '\nSecond line'
        doc['evidence'] = [{'id': 'E-1', 'path': '/missing/private-evidence.png',
                            'caption': 'PRIVATE screenshot', 'captured_at': '2026-09-27T10:00:00Z',
                            'sha256': 'a' * 64, 'redaction_status': 'unreviewed'}]
        doc['review'] = {'status': 'reviewed', 'reviewer': 'PRIVATE reviewer',
                         'reviewed_at': '2026-09-27T11:00:00Z', 'notes': 'PRIVATE review notes'}
        doc['retest'] = {'status': 'resolved', 'tester': 'PRIVATE tester',
                         'tested_at': '2026-09-27T12:00:00Z', 'method': 'PRIVATE exact action',
                         'result': 'PRIVATE access denied', 'evidence_ids': ['E-1']}
        return doc

    def test_legacy_migration_preserves_originals_and_is_repeatable(self):
        self.db.execute('DROP TABLE finding_details')
        before = tuple(self.db.execute('SELECT * FROM findings').fetchone())
        init_details(self.db)
        self.assertEqual(read_details(self.db, 1), empty_details())
        saved = self.populated()
        save_details(self.db, 1, saved)
        init_details(self.db)
        self.assertEqual(read_details(self.db, 1), saved)
        self.assertEqual(tuple(self.db.execute('SELECT * FROM findings').fetchone()), before)

    def test_failed_backfill_rolls_back_without_changing_records(self):
        self.db.execute('DELETE FROM finding_details')
        self.db.execute("CREATE TRIGGER fail_details BEFORE INSERT ON finding_details BEGIN SELECT RAISE(ABORT, 'test'); END")
        self.db.commit()
        with self.assertRaises(sqlite3.IntegrityError):
            init_details(self.db)
        self.assertEqual(self.db.execute('SELECT COUNT(*) FROM finding_details').fetchone()[0], 0)
        self.assertEqual(self.db.execute('SELECT COUNT(*) FROM findings').fetchone()[0], 1)

    def test_unknown_version_and_fields_leave_saved_document_unchanged(self):
        saved = self.populated()
        save_details(self.db, 1, saved)
        for change in ({'model_version': 2}, {'typo_remediation': 'discard me'}, {'impact': 42}):
            bad = copy.deepcopy(saved);bad.update(change)
            with self.assertRaises(ValueError):
                save_details(self.db, 1, bad)
            self.assertEqual(read_details(self.db, 1), saved)
        with self.assertRaises(ValueError):
            decode('{"model_version":1,"model_version":2}')

    def test_invalid_evidence_and_retest_claims_rejected(self):
        for section, key, value in [('review', 'reviewer', ''), ('review', 'reviewed_at', '2026-09-27'),
                                     ('retest', 'method', ''), ('retest', 'evidence_ids', ['missing']),
                                     ('retest', 'status', 'passed')]:
            doc = self.populated();doc[section][key] = value
            with self.subTest(section=section, key=key), self.assertRaises(ValueError):
                validate(doc)
        for key, value in [('sha256', 'not-a-digest'), ('redaction_status', 'safe'), ('id', '')]:
            doc = self.populated();doc['evidence'][0][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                validate(doc)
        doc = self.populated();doc['evidence'].append(copy.deepcopy(doc['evidence'][0]))
        with self.assertRaises(ValueError):validate(doc)

    def test_restricted_renderers_show_real_content_without_reading_artifacts(self):
        doc = self.populated();save_details(self.db, 1, doc)
        for name in ('rb-report', 'rb-findings'):
            body = self.fixture.export(name, restricted=True).read_text()
            for marker in ('PRIVATE remediation', 'PRIVATE reproduction', 'PRIVATE impact',
                           '/missing/private-evidence.png', 'PRIVATE reviewer', 'PRIVATE access denied'):
                self.assertIn(marker, body)
            self.assertNotIn('Add remediation guidance here.', body)
            public = self.fixture.export(name).read_text()
            self.assertNotIn('PRIVATE', public)
            self.assertNotIn('/missing/', public)

    def test_details_cli_replaces_and_displays_document(self):
        doc = self.populated();path = self.fixture.root / 'details.json'
        path.write_text(json.dumps(doc))
        module = self.fixture.modules['rb-findings']
        with patch.object(sys, 'argv', ['rb-findings', 'details', '1', '--file', str(path)]):
            module.main()
        self.assertEqual(read_details(self.db, 1), doc)
        with patch.object(sys, 'argv', ['rb-findings', 'details', '1']), patch('builtins.print') as output:
            module.main()
        self.assertEqual(json.loads(output.call_args.args[0]), doc)
        self.assertEqual(path.read_text(), json.dumps(doc))

    def test_unknown_finding_cannot_create_orphan_details(self):
        with self.assertRaises(ValueError):save_details(self.db, 999, empty_details())
        self.assertIsNone(self.db.execute('SELECT 1 FROM finding_details WHERE finding_id=999').fetchone())

    def test_legacy_report_can_read_without_migrating(self):
        self.db.execute('DROP TABLE finding_details')
        report = self.fixture.export('rb-report', restricted=True).read_text()
        self.assertIn('Not recorded.', report)
        self.assertIsNone(self.db.execute("SELECT 1 FROM sqlite_master WHERE name='finding_details'").fetchone())

    def test_new_interactive_finding_has_default_detail_record(self):
        # Title, description, host; eight default CVSS answers; save confirmation.
        module = self.fixture.modules['rb-findings']
        with patch('builtins.input', side_effect=['Synthetic', 'Observed behavior', 'lab'] + [''] * 9), patch.object(sys, 'argv', ['rb-findings', 'add']):
            module.main()
        identifier = self.db.execute('SELECT MAX(id) FROM findings').fetchone()[0]
        self.assertEqual(read_details(self.db, identifier), empty_details())


if __name__ == '__main__':
    unittest.main()
