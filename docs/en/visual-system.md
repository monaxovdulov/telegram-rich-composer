# Visual system

[Русская версия](../ru/visual-system.md)

## What the skill controls

Telegram clients control the font family, radius, color, and exact size. The skill does not treat these client choices as design tokens.

The skill controls order, repetition, density, accent count, block type, disclosure, and media relationship.

## Four visual layers

1. The outer message card reads as one editorial page.
2. Typography sets hierarchy. Large serif headings, sans-serif body text, and monospace code are client behavior. The composition controls where each role appears.
3. Quotes, code, tables, and details make nested surfaces.
4. Photos, video, audio, maps, collage, and slideshow make full-width geometric planes.

Use a Blade Runner-like example only as a rhythm reference. One large heading, one short divider, one metadata quotation, repeated scene headings, plain body text, rare italics, and one final divider create a clear beat. The package does not require that aesthetic.

## Visual weight and editorial budgets

These values are editorial guidance. They are not Bot API limits.

| Element | Visual role | Good use | Bad use | Typical budget |
|---|---|---|---|---|
| H1-H6 | Cover, scene, or fading voice | One cover title and a few section beats | Heading for every paragraph | One H1 and two to four smaller headings |
| Divider | Cut or scene change | Separate major phases | Separate every block | One to three |
| Blockquote | Metadata or service panel | Compact status or object facts | Long body copy | One to two |
| Pullquote | Poster phrase or second voice | One short statement with credit | A full paragraph | One short block |
| Mark | Index or second reading | One to three words per accent | Long highlighted passage | One to three words at a time |
| Spoiler | Intentional reveal | One coordinated reveal | Hiding ordinary body text | One visible spoiler |
| Inline code | Machine token | Command, field, or identifier | Styling normal prose | Short fragments |
| Code or pre | Code, metadata, or machine voice | Three to five short lines | A layout aligned with spaces | One block |
| Table | Ticket, passport, legend, or comparison | Two mobile columns | Long prose in many columns | Two columns, third only for short values |
| Details | Chapter or drawer | Secondary proof, logs, or sources | Hiding the answer or warning | Three to five, one or two nesting levels |
| Collage | Diptych, quadriptych, contact sheet | Compare two or four frames now | Tell a time sequence | Two or four frames |
| Slideshow | Ordered states | Swipe through three to five related frames | Compare values side by side | Three to five frames |
| Map | Cover, coordinate, or geometry | One location plane | Compete with a second hero | One map |
| Custom emoji | Glyph system | One coherent pack | Mixed visual packs | One pack and one to three sign types |
| Reference | Source or second narrator | Two to four concise notes | Turn a chat reply into a paper | Two to four notes |

## Accent policy

Do not combine bold, italic, underline, strikethrough, spoiler, mark, subscript, and superscript in one showcase paragraph. Use one primary accent method in one paragraph.

Assign separate jobs to mark, spoiler, code, and strikethrough. Underline can look like a link. Do not use it for ordinary emphasis.

Plain URLs, e-mail addresses, phone numbers, commands, hashtags, and mentions can split a calm surface into blue fragments. Use `skip_entity_detection` when the composition needs controlled click targets. Add required links explicitly. Keep automatic detection for normal conversation.

## Density profiles

### calm

Use for normal private and group replies. Apply these target budgets to one message:

- one large heading;
- one dominant media object;
- one main nested surface from quote, table, or code;
- three to five details blocks;
- no more than two nesting levels;
- usually two table columns;
- two to four visible images;
- one animated custom emoji;
- two or three visible links above the fold;
- one spoiler;
- one pullquote;
- one primary accent method per paragraph.

The profile can use less. It must not fill every slot.

### standard

Use for requested briefs, guides, comparisons, and reports. The profile can add one more nested surface or media group. It must keep the answer and warnings visible.

### showcase

Use only for an explicit demo, component catalog, or request to show capabilities. The validator still enforces Telegram limits, nesting, safety, and mobile table rules.

## Standard utility patterns

### Short plain answer

Use for greetings, confirmations, one fact, or a short correction. Do not add a card, heading, divider, or details.

### Summary with collapsed details

Put the answer first. Put evidence, logs, sources, and secondary examples in details. Never hide a warning.

### Decision card

Show the decision, reason, owner, and next step. Use buttons only for a real choice or action.

### Comparison table

Use two columns on a phone. Use a third column only for short values. Convert long prose to short rows or stacked sections.

### Step-by-step guide

Show the outcome first, then ordered steps. Keep one action per step. Put long commands or troubleshooting in details.

