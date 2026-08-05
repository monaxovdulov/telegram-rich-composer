# Architecture

[Русская версия](../ru/architecture.md)

Status: accepted design for version 1 of the package.

## Purpose

`telegram-rich-composer` helps an agent decide whether a Telegram reply should be plain or rich. It then compiles a semantic `CompositionSpec` for the best available transport.

The package does not replace a Telegram gateway. The host owns authentication, the current conversation, retries, and final delivery.

## Scope

The package contains six layers.

1. `SKILL.md` selects plain or rich output and selects a composition pattern.
2. `CompositionSpec` stores the response structure without harness-specific fields.
3. The renderer compiles the specification to explicit Telegram blocks, Rich Markdown, Rich HTML, standard Telegram text, or plain text.
4. The validator checks the schema, Telegram limits, editorial budgets, anchors, media, and safety rules.
5. A harness adapter binds the payload to a trusted conversation context and negotiates capabilities.
6. The fallback controller degrades the representation without losing the main answer.

The package has no polling loop, conversation database, or end-user editor.

## Data flow

```text
user request
  -> always-on Telegram routing rule
  -> lazy-loaded SKILL.md
  -> selector
  -> CompositionSpec
  -> schema and semantic validation
  -> capability negotiation
  -> renderer
  -> harness adapter + trusted conversation context
  -> Telegram
              \-> safe fallback for permanent rejection
```

The main answer is the first visible content. A warning is never hidden in `details`. Diagnostics stay outside the user-facing payload.

## CompositionSpec v1

The canonical schema is `schemas/composition-spec.schema.json`. A specification has these top-level fields:

| Field | Role |
|---|---|
| `schema_version` | Version of the semantic contract. Version 1 uses `1.0` semantics. |
| `surface` | Telegram chat type, draft state, locale, and offered capabilities. |
| `selection` | Plain or rich mode, pattern, density profile, and reason codes. |
| `summary` | The visible answer that must remain available in every fallback. |
| `blocks` | Ordered semantic blocks. |
| `media` | Named media references and their controlled source types. |
| `delivery` | Reply, thread, silent, protection, entity detection, and button intent. |
| `fallback` | Ordered degradation policy and duplicate-send policy. |
| `diagnostics` | Warnings for the host. The adapter must not send them to the user. |

`CompositionSpec` has no `chat_id`, token, URL for the Bot API, or harness session identifier. This prevents the model from selecting an arbitrary recipient.

### Rich text

Text fields accept a string or an ordered list of inline nodes. Version 1 supports plain text, bold, italic, underline, strikethrough, spoiler, mark, inline code, subscript, superscript, explicit links, anchor links, references, reference links, formulas, and custom emoji.

### Blocks

Version 1 supports paragraph, heading, divider, list, checklist, quote, pull quote, code, preformatted text, formula, table, details, footer, anchor, map, photo, video, animation, audio, voice note, collage, slideshow, and thinking.

`thinking` is valid only for a temporary rich draft. It is invalid for a final message.

### Media

A media reference uses exactly one source:

- Telegram `file_id`;
- an HTTP or HTTPS URL that passes the adapter policy;
- a local path that passes an allowed-root check and has explicit upload permission.

The core never uploads a local file to an anonymous public host. A direct adapter can use Telegram multipart upload when the host grants `controlled_local_upload`.

## Validation

Validation has three stages.

1. JSON Schema validation checks shape and types.
2. Semantic validation checks cross-field rules and Telegram limits.
3. Editorial validation checks density budgets and mobile readability. Editorial violations are warnings unless they can break delivery or hide required content.

The semantic validator checks these Bot API 10.2 limits:

- 32,768 characters;
- 500 blocks, including nested structures, list items, and table rows;
- 16 nesting levels;
- 50 media attachments;
- 20 table columns.

It also checks unique media IDs, anchor targets, `details` state, table spans, map dimensions, media source policy, and draft-only blocks.

## Rendering

The renderer has four outputs.

1. `rich_blocks` produces an `InputRichMessage.blocks` payload.
2. `rich_markdown` produces `InputRichMessage.markdown` and explicit media bindings.
3. `rich_html` produces `InputRichMessage.html` and explicit media bindings.
4. The compatibility targets produce ordinary HTML, Markdown, or plain text with a conventional media plan.

Exactly one of `blocks`, `markdown`, or `html` is present in one rich payload.

The explicit block renderer is the preferred target. It avoids parser ambiguity and preserves table spans, details state, references, and media metadata. Rich Markdown or Rich HTML remains useful for harnesses that already expose those paths.

## Selection

Plain text is the default for short conversational answers. Rich output needs a clear gain in scanning, comparison, disclosure, sequence, media, or structured action.

The selector returns reason codes. This makes every choice testable. Examples include `short_conversation`, `collapsed_evidence`, `simultaneous_comparison`, `ordered_visual_sequence`, and `structured_decision`.

One image uses one media block. A collage supports simultaneous comparison. A slideshow supports a sequence of related states or diagrams.

## Capability negotiation

An adapter reports atomic capabilities. The core does not infer support from a harness name. Negotiation uses this order:

1. explicit rich blocks;
2. Rich Markdown or Rich HTML;
3. ordinary Telegram HTML or Markdown;
4. plain text and an ordinary media group.

Nested blocks and nested media inside `details` are separate capabilities. So are anchors, media spoilers, references, custom emoji, maps, reply parameters, topics, reply markup, draft streaming, and controlled local upload.

## Delivery and duplicate safety

The adapter receives a `TrustedConversationContext` from the harness. It contains the current chat, reply target, thread or topic, sender authorization, and optional allowlist evidence.

The adapter must bind `delivery.reply` and `delivery.thread` to that context. A different chat or channel requires an explicit user request and an allowlist decision outside the specification.

A permanent syntax or capability rejection can fall back before another send. A timeout, disconnected response, or unknown network result cannot trigger an automatic second send. The adapter records the attempt as `unknown` and asks the host to reconcile it.

## Current harness decisions

### Eve

Eve supports packaged skills and typed tools. Its stock Telegram channel currently asks for concise plain text and has no `sendRichMessage` path. The integration therefore includes an always-on instruction, a typed composition tool, and a channel adapter example that binds `channel.telegram.chatId` and `messageThreadId`.

### Iva

Iva already routes tables, task lists, details, and block math to `sendRichMessage`. It also applies outbound redaction and falls back to HTML. The integration reuses that transport. It adds `CompositionSpec` validation and pattern selection before the existing send path. It does not replace the allowlist or redaction gate.

### Hermes Agent

Hermes already has an opt-in rich fast path, draft streaming, rich final edits, reply parameters, topic routing, and conservative duplicate protection. The integration uses a skill for selection and a plugin tool for compile and validation. Native Telegram delivery remains the owner of the final send.

### Direct Bot API

The reference adapter accepts a trusted context supplied by the caller. It supports JSON requests and controlled multipart upload. It has an attempt ledger and never retries an unknown result automatically.

## Source baseline

Research was completed on 2026-08-05 against:

- Telegram Bot API 10.2 documentation;
- Agent Skills specification as published on 2026-08-05;
- ASD-STE100 Issue 9 public information;
- Eve commit `e5c91918ed898f72047d2a1e33902cbb9db3e452`;
- Iva commit `b3544a2c19341a2231353b2942905748bf391751`;
- Hermes Agent commit `6564f319a647b47de391cab2f608660323804a2b`;
- humanizer-ru commit `91f70df11f7fb30722e6fcf18803d402e2d86a53`.

See `references/sources.md` for links and review notes.
