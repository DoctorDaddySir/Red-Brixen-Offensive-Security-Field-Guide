"""Synthetic credential storage, disclosure, migration and recovery regressions."""
import contextlib
import getpass
import io
import os
import pty
import select
import time
from pathlib import Path
import sqlite3
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from test_rb_exports import load, TOOLS
import rb_credentials as vault
import rb_private


class CredentialTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.engagement = self.root / 'engagement'
        self.engagement.mkdir(mode=0o700)
        self.db_path = self.engagement / '.redbrixen/opskit.db'
        self.env = patch.dict(os.environ, {'RB_CREDENTIAL_KEY_FILE': str(self.root / 'key')})
        self.env.start()
        self.addCleanup(self.env.stop)
        self.umask = os.umask(0o022)
        self.addCleanup(os.umask, self.umask)
        self.creds = load('rb-creds')
        self.creds.engagement_context = lambda: ('synthetic', self.engagement, self.db_path)
        original_connect = self.creds.connect
        def tracked_connect():
            connection = original_connect()
            self.addCleanup(connection.close)
            return connection
        self.creds.connect = tracked_connect
        vault.create_key(self.db_path)
        self.key = vault.cipher(self.db_path)
        self.secret = 'SYNTHETIC_SECRET_!_☃_MULTILINE\nsecond line'

    def conn(self):
        conn = self.creds.connect()
        self.addCleanup(conn.close)
        return conn

    def cli(self, *args, secret=None):
        with patch.object(sys, 'argv', ['rb-creds', *args]), patch.object(
                getpass, 'getpass', return_value=self.secret if secret is None else secret):
            self.creds.main()

    def seed_legacy(self):
        conn = self.conn()
        conn.execute('INSERT INTO credentials VALUES (1,?,?,?,?,?,?,?,1,?)',
                     ('alice', self.secret, 'password', 'host', 'service', 'source', 'notes', 'date'))
        conn.execute('INSERT INTO credential_validations VALUES (1,1,?,?,?,?)',
                     ('host', 'service', 'note', 'date'))
        conn.execute('CREATE TABLE unrelated (value TEXT)')
        conn.execute("INSERT INTO unrelated VALUES ('preserved')")
        conn.commit()
        self.assertIn(self.secret.encode(), self.db_path.read_bytes())
        return conn

    def test_hidden_entry_and_authenticated_round_trip(self):
        self.cli('add', 'alice')
        conn = self.conn()
        self.assertEqual(conn.execute('SELECT secret FROM credentials').fetchone()[0], '')
        self.assertEqual(vault.reveal(conn, 1, self.key), self.secret)
        for path in self.db_path.parent.iterdir():
            self.assertNotIn(self.secret.encode(), path.read_bytes())
        capture = io.StringIO()
        with contextlib.redirect_stdout(capture):
            self.cli('list')
        self.assertNotIn(self.secret, capture.getvalue())
        with contextlib.redirect_stdout(capture):
            self.cli('list', '--show-secrets')
        self.assertIn(self.secret, capture.getvalue())

    def test_real_terminal_input_is_not_echoed(self):
        # Use a real PTY for getpass; only tmux engagement discovery is simulated.
        binaries = self.root / 'bin'
        binaries.mkdir(mode=0o700)
        tmux = binaries / 'tmux'
        tmux.write_text('#!/bin/sh\nprintf engagement\n')
        tmux.chmod(0o700)
        master, slave = pty.openpty()
        self.addCleanup(os.close, master)
        self.addCleanup(os.close, slave)
        env = dict(os.environ, TMUX='synthetic', PENTEST_BASE=str(self.root),
                   PATH=str(binaries) + os.pathsep + os.environ['PATH'])
        process = subprocess.Popen([sys.executable, str(TOOLS / 'rb-creds'), 'add', 'alice'],
                                   stdin=slave, stdout=slave, stderr=slave, env=env)
        self.addCleanup(lambda: process.wait(timeout=5))
        self.addCleanup(lambda: process.kill() if process.poll() is None else None)
        transcript = b''
        deadline = time.monotonic() + 10
        while b'Credential secret: ' not in transcript and time.monotonic() < deadline:
            if select.select([master], [], [], 0.1)[0]:
                transcript += os.read(master, 65536)
        self.assertIn(b'Credential secret: ', transcript)
        marker = b'SYNTHETIC_PTY_SECRET_123'
        os.write(master, marker + b'\n')
        while process.poll() is None and time.monotonic() < deadline:
            if select.select([master], [], [], 0.1)[0]:
                transcript += os.read(master, 65536)
        self.assertEqual(process.wait(timeout=2), 0, transcript)
        while select.select([master], [], [], 0)[0]:
            transcript += os.read(master, 65536)
        self.assertNotIn(marker, transcript)
        self.assertEqual(vault.reveal(self.conn(), 1, self.key), marker.decode())

    def test_old_positional_secret_rejected_without_echo(self):
        result = subprocess.run([sys.executable, str(TOOLS / 'rb-creds'), 'add', 'alice', self.secret],
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn(self.secret, result.stdout + result.stderr)

    def test_hidden_input_failure_creates_no_database(self):
        with patch.object(sys, 'argv', ['rb-creds', 'add', 'alice']), patch.object(
                getpass, 'getpass', side_effect=getpass.GetPassWarning):
            with self.assertRaises(getpass.GetPassWarning):
                self.creds.main()
        self.assertFalse(self.db_path.exists())

    def test_missing_wrong_key_and_tampering_fail_closed(self):
        self.cli('add', 'alice')
        conn = self.conn()
        from cryptography.fernet import Fernet
        with self.assertRaises(ValueError):
            vault.reveal(conn, 1, Fernet(Fernet.generate_key()))
        original = conn.execute('SELECT token FROM credential_secrets').fetchone()[0]
        conn.execute('UPDATE credential_secrets SET token=?', ('broken',))
        conn.commit()
        with self.assertRaises(ValueError):
            vault.reveal(conn, 1, self.key)
        conn.execute('UPDATE credential_secrets SET token=?', (vault.seal(self.key, 2, self.secret),))
        conn.commit()
        with self.assertRaises(ValueError):
            vault.reveal(conn, 1, self.key)
        conn.execute('UPDATE credential_secrets SET token=?', (original,))
        conn.commit()
        (self.root / 'key').unlink()
        with self.assertRaises(OSError):
            self.cli('add', 'bob')
        self.assertEqual(conn.execute('SELECT COUNT(*) FROM credentials').fetchone()[0], 1)
        self.assertFalse((self.root / 'key').exists())

    def test_all_database_creators_enforce_permissions(self):
        for name in ('rb-creds', 'rb-chain', 'rb-findings', 'rb-report'):
            with self.subTest(name=name):
                os.umask(0)
                directory = self.root / name
                directory.mkdir(mode=0o700)
                path = directory / '.redbrixen/opskit.db'
                module = load(name)
                module.engagement_context = lambda: ('test', directory, path)
                conn = module.connect()
                conn.execute('CREATE TABLE IF NOT EXISTS probe (value)')
                conn.commit()
                conn.execute('PRAGMA journal_mode=WAL')
                conn.execute('INSERT INTO probe VALUES (1)')
                conn.commit()
                self.assertEqual(stat.S_IMODE(path.parent.stat().st_mode), 0o700)
                for item in path.parent.iterdir():
                    self.assertEqual(stat.S_IMODE(item.stat().st_mode), 0o600)
                conn.close()
                path.chmod(0o644)
                path.parent.chmod(0o755)
                conn = module.connect()
                conn.close()
                self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)
                self.assertEqual(stat.S_IMODE(path.parent.stat().st_mode), 0o700)

    def test_links_unsafe_parents_and_key_modes_rejected(self):
        self.db_path.parent.mkdir()
        target = self.root / 'target'
        target.write_text('unchanged')
        self.db_path.symlink_to(target)
        with self.assertRaises((OSError, ValueError)):
            self.conn()
        self.db_path.unlink()
        os.link(target, self.db_path)
        with self.assertRaises(ValueError):
            self.conn()
        self.assertEqual(target.read_text(), 'unchanged')
        self.db_path.unlink()
        self.engagement.chmod(0o777)
        with self.assertRaises(ValueError):
            self.conn()
        self.engagement.chmod(0o700)
        key_path = self.root / 'key'
        key_path.chmod(0o644)
        with self.assertRaises(ValueError):
            vault.cipher(self.db_path)
        key_path.chmod(0o600)
        with self.assertRaises(FileExistsError):
            vault.create_key(self.db_path)
        with patch.dict(os.environ, {'RB_CREDENTIAL_KEY_FILE': str(self.engagement / 'key')}):
            with self.assertRaises(ValueError):
                vault.create_key(self.db_path)

    def test_writable_ancestor_rejected_before_sqlite_reopens_path(self):
        shared = self.root / 'shared'
        shared.mkdir(mode=0o700)
        shared.chmod(0o777)
        engagement = shared / 'engagement'
        engagement.mkdir(mode=0o700)
        with patch.object(rb_private.sqlite3, 'connect') as opener:
            with self.assertRaises(ValueError):
                rb_private.connect_private(engagement / '.redbrixen/opskit.db')
            opener.assert_not_called()
        # A shared sticky parent cannot rename another owner's private child.
        shared.chmod(0o1777)
        conn = rb_private.connect_private(engagement / '.redbrixen/opskit.db')
        conn.close()

    def test_legacy_migration_backup_recovery_preserves_records(self):
        conn = self.seed_legacy()
        conn.execute('PRAGMA journal_mode=WAL')
        backup = self.root / 'legacy.backup'
        self.assertTrue(vault.migrate(conn, self.key, backup))
        self.assertEqual(vault.reveal(conn, 1, self.key), self.secret)
        self.assertEqual(conn.execute('SELECT notes FROM credential_validations').fetchone()[0], 'note')
        self.assertEqual(conn.execute('SELECT value FROM unrelated').fetchone()[0], 'preserved')
        self.assertFalse(vault.migrate(conn, self.key, backup))
        for path in self.db_path.parent.iterdir():
            self.assertNotIn(self.secret.encode(), path.read_bytes())
        self.assertNotIn(self.secret.encode(), backup.read_bytes())
        self.assertEqual(stat.S_IMODE(backup.stat().st_mode), 0o600)
        fresh = self.root / 'restored'
        fresh.mkdir(mode=0o700)
        destination = fresh / '.redbrixen/opskit.db'
        vault.restore(self.key, backup, destination)
        recovered = rb_private.connect_private(destination)
        self.addCleanup(recovered.close)
        self.assertEqual(recovered.execute('SELECT secret FROM credentials').fetchone()[0], self.secret)
        self.assertEqual(recovered.execute('SELECT value FROM unrelated').fetchone()[0], 'preserved')
        vault.migrate(recovered, self.key, self.root / 'recovered.backup')
        self.assertEqual(vault.reveal(recovered, 1, self.key), self.secret)
        with self.assertRaises(ValueError):
            vault.restore(self.key, backup, destination)

    def test_migration_failure_rolls_back_and_requires_backup(self):
        conn = self.seed_legacy()
        with patch.object(vault, 'seal', side_effect=ValueError('synthetic interruption')):
            with self.assertRaises(ValueError):
                vault.migrate(conn, self.key, self.root / 'interrupted.backup')
        self.assertEqual(conn.execute('SELECT secret FROM credentials').fetchone()[0], self.secret)
        self.assertEqual(conn.execute('SELECT COUNT(*) FROM credential_secrets').fetchone()[0], 0)
        with self.assertRaises(FileExistsError):
            vault.migrate(conn, self.key, self.root / 'interrupted.backup')
        with self.assertRaises(ValueError):
            self.cli('add', 'bob')
        self.assertEqual(conn.execute('SELECT COUNT(*) FROM credentials').fetchone()[0], 1)

    def test_protected_backup_restore_wrong_key_and_corruption(self):
        self.cli('add', 'alice', secret='')
        conn = self.conn()
        output = self.root / 'protected.backup'
        vault.backup(conn, self.key, output)
        fresh = self.root / 'fresh'
        fresh.mkdir(mode=0o700)
        destination = fresh / '.redbrixen/opskit.db'
        from cryptography.fernet import Fernet
        with self.assertRaises(ValueError):
            vault.restore(Fernet(Fernet.generate_key()), output, destination)
        self.assertFalse(destination.exists())
        vault.restore(self.key, output, destination)
        restored = rb_private.connect_private(destination)
        self.addCleanup(restored.close)
        self.assertEqual(vault.reveal(restored, 1, self.key), '')
        output.write_bytes(b'corrupted')
        with self.assertRaises(ValueError):
            vault.restore(self.key, output, self.root / 'absent/.redbrixen/opskit.db')

    def test_secret_export_requires_both_flags_and_key(self):
        self.cli('add', 'alice')
        for name in ('rb-creds', 'rb-report'):
            module = self.creds if name == 'rb-creds' else load(name)
            module.engagement_context = lambda: ('synthetic', self.engagement, self.db_path)
            if name == 'rb-report':
                module.connect = self.creds.connect
            base = [name] + (['export'] if name == 'rb-creds' else [])
            output = self.root / (name + '.restricted.md')
            with patch.object(sys, 'argv', base + ['--restricted', '--output', str(output)]):
                module.main()
            self.assertNotIn(self.secret, output.read_text())
            with patch.object(sys, 'argv', base + ['--include-secrets']):
                with self.assertRaises(ValueError):
                    module.main()
            with patch.object(sys, 'argv', base + ['--restricted', '--include-secrets', '--output', str(output)]):
                module.main()
            self.assertIn(self.secret, output.read_text())
            self.assertEqual(stat.S_IMODE(output.stat().st_mode), 0o600)
        (self.root / 'key').unlink()
        # Neither safe default needs key material.
        self.cli('export')
        self.cli('export', '--restricted')
        old = output.read_bytes()
        with patch.object(sys, 'argv', ['rb-report', '--restricted', '--include-secrets', '--output', str(output)]):
            with self.assertRaises(OSError):
                module.main()
        self.assertEqual(output.read_bytes(), old)
