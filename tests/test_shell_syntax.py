#!/usr/bin/env python3
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]


def main():
    failures = []
    for path in (ROOT / 'scripts').glob('*.sh'):
        result = subprocess.run(['bash', '-n', str(path)], text=True, capture_output=True)
        if result.returncode != 0:
            failures.append(f'{path.relative_to(ROOT)}: {result.stderr.strip()}')
    if failures:
        print('\n'.join(failures), file=sys.stderr)
        return 1
    print('shell syntax: PASS')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
