---
name: telegram-rich-composer
description: Shape tone-aware Hermes replies for Telegram with a visible answer, useful navigation, collapsible details, tables, or task lists. Use for reports, comparisons, plans, evidence, risks, and structured demonstrations.
metadata:
  hermes:
    tags: [telegram, rich-messages, writing]
    category: communication
---

# Telegram Rich Composer for Hermes

Use this skill for Hermes replies in Telegram.

Follow the [Telegram Bot API formatting options](https://core.telegram.org/bots/api#rich-message-formatting-options) for supported Rich Message syntax and blocks.

## Choose the reply type

Use a normal message for a greeting, confirmation, link, correction, or short answer.

Use a layered reply when the reader needs a conclusion now and may need evidence, a comparison, logs, sources, or risks later.

## Build a layered reply

1. Put the conclusion or next action in the first one to three lines.
2. Add a one-line index only when it materially improves scanning. Prefer numbers for ordered or formal sections. Use short semantic emoji labels only when they match the user's tone and remain unambiguous.
3. Put each secondary section in one `<details>` block.
4. When an index is present, match each `<summary>` label and title to it.
5. Use two to four details blocks and one nesting level.
6. Keep warnings, deadlines, destructive actions, and the required next step visible.
7. Write in the user's language.
8. Return the reply as Markdown.

Use this shape:

```markdown
Short answer: {conclusion and next action}

Index: 1. {first topic} · 2. {second topic} · 3. {third topic}

<details>
<summary>1. {first topic}</summary>

{secondary information}

</details>

<details>
<summary>2. {second topic}</summary>

{secondary information}

</details>
```

Keep short conversations compact. Place the answer before the sections. Place block mathematics outside `<details>`.

## Tone and content fidelity

Match the user's language and level of formality. Treat user-supplied text that is explicitly marked as exact or verbatim as fixed content: preserve its wording, capitalization, order, repetition, and intentional spelling.

Standard Unicode emoji can appear directly in text and `<summary>` labels. Use them only when they carry navigation, status, or emphasis. Do not add emoji to every list item or use them as confetti. Keep facts, warnings, deadlines, and required actions clear in every tone.

## Hermes delivery boundaries

Set `gateway.platforms.telegram.extra.rich_messages` to `true`.

The Hermes Telegram adapter handles the bot token, recipient, topic, reply target, and delivery. Keep those values in the adapter.

Keep the fallback readable. After an unknown delivery result, check the delivery state before retrying.
