# Getting started

[Русская версия](../ru/getting-started.md)

This guide covers local setup, the command-line tool, the Python API, Agent Skill use, and direct delivery.

## Install from the repository

You need Git and Python 3.11 or newer. The commands below use macOS and Linux paths.

```bash
git clone https://github.com/monaxovdulov/telegram-rich-composer.git
cd telegram-rich-composer
python3 -m venv .venv
.venv/bin/python -m pip install -e .
```

On Windows, the executables are in a different directory. Use `.venv\Scripts\python` and `.venv\Scripts\trc`.

## Run a local check

Validate a complete specification.

```bash
.venv/bin/trc validate examples/golden/ticket-table.json
```

If the result contains `"valid": true`, Composer found no errors in the file. Render the same file as a Telegram Rich Message payload.

```bash
.venv/bin/trc render examples/golden/ticket-table.json \
  --target rich_blocks > rendered.json
```

These commands do not use a bot token and do not contact Telegram.

## Command-line reference

| Command | Purpose |
|---|---|
| `trc select context.json` | Choose a plain or rich reply. |
| `trc validate spec.json` | Check a specification. |
| `trc render spec.json --target rich_blocks` | Build a Rich Message payload. |
| `trc plan spec.json --capability rich_blocks` | Choose a supported delivery format. |
| `trc request spec.json --chat-id ID` | Build a request without sending it. |
| `trc send spec.json --chat-id ID --yes` | Send one request to Telegram. |

Run `trc COMMAND --help` for all options.

## Use the Python API

```python
import json
from pathlib import Path

from telegram_rich_composer import render, validate_spec

spec = json.loads(Path("examples/golden/ticket-table.json").read_text(encoding="utf-8"))
report = validate_spec(spec)
if not report.valid:
    raise ValueError(report.as_dict()["issues"])

payload = render(spec, "rich_blocks").as_dict()
```

Use `select_composition()` when your application must choose between plain and rich output. Use `negotiate()` when an adapter supports only part of the Rich Message format.

## Use it as an Agent Skill

Place the repository in the skill directory used by your agent. Keep `SKILL.md`, `references/`, and `schemas/` together.

Install the Python package from the same directory if the agent will call `trc`. The skill keeps normal chat plain. It selects rich mode when structure or media improves the reply.

## Send through the direct Bot API

The command reads the bot token from the environment. The specification does not contain the token or chat ID.

```bash
export TELEGRAM_BOT_TOKEN='your-bot-token'
.venv/bin/trc send examples/golden/ticket-table.json \
  --chat-id "$TRUSTED_CHAT_ID" --yes
```

Take the chat ID from the active Telegram conversation or an allowlist. Use `--media-root /allowed/path` when a specification refers to a local file.

The package targets the Rich Message format documented in Telegram Bot API 10.2. Read the [adapter guide](adapters.md) before you add delivery to an existing bot.
