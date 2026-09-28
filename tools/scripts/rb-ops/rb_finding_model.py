"""Versioned private finding details; original findings rows stay compatible."""
from __future__ import annotations

from datetime import datetime
import json
import re
import sqlite3

TEXT_FIELDS = ('prerequisites', 'reproduction', 'expected_result', 'observed_result',
               'impact', 'remediation', 'limitations', 'severity_rationale', 'client_priority')


def empty_details():
    return {'model_version': 1, **{key: '' for key in TEXT_FIELDS}, 'evidence': [],
            'review': {'status': 'draft', 'reviewer': '', 'reviewed_at': '', 'notes': ''},
            'retest': {'status': 'not_tested', 'tester': '', 'tested_at': '',
                       'method': '', 'result': '', 'evidence_ids': []}}


def exact_keys(value, keys):
    if not isinstance(value, dict) or set(value) != set(keys):
        raise ValueError('Finding details contain missing or unknown fields.')


def text(value):
    if not isinstance(value, str):
        raise ValueError('Finding detail text must be a string.')


def timestamp(value):
    text(value)
    if value:
        parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
        if parsed.tzinfo is None:
            raise ValueError('Evidence/review/retest timestamps require a time zone.')


def validate(document):
    exact_keys(document, empty_details())
    if type(document['model_version']) is not int or document['model_version'] != 1:
        raise ValueError('Unsupported finding model version.')
    for key in TEXT_FIELDS:
        text(document[key])
    if not isinstance(document['evidence'], list):
        raise ValueError('Evidence must be a list.')
    identifiers = set()
    for evidence in document['evidence']:
        exact_keys(evidence, ('id', 'path', 'caption', 'captured_at', 'sha256', 'redaction_status'))
        for value in evidence.values():
            text(value)
        if not evidence['id'].strip() or evidence['id'] in identifiers or not evidence['path'].strip():
            raise ValueError('Evidence requires unique nonempty IDs and artifact references.')
        identifiers.add(evidence['id'])
        timestamp(evidence['captured_at'])
        if evidence['sha256'] and not re.fullmatch('[0-9a-fA-F]{64}', evidence['sha256']):
            raise ValueError('Evidence SHA-256 must contain 64 hexadecimal characters.')
        if evidence['redaction_status'] not in ('unreviewed', 'redacted', 'no_redaction_needed'):
            raise ValueError('Unknown evidence redaction status.')
    review = document['review']
    exact_keys(review, ('status', 'reviewer', 'reviewed_at', 'notes'))
    for value in review.values():
        text(value)
    timestamp(review['reviewed_at'])
    if review['status'] not in ('draft', 'reviewed'):
        raise ValueError('Unknown review status.')
    if review['status'] == 'reviewed' and not all(review[k].strip() for k in ('reviewer', 'reviewed_at')):
        raise ValueError('Reviewed status requires reviewer and time.')
    retest = document['retest']
    exact_keys(retest, ('status', 'tester', 'tested_at', 'method', 'result', 'evidence_ids'))
    for key in ('status', 'tester', 'tested_at', 'method', 'result'):
        text(retest[key])
    timestamp(retest['tested_at'])
    if retest['status'] not in ('not_tested', 'resolved', 'partial', 'unresolved', 'unable_to_retest'):
        raise ValueError('Unknown retest status.')
    if not isinstance(retest['evidence_ids'], list) or any(not isinstance(x, str) or x not in identifiers for x in retest['evidence_ids']):
        raise ValueError('Retest evidence IDs must reference recorded evidence.')
    if retest['status'] != 'not_tested' and not all(retest[k].strip() for k in ('tester', 'tested_at', 'result')):
        raise ValueError('Retest decisions require tester, time and result/reason.')
    if retest['status'] in ('resolved', 'partial', 'unresolved') and (not retest['method'].strip() or not retest['evidence_ids']):
        raise ValueError('Executed retests require method and evidence.')
    return document


def reject_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Duplicate finding detail field.')
        result[key] = value
    return result


def decode(source):
    return validate(json.loads(source, object_pairs_hook=reject_duplicate_keys))


def init_details(conn):
    # Savepoint keeps DDL and legacy backfill atomic, including within caller transactions.
    conn.execute('SAVEPOINT finding_details_migration')
    try:
        conn.execute('''CREATE TABLE IF NOT EXISTS finding_details (
            finding_id INTEGER PRIMARY KEY REFERENCES findings(id),
            document TEXT NOT NULL)''')
        conn.execute('''INSERT INTO finding_details (finding_id, document)
            SELECT id, ? FROM findings WHERE id NOT IN (SELECT finding_id FROM finding_details)''',
            (json.dumps(empty_details()),))
        conn.execute('RELEASE finding_details_migration')
    except Exception:
        conn.execute('ROLLBACK TO finding_details_migration')
        conn.execute('RELEASE finding_details_migration')
        raise


def read_details(conn, finding_id):
    if not conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='finding_details'").fetchone():
        return empty_details()
    row = conn.execute('SELECT document FROM finding_details WHERE finding_id=?', (finding_id,)).fetchone()
    return decode(row[0]) if row else empty_details()


def save_details(conn, finding_id, document):
    # Local import avoids a cycle; all detail writes share atomic history handling.
    from rb_ops.lifecycle import save_details as save_with_history
    return save_with_history(conn, finding_id, document)


def detail_lines(conn, finding_id):
    """Restricted exports only: references are text; never open/copy evidence files."""
    doc = read_details(conn, finding_id)
    lines = ['- Finding detail model: 1']
    for key in TEXT_FIELDS:
        lines += [f"- {key.replace('_', ' ').title()}:", doc[key] or 'Not recorded.']
    lines += ['- Evidence:']
    if not doc['evidence']:
        lines += ['Not recorded.']
    for item in doc['evidence']:
        lines += [f"  - {item['id']}: {item['caption']}",
                  f"    Reference: {item['path']}", f"    Captured: {item['captured_at'] or 'Not recorded.'}",
                  f"    SHA-256 (operator supplied): {item['sha256'] or 'Not recorded.'}",
                  f"    Redaction status: {item['redaction_status']}"]
    for section in ('review', 'retest'):
        lines += [f'- {section.title()}:']
        for key, value in doc[section].items():
            value = ', '.join(value) if isinstance(value, list) else value
            lines += [f"  - {key.replace('_', ' ')}: {value or 'Not recorded.'}"]
    return lines
