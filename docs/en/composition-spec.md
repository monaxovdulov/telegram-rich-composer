# CompositionSpec 1.0

[Русская версия](../ru/composition-spec.md)

The canonical schema is [`schemas/composition-spec.schema.json`](../../schemas/composition-spec.schema.json). The document represents one semantic Telegram response before recipient binding.

| Section | Purpose | Trust level |
|---|---|---|
| `surface` | Telegram chat type, locale, draft state, advisory capabilities | Untrusted model context |
| `selection` | Plain/rich decision, pattern, density, reason codes | Untrusted and validated |
| `summary` | Fallback-safe answer text | Untrusted and validated |
| `blocks` | Semantic block and inline tree | Untrusted and validated |
| `media` | Logical IDs and Telegram, HTTPS, or controlled local sources | Untrusted; adapter policy applies |
| `delivery` | Reply/thread inheritance, notification, protection, entity policy, buttons | Intent only; adapter binds values |
| `fallback` | Ordered representations and unknown-result rule | Untrusted and validated |
| `diagnostics` | Structured warnings produced during composition | Informational |

The schema deliberately has no `chat_id`, thread ID, reply message ID, bot token, authorization claim, or harness session. Those values exist only in `TrustedConversationContext`.

Rich text supports nested formatting, safe explicit links, anchors, references, custom emoji, and formulas. Blocks cover paragraphs, headings, preformatted text, lists, quotations, tables, details, maps, media, collage, slideshow, and draft-only thinking.

Validation combines JSON Schema, Telegram limits, binding integrity, URL and local-path safety, draft constraints, capability warnings, and editorial budgets. Passing schema validation alone is insufficient.
