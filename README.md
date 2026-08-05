# Telegram Rich Composer

[Read in Russian](README.ru.md)

Telegram Rich Composer builds structured replies for Telegram bots and AI agents. A reply can contain tables, expandable sections, maps, galleries, audio, and other Rich Message blocks.

The project also checks whether a rich layout is useful. Short replies stay as normal Telegram messages.

Telegram added [Rich Messages](https://core.telegram.org/bots/api#rich-messages) in Bot API 10.1. Bot API 10.2 added explicit input blocks. This project supports the documented Bot API 10.2 format.

## When to use it

| Your reply | Recommended format |
|---|---|
| A short answer, confirmation, or link | Plain message |
| A comparison or compact set of values | Table or short sections |
| A tutorial or ordered process | List or slideshow |
| A report with optional evidence | Headings and expandable details |
| A place, route, or field observation | Map and captioned media |
| A visual story or product showcase | Gallery, slideshow, or a preset |

Rich formatting should make the answer easier to scan. Use a plain message when structure does not help.

## What the project provides

- An Agent Skill that tells an AI agent when to use a plain or rich reply.
- `CompositionSpec`, a JSON format that describes content without a bot token or recipient.
- A validator for the schema, Telegram limits, media references, and safety rules.
- A renderer for Rich Message blocks, Rich Markdown, Rich HTML, and plain fallbacks.
- A command-line tool and a Python API.
- Integration guides for direct Bot API use, Eve, Iva, and Hermes Agent.

This project is not a bot framework. It does not receive Telegram updates or store conversations. Your bot or agent remains responsible for those tasks.

## Quick start

You need Git and Python 3.11 or newer.

```bash
git clone https://github.com/monaxovdulov/telegram-rich-composer.git
cd telegram-rich-composer
python3 -m venv .venv
.venv/bin/python -m pip install -e .
```

Validate a complete example. This command does not contact Telegram.

```bash
.venv/bin/trc validate examples/golden/ticket-table.json
```

The result must contain `"valid": true`. Now render the same example as a Bot API payload.

```bash
.venv/bin/trc render examples/golden/ticket-table.json \
  --target rich_blocks > rendered.json
```

You can inspect `rendered.json` before you connect a bot.

## Ways to use it

### As an Agent Skill

Place the repository in the skill directory used by your agent. The directory must include `SKILL.md`, `references/`, and `schemas/`.

Install the Python package from the same directory if the agent will call `trc`. The skill keeps normal chat plain and selects rich mode only when the reply needs structure or semantic media.

See [SKILL.md](SKILL.md) for the workflow. See the [adapter guide](docs/en/adapters.md) for Eve, Iva, Hermes Agent, and direct Bot API setup.

### From the command line

| Command | Purpose |
|---|---|
| `trc select context.json` | Choose a plain or rich reply. |
| `trc validate spec.json` | Check a specification before use. |
| `trc render spec.json --target rich_blocks` | Build a Rich Message payload. |
| `trc plan spec.json --capability rich_blocks` | Select a supported delivery format. |
| `trc request spec.json --chat-id ID` | Build a request without sending it. |
| `trc send spec.json --chat-id ID --yes` | Send one request to Telegram. |

Run `trc COMMAND --help` for all options.

### From Python

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

### With the direct Bot API

The command reads the bot token from the environment. The specification does not contain the token or chat ID.

```bash
export TELEGRAM_BOT_TOKEN='your-bot-token'
.venv/bin/trc send examples/golden/ticket-table.json \
  --chat-id "$TRUSTED_CHAT_ID" --yes
```

Your application must take the chat ID from the active Telegram conversation or an allowlist. Use `--media-root /allowed/path` when a specification refers to a local file.

## Start from an example

The files in [`examples/golden/`](examples/golden/) are valid specifications that you can copy and edit.

| Example | Use it for |
|---|---|
| [`ticket-table.json`](examples/golden/ticket-table.json) | Compact values, schedules, and comparisons |
| [`map-cover.json`](examples/golden/map-cover.json) | A place, route, or field report |
| [`museum-drawers.json`](examples/golden/museum-drawers.json) | A product, exhibit, or object with optional details |
| [`manual-animation.json`](examples/golden/manual-animation.json) | Ordered visual steps |
| [`hidden-sound-note.json`](examples/golden/hidden-sound-note.json) | Optional audio with a clear label |
| [`preset-issue.json`](examples/golden/preset-issue.json) | A long article or research note |
| [`preset-artifact.json`](examples/golden/preset-artifact.json) | A visual object card |
| [`preset-scene.json`](examples/golden/preset-scene.json) | A visual story |

The [composition catalog](references/composition-patterns.md) explains every included pattern.

## Safety rules

- Validate every specification before delivery.
- Keep the bot token and recipient outside `CompositionSpec`.
- Do not send a second message after a timeout or an unknown result. Check Telegram state first.
- Allow local files only from directories that your application controls.
- Test visual output on the Telegram clients that your users have.

## Documentation

- [CompositionSpec fields](docs/en/composition-spec.md)
- [Visual and editorial rules](docs/en/visual-system.md)
- [Adapter setup](docs/en/adapters.md)
- [Architecture and safety boundaries](docs/en/architecture.md)
- [Test plan](docs/en/test-plan.md)
- [Current visual QA matrix](docs/en/visual-qa-matrix.md)
- [Contributing](CONTRIBUTING.md) and [security policy](SECURITY.md)

Automated tests cover validation, rendering, selection, and delivery safeguards. Check the visual QA matrix before you claim support for a specific Telegram client.

## License

[MIT](LICENSE)
