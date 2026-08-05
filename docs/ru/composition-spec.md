# CompositionSpec 1.0

[English version](../en/composition-spec.md)

Каноническая схема находится в [`schemas/composition-spec.schema.json`](../../schemas/composition-spec.schema.json). Документ представляет один смысловой ответ в Telegram до привязки получателя.

| Раздел | Назначение | Уровень доверия |
|---|---|---|
| `surface` | Тип чата, locale, состояние draft и заявленные возможности | Недоверенный контекст модели |
| `selection` | Выбор plain/rich, pattern, density и причины | Недоверенные проверяемые данные |
| `summary` | Текст ответа, который переживает fallback | Недоверенные проверяемые данные |
| `blocks` | Смысловое дерево блоков и inline-узлов | Недоверенные проверяемые данные |
| `media` | Логические ID и источники Telegram, HTTPS или controlled local | Недоверенные данные под политикой адаптера |
| `delivery` | Наследование reply/thread, уведомления, защита, entity policy и кнопки | Только намерение, значения добавляет адаптер |
| `fallback` | Порядок представлений и правило неизвестного результата | Недоверенные проверяемые данные |
| `diagnostics` | Структурированные предупреждения композиции | Информационные данные |

В схеме намеренно нет `chat_id`, ID темы, ID сообщения для ответа, bot token, заявления об авторизации и сессии harness. Эти значения существуют только в `TrustedConversationContext`.

Rich text поддерживает вложенное форматирование, безопасные явные ссылки, anchors, references, custom emoji и formulas. В blocks входят paragraphs, headings, preformatted text, lists, quotations, tables, details, maps, media, collage, slideshow и thinking только для draft.

Validator объединяет JSON Schema, ограничения Telegram, целостность привязок, безопасность URL и локальных путей, правила draft, предупреждения о возможностях и редакционные бюджеты. Одной проверки JSON Schema недостаточно.
