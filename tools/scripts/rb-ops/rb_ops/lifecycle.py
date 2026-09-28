"""Atomic private record edits and append-only application history."""
from datetime import datetime, timezone
import json
import os
import pwd

from rb_finding_model import validate, read_details, empty_details
from .database import atomic
from .scoring import parse_vector

FINDING_FIELDS = ('title', 'description', 'host', 'cvss_vector', 'cvss_score', 'severity')
CHAIN_FIELDS = ('step_order', 'title', 'tactic', 'host', 'command', 'outcome', 'evidence_path', 'notes')
TABLES = {'finding': 'findings', 'chain': 'exploit_chain_steps'}


def timestamp():
    return datetime.now(timezone.utc).isoformat(timespec='microseconds')


def encode(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def record(conn, entity, identifier):
    if entity not in TABLES or type(identifier) is not int or identifier < 1:
        raise ValueError('Invalid record selector.')
    cursor = conn.execute(f'SELECT * FROM {TABLES[entity]} WHERE id=?', (identifier,))
    row = cursor.fetchone()
    if row is None:
        raise ValueError('Record not found.')
    return dict(zip((column[0] for column in cursor.description), row))


def event(conn, entity, identifier, action, before, after):
    # No credential or key objects are accepted by this history interface.
    if entity not in TABLES:
        raise ValueError('Unsupported history entity.')
    conn.execute('''INSERT INTO record_history
        (entity, record_id, action, actor, occurred_at, before_json, after_json)
        VALUES (?,?,?,?,?,?,?)''', (entity, identifier, action, pwd.getpwuid(os.getuid()).pw_name,
                                  timestamp(), encode(before), encode(after)))


def validate_fields(entity, changes, *, creating=False):
    allowed = FINDING_FIELDS if entity == 'finding' else CHAIN_FIELDS
    if not changes or set(changes) - set(allowed):
        raise ValueError('Missing or unknown editable fields.')
    changes = dict(changes)
    for key, value in changes.items():
        if key == 'step_order':
            if type(value) is not int or value < 1:
                raise ValueError('Step order must be a positive integer.')
        elif key in ('cvss_score', 'severity'):
            # Values are always derived from a validated vector below.
            if not creating:
                raise ValueError('Edit the vector, not a detached score or severity.')
        elif not isinstance(value, str) or (key in ('title', 'description') and not value.strip()):
            raise ValueError('Required record text cannot be empty.')
    if 'cvss_vector' in changes:
        vector, score, severity = parse_vector(changes['cvss_vector'])
        changes.update(cvss_vector=vector, cvss_score=score, severity=severity)
    return changes


def create_record(conn, entity, fields):
    if entity not in TABLES:
        raise ValueError('Unsupported record type.')
    fields = validate_fields(entity, fields, creating=True)
    required = set(FINDING_FIELDS if entity == 'finding' else CHAIN_FIELDS)
    if set(fields) != required:
        raise ValueError('Incomplete record.')
    with atomic(conn):
        fields['created_at'] = timestamp()
        columns = ','.join(fields)
        cursor = conn.execute(f'INSERT INTO {TABLES[entity]} ({columns}) VALUES ({",".join("?" for _ in fields)})',
                              tuple(fields.values()))
        identifier = cursor.lastrowid
        if entity == 'finding':
            conn.execute('INSERT INTO finding_details VALUES (?,?)', (identifier, encode(empty_details())))
        event(conn, entity, identifier, 'create', None, record(conn, entity, identifier))
    return identifier


def update_record(conn, entity, identifier, changes):
    if entity not in TABLES:
        raise ValueError('Unsupported record type.')
    changes = validate_fields(entity, changes)
    with atomic(conn):
        before = record(conn, entity, identifier)
        if all(before[key] == value for key, value in changes.items()):
            return False
        assignments = ','.join(f'{key}=?' for key in changes)
        conn.execute(f'UPDATE {TABLES[entity]} SET {assignments} WHERE id=?', (*changes.values(), identifier))
        event(conn, entity, identifier, 'update', before, record(conn, entity, identifier))
    return True


def save_details(conn, identifier, document, *, retest_only=False):
    # Validate and read under the same writer lock as the update and history insert.
    with atomic(conn):
        record(conn, 'finding', identifier)
        before = read_details(conn, identifier)
        after = dict(before, retest=document) if retest_only else document
        validate(after)
        if before['retest']['status'] != 'not_tested' and after['retest']['status'] == 'not_tested':
            raise ValueError('A recorded retest cannot be reset to not_tested; record a new decision.')
        if before == after:
            return False
        conn.execute('''INSERT INTO finding_details VALUES (?,?)
            ON CONFLICT(finding_id) DO UPDATE SET document=excluded.document''', (identifier, encode(after)))
        action = 'retest' if before['retest'] != after['retest'] else 'details'
        event(conn, 'finding', identifier, action, before, after)
    return True


def history(conn, entity, identifier):
    record(conn, entity, identifier)
    cursor = conn.execute('''SELECT id, action, actor, occurred_at, before_json, after_json
        FROM record_history WHERE entity=? AND record_id=? ORDER BY id''', (entity, identifier))
    return [{'id': row[0], 'action': row[1], 'actor': row[2], 'occurred_at': row[3],
             'before': json.loads(row[4]), 'after': json.loads(row[5])} for row in cursor]
