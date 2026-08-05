# Hermes Agent integration

Current Hermes releases have an opt-in Rich Message path in the native Telegram adapter. Start with the small skill-only package. It needs no Python package or third-party plugin.

```bash
hermes skills inspect monaxovdulov/telegram-rich-composer/skills/telegram-rich-composer
hermes skills install monaxovdulov/telegram-rich-composer/skills/telegram-rich-composer --yes
```

Enable final Rich Messages in the active profile's `config.yaml`. Keep rich drafts off for the first test.

```yaml
gateway:
  platforms:
    telegram:
      extra:
        rich_messages: true
        rich_drafts: false
```

Restart the gateway. Then use the test prompt in the [beginner guide](../../docs/en/hermes-quickstart.md), or the [Russian version](../../docs/ru/hermes-quickstart.md).

The skill keeps normal conversation plain. It uses a short visible answer, useful navigation, and collapsed details only when the reply needs layers. Emoji labels appear only when they match the user's tone and improve scanning.

## Full composer integration

Use `plugin.py` as a small policy plugin or copy its pure functions into the existing Telegram adapter. Preserve Hermes behavior that does not resend a legacy message after a timeout or unknown result. Keep forum topic routing and `reply_parameters` from the inbound event.

For draft streaming, declare `draft=true` only in private chat, use a stable nonzero draft ID, avoid direct upload of new files, and finish with a persistent `sendRichMessage`. Never use a `thinking` block in the final message.
