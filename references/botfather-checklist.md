# BotFather checklist

Run these for each bot through `@BotFather`.

## Required for group operation

1. `/setjoingroups`
   - Enable if the bot should be added to groups.
   - Disable for bots that must remain DM-only.

2. `/setprivacy`
   - Keep **enabled** for command/reply/mention-only behavior.
   - Disable only when the bot must receive ordinary human group messages.
   - This does not allow the bot to see messages from other bots.

3. `/setcommands`
   - Add commands that are unambiguous in shared chats.
   - Prefer namespaced commands when two bots have overlapping verbs.
   - Example shape: `/hermes_status`, `/openclaw_status`, `/handoff`.

4. Add bot to the target group/supergroup/forum.

5. Admin status:
   - Not required just to receive human group messages when privacy mode is disabled.
   - Required for admin-only operations: deleting messages, pinning, managing topics, reading some channel contexts, etc.

## After changing BotFather settings

- Send new test messages; old messages will not be replayed.
- Restart your gateway only if your runtime caches bot metadata or webhook/polling state.
- If the bot still does not receive group messages, verify chat ID allowlists and sender user allowlists before blaming BotFather.
