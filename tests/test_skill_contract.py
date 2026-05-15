#!/usr/bin/env python3
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / 'skills' / 'public' / 'chip-bot-coop'
SKILL = SKILL_ROOT / 'SKILL.md'


def require(condition, message, failures):
    if not condition:
        failures.append(message)


def main():
    text = SKILL.read_text(encoding='utf-8')
    failures = []
    require(text.startswith('---\n'), 'SKILL.md must start with YAML frontmatter', failures)
    require(re.search(r'^name:\s*chip-bot-coop\s*$', text, re.M), 'frontmatter name missing', failures)
    desc = re.search(r'^description:\s*["\']?(.*?)["\']?\s*$', text, re.M)
    require(desc is not None and len(desc.group(1)) <= 1024, 'description missing or too long', failures)
    require('does **not** deliver messages sent by other bots' in text, 'missing Telegram bot-to-bot limitation', failures)
    require('## Output contract' in text, 'missing Output contract', failures)
    require('## Quick test checklist' in text, 'missing Quick test checklist', failures)
    require('## Done criteria' in text, 'missing Done criteria', failures)
    for ref in [
        'references/telegram-reality.md',
        'references/botfather-checklist.md',
        'references/hermes-config.md',
        'references/openclaw-config.md',
        'references/coop-patterns.md',
        'references/troubleshooting.md',
    ]:
        require((SKILL_ROOT / ref).exists(), f'missing {ref}', failures)
        require(ref in text, f'{ref} not linked from SKILL.md', failures)
    if failures:
        print('\n'.join(failures), file=sys.stderr)
        return 1
    print('skill contract: PASS')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
