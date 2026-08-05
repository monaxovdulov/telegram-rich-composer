# Test plan and release criteria

[Русская версия](../ru/test-plan.md)

## Test layers

1. Schema tests validate all examples and reject malformed specifications.
2. Unit tests cover selection, rendering, validation, media binding, and fallback.
3. Golden tests cover every catalog pattern and preset.
4. Adapter conformance tests run the same fixtures against Eve, Iva, Hermes, and direct adapters.
5. Safety tests cover recipient binding, allowlists, local media, secret patterns, and duplicate prevention.
6. Documentation tests check links, paired files, commands, and required sections.

## Required limit cases

Test the exact boundary and one value over the boundary for:

- 32,768 characters;
- 500 counted blocks;
- 16 nesting levels;
- 50 media attachments;
- 20 table columns.

Count nested blocks, list items, table rows, quotes, and details according to the Bot API description.

## Golden fixtures

Keep one accepted specification and one rendered output for each standard utility pattern, all 12 advanced patterns, and all three presets.

Advanced patterns:

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

## Selection evaluation

The eval set includes household questions, group discussion, technical diagnosis, research, decisions, tables, long logs, one diagram, multiple diagrams, collage comparison, slideshow sequence, anchors, nested details, hidden audio, controlled spoilers, custom emoji, references, link noise, and no-rich capability cases.

Each case declares:

- expected plain or rich mode;
- accepted pattern set;
- expected density profile;
- required visible summary text;
- forbidden hidden warnings;
- media relation: none, single, simultaneous, or sequence.

## Fallback tests

Test every edge in the degradation ladder. Confirm that the summary survives and unsupported features have readable replacements.

Test two network classes separately:

- a confirmed permanent rejection can produce one fallback send;
- an unknown result cannot produce another send until reconciliation.

## Entity and link tests

- Explicit links with `entity_detection: explicit_only` must set `skip_entity_detection`.
- Raw URLs with `entity_detection: auto` must not set it.
- Every anchor link must resolve or return a validation error.
- An anchor must be directly before a visible heading or details row.
- Return-to-index links must survive Rich HTML and explicit blocks.

## Media tests

- Bind Telegram `file_id` without downloading it.
- Accept safe HTTPS media.
- Reject unsafe and private-network URLs by default.
- Reject local paths without explicit permission.
- Resolve symlinks before allowed-root checks.
- Build multipart upload without a public hosting service.
- Keep caption, credit, and media spoiler data.
- Move nested media out of details when the adapter lacks that capability.
- Select collage for simultaneous comparison and slideshow for sequence.

## Density tests

`calm` is the default for groups. It must stay within the calm editorial budget or return clear warnings. `showcase` is valid only for an explicit demonstration, component catalog, or user request.

## Documentation checks

- Every required English document has a Russian peer.
- Paired documents contain the same commands, limits, capability names, and known limitations.
- English prose passes the repository ASD-STE100 principles checklist.
- Russian prose passes a humanizer-ru audit and has no lint `ERROR`.
- External links pass the link checker.

## Visual QA

Publish a matrix for Android, iOS, and Desktop. Include light and dark themes, normal and increased system font, forwarded headers, reply headers, topics, anchors, details, hidden media, spoilers, and narrow tables.

Mark each cell `verified`, `failed`, or `not tested`. Never convert `not tested` to a claim of support.

## Security and release gates

- Unit, golden, eval, adapter conformance, and documentation tests pass.
- Agent Skill package validation passes.
- Secret scanning passes for files and Git history.
- No `.env`, token, private chat ID, user data, database, log, or unlicensed media is present.
- The local repository has a clean status.
- Public CI passes on the release commit.
- The release report lists the repository URL, install commands, test commands, known limitations, source baselines, and differences from the prototype.
