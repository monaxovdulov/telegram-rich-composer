# Руководство по adapters

[English version](../en/adapters.md)

## Контракт

Adapter связывает семантический ответ с одним доверенным разговором в Telegram. Он выполняет четыре операции.

```text
capabilities(context) -> CapabilitySet
prepare(spec, context, capabilities) -> DeliveryPlan
send(plan, context) -> DeliveryResult
reconcile(attempt_id, context) -> DeliveryResult
```

`prepare` не меняет внешнее состояние. `send` может отправить сообщение. `reconcile` проверяет прошлую попытку с неизвестным результатом.

## TrustedConversationContext

Этот объект создаёт харнес. Модель его не составляет.

| Поле | Смысл |
|---|---|
| `conversation_id` | Устойчивый идентификатор активного разговора в харнесе. |
| `chat_id` | Telegram-чат, из которого пришёл активный запрос. |
| `chat_type` | `private`, `group`, `supergroup` или `channel`. |
| `message_id` | Входящее сообщение, на которое можно ответить. |
| `message_thread_id` | Текущий forum topic, если он есть. |
| `direct_messages_topic_id` | Текущий direct-message topic, если он есть. |
| `sender_id` | Проверенный отправитель, если харнес его предоставляет. |
| `authorized` | Результат проверки доступа в харнесе. |
| `explicit_target` | Необязательная цель из явного запроса пользователя. |
| `allowlist_evidence` | Подтверждение allowlist для цели вне активного чата. |

Adapter отказывает в доставке, если `authorized` равен false. Другая цель допустима только при наличии `explicit_target` и `allowlist_evidence`.

## CapabilitySet

Каждая возможность задаётся отдельным boolean. Одного флага `rich_messages` недостаточно.

Обязательные ключи:

- `rich_blocks`
- `rich_markdown`
- `rich_html`
- `rich_draft_streaming`
- `legacy_markdown`
- `legacy_html`
- `reply_parameters`
- `reply_markup`
- `topics`
- `direct_message_topics`
- `media_file_id`
- `media_url`
- `controlled_local_upload`
- `details_nested_blocks`
- `details_nested_media`
- `media_spoiler`
- `anchors`
- `references`
- `custom_emoji`
- `maps`
- `diagram_renderer`

Adapter может добавить ключи со своим namespace. Ядро игнорирует неизвестные ключи.

## Выбор транспорта

Ядро использует такой порядок.

1. Выбрать explicit blocks, если `rich_blocks` включён и поддержаны все запрошенные функции.
2. Выбрать Rich Markdown или Rich HTML, если этот путь сохраняет обязательные функции.
3. Выбрать обычный HTML или Markdown для текста, который помещается в стандартное Telegram-сообщение.
4. Выбрать plain text и план обычных медиа.

Renderer добавляет warning для каждой потерянной функции. Видимый summary сохраняется на каждом шаге.

Если `details_nested_media` выключен, медиа переносится после details и получает видимую подпись. Если нет `anchors`, содержание превращается в короткий список. Если нет `references`, в конце появляются нумерованные источники. Если нет `maps`, остаются координаты и явная безопасная ссылка на карту.

## Параметры доставки

У `delivery.reply` есть режимы `inherit`, `none` и `required`. `inherit` использует текущее сообщение по обычным правилам харнеса. `required` возвращает ошибку, если нет доверенного reply target.

У `delivery.thread` есть `inherit` и `none`. В первой версии модель не может передать произвольный thread ID.

`silent`, `protect_content` и `reply_markup` передаются только при соответствующей capability. Кнопка должна запускать действие или отражать реальный выбор. Декоративные кнопки запрещены в профиле `calm`.

## Entity detection

Для обычного текста используй `entity_detection: auto`. Renderer не добавляет `skip_entity_detection`, поэтому Telegram распознаёт URL, email, phone, commands, hashtags и mentions.

Используй `entity_detection: explicit_only`, когда автоматические синие участки ломают иерархию. Renderer ставит `skip_entity_detection: true`. Все нужные ссылки должны быть явными inline nodes.

Не выключай entity detection для каждого сообщения.

## Политика медиа

### Telegram file ID

Используй `file_id`, если медиа уже находится в Telegram. Renderer связывает его через `InputRichMessage.media` или explicit media block.

