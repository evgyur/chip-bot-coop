# Cooperation patterns

## Pattern A: shared-room, mention-gated

Best default for human-facing groups.

- Both bots are in the group.
- Humans mention the intended bot or reply to it.
- Both bots maintain strict chat and user allowlists.
- Bots do not consume each other's Telegram messages.

Use when the goal is “both agents are available in this chat.”

## Pattern B: external relay/control plane

Best for true agent-to-agent cooperation.

Common relay options:

- HTTP webhook endpoint from Bot A to Bot B.
- Shared queue such as Redis, NATS, SQS, or a database table.
- MCP/server tool exposed to both agents.
- Internal API with signed events and idempotency keys.

Minimal relay event fields:

```json
{
  "event_id": "unique-id",
  "source_agent": "hermes",
  "target_agent": "openclaw",
  "origin_platform": "telegram",
  "origin_chat_id": "<chat_id>",
  "origin_thread_id": "<thread_or_topic_id>",
  "human_sender_id": "<trusted_human_user_id>",
  "text": "handoff text",
  "created_at": "2026-01-01T00:00:00Z"
}
```

Security requirements:

- signed requests or private network;
- replay protection using `event_id`;
- no bot tokens in event payloads;
- clear audit log of who triggered the handoff.

## Pattern C: user-account bridge

Use only when accepted explicitly.

A real Telegram user account/client can observe bot messages in a chat and relay selected content to agents. This may be useful for operator dashboards, but it is more fragile and carries account, compliance, and privacy risk.

Rules:

- never share session files casually;
- run a single client per account/session;
- document retention and access;
- prefer read-only observation unless a human explicitly approves sending.