### Technical answer with code and logs

Show diagnosis and fix before code. Use one code block. Put long logs in closed details.

### Research brief

Show the finding first. Use short evidence sections and explicit source links. Put methods and long source notes last.

### Checklist or action plan

Use checkboxes only for actions that can change state. Keep ownership and timing visible.

### Incident or status card

Show state, impact, time, and next update. Never hide current impact or a safety warning.

### Digest

Give one line per item above the fold. Expand only items that need context.

### Visual comparison

Use a collage when the user must inspect frames at the same time.

### Diagram sequence

Use a slideshow when frames show ordered states. Use one media block for one diagram.

## Advanced patterns

### hypertext-journal

Start with a one-line index of three or four anchors. Add a short introduction. Open the first chapter and close the rest. Put a return-to-index link at the end of each chapter. Put sources and technical details last. Support read, watch, listen, and inspect routes when the content has them. Place each anchor directly before its visible heading or details row.

### museum-drawers

Use one hero media object or slideshow. Add three or four drawers for object, place, sound, and provenance. Open the first drawer. Keep its caption short. Use one blockquote panel, one two-by-two table, and at most one reference. Maps and audio can stay in closed drawers when capabilities allow it.

### marked-second-reading

Mark short words across separate sentences so they form a second phrase, index, date sequence, or state sequence. Never mark a long passage.

### interactive-redaction

Use one text spoiler and, when needed, one media spoiler for the same reveal action. Keep captions and credit outside accidental concealment. Do not make the whole card look censored.

### ticket-table

Use a table as a ticket, passport, coordinate plate, mini-calendar, or grid. Support bordered and striped forms, alignment, rowspan, and colspan. Table cells contain inline formatting only.

### map-cover

Use one map as the hero or final coordinate. Keep nearby text short. Add one monospace coordinate line and one divider. Do not add a second hero.

### code-typography

Use one short code or pre block as a machine voice, programmatic epigraph, or metadata panel. Keep lines short. Do not align a complex design with spaces.

### manual-animation

Use a slideshow for successive states of one place, object, interface, or diagram. The user moves time by swiping. Use collage when simultaneous comparison matters more.

### hidden-sound-note

Put short audio or a voice note in closed details with a clear duration label. Keep the main card visually calm. Move the audio outside details when the adapter lacks nested media support.

### title-pullquote

Use one or two short lines and a credit as a poster card. The credit can contain a series name, issue number, character, coordinates, time, or source.

### emoji-glyph-system

Use custom emoji as issue marks, category glyphs, or punctuation. Use one coherent pack. Do not mix incompatible volumetric, flat, and standard emoji styles.

### second-narrator-notes

Use two or three references for doubt, an alternative account, time, source, technical detail, or another voice. Keep the main message conversational.

## Special-use typography

- `fading-voice` uses a short H1-to-H6 sequence to lower visual volume. Use it for an interlude, not navigation.
- `reverse-countdown` uses ordered-list `start`, `type`, and `reversed` data.
- `edit-trace` uses strikethrough for a prior version, time, or state.
- `issue-superscript` uses superscript for a compact issue number or service index.

## High-level presets

### issue

Use for articles and research. Combine one custom emoji, a title with issue index, three or four anchors, a divider, a short introduction, three to five details, two or three references, and return-to-index links. Typography and chapters dominate.

### artifact

Use for places, objects, products, and observations. Combine one map or photo, H1, compact table, monospace metadata, one blockquote panel, and provenance details. Grid and one large media plane dominate.

### scene

Use for visual stories and diagram sequences. Combine a three-to-five-frame slideshow, one short pullquote, one paragraph, and closed details for sound, location, and credits. Sequence dominates.

## Group chat policy

- Plain text is the default for short replies.
- Put the answer first.
- Collapse long proof, logs, sources, and secondary examples.
- Keep warnings visible.
- Prefer one Rich Message bubble.
- Keep tables readable on a phone.
- Use slideshow for sequence and collage for simultaneous comparison.
- Do not wrap one image in a slideshow.
- Use buttons only for a real action or choice.
- Preserve reply and topic context.
- Do not treat details or spoilers as secret protection.

## Client QA

Test Android, iOS, and Desktop in light and dark themes. Repeat with an increased system font. Include forwarded headers, reply headers, forum topics, link colors, button placement, anchors, nested details, hidden media, media spoilers, narrow screens, and long table values.

Buttons are outside the Rich Message card and use interface colors. Do not assume a card color or exact radius. Do not align content with spaces.
