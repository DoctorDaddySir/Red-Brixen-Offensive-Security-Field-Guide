"""Synthetic export boundary tests; no real tmux session or engagement data."""
import importlib.machinery
import importlib.util
import os
from pathlib import Path
import sqlite3
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / 'tools/scripts/rb-ops'
sys.path.insert(0, str(TOOLS))
import rb_exports


def load(name):
    loader = importlib.machinery.SourceFileLoader(name.replace('-', '_'), str(TOOLS / name))
    module = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    loader.exec_module(module)
    return module


class ExportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.modules = {name: load(name) for name in ('rb-report', 'rb-creds', 'rb-chain', 'rb-findings')}
        self.db = sqlite3.connect(':memory:')
        self.db.row_factory = sqlite3.Row
        self.addCleanup(self.db.close)
        for name in ('rb-creds', 'rb-chain', 'rb-findings'):
            self.modules[name].init_db(self.db)
        for module in self.modules.values():
            module.engagement_context = lambda: ('SESSION_PRIVATE', self.root, self.root / 'db')
            module.connect = lambda: self.db
        self.payload = 'UNKNOWN_PRIVATE ![attachment](file:///private/proof.png) <img src="https://private.invalid/token">'
        self.db.execute('INSERT INTO credentials VALUES (1,?,?,?,?,?,?,?,1,?)',
                        (self.payload, 'REGISTERED_SECRET', self.payload, self.payload, self.payload, self.payload, self.payload, self.payload))
        self.db.execute('INSERT INTO credential_validations VALUES (1,1,?,?,?,?)', (self.payload,) * 4)
        self.db.execute('INSERT INTO exploit_chain_steps VALUES (1,1,?,?,?,?,?,?,?,?)', (self.payload,) * 8)
        self.db.execute('INSERT INTO findings VALUES (1,?,?,?,?,9.8,?,?)', (self.payload,) * 6)
        for file in ('notes.md', 'scope.md'):
            (self.root / file).write_text('FILE_PRIVATE ' + self.payload)

    def export(self, name, restricted=False, output=None):
        output = output or self.root / ('result.restricted.md' if restricted else 'result.md')
        argv = [name] + ([] if name == 'rb-report' else ['export']) + ['--output', str(output)]
        if restricted:
            argv += ['--restricted']
        with patch.object(sys, 'argv', argv):
            self.modules[name].main()
        return output

    def test_all_default_exports_exclude_every_unreviewed_text_source(self):
        for name in self.modules:
            with self.subTest(name=name):
                out = self.export(name)
                text = out.read_text()
                for marker in ('UNKNOWN_PRIVATE', 'REGISTERED_SECRET', 'FILE_PRIVATE', 'SESSION_PRIVATE',
                               'file://', 'https://private', '<img', '![attachment]'):
                    self.assertNotIn(marker, text)
                self.assertIn('review', text)
                self.assertEqual(stat.S_IMODE(out.stat().st_mode), 0o600)
        self.assertIn('9.8', self.export('rb-findings').read_text())
        self.assertIn('Validation recorded: Yes', self.export('rb-creds').read_text())
        self.assertIn('Chain record 1', self.export('rb-chain').read_text())

    def test_default_never_reads_private_files(self):
        with patch.object(Path, 'read_text', side_effect=AssertionError('private file read')):
            self.export('rb-report')

    def test_restricted_preserves_operator_detail(self):
        for name in self.modules:
            with self.subTest(name=name):
                out = self.export(name, restricted=True)
                text = out.read_text()
                self.assertIn('RESTRICTED APPENDIX', text)
                self.assertIn(self.payload, text)
                self.assertEqual(stat.S_IMODE(out.stat().st_mode), 0o600)
        for name in ('rb-creds', 'rb-report'):
            self.assertNotIn('REGISTERED_SECRET', self.export(name, restricted=True).read_text())
        report = self.export('rb-report', restricted=True).read_text()
        for marker in ('FILE_PRIVATE', 'SESSION_PRIVATE'):
            self.assertIn(marker, report)

    def test_restricted_cannot_overwrite_default_name(self):
        out = self.root / 'client.md'
        out.write_text('original')
        for name in self.modules:
            with self.subTest(name=name), self.assertRaises(ValueError):
                self.export(name, restricted=True, output=out)
        self.assertEqual(out.read_text(), 'original')
        for name in self.modules:
            with self.subTest(name=name), self.assertRaises(ValueError):
                self.export(name, output=self.root / 'reserved.restricted.md')

    def test_defaults_have_separate_paths(self):
        for restricted, suffix in ((False, '.md'), (True, '.restricted.md')):
            for name, base in [('rb-report', 'engagement_report'), ('rb-creds', 'credentials'),
                               ('rb-chain', 'attack_chain'), ('rb-findings', 'findings')]:
                argv = [name] + ([] if name == 'rb-report' else ['export']) + (['--restricted'] if restricted else [])
                with patch.object(sys, 'argv', argv):
                    self.modules[name].main()
                self.assertTrue((self.root / '07-reporting' / (base + suffix)).exists())

    def test_invalid_numeric_metadata_fails_without_replacing_output(self):
        out = self.root / 'client.md'
        out.write_text('original')
        for value in ('UNKNOWN_PRIVATE', float('inf'), -1, 11):
            self.db.execute('UPDATE findings SET cvss_score=?', (value,))
            for name in ('rb-report', 'rb-findings'):
                with self.subTest(value=value, name=name), self.assertRaises(ValueError):
                    self.export(name, output=out)
                self.assertEqual(out.read_text(), 'original')
        self.db.execute('UPDATE credentials SET validated=?', ('UNKNOWN_PRIVATE',))
        with self.assertRaises(ValueError):
            self.export('rb-creds', output=out)

    def test_symlink_and_hardlink_outputs_do_not_modify_target(self):
        target = self.root / 'target'
        target.write_text('original')
        symlink = self.root / 'link.md'
        symlink.symlink_to(target)
        with self.assertRaises(ValueError):
            self.export('rb-report', output=symlink)
        hardlink = self.root / 'hard.md'
        os.link(target, hardlink)
        self.export('rb-report', output=hardlink)
        self.assertEqual(target.read_text(), 'original')

    def test_write_failure_keeps_existing_output_and_removes_temporary(self):
        out = self.root / 'report.md'
        out.write_text('original')
        with patch.object(rb_exports.os, 'replace', side_effect=OSError('test')):
            with self.assertRaises(OSError):
                self.export('rb-report', output=out)
        self.assertEqual(out.read_text(), 'original')
        self.assertEqual(list(self.root.glob('.rb-export-*')), [])

    def test_unvalidated_status_and_zero_score_remain_valid(self):
        self.db.execute('UPDATE credentials SET validated=0')
        self.db.execute('UPDATE findings SET cvss_score=0')
        self.assertIn('Validation recorded: No', self.export('rb-creds').read_text())
        self.assertIn('Recorded CVSS score: 0', self.export('rb-findings').read_text())

    def test_empty_and_partial_databases(self):
        for table in ('findings', 'exploit_chain_steps', 'credential_validations', 'credentials'):
            self.db.execute(f'DROP TABLE {table}')
        for name in self.modules:
            self.assertIn('No ', self.export(name).read_text())

    def test_copied_and_symlinked_installation_help(self):
        import shutil
        install = self.root / 'bin'
        install.mkdir()
        shutil.copy(TOOLS / 'rb_exports.py', install)
        shutil.copy(TOOLS / 'rb_finding_model.py', install)
        shutil.copy(TOOLS / 'rb_private.py', install)
        shutil.copy(TOOLS / 'rb_credentials.py', install)
        for name in self.modules:
            shutil.copy(TOOLS / name, install)
            for script in (install / name, self.root / name):
                if script.parent != install:
                    script.symlink_to(install / name)
                result = subprocess.run([sys.executable, str(script), '--help'], capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == '__main__':
    unittest.main()
