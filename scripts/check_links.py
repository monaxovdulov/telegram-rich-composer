#!/usr/bin/env python3
"""Check local Markdown links without making network requests."""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"(?<!!)\[[^]]*]\(([^)]+)\)")


def main() -> int:
    errors = []
    files = [ROOT / "SKILL.md", ROOT / "README.md", ROOT / "README.ru.md"]
    files.extend((ROOT / "docs").rglob("*.md"))
    files.extend((ROOT / "references").glob("*.md"))
    for path in files:
        text = path.read_text(encoding="utf-8")
        for raw in LINK.findall(text):
            target = raw.split("#", 1)[0].strip("<>")
            if not target or target.startswith(("https://", "http://", "mailto:")):
                continue
            resolved = (path.parent / unquote(target)).resolve()
            if not resolved.exists():
                errors.append(f"{path.relative_to(ROOT)} -> {raw}")
    if errors:
        raise SystemExit("Broken local links:\n" + "\n".join(errors))
    print(f"local links ok: {len(files)} Markdown files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
