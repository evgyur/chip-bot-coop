# chip-bot-coop

A public, secret-free Hermes skill for configuring Telegram agent bots so Hermes Agent and OpenClaw-style bots can coexist in the same chats.

The key point: Telegram Bot API does **not** deliver messages from other bots to a bot. BotFather privacy mode controls whether a bot receives ordinary human group messages; it does not enable bot-to-bot reading.

Use this skill to set up:

- shared Telegram groups/forums where humans mention the intended agent;
- strict allowed-chat and allowed-user gates;
- safe mention/reply policies;
- external relay designs for true agent-to-agent handoff.

## Layout

The public reusable skill package lives at:

```text
skills/public/chip-bot-coop/
```

A root-level copy is kept so a direct clone into `~/.hermes/skills/chip-bot-coop` still works for Hermes.

## Install

Install the public package directly:

```bash
hermes skills install https://raw.githubusercontent.com/evgyur/chip-bot-coop/main/skills/public/chip-bot-coop/SKILL.md
```

Or clone into your skills directory:

```bash
git clone https://github.com/evgyur/chip-bot-coop.git ~/.hermes/skills/chip-bot-coop
```

## Validate

```bash
python3 tests/test_public_hygiene.py
python3 tests/test_skill_contract.py
python3 tests/test_shell_syntax.py
```

## Public hygiene

This repo intentionally uses placeholders such as `<TELEGRAM_BOT_TOKEN>` and `<group_or_supergroup_chat_id>`. Do not commit real bot tokens, `.env` files, session files, logs, private paths, or screenshots of logged-in systems.
