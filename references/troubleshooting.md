# Troubleshooting

## “Bot A cannot see Bot B”

Expected via plain Telegram Bot API. Telegram Bot API does not deliver messages from other bots.

Fix: use an external relay or user-account bridge if true machine-to-machine handoff is required. In shared or bridged threads, bot-authored handoffs/statuses must use the explicit target envelope so routing is unambiguous:

- Hermes → Claw: `@chipsclawbot [ACK/DONE/BLOCKED] ...`
- Claw → Hermes: `@chipshermesbot [ACK/DONE/BLOCKED] ...`

Mention is preferred over relying only on reply-to because the receiving gateway/relay may require mention.

## “Bot does not see human group messages”

Check in order:

1. BotFather `/setprivacy` is disabled if full-room human messages are required.
2. Bot is in the correct group/supergroup/forum.
3. Gateway is using the correct bot token.
4. Only one webhook/polling consumer is active for that token.
5. Chat ID allowlist includes the real supergroup ID, usually shaped like `-100...`.
6. Human sender allowlist includes the sender's numeric user ID.
7. Mention/reply gate is not intentionally suppressing ordinary messages.
8. Gateway logs do not show unauthorized chat/user.

## “Bot answers too often”

Do not rely on BotFather privacy alone. Add runtime gates:

- allowed chat IDs;
- allowed human user IDs;
- mention/reply requirement in shared groups;
- ignored threads/topics where needed.

## “Messages arrive in Bot API getUpdates but agent ignores them”

This is a gateway policy issue, not a Telegram issue. Inspect allowlists, mention patterns, thread filters, and per-chat policies.

## “No updates arrive at all”

Check webhook/polling conflict:

```bash
curl -sS "https://api.telegram.org/bot<TELEGRAM_BOT_TOKEN>/getWebhookInfo"
```

Do not paste real tokens in chat, logs, issues, or public repos.
