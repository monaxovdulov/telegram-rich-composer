# Архитектура

[English version](../en/architecture.md)

Статус: принятое решение для первой версии пакета.

## Назначение

`telegram-rich-composer` помогает агенту решить, нужен ли ответу в Telegram формат Rich Message. Затем пакет собирает семантическую спецификацию `CompositionSpec` и готовит её для доступного транспорта.

Пакет не заменяет Telegram gateway. Харнес отвечает за авторизацию, текущий разговор, повторные попытки и доставку.

## Границы проекта

В пакете шесть слоёв.

1. `SKILL.md` выбирает plain или rich и подходящую композицию.
2. `CompositionSpec` хранит структуру ответа без полей конкретного харнеса.
3. Renderer собирает explicit Telegram blocks, Rich Markdown, Rich HTML, обычный HTML или plain text.
4. Validator проверяет схему, лимиты Telegram, редакционные бюджеты, anchors, медиа и правила безопасности.
5. Adapter связывает payload с доверенным контекстом разговора и сверяет возможности транспорта.
6. Fallback упрощает представление и сохраняет главный ответ.

Polling-бот, SQLite-редактор черновиков и интерфейс черновиков из прототипа сюда не входят.

## Граница происхождения кода

На 5 августа 2026 года у локального прототипа `telegram-rich-publisher` не было файла лицензии. Новый проект не копирует его исходный код. С нуля воспроизведены только проверенные варианты поведения:

- связь Telegram `file_id` с rich media;
- разделение preview и publish;
- slideshow, collage, article и обычный album;
- проверка медиа и текста до запроса;
- разделение ошибок Bot API и транспорта;
- обычный media group как последний совместимый fallback.

Новая реализация опубликована по лицензии MIT.

## Поток данных

```text
запрос пользователя
  -> постоянное правило маршрутизации Telegram
  -> лениво загруженный SKILL.md
  -> selector
  -> CompositionSpec
  -> schema и semantic validation
  -> capability negotiation
  -> renderer
  -> adapter и trusted conversation context
  -> Telegram
              \-> безопасный fallback при окончательном отказе
```

Главный ответ стоит первым и виден сразу. Предупреждения нельзя прятать в `details`. Диагностика не попадает в пользовательский payload.

## CompositionSpec v1

Каноническая схема лежит в `schemas/composition-spec.schema.json`. Верхний уровень содержит такие поля:

| Поле | Назначение |
|---|---|
| `schema_version` | Версия семантического контракта. Первая версия использует семантику `1.0`. |
| `surface` | Тип Telegram-чата, режим draft, язык и доступные возможности. |
| `selection` | Plain или rich, pattern, профиль плотности и коды причин. |
| `summary` | Видимый ответ, который сохраняется при любом fallback. |
| `blocks` | Упорядоченные семантические блоки. |
| `media` | Именованные медиа и контролируемые типы источников. |
| `delivery` | Reply, thread, silent, protection, entity detection и намерение кнопок. |
| `fallback` | Порядок упрощения и политика повторной отправки. |
| `diagnostics` | Предупреждения для харнеса. Adapter не должен отправлять их пользователю. |

В `CompositionSpec` нет `chat_id`, токена, адреса Bot API и идентификатора сессии харнеса. Модель не может выбрать произвольного получателя.

### Форматированный текст

Текстовое поле принимает строку или последовательность inline nodes. Первая версия поддерживает plain text, bold, italic, underline, strikethrough, spoiler, mark, inline code, subscript, superscript, явные ссылки, anchor links, references, reference links, формулы и custom emoji.

### Блоки

Первая версия поддерживает paragraph, heading, divider, list, checklist, quote, pull quote, code, preformatted text, formula, table, details, footer, anchor, map, photo, video, animation, audio, voice note, collage, slideshow и thinking.

`thinking` допустим только во временном rich draft. В финальном сообщении такой блок запрещён.

### Медиа

Медиа использует ровно один источник:

- Telegram `file_id`;
- HTTP или HTTPS URL, который прошёл политику адаптера;
- локальный путь, который входит в разрешённый корень и имеет явное разрешение на upload.

Ядро не загружает локальные файлы на анонимные публичные хосты. Direct adapter может использовать Telegram multipart upload, если харнес дал capability `controlled_local_upload`.

## Проверка

Проверка состоит из трёх этапов.

1. JSON Schema проверяет форму и типы.
2. Semantic validation проверяет связи между полями и лимиты Telegram.
3. Editorial validation проверяет плотность и чтение с телефона. Нарушение редакционного бюджета даёт warning, если оно не ломает доставку и не скрывает обязательный текст.

Semantic validator проверяет лимиты Bot API 10.2:

- 32 768 символов;
- 500 блоков с учётом вложенных структур, list items и строк таблиц;
- 16 уровней вложенности;
- 50 медиа;
- 20 колонок таблицы.

