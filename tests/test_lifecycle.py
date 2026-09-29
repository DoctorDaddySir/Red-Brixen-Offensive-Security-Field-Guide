"""Actual CLI selection, transactional migration, edits and private history."""
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from test_rb_exports import TOOLS
from rb_ops import context, database, lifecycle
from rb_finding_model import empty_details, read_details, save_details
import rb_credentials as vault

VECTOR = 'CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H'


class LifecycleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in ('alpha', 'beta'):
            (self.root / name).mkdir(mode=0o700)
        self.env = dict(os.environ, PENTEST_BASE=str(self.root))
        self.env.pop('TMUX', None)
        self.env.pop('RB_CREDENTIAL_KEY_FILE', None)
        self.previous_umask = os.umask(0o077)
        self.addCleanup(os.umask, self.previous_umask)

    def conn(self, name='alpha'):
        conn = database.open_database(self.root / name / '.redbrixen/opskit.db')
        self.addCleanup(conn.close)
        return conn

    def cli(self, tool, *args, ok=True):
        result = subprocess.run([sys.executable, str(TOOLS / tool), *args], env=self.env,
                                capture_output=True, text=True, timeout=10)
        if ok:
            self.assertEqual(result.returncode, 0, result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0)
        return result

    def finding(self, conn):
        return lifecycle.create_record(conn, 'finding', dict(title='Synthetic finding', description='Observed',
            host='host', cvss_vector=VECTOR, cvss_score=9.8, severity='Critical'))

    def test_selection_is_explicit_safe_and_resolved_once(self):
        with patch.dict(os.environ, self.env, clear=True), patch.object(context.subprocess, 'check_output') as tmux:
            with context.invocation('alpha'):
                first = context.engagement_context()
                with patch.dict(os.environ, {'PENTEST_BASE': '/absent'}):
                    self.assertEqual(context.engagement_context(), first)
            tmux.assert_not_called()
            with self.assertRaises(ValueError):
                context.resolve()
            with patch.dict(os.environ, {'TMUX': 'synthetic'}):
                tmux.side_effect = ['alpha', 'beta']
                with context.invocation():
                    self.assertEqual(context.engagement_context()[0], 'alpha')
                    self.assertEqual(context.engagement_context()[0], 'alpha')
                self.assertEqual(tmux.call_count, 1)
                with context.invocation():
                    self.assertEqual(context.engagement_context()[0], 'beta')
            for bad in ('../alpha', '.', '..', '/alpha', 'alpha/beta', '', ' alpha', 'alpha\\beta', 'missing'):
                with self.subTest(bad=bad), self.assertRaises(ValueError):
                    context.resolve(bad)
            (self.root / 'alias').symlink_to(self.root / 'alpha', target_is_directory=True)
            with self.assertRaises(ValueError):
                context.resolve('alias')
        self.cli('rb-chain', '--engagement', 'alpha', '--engagement', 'beta', 'list', ok=False)
        self.assertFalse((self.root / 'missing').exists())

    def test_two_engagement_cli_isolation_and_no_tmux_requirement(self):
        with ThreadPoolExecutor(max_workers=2) as pool:
            jobs = [pool.submit(self.cli, 'rb-chain', '--engagement', name, 'add', name + ' private')
                    for name in ('alpha', 'beta')]
            for job in jobs:
                job.result()
        for name, other in (('alpha', 'beta'), ('beta', 'alpha')):
            output = self.cli('rb-chain', '--engagement', name, 'list').stdout
            self.assertIn(name + ' private', output)
            self.assertNotIn(other + ' private', output)
            history = json.loads(self.cli('rb-chain', '--engagement', name, 'history', '1').stdout)
            self.assertEqual(history[0]['after']['title'], name + ' private')
            for tool, args in (('rb-findings', ('list',)), ('rb-creds', ('list',)), ('rb-report', ())):
                self.cli(tool, '--engagement', name, *args)
        with patch.dict(self.env, {'TMUX': '/invalid'}):
            self.cli('rb-chain', '--engagement', 'alpha', 'list')

    def test_migration_legacy_and_encrypted_data_preserved(self):
        conn = sqlite3.connect(':memory:')
        self.addCleanup(conn.close)
        for ddl in database.LEGACY_TABLES:
            conn.execute(ddl)
        conn.execute("INSERT INTO findings VALUES (7,'old','description','host',?,9.8,'Critical','date')", (VECTOR,))
        conn.execute("INSERT INTO credentials VALUES (2,'alice','LEGACY_SECRET','password','','','','',0,'date')")
        conn.execute("INSERT INTO credential_validations VALUES (4,2,'host','service','notes','date')")
        conn.commit()
        before = tuple(conn.execute('SELECT * FROM credentials').fetchone())
        database.migrate(conn)
        self.assertEqual(tuple(conn.execute('SELECT * FROM credentials').fetchone()), before)
        self.assertEqual(read_details(conn, 7), empty_details())
        self.assertEqual(conn.execute('SELECT COUNT(*) FROM credential_secrets').fetchone()[0], 0)
        self.assertEqual(conn.execute('SELECT COUNT(*) FROM record_history').fetchone()[0], 0)
        self.assertEqual(conn.execute('SELECT credential_id FROM credential_validations').fetchone()[0], 2)
        # Generic migrations never invoke credential crypto or convert legacy secrets.
        conn.execute("UPDATE credentials SET secret='' WHERE id=2")
        conn.execute("INSERT INTO credential_secrets VALUES (2,1,'OPAQUE_ENCRYPTED_TOKEN')")
        saved = empty_details(); saved['impact'] = 'existing detail'
        conn.execute('UPDATE finding_details SET document=? WHERE finding_id=7', (json.dumps(saved),))
        conn.commit()
        with patch.object(vault, 'cipher', side_effect=AssertionError('key access')):
            database.migrate(conn)
        self.assertEqual(conn.execute('SELECT token FROM credential_secrets').fetchone()[0], 'OPAQUE_ENCRYPTED_TOKEN')
        self.assertEqual(read_details(conn, 7), saved)
        self.assertEqual(conn.execute('SELECT version FROM rb_schema').fetchone()[0], 2)

    def test_failed_schema_step_rolls_back_and_unknown_future_rejected(self):
        conn = sqlite3.connect(':memory:')
        self.addCleanup(conn.close)
        conn.execute('CREATE TABLE sentinel (value)')
        conn.execute("INSERT INTO sentinel VALUES ('keep')")
        conn.commit()
        def broken(connection):
            connection.execute('CREATE TABLE should_rollback (value)')
            raise RuntimeError('injected interruption')
        with patch.object(database, 'MIGRATIONS', (database.baseline, broken)):
            with self.assertRaises(RuntimeError):
                database.migrate(conn)
        names = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertEqual(names, {'sentinel'})
        database.migrate(conn)
        conn.execute('UPDATE rb_schema SET version=999')
        conn.commit()
        before = conn.serialize()
        with self.assertRaises(ValueError):
            database.migrate(conn)
        self.assertEqual(conn.serialize(), before)
        self.assertEqual(conn.execute('SELECT value FROM sentinel').fetchone()[0], 'keep')

    def test_version_one_upgrade_and_concurrent_initialization(self):
        conn = sqlite3.connect(':memory:')
        self.addCleanup(conn.close)
        database.baseline(conn)
        conn.execute('CREATE TABLE rb_schema (singleton INTEGER PRIMARY KEY, version INTEGER)')
        conn.execute('INSERT INTO rb_schema VALUES (1,1)')
        conn.commit()
        database.migrate(conn)
        self.assertEqual(conn.execute('SELECT version FROM rb_schema').fetchone()[0], 2)
        with ThreadPoolExecutor(max_workers=4) as pool:
            results = [pool.submit(self.cli, tool, '--engagement', 'alpha', *args)
                       for tool, args in (('rb-creds', ('list',)), ('rb-findings', ('list',)),
                                          ('rb-chain', ('list',)), ('rb-report', ()))]
            for result in results:
                result.result()
        conn2 = self.conn()
        self.assertEqual(conn2.execute('SELECT version FROM rb_schema').fetchone()[0], 2)
        self.assertEqual(conn2.execute('SELECT COUNT(*) FROM rb_schema').fetchone()[0], 1)

    def test_finding_updates_retest_history_and_invalid_transitions(self):
        conn = self.conn()
        identifier = self.finding(conn)
        self.cli('rb-findings', '--engagement', 'alpha', 'update', str(identifier), '--title', 'Revised',
                 '--vector', 'CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:N')
        record = lifecycle.record(conn, 'finding', identifier)
        self.assertEqual((record['title'], record['cvss_score'], record['severity']), ('Revised', 0, 'None'))
        document = empty_details()
        document['evidence'] = [{'id': 'E1', 'path': 'synthetic-proof', 'caption': '',
            'captured_at': '', 'sha256': '', 'redaction_status': 'unreviewed'}]
        source = self.root / 'details.json'; source.write_text(json.dumps(document))
        self.cli('rb-findings', '--engagement', 'alpha', 'details', str(identifier), '--file', str(source))
        decision = {'status': 'resolved', 'tester': 'synthetic tester', 'tested_at': '2026-09-28T12:00:00Z',
                    'method': 'negative control', 'result': 'access denied', 'evidence_ids': ['E1']}
        source.write_text(json.dumps(decision))
        self.cli('rb-findings', '--engagement', 'alpha', 'retest', str(identifier), '--file', str(source))
        events = json.loads(self.cli('rb-findings', '--engagement', 'alpha', 'history', str(identifier)).stdout)
        self.assertEqual([e['action'] for e in events], ['create', 'update', 'details', 'retest'])
        self.assertEqual(events[-1]['before']['retest']['status'], 'not_tested')
        self.assertEqual(events[-1]['after']['retest']['status'], 'resolved')
        self.assertTrue(all(e['actor'] and e['occurred_at'] for e in events))
        for invalid in (empty_details()['retest'], dict(decision, status='passed'), dict(decision, evidence_ids=['missing'])):
            with self.assertRaises(ValueError):
                lifecycle.save_details(conn, identifier, invalid, retest_only=True)
        with self.assertRaises(ValueError):
            save_details(conn, identifier, document)
        self.assertEqual(read_details(conn, identifier)['retest'], decision)
        self.assertEqual(len(lifecycle.history(conn, 'finding', identifier)), 4)

    def test_history_failure_rolls_back_mutation_and_history_is_append_only(self):
        conn = self.conn(); identifier = self.finding(conn)
        before = lifecycle.record(conn, 'finding', identifier)
        conn.execute("CREATE TRIGGER fail_event BEFORE INSERT ON record_history BEGIN SELECT RAISE(ABORT,'test'); END")
        conn.commit()
        with self.assertRaises(sqlite3.IntegrityError):
            lifecycle.update_record(conn, 'finding', identifier, {'title': 'must rollback'})
        self.assertEqual(lifecycle.record(conn, 'finding', identifier), before)
        detail = empty_details();detail['impact'] = 'must rollback'
        with self.assertRaises(sqlite3.IntegrityError):
            save_details(conn, identifier, detail)
        self.assertEqual(read_details(conn, identifier), empty_details())
        with self.assertRaises(sqlite3.IntegrityError):
            self.finding(conn)
        self.assertEqual(conn.execute('SELECT COUNT(*) FROM findings').fetchone()[0], 1)
        for statement in ("UPDATE record_history SET actor='changed'", 'DELETE FROM record_history'):
            with self.assertRaises(sqlite3.IntegrityError):
                conn.execute(statement)
            conn.rollback()
        self.assertEqual(len(lifecycle.history(conn, 'finding', identifier)), 1)

    def test_invalid_record_changes_and_vectors_leave_data_unchanged(self):
        conn = self.conn(); identifier = self.finding(conn)
        before = lifecycle.record(conn, 'finding', identifier)
        for changes in ({}, {'title': ''}, {'description': ' '}, {'host': 4}, {'cvss_score': 10},
                        {'secret': 'never logged'}, {'cvss_vector': 'CVSS:4.0/AV:N'},
                        {'cvss_vector': VECTOR + '/AV:N'}, {'cvss_vector': VECTOR.replace('/AV:N', '/AV:')},
                        {'cvss_vector': VECTOR.replace('/AC:L', '')}):
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                lifecycle.update_record(conn, 'finding', identifier, changes)
        with self.assertRaises(ValueError):
            lifecycle.update_record(conn, 'finding', 999, {'title': 'missing'})
        self.assertEqual(lifecycle.record(conn, 'finding', identifier), before)
        self.assertEqual(len(lifecycle.history(conn, 'finding', identifier)), 1)

    def test_encrypted_backup_restore_preserves_schema_and_history(self):
        from cryptography.fernet import Fernet
        conn = self.conn(); identifier = self.finding(conn)
        lifecycle.update_record(conn, 'finding', identifier, {'title': 'Before backup'})
        key = Fernet(Fernet.generate_key())
        backup = self.root / 'history.rbbackup'
        vault.backup(conn, key, backup)
        destination = self.root / 'beta/.redbrixen/opskit.db'
        vault.restore(key, backup, destination)
        recovered = self.conn('beta')
        self.assertEqual(lifecycle.history(recovered, 'finding', identifier),
                         lifecycle.history(conn, 'finding', identifier))
        self.assertEqual(recovered.execute('SELECT version FROM rb_schema').fetchone()[0], 2)
        lifecycle.update_record(recovered, 'finding', identifier, {'title': 'After restore'})
        self.assertEqual(len(lifecycle.history(recovered, 'finding', identifier)), 3)
        self.assertEqual(lifecycle.record(conn, 'finding', identifier)['title'], 'Before backup')
        with self.assertRaises(sqlite3.IntegrityError):
            recovered.execute('DELETE FROM record_history')
        recovered.rollback()

    def test_chain_edits_concurrent_partial_updates_and_private_history(self):
        self.cli('rb-chain', '--engagement', 'alpha', 'add', 'Original', '--command', 'PRIVATE old command')
        with ThreadPoolExecutor(max_workers=2) as pool:
            first = pool.submit(self.cli, 'rb-chain', '--engagement', 'alpha', 'update', '1', '--title', 'Changed')
            second = pool.submit(self.cli, 'rb-chain', '--engagement', 'alpha', 'update', '1', '--host', 'new-host')
            first.result();second.result()
        self.cli('rb-chain', '--engagement', 'alpha', 'update', '1', '--command', 'replacement')
        conn = self.conn()
        row = lifecycle.record(conn, 'chain', 1)
        self.assertEqual((row['title'], row['host'], row['command']), ('Changed', 'new-host', 'replacement'))
        history = lifecycle.history(conn, 'chain', 1)
        self.assertEqual(len(history), 4)
        self.assertEqual(history[-1]['before']['command'], 'PRIVATE old command')
        self.assertFalse(lifecycle.update_record(conn, 'chain', 1, {'title': 'Changed'}))
        self.cli('rb-chain', '--engagement', 'alpha', 'update', '1', '--order', '0', ok=False)
        for tool in ('rb-chain', 'rb-report'):
            args = ('export',) if tool == 'rb-chain' else ()
            path = self.root / (tool + '.md')
            self.cli(tool, '--engagement', 'alpha', *args, '--output', str(path))
            self.assertNotIn('PRIVATE', path.read_text())
            self.cli(tool, '--engagement', 'alpha', *args, '--restricted', '--output', str(path.with_suffix('.restricted.md')))
            self.assertNotIn('PRIVATE old command', path.with_suffix('.restricted.md').read_text())
        conn.execute("CREATE TRIGGER fail_chain_event BEFORE INSERT ON record_history BEGIN SELECT RAISE(ABORT,'test'); END")
        conn.commit()
        with self.assertRaises(sqlite3.IntegrityError):
            lifecycle.update_record(conn, 'chain', 1, {'host': 'rollback'})
        self.assertEqual(lifecycle.record(conn, 'chain', 1), row)
