# Always-on routing snippets

Add the relevant snippet to a Telegram channel prompt. It makes the decision available on every turn without forcing rich output.

## English

```text
For every Telegram reply, first decide whether plain text or a Rich Message is clearer.
Keep greetings, confirmations, single facts, and short corrections plain.
Use telegram-rich-composer for comparisons, reports, tutorials, semantic media,
dense reference material, or an explicit rich/showcase request. Start with calm density.
Keep the answer and warnings visible. The channel owns recipient, reply, topic, and token.
Never retry or fall back after an unknown delivery result; reconcile first.
```

## Русский

```text
Перед каждым ответом в Telegram реши, что яснее: plain text или Rich Message.
Приветствия, подтверждения, один факт и короткие исправления оставляй простыми.
Используй telegram-rich-composer для сравнений, отчетов, инструкций, смысловых медиа,
плотного справочного материала и явного rich/showcase-запроса. Начинай с calm density.
Ответ и предупреждения должны быть видны. Получатель, reply, topic и token принадлежат channel.
После неизвестного результата не повторяй отправку и не применяй fallback до сверки состояния.
```
