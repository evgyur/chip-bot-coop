# OpenClaw-style Telegram config

OpenClaw deployments differ, so use concepts rather than hardcoded private file names.

## Required gates

```bash
OPENCLAW_TELEGRAM_BOT_TOKEN=<TELEGRAM_BOT_TOKEN>
OPENCLAW_TELEGRAM_ALLOWED_CHATS=<comma_separated_group_chat_ids>
OPENCLAW_TELEGRAM_GROUP_ALLOWED_USERS=<comma_separated_human_user_ids>
OPENCLAW_TELEGRAM_REQUIRE_MENTION=true
OPENCLAW_TELEGRAM_MENTION_PATTERNS=@<openclaw_bot_username>,openclaw,claw
```

Your actual variable names may differ. Preserve these semantics:

- Token lives in secret storage only.
- Chat whitelist is explicit.
- Human sender whitelist is explicit.
- Shared groups default to mention/reply-only.
- Bot-authored Telegram messages are not used as the handoff bus.

## Webhook vs polling

Only one update consumer should use a bot token at a time.

- If using webhook: ensure the public URL is correct and TLS is valid.
- If using long polling: delete stale webhook first.
- Do not run two gateway processes with the same bot token unless the framework explicitly coordinates update consumption.

## Verification

For a human message in a target group, logs should show:

- chat ID accepted;
- sender user ID accepted;
- mention/reply gate passed;
- agent run started.

For a message sent by another bot, logs should either show no update or an explicit ignore path. Both are acceptable; treating it as a normal user message is not.
