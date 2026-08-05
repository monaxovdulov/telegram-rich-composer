# telegram-rich-composer

Переносимый Agent Skill и Python-инструментарий для выбора между обычным ответом в Telegram и нативным Rich Message. Проект включает независимый от агента `CompositionSpec`, валидацию, согласование возможностей, renderer, безопасный fallback и адаптеры для Eve, Iva, Hermes, прямого Bot API, CLI и MCP-подобного stdio-интерфейса.

По умолчанию ответ остается спокойным: обычный диалог получает простой текст. Rich mode подходит для сравнений, отчетов, инструкций, смысловых медиа, плотного справочного материала и явного запроса пользователя.

## Быстрый старт

```bash
python3 -m venv .venv
.venv/bin/pip install -e '.[dev]'
.venv/bin/trc validate examples/golden/comparison-matrix.json
.venv/bin/trc render examples/golden/comparison-matrix.json --target rich_blocks
```

В спецификации есть контент и намерение доставки, но нет токена и получателя. Доверенный адаптер добавляет текущие `chat_id`, тему и сообщение для ответа:

```bash
TELEGRAM_BOT_TOKEN=... .venv/bin/trc send composition.json \
  --chat-id "$TRUSTED_CHAT_ID" --reply-to "$TRUSTED_MESSAGE_ID" --yes
```

Для локальных вложений укажите `--media-root /controlled/path`. Файл должен находиться внутри разрешенного корня. Проект не публикует его на стороннем хостинге.

## Состав проекта

- `SKILL.md`: переносимый рабочий процесс
- `schemas/`: JSON Schema для `CompositionSpec` 1.0
- `src/`: selector, validator, renderer, negotiation, прямой адаптер и CLI
- `scripts/mcp_stdio.py`: stdio-интерфейс без отдельной зависимости
- `adapters/`: инструкции для Eve, Iva, Hermes и прямого подключения
- `examples/golden/`: 12 композиционных паттернов и 3 showcase-пресета
- `docs/en` и `docs/ru`: парные документы по архитектуре, визуальной системе, адаптерам и тестированию

Подробнее: [архитектура](docs/ru/architecture.md), [визуальная система](docs/ru/visual-system.md), [каталог паттернов](references/composition-patterns.ru.md) и [источники](references/sources.md).

## Контракт безопасности

Валидация выполняется до доставки. После постоянного отказа из-за синтаксиса или отсутствующей возможности адаптер может перейти к следующему варианту fallback. При timeout, обрыве соединения или неизвестном результате отправка останавливается до сверки состояния. Автоматическая повторная отправка в такой ситуации способна создать дубликат.

## Статус и границы

Реализация ориентирована на документированный Bot API 10.2. Telegram-специфичные поля изолированы в renderer и адаптерах. Код написан независимо, распространяется по лицензии MIT и не копирует код изученного локального прототипа.

## Лицензия

[MIT](LICENSE)
