# Hermes Agent Telegram config

Use the Hermes setup flow when possible:

```bash
hermes gateway setup
hermes gateway status
```

Keep the Telegram token in `.env` or the platform secret store:

```bash
TELEGRAM_BOT_TOKEN=<TELEGRAM_BOT_TOKEN>
```

Do not commit `.env`.

## Group-safe config shape

In `~/.hermes/config.yaml`:

```yaml
telegram:
  require_mention: true
  allowed_chats:
    - "<group_or_supergroup_chat_id>"
  group_allowed_chats:
    - "<group_or_supergroup_chat_id>"
  group_allow_from:
    - "<trusted_human_user_id>"
  require_mention_chats:
    - "<group_or_supergroup_chat_id>"
  mention_patterns:
    - "@<hermes_bot_username>"
    - "hermes"
  reply_to_mode: "all"
```

Key meanings:

- `allowed_chats`: broad Telegram chat whitelist.
- `group_allowed_chats`: group/supergroup whitelist.
- `group_allow_from`: human sender IDs authorized to trigger the bot in groups.
- `require_mention`: require mention/reply before responding.
- `require_mention_chats`: apply mention-only behavior to specific noisy/shared chats.
- `mention_patterns`: strings treated as mentions in addition to Telegram-native replies.
- `reply_to_mode`: keep replies threaded/clear in busy chats when supported by the gateway version.

## Runtime verification

Use the live install, not a stale checkout:

```bash
hermes config path
hermes gateway status
```

Check logs after sending a human test message in the group:

```bash
grep -iE "telegram|unauthorized|allowed|mention" ~/.hermes/logs/gateway.log | tail -80
```

Expected outcomes:

- Unauthorized human sender: rejected by `group_allow_from` or equivalent gate.
- Unauthorized chat: rejected by chat whitelist.
- Bot-authored message: absent from updates or ignored; this is expected Telegram behavior.
