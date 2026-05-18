# Telegram reality: what bots can and cannot see

Telegram has two separate concepts that are easy to confuse.

## Privacy mode

BotFather privacy mode controls whether a bot receives ordinary **human** messages in groups.

- Privacy enabled: the bot receives commands, replies/mentions, service messages, and a limited set of relevant updates.
- Privacy disabled: the bot can receive ordinary human group messages, subject to your own gateway filtering.

## Bot-to-bot visibility

Telegram Bot API does not deliver messages sent by other bots to your bot. Bot admins and bots with privacy disabled receive all relevant group messages **except messages sent by other bots**.

Implication:

- Hermes cannot read OpenClaw bot messages through its Telegram bot token.
- OpenClaw cannot read Hermes bot messages through its Telegram bot token.
- Disabling privacy does not change this.
- Making both bots admins does not create a normal bot-to-bot conversation channel.

## Correct mental model

Telegram group chat is a user-facing surface, not a reliable agent message bus.

Use Telegram for human instructions and visible replies. Use an external relay for machine-to-machine handoff.

For shared or bridged threads, bot-authored handoffs/statuses must still be explicitly addressed:

- Hermes → Claw: `@chipsclawbot [ACK/DONE/BLOCKED] ...`
- Claw → Hermes: `@chipshermesbot [ACK/DONE/BLOCKED] ...`

Reply-to can help, but mention is the safer default because the target gateway/relay may run with `require_mention`. This is a routing envelope for humans, bridges, and relays; it does not bypass Telegram's bot-to-bot delivery limit.
