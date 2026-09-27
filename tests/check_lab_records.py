#!/usr/bin/env python3
"""Validate saved lab evidence structure; this does not rerun or certify a lab."""
from datetime import datetime
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORDS = {
    'labs/pivoting/ssh-socks-result.json': (
        'labs/pivoting/verify_ssh_socks.py', 'scope',
        ('platform',), ('versions',)),
    'labs/ligolo/result.json': (
        'labs/ligolo/verify.py', 'limits',
        ('release', 'image_id', 'docker_version'), ('archive_sha256',)),
}


def validate_record(record, scope_field, text_fields, mapping_fields):
    if not isinstance(record, dict):
        raise ValueError('record must be an object')
    for field in ('date_utc', scope_field, *text_fields):
        if not isinstance(record.get(field), str) or not record[field].strip():
            raise ValueError(f'{field} must be nonempty text')
    try:
        timestamp = datetime.fromisoformat(record['date_utc'].replace('Z', '+00:00'))
    except ValueError as error:
        raise ValueError('date_utc must be an ISO timestamp') from error
    if timestamp.tzinfo is None or timestamp.utcoffset().total_seconds() != 0:
        raise ValueError('date_utc must include UTC timezone')
    checks = record.get('checks')
    if (not isinstance(checks, list) or not checks
            or any(not isinstance(item, str) or not item.strip() for item in checks)):
        raise ValueError('checks must be a nonempty list of recorded assertions')
    if len(set(checks)) != len(checks):
        raise ValueError('checks must not repeat an assertion')
    for field in mapping_fields:
        values = record.get(field)
        if not isinstance(values, dict) or not values:
            raise ValueError(f'{field} must be a nonempty object')
        if any(not isinstance(value, str) or not value.strip() for value in values.values()):
            raise ValueError(f'{field} values must be nonempty text')
    if 'versions' in mapping_fields:
        if not {'ssh', 'curl', 'proxychains'} <= record['versions'].keys():
            raise ValueError('versions must identify ssh, curl and proxychains')
    if 'archive_sha256' in mapping_fields:
        hashes = record['archive_sha256']
        if set(hashes) != {'agent', 'proxy'}:
            raise ValueError('archive_sha256 must identify agent and proxy')
        for value in hashes.values():
            if len(value) != 64 or any(c not in '0123456789abcdef' for c in value):
                raise ValueError('archive_sha256 must contain SHA-256 digests')


def check(root=ROOT):
    errors = []
    for path, (fixture, scope_field, text_fields, mapping_fields) in RECORDS.items():
        try:
            if not (root / fixture).is_file():
                raise ValueError(f'missing executable source: {fixture}')
            record = json.loads((root / path).read_text(encoding='utf-8'))
            validate_record(record, scope_field, text_fields, mapping_fields)
        except (OSError, ValueError) as error:
            errors.append(f'{path}: {error}')
    return errors


if __name__ == '__main__':
    failures = check()
    for failure in failures:
        print('FAIL:', failure)
    print(f'{"FAIL" if failures else "PASS"}: {len(RECORDS)} saved lab records (structure only)')
    raise SystemExit(bool(failures))
