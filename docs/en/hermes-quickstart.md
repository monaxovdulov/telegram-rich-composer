# Hermes: agent-led setup

[Русская версия](../ru/hermes-quickstart.md)

Hermes supports Telegram Rich Messages. This task installs a skill that shapes replies with a short conclusion, a next step, an index, and collapsible details.

## Install

Send this text to Hermes or an agent with access to its computer:

```text
Install Telegram Rich Composer in the active Hermes profile.

Source:
https://github.com/monaxovdulov/telegram-rich-composer/tree/main/skills/telegram-rich-composer

Workflow:
1. Identify the active Hermes profile.
2. Inspect the skill and install it with the standard Hermes command.
3. Ensure that gateway.platforms.telegram.extra.rich_messages in config.yaml is true.
4. Before changing config.yaml, create a backup. Then validate the YAML and restart the gateway.
5. Preserve every other setting and all secrets.
6. Report the installation result and readiness for the test.

If an error occurs, stop and state the one action I need to take.
```

## Test

Send this message to Hermes:

```text
Use Telegram Rich Composer.

Three facts are known before a product launch:
- conversion increased from 4.1% to 5.0%;
- the error count stayed the same;
- retention has two days of data.

Give the decision and next step in the first three lines. Then add a one-line index. Put the evidence, validation plan, and risks in separate collapsible sections. Keep warnings and required actions visible.
```

The result starts with the decision, next step, and index. Three collapsible sections follow.

If the sections appear as plain text, ask the agent to check `gateway.platforms.telegram.extra.rich_messages` and restart the gateway.

The [full integration guide](adapters.md) covers the other connection paths.