### URL

По умолчанию разрешён HTTPS. HTTP можно включить только для контролируемой сети и отдельной политики. Без доверенного fetcher запрещены loopback, link-local, private-network, URL с учётными данными и неизвестные схемы.

### Локальный путь

Локальные медиа по умолчанию запрещены. Для включения харнес передаёт разрешённые корни и `controlled_local_upload`. Перед проверкой корня нужно раскрыть symlink. Файл должен быть обычным, иметь разрешённый media type и допустимый размер. Upload идёт прямо в Telegram через multipart. Анонимный публичный хост не используется.

## Классы ошибок

| Класс | Пример | Действие |
|---|---|---|
| `permanent_syntax` | Bot API вернул понятную ошибку rich syntax с кодом 400. | Подготовить более простой вариант и отправить один раз. |
| `capability` | Method или rich feature не поддерживается. | Выключить capability до конца сессии и перейти к следующему варианту. |
| `authorization` | Отправитель или цель не прошли проверку. | Остановиться. Нельзя выбирать другую цель через fallback. |
| `local_validation` | Ошибка schema, limit, URL, path или media policy. | Остановиться до сетевого запроса. |
| `transport_not_connected` | Соединение не установлено. | Харнес может повторить запрос по своей обычной политике. |
| `unknown_delivery` | Timeout или разрыв после возможной доставки запроса. | Записать `unknown`. Не отправлять другой вариант. Сначала выполнить reconcile. |

## Eve

Установи packaged skill в `agent/skills/telegram-rich-composer/`. Добавь короткое правило в `agent/instructions.md`, чтобы Telegram-сессия оценивала выбор plain или rich на каждом ходу. Полный каталог patterns должен загружаться только по необходимости.

Typed tool читает спецификацию и возвращает delivery plan. Telegram channel event handler отправляет запрос и получает trusted chat и thread из `channel.telegram`. Модель не передаёт `chat_id` в tool.

В Eve commit `e5c91918...` нет штатного rich transport. Пример adapter использует raw request surface. Его нужно пересмотреть после появления native rich delivery.

## Iva

В Iva commit `b3544a2c...` текущий chat и thread берутся из `channel.telegram`. Перед `sendRichMessage` и HTML fallback вызывается `scanOutbound`.

Сохрани эти проверки. Добавь selector и validator перед `needsRichMessage`. Raw Rich Markdown можно передать только после проверки. Окончательная rich error может использовать текущий HTML fallback. Неизвестный сетевой результат запрещает fallback, иначе ответ может прийти дважды.

Старый default digest recipient из `rich-post` не подходит для разговорного ответа. Используй активный channel context. Allowlist для digest остаётся только для явной отправки отчёта вне текущего чата.

## Hermes Agent

В Hermes commit `6564f319a...` уже есть включаемый rich fast path, rich drafts, rich final edits, topic routing, `reply_parameters` и запрет повторной отправки после неизвестного результата.

Для первого теста установи лёгкий Hermes-пакет. Он использует штатную отправку raw Markdown и не требует Python-пакета.

```bash
hermes skills install monaxovdulov/telegram-rich-composer/skills/telegram-rich-composer --yes
```

Установи `gateway.platforms.telegram.extra.rich_messages` в `true`. Для первого теста оставь `rich_drafts` в значении `false`. [Краткая инструкция для Hermes](hermes-quickstart.md) содержит готовое задание агенту и тестовый запрос.

Необязательный plugin добавляет policy helpers для полной интеграции через `CompositionSpec`. Он не заменяет Telegram platform adapter. Native adapter отвечает за `chat_id`, topics, reply anchors и доставку.

Код стороннего plugin нужно явно включить в `plugins.enabled`. Если native Rich Markdown достаточно, можно установить только skill без plugin.

## Direct Bot API

Reference CLI получает доверенные значения через аргументы, которые передает host. Token нельзя передавать аргументом командной строки. Он читается из `TELEGRAM_BOT_TOKEN`.

Примеры по умолчанию работают как dry-run. Для сети нужны явная команда `send` и флаг `--yes`. До запуска host получает `chat_id` из доверенного контекста или проверяет allowlist. В reference adapter нет delivery ledger, поэтому после неизвестного результата вызывающая система сверяет состояние через собственное хранилище updates или audit log.
