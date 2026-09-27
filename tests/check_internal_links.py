#!/usr/bin/env python3
"""Check parsed local Markdown destinations; maintainer QA, never a field prerequisite.

Run: python3 tests/check_internal_links.py [repository-root]
Requires requirements-dev.txt. External URLs and fragments are not validated.
Raw HTML links are outside this check; use Markdown for repository navigation.
"""
from __future__ import annotations
import argparse
from pathlib import Path
from urllib.parse import unquote, urlsplit
from markdown_it import MarkdownIt

PARSER = MarkdownIt('commonmark')
EXCLUDED = {'.git', '__pycache__', '.venv', 'venv', 'node_modules'}


def destinations(markdown: str):
    """Use the same syntax as rendered CommonMark, including reference links."""
    def walk(tokens):
        for token in tokens:
            if token.type == 'link_open':
                yield token.attrGet('href')
            elif token.type == 'image':
                yield token.attrGet('src')
            if token.children:
                yield from walk(token.children)
    yield from walk(PARSER.parse(markdown))


def check(root: Path) -> tuple[int, list[str]]:
    root = root.resolve()
    checked = 0
    errors = []
    for document in sorted(root.rglob('*.md')):
        if any(part in EXCLUDED for part in document.relative_to(root).parts):
            continue
        for target in destinations(document.read_text(encoding='utf-8')):
            parts = urlsplit(target)
            if parts.scheme or parts.netloc or not parts.path:
                continue
            checked += 1
            local = unquote(parts.path)
            candidate = (root / local.lstrip('/') if local.startswith('/') else document.parent / local).resolve()
            if not candidate.is_relative_to(root):
                errors.append(f'{document.relative_to(root)}: {target} escapes repository')
            elif not candidate.exists():
                errors.append(f'{document.relative_to(root)}: {target} not found')
    return checked, errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path, nargs='?', default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args()
    count, errors = check(args.root)
    print(f'Checked {count} rendered local Markdown destinations (files and directories).')
    for error in errors:
        print('FAIL:', error)
    print('FAIL' if errors else 'PASS', f'({len(errors)} broken destinations)')
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
