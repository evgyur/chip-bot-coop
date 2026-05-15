#!/usr/bin/env python3
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {'.md', '.txt', '.yaml', '.yml', '.json', '.sh', '.py', '.example', '.gitignore'}
SKIP_DIRS = {'.git', '__pycache__', '.pytest_cache'}

SECRET_PATTERNS = [
    re.compile(r'\b\d{8,12}:[A-Za-z0-9_-]{30,}\b'),  # Telegram bot token
    re.compile(r'\bgh[pousr]_[A-Za-z0-9_]{20,}\b'),
    re.compile(r'\bsk-[A-Za-z0-9_-]{20,}\b'),
    re.compile(r'\bxox[baprs]-[A-Za-z0-9-]{20,}\b'),
    re.compile(r'-----BEGIN (?:RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----'),
]
# Built without writing sensitive/private examples contiguously in this public file.
PRIVATE_STRINGS = [
    ''.join(['/home/', 'hermes']),
    ''.join(['/opt/', 'telegram-', 'chip']),
    ''.join(['/opt/', 'clawd-', 'workspace']),
    ''.join(['138', '.', '201', '.']),
    ''.join(['617', '744', '661']),
]


def iter_text_files():
    for path in ROOT.rglob('*'):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.is_file() and (path.suffix in TEXT_SUFFIXES or path.name in {'SKILL.md', 'README.md', 'LICENSE'}):
            yield path


def main():
    failures = []
    for path in iter_text_files():
        text = path.read_text(encoding='utf-8', errors='ignore')
        rel = path.relative_to(ROOT)
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                failures.append(f'{rel}: matched secret pattern {pattern.pattern}')
        for needle in PRIVATE_STRINGS:
            if needle in text:
                failures.append(f'{rel}: contains private string {needle!r}')
    if failures:
        print('\n'.join(failures), file=sys.stderr)
        return 1
    print('public hygiene: PASS')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
