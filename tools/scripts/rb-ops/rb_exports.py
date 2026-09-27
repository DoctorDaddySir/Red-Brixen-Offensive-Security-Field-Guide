"""Shared export policy for optional RB tools; never classify free text as public."""
from __future__ import annotations

import math
import os
from pathlib import Path
import sqlite3
import tempfile


def add_export_options(parser):
    parser.add_argument('--output', default='')
    parser.add_argument('--restricted', action='store_true',
                        help='Export private operator detail to an owner-only .restricted.md appendix')


def export_path(args, engagement_dir: Path, basename: str) -> Path:
    suffix = '.restricted.md' if args.restricted else '.md'
    path = Path(args.output) if args.output else engagement_dir / '07-reporting' / (basename + suffix)
    if args.restricted and not path.name.endswith('.restricted.md'):
        raise ValueError('Restricted output must have a .restricted.md filename.')
    if not args.restricted and path.name.endswith('.restricted.md'):
        raise ValueError('The .restricted.md suffix is reserved for restricted exports.')
    return path


def rows(conn, table, columns):
    # Only hard-coded identifiers from client_draft call sites reach this query.
    exists = conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (table,)).fetchone()
    return conn.execute(f'SELECT {columns} FROM {table} ORDER BY id').fetchall() if exists else []


def record_id(value):
    if type(value) is not int or value < 1:
        raise ValueError('Invalid record ID; export aborted.')
    return str(value)


def score_text(value):
    if type(value) not in (int, float) or not math.isfinite(value) or not 0 <= value <= 10:
        raise ValueError('Invalid numeric CVSS score; export aborted.')
    return str(value)


def client_draft(conn: sqlite3.Connection, kind: str) -> str:
    """Export only typed IDs, scores and boolean status; no stored text or files."""
    titles = {'engagement_report': 'Engagement Report', 'findings': 'Findings',
              'attack_chain': 'Attack Chain', 'credentials': 'Credentials'}
    lines = [f'# {titles[kind]} — client draft', '',
             '> DRAFT: fill in reviewed client prose before delivery. Stored text, credentials,',
             '> private notes, commands and attachment references are omitted. No evidence files are copied.', '',
             'Engagement / approved scope: [complete manually]', '']
    if kind == 'engagement_report':
        lines += ['## Executive Summary', '', '[Add reviewed results, impact and limitations.]', '']
    if kind in ('engagement_report', 'findings'):
        lines += ['## Findings', '']
        records = rows(conn, 'findings', 'id, cvss_score')
        if not records:
            lines += ['No findings recorded.', '']
        for identifier, score in records:
            lines += [f'### Finding {record_id(identifier)}', f'- Recorded CVSS score: {score_text(score)}',
                      '- Title / affected asset: [review and complete]',
                      '- Description / reproduction / impact: [review and complete]',
                      '- Evidence: [add a separately reviewed, redacted artifact]',
                      '- Remediation / retest: [review and complete]', '']
    if kind in ('engagement_report', 'attack_chain'):
        lines += ['## Attack Chain', '']
        records = rows(conn, 'exploit_chain_steps', 'id')
        if not records:
            lines += ['No exploit chain steps recorded.', '']
        for (identifier,) in records:
            lines += [f'### Chain record {record_id(identifier)}',
                      '- Sequence / action / result: [review and complete]', '']
    if kind in ('engagement_report', 'credentials'):
        lines += ['## Credentials', '']
        records = rows(conn, 'credentials', 'id, validated')
        if not records:
            lines += ['No credentials recorded.', '']
        for identifier, validated in records:
            if type(validated) is not int or validated not in (0, 1):
                raise ValueError('Invalid validation status; export aborted.')
            lines += [f'### Credential {record_id(identifier)}',
                      f"- Validation recorded: {'Yes' if validated else 'No'}",
                      '- Identity / access / remediation: [review and complete; omit reusable secrets]', '']
    if kind == 'engagement_report':
        lines += ['## Cleanup and Limitations', '', '[Add reviewed restoration and untested items.]', '']
    return '\n'.join(lines)


def write_export(path: Path, text: str, restricted: bool):
    if restricted:
        text = '> RESTRICTED APPENDIX — private operator data; distribute separately under agreed handling.\n\n' + text
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_symlink():
        raise ValueError('Refusing to export over a symbolic link.')
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=path.parent,
                                         prefix='.rb-export-', delete=False) as stream:
            temporary = Path(stream.name)
            os.fchmod(stream.fileno(), 0o600)
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        temporary = None
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
