"""Resolve exactly one existing engagement per command invocation."""
from contextlib import contextmanager
from contextvars import ContextVar
import os
import argparse
from pathlib import Path
import re
import subprocess

from rb_private import safe_parent

_CURRENT = ContextVar('rb_ops_engagement', default=None)


class SelectOnce(argparse.Action):
    def __call__(self, parser, namespace, value, option_string=None):
        if getattr(namespace, self.dest, None) is not None:
            parser.error('Specify --engagement only once.')
        setattr(namespace, self.dest, value)


def add_engagement_option(parser):
    parser.add_argument('--engagement', metavar='NAME', action=SelectOnce,
                        help='Existing engagement under PENTEST_BASE; overrides tmux (place before subcommand)')


@contextmanager
def invocation(name=None):
    state = {'name': name, 'resolved': None, 'connections': []}
    token = _CURRENT.set(state)
    try:
        yield
    finally:
        try:
            for connection in state["connections"]:
                connection.close()
        finally:
            _CURRENT.reset(token)


def resolve(name=None):
    if name is None:
        if not os.environ.get('TMUX'):
            raise ValueError('Select --engagement NAME or run inside an engagement tmux session.')
        try:
            name = subprocess.check_output(['tmux', 'display-message', '-p', '#S'],
                                           text=True, stderr=subprocess.DEVNULL, timeout=5).strip()
        except (OSError, subprocess.SubprocessError) as error:
            raise ValueError('Unable to determine tmux engagement.') from error
    if not isinstance(name, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,127}', name):
        raise ValueError('Engagement must be a single safe directory name, not a path.')
    base = Path(os.environ.get('PENTEST_BASE', '~/pentest/engagements')).expanduser().absolute()
    directory = base / name
    if not directory.is_dir():
        raise ValueError('Selected engagement does not exist; create it explicitly with rb-start.')
    safe_parent(directory)
    return name, directory, directory / '.redbrixen' / 'opskit.db'


def engagement_context():
    state = _CURRENT.get()
    if state is None:
        return resolve()
    if state['resolved'] is None:
        state['resolved'] = resolve(state['name'])
    return state['resolved']


def register_connection(conn):
    state = _CURRENT.get()
    if state is not None:
        state['connections'].append(conn)
