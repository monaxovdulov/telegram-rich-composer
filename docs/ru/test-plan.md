# План тестов и критерии релиза

[English version](../en/test-plan.md)

## Уровни проверки

1. Schema tests проверяют все examples и отклоняют неправильные спецификации.
2. Unit tests проверяют выбор, rendering, validation, media binding и fallback.
3. Golden tests охватывают каждый pattern и preset из каталога.
4. Adapter conformance запускает одинаковые fixtures для Eve, Iva, Hermes и direct adapters.
5. Safety tests проверяют привязку получателя, allowlist, локальные медиа, признаки секретов и защиту от дублей.
6. Documentation tests проверяют ссылки, парные файлы, команды и обязательные разделы.

## Проверка лимитов

Для каждой границы нужен тест на точное значение и на превышение на одну единицу:

- 32 768 символов;
- 500 учитываемых блоков;
- 16 уровней вложенности;
- 50 медиа;
- 20 колонок таблицы.

Nested blocks, list items, table rows, quotes и details считаются по описанию Bot API.

## Golden fixtures

Храни принятую спецификацию и готовый результат для каждого утилитарного pattern, всех 12 сложных patterns и трёх presets.

Сложные patterns:

- `hypertext-journal`
- `museum-drawers`
- `marked-second-reading`
- `interactive-redaction`
- `ticket-table`
- `map-cover`
- `code-typography`
- `manual-animation`
- `hidden-sound-note`
- `title-pullquote`
- `emoji-glyph-system`
- `second-narrator-notes`

Presets:

- `issue`
- `artifact`
- `scene`

## Проверка выбора

Eval-набор включает бытовые вопросы, групповые обсуждения, техническую диагностику, исследования, решения, таблицы, длинные логи, одну схему, несколько схем, collage comparison, slideshow sequence, anchors, nested details, hidden audio, controlled spoilers, custom emoji, references, link noise и случай без rich capabilities.

Каждый случай задаёт:

- ожидаемый plain или rich;
- допустимый набор patterns;
- ожидаемый density profile;
- обязательный видимый summary;
- предупреждения, которые нельзя прятать;
- связь медиа: нет, одно, одновременное сравнение или последовательность.

## Fallback tests

Проверь каждый переход в degradation ladder. Summary должен сохраниться, а неподдержанные функции должны получить читаемую замену.

Два сетевых случая проверяются отдельно:

- подтверждённая окончательная ошибка разрешает одну fallback-отправку;
- неизвестный результат запрещает новую отправку до reconcile.

## Entity и ссылки

- Явные ссылки с `entity_detection: explicit_only` включают `skip_entity_detection`.
- Raw URL с `entity_detection: auto` не включает его.
- Каждый anchor link должен разрешаться. Иначе validator возвращает ошибку.
- Anchor должен стоять прямо перед видимым heading или details row.
- Return-to-index links сохраняются в Rich HTML и explicit blocks.

## Медиа

- Telegram `file_id` связывается без скачивания.
- Безопасное HTTPS media принимается.
- Unsafe URL и private-network URL по умолчанию отклоняются.
- Локальный путь без явного разрешения отклоняется.
- Symlink раскрывается до проверки allowed roots.
- Multipart upload собирается без публичного hosting service.
- Caption, credit и media spoiler сохраняются.
- При отсутствии capability медиа выносится из details.
- Одновременное сравнение выбирает collage, последовательность выбирает slideshow.

## Density profiles

Для группы по умолчанию используется `calm`. Он должен укладываться в редакционный бюджет или выдавать понятные warnings. `showcase` допустим только для явной демонстрации, component catalog или прямого запроса пользователя.

## Документация

- У каждого обязательного английского документа есть русская пара.
- Парные документы содержат одинаковые команды, лимиты, capability names и known limitations.
- Английский текст проходит checklist принципов ASD-STE100.
- Русский текст проходит humanizer-ru audit и не имеет lint `ERROR`.
- Внешние ссылки проходят link checker.

## Visual QA

Опубликуй матрицу для Android, iOS и Desktop. Включи светлую и тёмную темы, обычный и увеличенный system font, forwarded headers, reply headers, topics, anchors, details, hidden media, spoilers и узкие таблицы.

Каждая клетка получает статус `verified`, `failed` или `not tested`. Статус `not tested` нельзя описывать как подтверждённую поддержку.

## Проверки перед релизом

- Unit, golden, eval, adapter conformance и documentation tests проходят.
- Проверка Agent Skill package проходит.
- Secret scanning файлов и Git history проходит.
- В репозитории нет `.env`, token, private chat ID, user data, database, log и медиа без лицензии.
- Локальный Git status чистый.
- Public CI проходит на release commit.
- Release report содержит URL, install commands, test commands, known limitations, source baselines и отличия от прототипа.
