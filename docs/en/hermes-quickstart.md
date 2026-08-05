# Hermes: setup without terminal experience

[Русская версия](../ru/hermes-quickstart.md)

Use this path when Hermes already replies to you in Telegram. You give a prepared task to an agent. The agent checks the installation, changes one setting, and prepares a test.

The first trial uses a small Hermes-specific skill. It works through the native Telegram adapter. You do not need the Python package or the optional third-party plugin yet.

## What changes in a reply

Short replies remain normal text. For a long reply, Hermes can keep the conclusion and next action at the top, add a short index, and put evidence, comparisons, and risks in collapsible sections.

Warnings and required actions always remain visible.

## Task for your agent

Send the text below to Hermes or to another coding agent that has access to the computer that runs Hermes.

```text
Connect the Telegram Rich Composer skill to my active Hermes profile.

Source:
https://github.com/monaxovdulov/telegram-rich-composer

Goal:
Keep short Telegram replies as normal messages. For a long reply, show the conclusion and next action first. Then add a one-line numbered index. Put evidence, comparisons, and risks in separate collapsible <details> sections.

Check the environment first:
1. Identify the active Hermes profile and its HERMES_HOME. Do not assume that it is always ~/.hermes.
2. Check the Hermes version and confirm that `hermes skills inspect` and `hermes skills install` are available.
3. Inspect the skill before installation:
   hermes skills inspect monaxovdulov/telegram-rich-composer/skills/telegram-rich-composer
4. If the command is unavailable or the security scan blocks installation, stop and explain the reason. Do not use --force without my permission.

Then install and verify the skill:
1. Run:
   hermes skills install monaxovdulov/telegram-rich-composer/skills/telegram-rich-composer --yes
2. Use `hermes skills list` to confirm that telegram-rich-composer is installed.
3. Do not enable the third-party plugin or install the Python package for this first test. Use the native Hermes Telegram Rich Message transport.

Enable Rich Messages carefully:
1. Find config.yaml for the active profile and create a backup beside it.
2. Preserve all existing settings. Add or update only these fields:

   gateway:
     platforms:
       telegram:
         extra:
           rich_messages: true
           rich_drafts: false

3. Do not print or change the Telegram token, allowlists, chat ID, topic ID, or other secrets.
4. Validate the final YAML. If a gateway restart is safe and the session can continue, run `hermes gateway restart`. Otherwise, stop and tell me the one action that I must complete.

After installation, report:
- the profile and config.yaml path that you used;
- the skill installation path;
- the two configuration fields that changed;
- whether the gateway restarted;
- the rollback steps.
```

Hermes scans this skill as a third-party source. The task permits automatic installation only after the agent confirms the repository `monaxovdulov/telegram-rich-composer`. It must stop if the source is different.

## First Telegram test

After the restart, send this message to Hermes:

```text
Use Telegram Rich Composer.

Assume that we have three facts before a product launch:
- conversion increased from 4.1% to 5.0%;
- the error count did not change;
- retention covers only two days.

Start with the decision and next action in no more than three lines. Then add a one-line index. Put the evidence, validation plan, and risks in three separate collapsible sections. Do not hide a warning or required action.
```

The decision, next action, and index must remain at the top. Three sections appear below them and can be opened separately.

## If sections do not collapse

Ask the agent to check these items:

1. Hermes is current and supports Telegram Rich Messages.
2. The setting is at the exact path `gateway.platforms.telegram.extra.rich_messages`.
3. The gateway restarted after the `config.yaml` change.
4. The Telegram client is current.

Hermes keeps Rich Messages disabled by default because Telegram clients can render them differently. Keep `rich_drafts` disabled for the first test. If Telegram rejects a Rich Message, Hermes must use a readable fallback and must not resend after an unknown network result.

See the [official Hermes Telegram guide](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/telegram/) for current limitations.

## Roll back

Ask the agent to uninstall `telegram-rich-composer`, set `rich_messages: false`, and restart the gateway. Use the `config.yaml` backup only if the agent changed adjacent settings by mistake.

For `CompositionSpec` validation, the Python API, or the plugin, continue with the [full adapter guide](adapters.md).
