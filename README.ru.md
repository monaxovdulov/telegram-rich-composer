# Telegram Rich Composer

[English version](README.md)

Telegram Rich Composer собирает структурированные ответы для Telegram-ботов и AI-агентов. В ответ можно добавить таблицу, сворачиваемые разделы, карту, галерею, аудио и другие блоки Rich Message.

Проект также проверяет, нужен ли ответу сложный формат. Короткая реплика остаётся обычным сообщением Telegram.

Telegram добавил [Rich Messages](https://core.telegram.org/bots/api#rich-messages) в Bot API 10.1. В Bot API 10.2 появились явные блоки для отправки. Проект поддерживает документированный формат Bot API 10.2.

## Когда это пригодится

| Ответ | Подходящий формат |
|---|---|
| Короткий ответ, подтверждение или ссылка | Обычное сообщение |
| Сравнение или набор значений | Таблица или короткие разделы |
| Инструкция по шагам | Список или слайд-шоу |
| Отчёт с дополнительными материалами | Заголовки и сворачиваемые разделы |
| Место, маршрут или полевое наблюдение | Карта и медиа с подписями |
| Визуальная история или показ продукта | Галерея, слайд-шоу или готовый шаблон |

Сложное оформление должно упрощать чтение. Если структура не помогает, отправьте обычное сообщение.

## Что есть в проекте

- Agent Skill с правилами выбора между обычным и структурированным ответом.
- `CompositionSpec` - JSON-формат с содержанием сообщения. В нём нет токена бота и получателя.
- Проверка схемы, лимитов Telegram, ссылок на медиа и правил безопасности.
- Сборка Rich Message blocks, Rich Markdown, Rich HTML и обычного запасного варианта.
- Команды для терминала и Python API.
- Инструкции для прямого Bot API, Eve, Iva и Hermes Agent.

Это библиотека и набор правил для агента. Проект не запускает бота, не читает обновления Telegram и не хранит диалоги. Эти задачи остаются в вашем приложении.

## Быстрый старт

Понадобятся Git и Python 3.11 или новее.

```bash
git clone https://github.com/monaxovdulov/telegram-rich-composer.git
cd telegram-rich-composer
python3 -m venv .venv
.venv/bin/python -m pip install -e .
```

Проверьте готовый пример. Команда не обращается к Telegram.

```bash
.venv/bin/trc validate examples/golden/ticket-table.json
```

В результате должно быть `"valid": true`. Теперь соберите данные для запроса к Bot API.

```bash
.venv/bin/trc render examples/golden/ticket-table.json \
  --target rich_blocks > rendered.json
```

Файл `rendered.json` можно изучить до подключения бота.

## Варианты подключения

### Как Agent Skill

Поместите репозиторий в папку навыков вашего агента. Внутри должны остаться `SKILL.md`, `references/` и `schemas/`.

Установите Python-пакет из той же папки, если агент будет вызывать `trc`. Навык оставляет обычный разговор без сложного оформления. Структурированный формат включается для таблиц, отчётов, инструкций и смысловых медиа.

Рабочий процесс описан в [SKILL.md](SKILL.md). Подключение к Eve, Iva, Hermes Agent и прямому Bot API описано в [руководстве по адаптерам](docs/ru/adapters.md).

### Из терминала

| Команда | Результат |
|---|---|
| `trc select context.json` | Выбор обычного или структурированного ответа |
| `trc validate spec.json` | Проверка спецификации перед использованием |
| `trc render spec.json --target rich_blocks` | Готовые данные Rich Message |
| `trc plan spec.json --capability rich_blocks` | Выбор доступного формата отправки |
| `trc request spec.json --chat-id ID` | Сборка запроса без отправки |
| `trc send spec.json --chat-id ID --yes` | Одна отправка в Telegram |

Полный список параметров выводит команда `trc КОМАНДА --help`.

### Из Python

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

Функция `select_composition()` выбирает между обычным и структурированным ответом. Функция `negotiate()` нужна, когда адаптер поддерживает часть формата Rich Message.

### Через прямой Bot API

Команда читает токен бота из переменной окружения. В спецификации нет токена и номера чата.

```bash
export TELEGRAM_BOT_TOKEN='your-bot-token'
.venv/bin/trc send examples/golden/ticket-table.json \
  --chat-id "$TRUSTED_CHAT_ID" --yes
```

Приложение должно брать номер чата из текущего разговора Telegram или из списка разрешённых получателей. Параметр `--media-root /allowed/path` разрешает локальные файлы из указанной папки.

## Готовые примеры

Файлы в папке [`examples/golden/`](examples/golden/) можно копировать и менять под свою задачу.

| Пример | Для чего подходит |
|---|---|
| [`ticket-table.json`](examples/golden/ticket-table.json) | Компактные значения, расписания и сравнения |
| [`map-cover.json`](examples/golden/map-cover.json) | Место, маршрут или полевой отчёт |
| [`museum-drawers.json`](examples/golden/museum-drawers.json) | Товар, экспонат или предмет с дополнительными сведениями |
| [`manual-animation.json`](examples/golden/manual-animation.json) | Последовательность наглядных шагов |
| [`hidden-sound-note.json`](examples/golden/hidden-sound-note.json) | Необязательное аудио с понятной подписью |
| [`preset-issue.json`](examples/golden/preset-issue.json) | Длинная статья или исследовательская заметка |
| [`preset-artifact.json`](examples/golden/preset-artifact.json) | Карточка предмета с изображением |
| [`preset-scene.json`](examples/golden/preset-scene.json) | Визуальная история |

[Каталог композиций](references/composition-patterns.ru.md) объясняет все примеры из проекта.

## Правила безопасности

- Проверяйте каждую спецификацию до отправки.
- Храните токен бота и получателя вне `CompositionSpec`.
- После тайм-аута или неизвестного результата сначала проверьте состояние Telegram. Вторая отправка может создать дубликат.
- Разрешайте локальные файлы только из папок под контролем приложения.
- Проверяйте внешний вид на тех клиентах Telegram, которыми пользуется ваша аудитория.

## Документация

- [Поля CompositionSpec](docs/ru/composition-spec.md)
- [Правила оформления и текста](docs/ru/visual-system.md)
- [Подключение адаптеров](docs/ru/adapters.md)
- [Архитектура и границы безопасности](docs/ru/architecture.md)
- [План тестирования](docs/ru/test-plan.md)
- [Текущая матрица внешнего вида](docs/ru/visual-qa-matrix.md)
- [Как внести изменения](CONTRIBUTING.md) и [как сообщить об уязвимости](SECURITY.md)

Автоматические тесты проверяют сборку, выбор формата и защиту отправки. Сверьтесь с матрицей внешнего вида перед заявлением о поддержке конкретного клиента Telegram.

## Лицензия

[MIT](LICENSE)
