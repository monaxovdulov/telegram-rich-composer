# telegram-rich-composer

A portable Agent Skill and Python toolkit for choosing when a Telegram answer should stay plain and when it benefits from a native Rich Message. It provides a harness-independent `CompositionSpec`, validation, capability negotiation, rendering, safe fallback, and adapters for Eve, Iva, Hermes, direct Bot API, CLI, and MCP-style stdio use.

The default is deliberately quiet: ordinary chat stays plain. Rich mode is reserved for comparisons, reports, tutorials, semantic media, dense reference material, or an explicit request.

## Quick start

```bash
python3 -m venv .venv
.venv/bin/pip install -e '.[dev]'
.venv/bin/trc validate examples/golden/comparison-matrix.json
.venv/bin/trc render examples/golden/comparison-matrix.json --target rich_blocks
```

The spec contains content and delivery intent but never a bot token or recipient. A trusted adapter supplies the active `chat_id`, topic, and reply target:

```bash
TELEGRAM_BOT_TOKEN=... .venv/bin/trc send composition.json \
  --chat-id "$TRUSTED_CHAT_ID" --reply-to "$TRUSTED_MESSAGE_ID" --yes
```

Use `--media-root /controlled/path` for local attachments. No local file may escape those roots, and the project never uploads files to public hosting.

## What is included

- `SKILL.md`: portable skill workflow
- `schemas/`: JSON Schema for `CompositionSpec` 1.0
- `src/`: selector, validator, renderer, negotiation, direct request builder, CLI
- `scripts/mcp_stdio.py`: dependency-free stdio tool bridge
- `adapters/`: Eve, Iva, Hermes, and direct integration guidance
- `examples/golden/`: 12 composition patterns and 3 showcase presets
- `docs/en` and `docs/ru`: mirrored architecture, visual system, adapters, and test plan

See [Russian README](README.ru.md), [architecture](docs/en/architecture.md), [visual system](docs/en/visual-system.md), and [sources](references/sources.md).

## Safety contract

Validation happens before delivery. Permanent capability or syntax rejection may advance to the next declared fallback. Timeout, connection loss, or any unknown result must stop delivery and trigger reconciliation, because automatic resend can duplicate a message.

## Status and scope

Telegram Rich Messages arrived in Bot API 10.1 and explicit input blocks in 10.2. This repository targets the documented 10.2 surface while keeping Telegram-specific field names in the renderer and adapters. It is an independent MIT-licensed implementation and does not copy code from the inspected local prototype.

## License

[MIT](LICENSE)
