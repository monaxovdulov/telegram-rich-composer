from __future__ import annotations

import json
from pathlib import Path

import pytest

from telegram_rich_composer.render import render


def test_explicit_field_translation(load_golden):
    rendered = render(load_golden("ticket-table"), "rich_blocks").rich_message
    heading, table = rendered["blocks"]
    assert heading == {"type": "heading", "text": "Observation ticket", "size": 2}
    assert table["type"] == "table"
    assert "cells" in table and "rows" not in table
    assert table["is_bordered"] is True
    assert table["cells"][0][0]["is_header"] is True


def test_inline_field_translation(load_golden):
    rendered = render(load_golden("hypertext-journal"), "rich_blocks").rich_message
    first = rendered["blocks"][0]["text"][0]
    assert first["type"] == "anchor_link"
    assert first["anchor_name"] == "thesis"


def test_media_binding_uses_input_media(load_golden):
    rendered = render(load_golden("museum-drawers"), "rich_blocks").rich_message
    assert rendered["blocks"][0]["photo"] == {
        "type": "photo",
        "media": "telegram-hero",
    }


def test_spoiler_maps_to_input_media(load_golden):
    rendered = render(load_golden("interactive-redaction"), "rich_blocks").rich_message
    assert rendered["blocks"][1]["photo"]["has_spoiler"] is True


def test_voice_note_keeps_official_input_type(load_golden):
    rendered = render(load_golden("hidden-sound-note"), "rich_blocks").rich_message
    voice = rendered["blocks"][1]["blocks"][0]["voice_note"]
    assert voice["type"] == "voice_note"


def test_plain_fallback_preserves_readable_content(load_golden):
    rendered = render(load_golden("ticket-table"), "plain_album")
    assert rendered.parse_mode is None
    assert "Observation ticket" in rendered.text
    assert "Gate | C12" in rendered.text


def test_exactly_one_rich_input_representation(load_golden):
    for target, key in (
        ("rich_blocks", "blocks"),
        ("rich_markdown", "markdown"),
        ("rich_html", "html"),
    ):
        rich = render(load_golden("ticket-table"), target).rich_message
        assert key in rich
        assert len({"blocks", "markdown", "html"} & rich.keys()) == 1


def test_every_golden_renders_to_every_route():
    root = Path(__file__).resolve().parents[1] / "examples" / "golden"
    targets = (
        "rich_blocks",
        "rich_markdown",
        "rich_html",
        "legacy_html",
        "legacy_markdown",
        "plain_album",
    )
    for path in root.glob("*.json"):
        spec = json.loads(path.read_text(encoding="utf-8"))
        for target in targets:
            assert render(spec, target).target == target


def test_rendered_composition_serializes(load_golden):
    output = render(load_golden("museum-drawers"), "rich_html").as_dict()
    assert output["target"] == "rich_html"
    assert output["rich_message"]["media"][0]["id"] == "hero"


def test_unknown_route_fails(load_golden):
    with pytest.raises(ValueError, match="Unknown render target"):
        render(load_golden("ticket-table"), "unknown")


def test_auto_entity_detection_omits_skip_flag(load_golden):
    spec = load_golden("ticket-table")
    spec["delivery"]["entity_detection"] = "auto"
    assert "skip_entity_detection" not in render(spec, "rich_blocks").rich_message
