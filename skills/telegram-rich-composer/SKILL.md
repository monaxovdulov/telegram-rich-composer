---
name: telegram-rich-composer
description: Shape Hermes replies for Telegram with a visible conclusion, next step, numbered index, collapsible details, table, or task list. Use for reports, comparisons, plans, evidence, and risks.
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
2. Add a one-line numbered index when the reply has two or more secondary sections.
3. Put each secondary section in one `<details>` block.
4. Match each `<summary>` number and title to the index.
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

## Hermes delivery boundaries

Set `gateway.platforms.telegram.extra.rich_messages` to `true`.

The Hermes Telegram adapter handles the bot token, recipient, topic, reply target, and delivery. Keep those values in the adapter.

Keep the fallback readable. After an unknown delivery result, check the delivery state before retrying.
