"""Ordered transactional schema migrations; credential conversion stays explicit."""
from contextlib import contextmanager
from rb_private import connect_private

SCHEMA_VERSION = 2
LEGACY_TABLES = (
    """CREATE TABLE IF NOT EXISTS credentials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            secret TEXT NOT NULL,
            kind TEXT DEFAULT 'password',
            host TEXT DEFAULT '',
            service TEXT DEFAULT '',
            source TEXT DEFAULT '',
            notes TEXT DEFAULT '',
            validated INTEGER DEFAULT 0,
            created_at TEXT NOT NULL
        )""",
    """CREATE TABLE IF NOT EXISTS credential_validations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            credential_id INTEGER NOT NULL,
            host TEXT DEFAULT '',
            service TEXT DEFAULT '',
            notes TEXT DEFAULT '',
            created_at TEXT NOT NULL,
            FOREIGN KEY (credential_id) REFERENCES credentials(id)
        )""",
    """CREATE TABLE IF NOT EXISTS exploit_chain_steps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            step_order INTEGER NOT NULL,
            title TEXT NOT NULL,
            tactic TEXT DEFAULT '',
            host TEXT DEFAULT '',
            command TEXT DEFAULT '',
            outcome TEXT DEFAULT '',
            evidence_path TEXT DEFAULT '',
            notes TEXT DEFAULT '',
            created_at TEXT NOT NULL
        )""",
    """CREATE TABLE IF NOT EXISTS findings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            host TEXT DEFAULT '',
            cvss_vector TEXT NOT NULL,
            cvss_score REAL NOT NULL,
            severity TEXT NOT NULL,
            created_at TEXT NOT NULL
        )""",
)


@contextmanager
def atomic(conn):
    nested = conn.in_transaction
    conn.execute('SAVEPOINT rb_ops_atomic' if nested else 'BEGIN IMMEDIATE')
    try:
        yield
        if nested:
            conn.execute('RELEASE rb_ops_atomic')
        else:
            conn.commit()
    except BaseException:
        if nested:
            conn.execute('ROLLBACK TO rb_ops_atomic')
            conn.execute('RELEASE rb_ops_atomic')
        else:
            conn.rollback()
        raise


def baseline(conn):
    from rb_finding_model import init_details
    for statement in LEGACY_TABLES:
        conn.execute(statement)
    conn.execute("""CREATE TABLE IF NOT EXISTS credential_secrets (
        credential_id INTEGER PRIMARY KEY REFERENCES credentials(id),
        format_version INTEGER NOT NULL CHECK(format_version = 1), token TEXT NOT NULL)""")
    init_details(conn)


def history_schema(conn):
    conn.execute("""CREATE TABLE record_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        entity TEXT NOT NULL CHECK(entity IN ('finding', 'chain')),
        record_id INTEGER NOT NULL,
        action TEXT NOT NULL CHECK(action IN ('create','update','details','retest')),
        actor TEXT NOT NULL, occurred_at TEXT NOT NULL,
        before_json TEXT NOT NULL, after_json TEXT NOT NULL)""")
    for operation in ('UPDATE', 'DELETE'):
        conn.execute(f"""CREATE TRIGGER history_no_{operation.lower()}
            BEFORE {operation} ON record_history
            BEGIN SELECT RAISE(ABORT, 'Record history is append-only'); END""")


MIGRATIONS = (baseline, history_schema)


def migrate(conn):
    with atomic(conn):
        conn.execute("""CREATE TABLE IF NOT EXISTS rb_schema (
            singleton INTEGER PRIMARY KEY CHECK(singleton=1), version INTEGER NOT NULL)""")
        rows = conn.execute('SELECT singleton, version FROM rb_schema').fetchall()
        if len(rows) > 1 or (rows and rows[0][0] != 1):
            raise ValueError('Invalid schema version record.')
        version = rows[0][1] if rows else 0
        if type(version) is not int or not 0 <= version <= SCHEMA_VERSION:
            raise ValueError('Unsupported database schema version; use a compatible tool version.')
        for index in range(version, SCHEMA_VERSION):
            MIGRATIONS[index](conn)
            conn.execute('INSERT INTO rb_schema VALUES (1, ?) ON CONFLICT(singleton) DO UPDATE SET version=excluded.version',
                         (index + 1,))


def open_database(path):
    conn = connect_private(path)
    try:
        migrate(conn)
        from .context import register_connection
        register_connection(conn)
        return conn
    except BaseException:
        conn.close()
        raise