Он также проверяет уникальность media ID, anchor targets, состояние `details`, table spans, размеры карты, политику источников медиа и draft-only blocks.

## Renderer

Renderer поддерживает четыре результата.

1. `rich_blocks` создаёт `InputRichMessage.blocks`.
2. `rich_markdown` создаёт `InputRichMessage.markdown` и явные media bindings.
3. `rich_html` создаёт `InputRichMessage.html` и явные media bindings.
4. `legacy` создаёт обычный HTML или plain text и план обычных медиа.

В одном rich payload присутствует ровно одно поле из `blocks`, `markdown` и `html`.

Explicit blocks выбраны основным форматом. Они убирают неоднозначность parser и сохраняют table spans, состояние details, references и метаданные медиа. Rich Markdown и Rich HTML нужны харнесам, которые уже поддерживают эти пути.

## Выбор композиции

Короткий разговорный ответ по умолчанию остаётся plain. Rich нужен, когда он заметно улучшает чтение, сравнение, раскрытие деталей, последовательность, медиа или список действий.

Selector возвращает коды причин. Благодаря этому выбор можно проверить тестом. Примеры: `short_conversation`, `collapsed_evidence`, `simultaneous_comparison`, `ordered_visual_sequence` и `structured_decision`.

Одна картинка получает один media block. Collage показывает сравнение одновременно. Slideshow показывает последовательность связанных состояний или схем.

## Capability negotiation

Adapter сообщает отдельные capabilities. Ядро не угадывает поддержку по имени харнеса. Используется такой порядок:

1. explicit rich blocks;
2. Rich Markdown или Rich HTML;
3. обычный Telegram HTML или Markdown;
4. plain text и обычный media group.

Вложенные blocks и медиа внутри `details` считаются разными capabilities. Отдельно проверяются anchors, media spoilers, references, custom emoji, maps, reply parameters, topics, reply markup, draft streaming и controlled local upload.

## Доставка без дублей

Adapter получает `TrustedConversationContext` от харнеса. В нём находятся текущий чат, исходное сообщение, thread или topic, результат авторизации отправителя и подтверждение allowlist при необходимости.

Adapter связывает `delivery.reply` и `delivery.thread` с этим контекстом. Другой чат или канал требует явного запроса пользователя и отдельной проверки allowlist вне спецификации.

После окончательной ошибки syntax или capability разрешён fallback до следующей отправки. Timeout, разрыв соединения и неизвестный результат сети не разрешают автоматическую вторую отправку. Adapter записывает состояние `unknown` и передаёт управление харнесу для сверки.

## Решения для текущих харнесов

### Eve

Eve поддерживает packaged skills и typed tools. Его штатный Telegram channel сейчас просит короткий plain text и не вызывает `sendRichMessage`. Интеграция содержит постоянное правило, typed composition tool и пример channel adapter. Adapter берёт `channel.telegram.chatId` и `messageThreadId` из текущего события.

### Iva

Iva уже направляет таблицы, task lists, details и block math в `sendRichMessage`. Перед отправкой он редактирует секреты, а при окончательной ошибке переходит на HTML. Интеграция использует этот transport и добавляет проверку `CompositionSpec` до отправки. Существующие allowlist и redaction gate остаются на месте.

### Hermes Agent

Hermes уже содержит включаемый rich fast path, streaming drafts, rich final edits, reply parameters, topic routing и осторожную защиту от дублей. Интеграция использует skill для выбора и plugin tool для compile и validation. Финальная отправка остаётся за native Telegram gateway.

### Direct Bot API

Reference adapter принимает trusted context от вызывающей стороны. Он поддерживает JSON-запросы и контролируемый multipart upload. Журнал попыток не даёт автоматически повторить отправку с неизвестным результатом.

## Отличия от прототипа

- Канонический объект стал семантическим и версируемым. Это не пользовательский черновик в базе.
- Основным результатом стали explicit blocks из Telegram Bot API 10.2.
- Медиа поддерживает `file_id`, URL и контролируемый multipart upload.
- Получателя выбирает trusted context, а не модель.
- Capabilities проверяются по отдельности.
- Timeout не создаёт повторную отправку.
- Обычный короткий ответ остаётся plain.
- В пакете нет polling loop, базы черновиков и анонимного upload service.

## База источников

Исследование проведено 5 августа 2026 года по таким версиям:

- документация Telegram Bot API 10.2;
- Agent Skills specification на 5 августа 2026 года;
- открытая информация об ASD-STE100 Issue 9;
- Eve commit `e5c91918ed898f72047d2a1e33902cbb9db3e452`;
- Iva commit `b3544a2c19341a2231353b2942905748bf391751`;
- Hermes Agent commit `1be70d63548845eb8918c08ed698cda0674cf9a7`;
- humanizer-ru commit `91f70df11f7fb30722e6fcf18803d402e2d86a53`.

Ссылки и заметки об исследовании лежат в `references/sources.md`.
