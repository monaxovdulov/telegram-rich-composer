# Telegram Rich Composer

[Русская версия](README.ru.md)

Telegram Rich Composer helps AI agents build clear Telegram replies. The conclusion and next step come first. Details open by section. Tables, maps, and media support comparisons, routes, and visual explanations.

## A layered Hermes reply

Hermes already supports [Rich Messages](https://core.telegram.org/bots/api#rich-messages). The skill defines the reply structure:

> Short answer: Continue the launch. First, check new-user retention again.
>
> Index: 1. Evidence · 2. Next step · 3. Risks

<details>
<summary>1. Evidence</summary>

Two primary metrics improved. The retention sample is still small.

</details>

<details>
<summary>2. Next step</summary>

Repeat the measurement for a complete week and assign an owner for the check.

</details>

<details>
<summary>3. Risks</summary>

If retention does not improve, delay the broad launch and keep the current user group.

</details>

The answer is visible before any tap. Each supporting section opens in place.

[Give Hermes this prepared task](docs/en/hermes-quickstart.md) to install the skill and test a reply.

## Choose a format

| You need to send | Best starting point |
|---|---|
| One fact, confirmation, or link | Plain text |
| Values or a side-by-side comparison | Table |
| A tutorial or report | Lists, headings, and details |
| A place or visual story | Map, gallery, or slideshow |

## Try it in one minute

You need Git and Python 3.11 or newer.

Validation and rendering run on your computer. They do not need a bot token or contact Telegram.

```bash
git clone https://github.com/monaxovdulov/telegram-rich-composer.git
cd telegram-rich-composer
python3 -m venv .venv
.venv/bin/python -m pip install -e .
.venv/bin/trc validate examples/golden/ticket-table.json
.venv/bin/trc render examples/golden/ticket-table.json --target rich_blocks
```

If validation prints `"valid": true`, the setup works. The last command shows the rendered JSON.

## Choose how to use it

- AI agents read [SKILL.md](SKILL.md) to choose a suitable message structure.
- Python and command-line users can follow the [getting started guide](docs/en/getting-started.md).
- Bot maintainers can use the [adapter guide](docs/en/adapters.md) for the direct Bot API, Eve, Iva, or Hermes Agent.

Composer only prepares the message. Your bot handles delivery and, if needed, conversation storage.

## Start from a working example

Do not start with an empty JSON file. Copy the closest example and change it for your reply.

- [`ticket-table.json`](examples/golden/ticket-table.json) for values and comparisons
- [`map-cover.json`](examples/golden/map-cover.json) for a place or route
- [`manual-animation.json`](examples/golden/manual-animation.json) for ordered visual steps
- [`preset-issue.json`](examples/golden/preset-issue.json) for a long article

The other examples are in [`examples/golden/`](examples/golden/). The [pattern catalog](references/composition-patterns.md) explains when each one works well.

## Before you send

- Validate every specification.
- Keep the bot token and chat ID outside `CompositionSpec`.
- After a timeout or unknown result, check Telegram state before another send.

Continue with [message fields](docs/en/composition-spec.md), [visual rules](docs/en/visual-system.md), [security](SECURITY.md), or [contributing](CONTRIBUTING.md).

## License

[MIT](LICENSE)
