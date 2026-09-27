#!/usr/bin/env python3
"""Run maintainer checks from any directory; never execute assessment commands."""
import ast
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def run(*args):
    print('+', ' '.join(map(str, args)), flush=True)
    subprocess.run(args, cwd=ROOT, check=True)


def main():
    run(sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-v')
    run(sys.executable, 'tests/check_internal_links.py')
    run(sys.executable, 'tests/check_lab_records.py')
    # Git's ignore rules keep virtualenvs and generated files out. Include new
    # unstaged sources so the local command also verifies work before a commit.
    names = subprocess.check_output(
        ['git', 'ls-files', '--cached', '--others', '--exclude-standard', '-z'],
        cwd=ROOT).decode().split('\0')
    python_count = shell_count = 0
    for name in sorted(set(names) - {''}):
        path = ROOT / name
        if not path.is_file():
            continue
        source = path.read_bytes()
        first_line = source.split(b'\n', 1)[0]
        if path.suffix == '.py' or (first_line.startswith(b'#!') and b'python' in first_line):
            ast.parse(source, filename=name)
            python_count += 1
        elif path.suffix == '.sh' or (first_line.startswith(b'#!') and b'bash' in first_line):
            run('bash', '-n', name)
            shell_count += 1
    print(f'PASS: parsed {python_count} Python and {shell_count} Bash sources; runtime behavior not implied.')
    print('PASS: maintainer validation. Full guide release acceptance remains a separate review.')


if __name__ == '__main__':
    try:
        main()
    except (OSError, SyntaxError, subprocess.CalledProcessError) as error:
        print(f'FAIL: {error}', file=sys.stderr)
        raise SystemExit(1)
