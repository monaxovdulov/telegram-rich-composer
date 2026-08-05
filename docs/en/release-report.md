# Release report 0.1.0

[Русская версия](../ru/release-report.md)

Release date: 2026-08-05. Repository: [monaxovdulov/telegram-rich-composer](https://github.com/monaxovdulov/telegram-rich-composer).

## Delivered

- portable `telegram-rich-composer` Agent Skill;
- independent Python package and CLI;
- `CompositionSpec` 1.0, renderer, semantic validator, capability negotiation, and fallback contract;
- Eve, Iva, Hermes, direct Bot API, CLI, and stdio integration material;
- twelve advanced patterns, three presets, and selection evals;
- paired English and Russian documentation, editorial checklist, and visual QA matrix;
- CI, security workflow, package build, docs parity, local-link checks, and unit/golden/safety tests.

## Prototype differences

The inspected local `telegram-rich-publisher` is an editor and publishing bot tied to local state. This project is a recipient-free semantic compiler and skill. It adds situational plain/rich selection, a public schema, atomic capabilities, adapter boundaries, conservative duplicate prevention, bilingual design guidance, and portable test fixtures. No prototype source was copied because the inspected directory had no license.

## Known limitations

- Automated tests do not replace manual Android, iOS, and Desktop visual QA.
- Eve's inspected baseline has no native Rich Message transport, so its sample requires a constrained raw request or CLI/MCP bridge.
- Harness APIs can change after the pinned commits in `references/sources.md`.
- The direct adapter performs one request and exposes unknown-result state; reconciliation and durable idempotency belong to the host.
- Rich Markdown and HTML fallbacks intentionally flatten some explicit-block semantics.
