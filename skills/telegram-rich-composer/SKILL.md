---
name: telegram-rich-composer
description: Use when Hermes answers in Telegram and the reply benefits from a short visible conclusion, a numbered index, collapsible details, a table, or a task list. Keep ordinary replies plain.
version: 0.1.0
metadata:
  hermes:
    tags: [telegram, rich-messages, writing]
    category: communication
---

# Telegram Rich Composer for Hermes

Use this skill only for replies that Hermes sends to Telegram.

## Choose the reply type

Use a normal message for a greeting, confirmation, link, correction, or short answer.

Use a layered reply when the reader needs a conclusion now and may need evidence, a comparison, logs, sources, or risks later.

## Build a layered reply

1. Put the conclusion or next action in the first one to three lines.
2. Add a one-line numbered index when the reply has two or more secondary sections.
3. Put each secondary section in one `<details>` block.
4. Match each `<summary>` number and title to the index.
5. Use two to four details blocks and one nesting level.
6. Keep warnings, deadlines, destructive actions, and the required next step outside collapsed details.
7. Write in the user's language.
8. Do not wrap the complete reply in a code fence.

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

Do not force this template onto a short conversation. Do not hide the answer to make the reader open a section. Keep block mathematics outside `<details>`.

## Hermes delivery boundaries

Hermes must have `gateway.platforms.telegram.extra.rich_messages` set to `true`. Keep `rich_drafts` set to `false` for the first test.

The native Hermes Telegram adapter owns the bot token, recipient, topic, reply target, and final send. This skill must not request or print those values.

If Telegram rejects rich rendering, keep the fallback readable. After a timeout or unknown delivery result, do not send a second copy.
