# Визуальная система

[English version](../en/visual-system.md)

## Чем управляет skill

Telegram client управляет шрифтом, радиусом, цветом и точным размером. Skill не считает эти параметры design tokens.

Skill управляет порядком, повторением, плотностью, числом акцентов, типом блока, раскрытием деталей и связью медиа.

## Четыре визуальных слоя

1. Внешняя карточка сообщения воспринимается как одна редакционная страница.
2. Типографика задаёт иерархию. Крупный serif heading, обычный sans-serif body и monospace code зависят от клиента. Композиция выбирает место для каждой роли.
3. Quotes, code, tables и details образуют вложенные поверхности.
4. Photos, video, audio, maps, collage и slideshow образуют полноширинные плоскости.

Пример уровня «Blade Runner» нужен только как образец ритма. Один крупный heading, короткий divider, metadata quotation, повторяющиеся headings сцен, обычный текст, редкий italic и финальный divider создают ясный темп. Пакет не навязывает эту эстетику.

## Визуальный вес и редакционные бюджеты

Эти значения помогают редактору. Они не относятся к лимитам Bot API.

| Элемент | Роль | Хорошее применение | Плохое применение | Обычный бюджет |
|---|---|---|---|---|
| H1-H6 | Обложка, сцена или затухание голоса | Один title и несколько ритмических разделов | Heading для каждого абзаца | Один H1 и два-четыре младших headings |
| Divider | Склейка или смена сцены | Разделить крупные фазы | Разделить каждый блок | Один-три |
| Blockquote | Metadata или service panel | Короткий status или сведения об объекте | Длинный основной текст | Один-два |
| Pullquote | Poster phrase или второй голос | Короткая фраза с credit | Полный абзац | Один короткий блок |
| Mark | Индекс или второе чтение | Одно-три слова в акценте | Длинный выделенный фрагмент | Одно-три слова за раз |
| Spoiler | Управляемое раскрытие | Одно согласованное действие | Скрыть обычный body | Один заметный spoiler |
| Inline code | Машинный token | Command, field или identifier | Оформить обычную прозу | Короткие фрагменты |
| Code или pre | Code, metadata или machine voice | Три-пять коротких строк | Макет, выровненный пробелами | Один блок |
| Table | Билет, паспорт, легенда или сравнение | Две мобильные колонки | Длинная проза в множестве колонок | Две колонки, третья только для коротких значений |
| Details | Глава или ящик | Доказательства, logs и sources | Скрыть ответ или warning | Три-пять, один-два уровня |
| Collage | Diptych, quadriptych или contact sheet | Сравнить два или четыре кадра сразу | Рассказать последовательность | Два или четыре кадра |
| Slideshow | Состояния по порядку | Перелистать три-пять связанных кадров | Сравнить значения рядом | Три-пять кадров |
| Map | Обложка, координата или геометрия | Одна плоскость места | Конкурировать со вторым hero | Одна карта |
| Custom emoji | Система glyphs | Один согласованный pack | Смешать разные packs | Один pack и один-три типа знаков |
| Reference | Источник или второй рассказчик | Два-четыре коротких примечания | Превратить чат в статью | Два-четыре примечания |

## Политика акцентов

Не собирай bold, italic, underline, strikethrough, spoiler, mark, subscript и superscript в одном показательном абзаце. У абзаца должен быть один основной акцентный приём.

Назначай mark, spoiler, code и strikethrough разные задачи. Underline легко спутать со ссылкой. Не используй его для обычного акцента.

Raw URL, email, phone, commands, hashtags и mentions могут разбить спокойную поверхность синими участками. Включай `skip_entity_detection`, когда нужны управляемые click targets. Нужные ссылки создавай явно. Для обычного разговора оставляй автоматическое распознавание.

## Профили плотности

### calm

Используй для обычных личных и групповых ответов. У одного сообщения такие целевые бюджеты:

- один крупный heading;
- один доминирующий media object;
- одна основная nested surface из quote, table или code;
- три-пять details;
- до двух уровней вложенности;
- обычно две колонки таблицы;
- две-четыре видимые картинки;
- один animated custom emoji;
- две-три видимые ссылки above the fold;
- один spoiler;
- один pullquote;
- один основной accent technique на paragraph.

Профиль может использовать меньше. Не нужно заполнять каждый слот.

### standard

Используй для заказанного brief, guide, comparison или report. Можно добавить ещё одну nested surface или media group. Ответ и warnings остаются видимыми.

### showcase

Используй только для явного demo, component catalog или просьбы показать возможности. Validator всё равно проверяет лимиты Telegram, вложенность, безопасность и мобильные таблицы.

## Утилитарные patterns

### Короткий plain answer

Подходит для приветствия, подтверждения, одного факта или короткого исправления. Не добавляй card, heading, divider и details.

### Summary со сворачиваемыми деталями

Сначала дай ответ. Evidence, logs, sources и вторичные примеры положи в details. Warning всегда остаётся видимым.

### Decision card

Покажи решение, причину, owner и следующий шаг. Кнопки нужны только для настоящего выбора или действия.

### Comparison table

На телефоне используй две колонки. Третья допустима для коротких значений. Длинный текст разбей на короткие rows или вертикальные sections.

### Step-by-step guide

