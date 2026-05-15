---
name: chip-bot-coop
description: "Configure Telegram BotFather, OpenClaw, and Hermes Agent so two Telegram agent bots can coexist in shared chats, see authorized human messages, and cooperate safely despite Telegram's bot-to-bot visibility limit. Use for group/forum setup, privacy mode, allowed users/chats, mention gating, relay design, and troubleshooting why one bot cannot see another bot's messages."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [telegram, bots, hermes, openclaw, gateway, cooperation]
    related_skills: [hermes-agent]
---

# chip-bot-coop

Public, secret-free setup playbook for making Hermes Agent and OpenClaw-style Telegram bots work in the same chats.

## Non-negotiable Telegram reality

Telegram Bot API does **not** deliver messages sent by other bots to your bot. This remains true when BotFather privacy mode is disabled.

So “bots see each other in chats” must mean one of these explicit designs:

1. **Shared-room mode** — both bots see the same authorized human messages in the same group/forum and answer when mentioned or replied to.
2. **Relay mode** — bot-to-bot events move through a non-Telegram control plane: HTTP webhook, queue, database, MCP, or another internal event bus.
3. **User-account bridge mode** — a real Telegram user account/client observes the chat and relays selected messages to agents. This has higher operational and compliance risk.

Do not promise direct bot-to-bot Telegram visibility. It is not a configuration bug.

See [Telegram reality](references/telegram-reality.md) before changing config.

## Trigger contexts

Use this skill when the user asks to:

- set up Hermes and OpenClaw in the same Telegram group, supergroup, or forum topic;
- configure BotFather so an agent bot receives group messages;
- debug “Hermes does not see OpenClaw” or “OpenClaw does not see Hermes”;
- decide between mention-only, full-room, relay, or userbot cooperation;
- configure allowed users/chats without leaking a bot to a public group;
- write a public setup guide without private tokens, chat IDs, server paths, or deployment details.

## Operator flow

### ➊ Decide the cooperation model

Pick one before touching BotFather:

- **Recommended default:** shared-room + mention-gated responses.
- **For true agent-to-agent handoff:** external relay/control plane.
- **Avoid by default:** user-account bridge unless the user explicitly accepts the security/compliance burden.

### ➋ Configure BotFather

For each Telegram bot:

- `/setjoingroups` → enable if the bot must join groups.
- `/setprivacy` → disable only if the bot must receive ordinary human group messages.
- `/setcommands` → include explicit commands and mention names to reduce accidental triggers.
- Add the bot to the target group/forum.
- Make the bot admin only if it needs admin-only abilities: deleting messages, reading channel posts, managing topics, pinning, etc.

Full checklist: [BotFather checklist](references/botfather-checklist.md).

### ➌ Configure Hermes Agent

Use `hermes gateway setup` or edit `~/.hermes/config.yaml`. Keep the token in `.env`, not in the YAML committed to git.

Minimal group-safe shape:

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
```

Then restart the live gateway and verify with logs/getUpdates.

Detailed Hermes notes: [Hermes config](references/hermes-config.md).

### ➍ Configure OpenClaw-style bot

OpenClaw deployments vary. Use the same three gates even if key names differ:

- **Token gate:** bot token comes from env/secret store only.
- **Chat gate:** only approved group IDs are processed.
- **Human gate:** only approved sender user IDs can trigger work in groups.
- **Mention/reply gate:** shared chats should not let every message start an agent run.

Generic template: [OpenClaw config](references/openclaw-config.md).

### ➎ Verify with a matrix, not vibes

Run these tests in the target chat/topic:

- Human → Hermes mention: Hermes receives and responds.
- Human → OpenClaw mention: OpenClaw receives and responds.
- Human ordinary message: ignored if mention-gated; received if full-room mode.
- Hermes bot message → OpenClaw: OpenClaw does **not** receive it through Bot API; expected.
- OpenClaw bot message → Hermes: Hermes does **not** receive it through Bot API; expected.
- Relay event → target agent: if relay mode exists, the target agent receives the event outside Telegram.

Troubleshooting: [Troubleshooting](references/troubleshooting.md).

## Output contract

When using this skill for a real setup or review, report:

1. selected cooperation model: shared-room, relay, or user-account bridge;
2. BotFather settings for each bot: privacy mode, join groups, admin status;
3. Hermes gates: allowed chats, allowed human users, mention policy;
4. OpenClaw gates: allowed chats, allowed human users, mention policy;
5. verification matrix results;
6. explicit statement on bot-to-bot Telegram visibility: direct visibility is impossible via Bot API;
7. secrets/public hygiene result if writing docs or a repo.

## Quick test checklist

- [ ] Skill states that Telegram Bot API does not deliver other bots' messages.
- [ ] BotFather section distinguishes privacy mode from bot-to-bot visibility.
- [ ] Hermes config uses placeholders, not real tokens, chat IDs, user IDs, or private paths.
- [ ] OpenClaw config is generic and names key concepts rather than private deployment files.
- [ ] At least one safe default uses mention/reply gating in shared groups.
- [ ] Relay mode is recommended for true agent-to-agent handoff.
- [ ] Public repo tests scan for secrets and private infrastructure strings.

## Done criteria

- [ ] No secrets, tokens, session files, private chat IDs, private IPs, or host-specific paths in the public repo.
- [ ] `python3 tests/test_public_hygiene.py` passes.
- [ ] `python3 tests/test_skill_contract.py` passes.
- [ ] `python3 tests/test_shell_syntax.py` passes.
- [ ] Hermes skill guard passes when available.
- [ ] Fresh public clone passes the same tests.

## References

- [Telegram reality](references/telegram-reality.md)
- [BotFather checklist](references/botfather-checklist.md)
- [Hermes config](references/hermes-config.md)
- [OpenClaw config](references/openclaw-config.md)
- [Cooperation patterns](references/coop-patterns.md)
- [Troubleshooting](references/troubleshooting.md)

## Templates and scripts

- [Hermes Telegram YAML](templates/hermes-telegram.yaml)
- [OpenClaw Telegram env example](templates/openclaw-telegram.env.example.txt)
- [Relay event JSON schema](templates/relay-event.schema.json)
- [Webhook info check script](scripts/check_bot_api_webhook.sh)
