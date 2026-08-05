#!/usr/bin/env python3
"""Check bilingual document and pattern parity."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def headings(path: Path, prefix: str) -> set[str]:
    result = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^### ([a-z0-9][a-z0-9-]+)$", line)
        if match and match.group(1).startswith(prefix):
            result.add(match.group(1))
    return result


def main() -> int:
    en = {path.name for path in (ROOT / "docs" / "en").glob("*.md")}
    ru = {path.name for path in (ROOT / "docs" / "ru").glob("*.md")}
    if en != ru:
        raise SystemExit(f"Bilingual document mismatch: en-only={en - ru}, ru-only={ru - en}")
    golden = {path.stem for path in (ROOT / "examples" / "golden").glob("*.json")}
    expected = {
        "hypertext-journal",
        "museum-drawers",
        "marked-second-reading",
        "interactive-redaction",
        "ticket-table",
        "map-cover",
        "code-typography",
        "manual-animation",
        "hidden-sound-note",
        "title-pullquote",
        "emoji-glyph-system",
        "second-narrator-notes",
        "preset-issue",
        "preset-artifact",
        "preset-scene",
    }
    if golden != expected:
        raise SystemExit(
            f"Golden catalog mismatch: missing={expected - golden}, extra={golden - expected}"
        )
    print(f"docs parity ok: {len(en)} pairs; golden catalog ok: {len(golden)} specs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
