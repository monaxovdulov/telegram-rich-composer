# Telegram Rich Composer

[English version](README.md)

Telegram Rich Composer помогает AI-агенту собирать понятные ответы для Telegram. Вывод и следующий шаг идут первыми. Подробности раскрываются по разделам. Для сравнений, маршрутов и иллюстраций используются таблицы, карты и медиа.

## Как выглядит ответ Hermes

Hermes уже поддерживает [Rich Messages из Telegram Bot API](https://core.telegram.org/bots/api#rich-message-formatting-options). Skill задаёт структуру ответа:

> Коротко: запуск можно продолжать. Сначала перепроверьте удержание новых пользователей.
>
> Индекс: 1. Основание · 2. Что сделать · 3. Риски

<details>
<summary>1. Основание</summary>

Две основные метрики выросли. Выборка по удержанию пока мала.

</details>

<details>
<summary>2. Что сделать</summary>

Повторить замер на полной неделе и назначить ответственного за проверку.

</details>

<details>
<summary>3. Риски</summary>

Если удержание не подтвердится, отложить широкий запуск и оставить текущую группу пользователей.

</details>

Главное видно сразу. Каждый раздел раскрывается отдельно.

[Отправьте Hermes готовое задание](docs/ru/hermes-quickstart.md), чтобы установить skill и проверить такой ответ.

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

- AI-агент читает [SKILL.md](SKILL.md) и выбирает подходящую структуру сообщения.
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
