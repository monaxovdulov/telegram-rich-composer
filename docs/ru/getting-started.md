# Начало работы

[English version](../en/getting-started.md)

Здесь собраны установка, команды для терминала, пример для Python, подключение к AI-агенту и прямая отправка.

## Установка из репозитория

Понадобятся Git и Python 3.11 или новее. В примерах ниже используются пути для macOS и Linux.

```bash
git clone https://github.com/monaxovdulov/telegram-rich-composer.git
cd telegram-rich-composer
python3 -m venv .venv
.venv/bin/python -m pip install -e .
```

В Windows исполняемые файлы лежат в другой папке: замените `.venv/bin/python` на `.venv\Scripts\python`, а `.venv/bin/trc` на `.venv\Scripts\trc`.

## Проверка на своём компьютере

Возьмите готовую спецификацию.

```bash
.venv/bin/trc validate examples/golden/ticket-table.json
```

Если в результате есть `"valid": true`, Composer принял структуру файла и не нашёл ошибок. Теперь соберите данные Rich Message для Telegram.

```bash
.venv/bin/trc render examples/golden/ticket-table.json \
  --target rich_blocks > rendered.json
```

Для этих команд не нужны токен бота и доступ к Telegram.

## Команды

| Команда | Результат |
|---|---|
| `trc select context.json` | Выбор обычного или структурированного ответа |
| `trc validate spec.json` | Проверка спецификации |
| `trc render spec.json --target rich_blocks` | Данные Rich Message |
| `trc plan spec.json --capability rich_blocks` | Выбор доступного формата отправки |
| `trc request spec.json --chat-id ID` | Запрос без отправки |
| `trc send spec.json --chat-id ID --yes` | Одна отправка в Telegram |

Полный список параметров выводит команда `trc КОМАНДА --help`.

## Python API

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

## Подключение к AI-агенту

Поместите репозиторий в папку навыков агента. Файлы `SKILL.md`, `references/` и `schemas/` должны лежать вместе.

Установите Python-пакет из той же папки, если агент будет вызывать `trc`. Навык оставляет короткий разговор обычным текстом. Структурированный режим включается, когда сообщение выигрывает от таблицы, разделов или медиа.

## Прямая отправка через Bot API

Команда читает токен бота из переменной окружения, поэтому в самой спецификации нет ни токена, ни номера чата.

```bash
export TELEGRAM_BOT_TOKEN='your-bot-token'
.venv/bin/trc send examples/golden/ticket-table.json \
  --chat-id "$TRUSTED_CHAT_ID" --yes
```

Берите номер чата из текущего разговора Telegram или списка разрешённых получателей. Параметр `--media-root /allowed/path` открывает доступ к локальным файлам из указанной папки.

Пакет рассчитан на формат Rich Message из Telegram Bot API 10.2. Перед подключением доставки прочитайте [инструкцию по адаптерам](adapters.md).
