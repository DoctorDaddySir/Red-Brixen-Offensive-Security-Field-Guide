"""Versioned, authenticated credential secrets; key bytes never enter SQLite."""
import json
import os
from pathlib import Path
import sqlite3

from rb_private import read_private, write_new_private, prepare_database


REDACTED = '[omitted; use --restricted --include-secrets explicitly]'


def key_path(db_path=None):
    value = os.environ.get('RB_CREDENTIAL_KEY_FILE')
    if not value:
        raise ValueError('Set RB_CREDENTIAL_KEY_FILE to a separate owner-only key file.')
    path = Path(value).expanduser().absolute()
    if db_path is not None and path.resolve().is_relative_to(Path(db_path).resolve().parent.parent):
        raise ValueError('Keep the credential key outside the engagement directory.')
    return path


def cipher(db_path=None):
    from cryptography.fernet import Fernet
    return Fernet(read_private(key_path(db_path)))


def create_key(db_path):
    from cryptography.fernet import Fernet
    write_new_private(key_path(db_path), Fernet.generate_key())


def init_secrets(conn):
    conn.execute('''CREATE TABLE IF NOT EXISTS credential_secrets (
        credential_id INTEGER PRIMARY KEY REFERENCES credentials(id),
        format_version INTEGER NOT NULL CHECK(format_version = 1),
        token TEXT NOT NULL)''')
    conn.commit()


def seal(key, identifier, secret):
    payload = json.dumps({'version': 1, 'credential_id': identifier, 'secret': secret}).encode()
    return key.encrypt(payload).decode('ascii')


def reveal(conn, identifier, key):
    from cryptography.fernet import InvalidToken
    try:
        row = conn.execute('SELECT format_version, token FROM credential_secrets WHERE credential_id=?',
                           (identifier,)).fetchone()
        if row is None or row[0] != 1:
            raise ValueError('Credential requires explicit migration.')
        payload = json.loads(key.decrypt(row[1].encode('ascii')))
        if (not isinstance(payload, dict) or payload.get('version') != 1 or payload.get('credential_id') != identifier
                or not isinstance(payload.get('secret'), str)):
            raise ValueError('Invalid credential payload.')
        return payload['secret']
    except (InvalidToken, UnicodeError, json.JSONDecodeError, sqlite3.OperationalError) as error:
        raise ValueError('Unable to decrypt credential; check key, migration and integrity.') from error


def check_secrets(conn, key, *, allow_legacy=False):
    legacy = []
    for row in conn.execute('SELECT id, secret FROM credentials ORDER BY id'):
        encrypted = conn.execute('SELECT 1 FROM credential_secrets WHERE credential_id=?', (row[0],)).fetchone()
        if encrypted:
            if row[1] != '':
                raise ValueError('Conflicting plaintext and protected credential state.')
            reveal(conn, row[0], key)
        elif allow_legacy:
            legacy.append((row[0], row[1]))
        else:
            raise ValueError('Run rb-creds migrate before adding or revealing credentials.')
    return legacy


def export_secret(conn, identifier, args, db_path):
    if not getattr(args, 'include_secrets', False):
        return REDACTED
    if not args.restricted:
        raise ValueError('--include-secrets requires --restricted.')
    return reveal(conn, identifier, cipher(db_path))


def add_secret_export_option(parser):
    parser.add_argument('--include-secrets', action='store_true',
                        help='Decrypt credential secrets; requires --restricted and the external key')


def validate_secret_export(args):
    if args.include_secrets and not args.restricted:
        raise ValueError('--include-secrets requires --restricted.')


def snapshot(conn):
    # SQLite's backup API captures a consistent database including committed WAL.
    if conn.in_transaction:
        raise ValueError('Backup requires a committed database.')
    memory = sqlite3.connect(':memory:')
    try:
        conn.backup(memory)
        # Serialized WAL-mode headers cannot be opened in memory for recovery.
        data = bytearray(memory.serialize())
        data[18:20] = b'\x01\x01'
        return bytes(data)
    finally:
        memory.close()


def backup(conn, key, output):
    data = key.encrypt(b'RB-OPS-BACKUP-v1\0' + snapshot(conn))
    write_new_private(output, data)


def migrate(conn, key, output):
    # Requires all other engagement writers stopped for backup and migration.
    legacy = check_secrets(conn, key, allow_legacy=True)
    if legacy:
        backup(conn, key, output)
    # Recheck under the write lock; do not store any plaintext in new rows.
    with conn:
        conn.execute('BEGIN IMMEDIATE')
        for identifier, secret in check_secrets(conn, key, allow_legacy=True):
            conn.execute('INSERT INTO credential_secrets VALUES (?,1,?)',
                         (identifier, seal(key, identifier, secret)))
            conn.execute("UPDATE credentials SET secret='' WHERE id=?", (identifier,))
    if conn.execute('PRAGMA wal_checkpoint(TRUNCATE)').fetchone()[0]:
        raise ValueError('WAL checkpoint busy; stop other clients and retry migration cleanup.')
    conn.execute('VACUUM')
    if conn.execute('PRAGMA wal_checkpoint(TRUNCATE)').fetchone()[0]:
        raise ValueError('WAL cleanup busy; stop other clients and retry migration cleanup.')
    return bool(legacy)


def restore(key, source, db_path):
    from cryptography.fernet import InvalidToken
    try:
        data = key.decrypt(read_private(source))
    except InvalidToken as error:
        raise ValueError('Wrong backup key or damaged backup.') from error
    prefix = b'RB-OPS-BACKUP-v1\0'
    if not data.startswith(prefix):
        raise ValueError('Unsupported backup format.')
    memory = sqlite3.connect(':memory:')
    try:
        memory.deserialize(data[len(prefix):])
        if memory.execute('PRAGMA integrity_check').fetchone()[0] != 'ok':
            raise ValueError('Invalid backup database.')
        if memory.execute("SELECT 1 FROM sqlite_master WHERE name='credentials'").fetchone():
            init_secrets(memory)
            check_secrets(memory, key, allow_legacy=True)
        path = prepare_database(db_path)
        if any(Path(str(path) + suffix).exists() for suffix in ('', '-wal', '-shm', '-journal')):
            raise ValueError('Restore requires a fresh engagement database destination.')
        write_new_private(path, data[len(prefix):])
    finally:
        memory.close()
