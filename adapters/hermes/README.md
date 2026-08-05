# Hermes Agent integration

Hermes already has an opt-in rich fast path and draft streaming in its Telegram platform adapter. Install this skill under `~/.hermes/skills/telegram-rich-composer` and merge the routing guidance into the platform prompt. The skill should make the current rich hint more conservative: rich mode is situational, not the default whenever formatting is available.

Use `plugin.py` as a small policy plugin or copy its pure functions into the existing Telegram adapter. Preserve Hermes behavior that does not resend a legacy message after a timeout or unknown result. Keep forum topic routing and `reply_parameters` from the inbound event.

For draft streaming, declare `draft=true` only in private chat, use a stable nonzero draft ID, avoid direct upload of new files, and finish with a persistent `sendRichMessage`. Never use a `thinking` block in the final message.
