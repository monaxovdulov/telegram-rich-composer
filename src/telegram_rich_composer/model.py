"""Shared constants and small model helpers."""

from __future__ import annotations

from collections.abc import Iterator
from importlib import resources
from pathlib import Path
from typing import Any

PACKAGE_ROOT = Path(__file__).resolve().parents[2]
_SOURCE_SCHEMA = PACKAGE_ROOT / "schemas" / "composition-spec.schema.json"
SCHEMA_PATH = (
    _SOURCE_SCHEMA
    if _SOURCE_SCHEMA.exists()
    else Path(
        str(
            resources.files("telegram_rich_composer").joinpath(
                "schemas/composition-spec.schema.json"
            )
        )
    )
)

RICH_MESSAGE_CHARACTER_LIMIT = 32_768
RICH_MESSAGE_BLOCK_LIMIT = 500
RICH_MESSAGE_NESTING_LIMIT = 16
RICH_MESSAGE_MEDIA_LIMIT = 50
RICH_MESSAGE_TABLE_COLUMN_LIMIT = 20
LEGACY_TEXT_LIMIT = 4096
ALBUM_ITEM_LIMIT = 10

MEDIA_BLOCK_TYPES = {"photo", "video", "animation", "audio", "voice_note"}
CONTAINER_BLOCK_TYPES = {"details", "quote", "collage", "slideshow"}


def iter_blocks(blocks: list[dict[str, Any]]) -> Iterator[dict[str, Any]]:
    """Yield all blocks depth-first, including nested list item blocks."""
    for block in blocks:
        yield block
        nested = block.get("blocks")
        if isinstance(nested, list):
            yield from iter_blocks(nested)
        for item in block.get("items", []):
            item_blocks = item.get("blocks") if isinstance(item, dict) else None
            if isinstance(item_blocks, list):
                yield from iter_blocks(item_blocks)
