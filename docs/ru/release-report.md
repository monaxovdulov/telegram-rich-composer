# Отчет о выпуске 0.1.0

[English version](../en/release-report.md)

Дата выпуска: 2026-08-05. Репозиторий: [monaxovdulov/telegram-rich-composer](https://github.com/monaxovdulov/telegram-rich-composer).

## Результат

- переносимый Agent Skill `telegram-rich-composer`;
- независимый Python package и CLI;
- `CompositionSpec` 1.0, renderer, semantic validator, capability negotiation и fallback contract;
- материалы для Eve, Iva, Hermes, прямого Bot API, CLI и stdio;
- двенадцать сложных паттернов, три пресета и selection evals;
- парные документы на английском и русском, редакционный checklist и visual QA matrix;
- CI, security workflow, package build, проверки парности документов и локальных ссылок, unit, golden и safety tests.

## Отличия от прототипа

Изученный локальный `telegram-rich-publisher` является редактором и publishing bot, связанным с локальным состоянием. Новый проект работает как compiler смысловой спецификации и переносимый skill без получателя внутри контента. Он добавляет ситуационный выбор plain/rich, публичную схему, атомарные возможности, границы адаптеров, осторожную защиту от дублей, двуязычные визуальные правила и переносимые fixtures. Код прототипа не копировался, поскольку в изученной папке не было лицензии.

## Известные ограничения

- Автоматические tests не заменяют ручной visual QA на Android, iOS и Desktop.
- В изученной версии Eve нет native Rich Message transport, поэтому sample использует ограниченный raw request или CLI/MCP bridge.
- Harness API может измениться после commits, указанных в `references/sources.md`.
- Direct adapter выполняет один request и сообщает о неизвестном результате. Reconciliation и durable idempotency принадлежат host.
- Rich Markdown и HTML fallback намеренно упрощают часть семантики explicit blocks.
