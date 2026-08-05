# Eve integration

Eve packages skills under its skill directory and exposes typed tools to the model. Install this repository as a skill, add the routing rule below to the Telegram channel prompt, and register a thin tool that validates and renders while the channel owns delivery.

```text
For Telegram responses, use telegram-rich-composer situationally. Keep normal chat plain.
Use rich mode for structured comparisons, reports, semantic media, or explicit requests.
Never invent chatId: channel.telegram.chatId and the incoming message context are authoritative.
```

The example `tool.ts` returns a rendered payload rather than issuing an arbitrary recipient request. The channel layer must inject its current `channel.telegram.chatId`, topic, and reply context. If Eve exposes a raw Telegram request tool, allow only `sendRichMessage` to the current channel context and keep outbound redaction ahead of this tool.

Capability declaration for a current Bot API 10.2 channel:

```json
{
  "rich_blocks": true,
  "rich_markdown": true,
  "rich_html": true,
  "legacy_html": true,
  "plain_album": true,
  "details_nested_media": true,
  "media_spoiler": true
}
```

Do not replace Eve's concise Telegram defaults globally. The selector decides per answer.
