# Telegram Rich Composer

[English version](README.md)

Если бот отвечает «Готово» или присылает одну ссылку, обычного текста достаточно. Сложности начинаются с четырёх тарифов, длинного отчёта или маршрута: смысл теряется в простыне текста.

Telegram Rich Composer собирает такие ответы в [Rich Message](https://core.telegram.org/bots/api#rich-messages) с таблицей, сворачиваемыми разделами, картой или медиа. Короткие ответы он не трогает.

## Что выбрать

| Что нужно отправить | С чего начать |
|---|---|
| Один факт, подтверждение или ссылка | Обычный текст |
| Значения или наглядное сравнение | Таблица |
| Инструкция или отчёт | Списки, заголовки и сворачиваемые разделы |
| Место или визуальная история | Карта, галерея или слайд-шоу |

## Проверить за минуту

Понадобятся Git и Python 3.11 или новее.

Проверка и сборка примера проходят на вашем компьютере, без токена бота и запросов к Telegram.

```bash
git clone https://github.com/monaxovdulov/telegram-rich-composer.git
cd telegram-rich-composer
python3 -m venv .venv
.venv/bin/python -m pip install -e .
.venv/bin/trc validate examples/golden/ticket-table.json
.venv/bin/trc render examples/golden/ticket-table.json --target rich_blocks
```

Если проверка вернула `"valid": true`, всё работает. Последняя команда покажет готовый JSON.

## Как подключить

- AI-агент читает [SKILL.md](SKILL.md) и выбирает между обычным сообщением и Rich Message.
- Для Python и терминала есть [инструкция по запуску](docs/ru/getting-started.md).
- Для готового бота есть [инструкция по адаптерам](docs/ru/adapters.md). Она охватывает прямой Bot API, Eve, Iva и Hermes Agent.

Composer только готовит сообщение. Ваш бот отвечает за отправку и, если нужно, за хранение диалога.

## Готовые примеры

Не начинайте с пустого JSON. Возьмите ближайший пример и переделайте под себя.

- [`ticket-table.json`](examples/golden/ticket-table.json) для значений и сравнений
- [`map-cover.json`](examples/golden/map-cover.json) для места или маршрута
- [`manual-animation.json`](examples/golden/manual-animation.json) для наглядных шагов
- [`preset-issue.json`](examples/golden/preset-issue.json) для длинной статьи

Остальные примеры лежат в [`examples/golden/`](examples/golden/). [Каталог композиций](references/composition-patterns.ru.md) подскажет, когда брать каждый из них.

## Перед отправкой

- Проверьте спецификацию.
- Храните токен бота и номер чата вне `CompositionSpec`.
- После тайм-аута или неизвестного результата проверьте Telegram перед новой отправкой.

Дальше можно открыть [поля сообщения](docs/ru/composition-spec.md), [правила оформления](docs/ru/visual-system.md), [безопасность](SECURITY.md) или [участие в разработке](CONTRIBUTING.md).

## Лицензия

[MIT](LICENSE)