Сначала покажи результат, затем ordered steps. В каждом шаге одно действие. Длинные commands и troubleshooting можно свернуть.

### Technical answer с code и logs

Диагноз и fix стоят перед code. Используй один code block. Длинные logs положи в закрытый details.

### Research brief

Сначала дай вывод. Evidence sections и явные source links должны быть короткими. Methods и длинные заметки об источниках стоят в конце.

### Checklist или action plan

Checkbox нужен только для действия, которое меняет состояние. Owner и срок остаются видимыми.

### Incident или status card

Покажи state, impact, time и время следующего update. Текущий impact и safety warning нельзя скрывать.

### Digest

Выведи по одной строке на item. Раскрывай только те items, которым нужен контекст.

### Visual comparison

Collage нужен, когда кадры надо видеть одновременно.

### Diagram sequence

Slideshow нужен для состояний по порядку. Одна схема получает один media block.

## Сложные patterns

### hypertext-journal

Начни с однострочного индекса на три-четыре anchors. Добавь короткое вступление. Первую главу открой, остальные закрой. В конце главы поставь return-to-index link. Sources и technical details идут последними. Если контент позволяет, поддержи маршруты read, watch, listen и inspect. Каждый anchor ставится прямо перед видимым heading или details row.

### museum-drawers

Используй одно hero media или slideshow. Добавь три-четыре ящика object, place, sound и provenance. Первый ящик открыт. Caption короткая. Внутри одна blockquote panel, одна table два на два и не больше одного reference. Map и audio могут лежать в закрытых ящиках, если adapter это умеет.

### marked-second-reading

Короткие marked words в разных предложениях образуют вторую фразу, индекс, даты или states. Длинный marked passage запрещён.

### interactive-redaction

Один text spoiler и при необходимости один media spoiler создают одно действие раскрытия. Caption и credit не должны исчезать случайно. Не превращай всю карточку в шум цензуры.

### ticket-table

Table работает как билет, паспорт, coordinate plate, mini-calendar или grid. Поддерживаются bordered и striped, alignment, rowspan и colspan. В table cells допустим только inline formatting.

### map-cover

Одна map работает как hero или финальная координата. Рядом остаётся короткий текст. Добавь одну monospace coordinate line и один divider. Второй hero не нужен.

### code-typography

Один короткий code или pre block работает как machine voice, programmatic epigraph или metadata panel. Строки должны быть короткими. Не выравнивай сложный макет пробелами.

### manual-animation

Slideshow показывает состояния одного места, предмета, interface или diagram. Пользователь двигает время свайпом. Если важнее сравнение в один момент, выбери collage.

### hidden-sound-note

Короткое audio или voice note лежит в закрытом details с ясной duration label. Основная карточка остаётся спокойной. Если adapter не поддерживает nested media, вынеси audio после details.

### title-pullquote

Одна-две короткие строки и credit образуют poster card. В credit можно указать series name, issue number, character, coordinates, time или source.

### emoji-glyph-system

Custom emoji работают как issue marks, category glyphs или punctuation. Используй один согласованный pack. Не смешивай несовместимые объёмные, плоские и стандартные emoji.

### second-narrator-notes

Два-три references добавляют сомнение, другую версию, время, source, technical detail или чужой голос. Основное сообщение сохраняет разговорный тон.

## Разовые приёмы

- `fading-voice` использует короткую последовательность H1-H6 для снижения визуальной громкости. Это interlude, а не navigation.
- `reverse-countdown` использует данные ordered list `start`, `type` и `reversed`.
- `edit-trace` использует strikethrough для прошлой версии, времени или состояния.
- `issue-superscript` использует superscript для компактного issue number или service index.

## Фирменные presets

### issue

Подходит для articles и research. Используй один custom emoji, title с issue index, три-четыре anchors, divider, короткое вступление, три-пять details, два-три references и return-to-index links. Главную роль играют typography и главы.

### artifact

Подходит для places, objects, products и observations. Используй одну map или photo, H1, компактную table, monospace metadata, одну blockquote panel и details с provenance. Главную роль играют grid и одна крупная media plane.

### scene

Подходит для visual stories и sequences of diagrams. Используй slideshow из трёх-пяти frames, один короткий pullquote, один paragraph и закрытые details для sound, location и credits. Главную роль играет последовательность.

## Политика группового чата

- Короткий ответ по умолчанию остаётся plain.
- Ответ стоит первым.
- Длинные доказательства, logs, sources и вторичные примеры можно свернуть.
- Warnings остаются видимыми.
- Обычно достаточно одного Rich Message bubble.
- Table должна читаться на телефоне.
- Slideshow показывает последовательность, collage показывает одновременное сравнение.
- Одна картинка не требует slideshow.
- Кнопка нужна только для действия или выбора.
- Reply и topic context сохраняются.
- Details и spoiler не защищают секреты.

## Client QA

Проверь Android, iOS и Desktop в светлой и тёмной теме. Повтори тест с увеличенным system font. Включи forwarded headers, reply headers, forum topics, link colors, button placement, anchors, nested details, hidden media, media spoilers, узкий экран и длинные table values.

Buttons находятся снаружи Rich Message card и используют цвета интерфейса. Не полагайся на цвет карточки и точный радиус. Не выравнивай контент пробелами.
