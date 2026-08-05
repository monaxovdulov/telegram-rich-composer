---
name: telegram-rich-composer
description: Compose, validate, render, and safely deliver situational Telegram replies as either concise plain messages or Bot API Rich Messages. Use for Telegram agent responses, structured reports, comparisons, tutorials, media compositions, previews, fallback design, or Eve, Iva, Hermes, direct Bot API, CLI, and MCP integrations.
---

# Telegram Rich Composer

Create one semantic `CompositionSpec`; keep the recipient, bot token, current reply ID, and topic ID in trusted adapter context.

## Workflow

1. Read [references/composition-patterns.md](references/composition-patterns.md), or [references/composition-patterns.ru.md](references/composition-patterns.ru.md) for Russian work.
2. Call `select_composition(context)` or `trc select context.json`. Keep ordinary conversational answers plain. Choose rich only when structure, semantic media, high information density, or an explicit user request improves the answer.
3. Build a spec against [schemas/composition-spec.schema.json](schemas/composition-spec.schema.json). Start with `calm`; use `showcase` only on explicit request.
4. Validate with `trc validate spec.json`. Treat every error as blocking. Review warnings instead of suppressing them blindly.
5. Negotiate adapter capabilities with `trc plan`. Prefer `rich_blocks`, then a supported rich text mode, then standard Telegram text or a plain album.
6. Render with `trc render spec.json --target rich_blocks`. The renderer owns Telegram field-name conversion.
7. Let the adapter bind trusted conversation context and deliver. Never take `chat_id` or a token from the spec. Never retry or fall back after a timeout or an unknown delivery result; stop and reconcile first.
8. Run the editorial and visual QA checks in [docs/en/visual-system.md](docs/en/visual-system.md) or [docs/ru/visual-system.md](docs/ru/visual-system.md).

## Non-negotiable rules

- Preserve the user's language and intent; decoration must clarify, not compete.
- Do not upload local media to anonymous public hosts. Permit files only below adapter-configured roots and use controlled multipart upload.
- Keep group replies calmer than private replies unless the user asks for a showcase.
- Use `thinking` only for private rich drafts. A draft is temporary; finalize it with a persistent message.
- Use buttons only for a real choice or action, never as ornament.
- Keep the fallback ladder explicit and accept feature loss only when the spec allows it.

## Integration routing

- For architecture and guarantees, read [docs/en/architecture.md](docs/en/architecture.md).
- For field semantics, read [docs/en/composition-spec.md](docs/en/composition-spec.md) and the canonical JSON Schema.
- For Eve, Iva, Hermes, direct Bot API, CLI, and MCP setup, read [docs/en/adapters.md](docs/en/adapters.md) and the matching `adapters/` directory.
- For a skill-only Hermes trial, use [skills/telegram-rich-composer/SKILL.md](skills/telegram-rich-composer/SKILL.md) and [docs/en/hermes-quickstart.md](docs/en/hermes-quickstart.md).
- For per-turn channel prompting, use [references/always-on-routing.md](references/always-on-routing.md).
- For test and release gates, read [docs/en/test-plan.md](docs/en/test-plan.md).
- For official and inspected-source provenance, read [references/sources.md](references/sources.md).

This project is original MIT-licensed code. Its Agent Skills guidance follows public specification principles; it does not claim specification certification or full Agent Skills Design conformance.
