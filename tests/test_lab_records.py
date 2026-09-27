"""Reject incomplete evidence without treating JSON validation as execution proof."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

from check_lab_records import RECORDS, ROOT, check, validate_record


class LabRecordTests(unittest.TestCase):
    def test_committed_records_are_complete(self):
        self.assertEqual(check(), [])

    def test_missing_record_and_fixture_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.assertEqual(len(check(root)), len(RECORDS))
            for path, (fixture, *_) in RECORDS.items():
                (root / fixture).parent.mkdir(parents=True, exist_ok=True)
                (root / fixture).write_text('# synthetic fixture')
            self.assertEqual(len(check(root)), len(RECORDS))
            for path in RECORDS:
                (root / path).write_text('{bad JSON')
            self.assertEqual(len(check(root)), len(RECORDS))

    def test_invalid_metadata_is_rejected(self):
        for path, (_, scope, text_fields, mapping_fields) in RECORDS.items():
            valid = json.loads((ROOT / path).read_text())
            changes = [
                {scope: ''}, {'date_utc': '2026-09-26'},
                {'date_utc': 'not a date'}, {'date_utc': '2026-09-26T12:00:00+01:00'},
                {'checks': []}, {'checks': 'passed'}, {'checks': [None]},
                {'checks': ['same', 'same']},
            ]
            changes.extend({field: ''} for field in text_fields)
            changes.extend({field: {}} for field in mapping_fields)
            for change in changes:
                record = copy.deepcopy(valid)
                record.update(change)
                with self.subTest(path=path, change=change), self.assertRaises(ValueError):
                    validate_record(record, scope, text_fields, mapping_fields)
            with self.assertRaises(ValueError):
                validate_record([], scope, text_fields, mapping_fields)

    def test_tool_versions_and_archive_integrity_metadata_required(self):
        for path, (_, scope, text_fields, mapping_fields) in RECORDS.items():
            record = json.loads((ROOT / path).read_text())
            field = mapping_fields[0]
            first = next(iter(record[field]))
            del record[field][first]
            with self.assertRaises(ValueError):
                validate_record(record, scope, text_fields, mapping_fields)
        path = 'labs/ligolo/result.json'
        _, scope, text_fields, mapping_fields = RECORDS[path]
        record = json.loads((ROOT / path).read_text())
        record['archive_sha256']['agent'] = 'not a checksum'
        with self.assertRaises(ValueError):
            validate_record(record, scope, text_fields, mapping_fields)
