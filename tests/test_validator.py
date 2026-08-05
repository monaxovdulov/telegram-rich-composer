from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from telegram_rich_composer.validator import validate_spec


def codes(report):
    return {issue.code for issue in report.issues}


def test_every_golden_example_is_valid():
    root = Path(__file__).resolve().parents[1] / "examples" / "golden"
    import json

    for path in root.glob("*.json"):
        report = validate_spec(json.loads(path.read_text(encoding="utf-8")))
        assert report.valid, (path.name, report.as_dict())


def test_readme_workout_example_is_valid():
    import json

    path = Path(__file__).resolve().parents[1] / "examples" / "readme" / "workout-meme.json"
    report = validate_spec(json.loads(path.read_text(encoding="utf-8")))
    assert report.valid, report.as_dict()


def test_recipient_data_is_rejected(load_golden):
    spec = load_golden("ticket-table")
    spec["chat_id"] = -100123
    assert not validate_spec(spec).valid


def test_showcase_requires_explicit_request(load_golden):
    spec = load_golden("preset-issue")
    spec["selection"]["showcase_requested"] = False
    report = validate_spec(spec)
    assert "showcase_not_requested" in codes(report)


def test_local_path_must_be_inside_adapter_root(load_golden, tmp_path):
    spec = load_golden("museum-drawers")
    spec["surface"]["capabilities"]["controlled_local_upload"] = True
    spec["media"][0]["source"] = {"type": "local_path", "path": "/etc/passwd"}
    report = validate_spec(spec, allowed_media_roots=(tmp_path,), check_local_files=True)
    assert {"local_media_outside_root"} <= codes(report)


def test_local_path_needs_capability_and_root(load_golden):
    spec = load_golden("museum-drawers")
    spec["media"][0]["source"] = {"type": "local_path", "path": "/tmp/image.png"}
    report = validate_spec(spec)
    assert {"local_upload_not_allowed", "local_media_roots_missing"} <= codes(report)


def test_http_media_is_rejected(load_golden):
    spec = load_golden("museum-drawers")
    spec["media"][0]["source"] = {"type": "url", "url": "http://example.com/a.jpg"}
    assert "insecure_media_url" in codes(validate_spec(spec))


def test_unsafe_inline_link_is_rejected(load_golden):
    spec = load_golden("ticket-table")
    spec["blocks"][0]["text"] = [
        {"type": "link", "content": "unsafe", "href": "http://127.0.0.1/private"}
    ]
    assert "unsafe_inline_url" in codes(validate_spec(spec))


def test_thinking_is_draft_only(load_golden):
    spec = load_golden("ticket-table")
    spec["blocks"] = [{"type": "thinking", "text": "Working"}]
    assert "thinking_in_final" in codes(validate_spec(spec))


@pytest.mark.parametrize(
    ("width", "height", "expected"),
    [(9000, 2000, "map_size_sum"), (1000, 20, "map_aspect_ratio")],
)
def test_map_constraints(load_golden, width, height, expected):
    spec = load_golden("map-cover")
    spec["blocks"][0].update(width=width, height=height)
    assert expected in codes(validate_spec(spec))


def test_unknown_media_binding(load_golden):
    spec = load_golden("museum-drawers")
    spec["blocks"][0]["media_id"] = "missing"
    assert "unknown_media_id" in codes(validate_spec(spec))


def test_unknown_anchor_target(load_golden):
    spec = load_golden("hypertext-journal")
    spec["blocks"][0]["text"][0]["target"] = "missing"
    assert "unknown_anchor_target" in codes(validate_spec(spec))


def test_telegram_character_limit(load_golden):
    spec = load_golden("ticket-table")
    spec["blocks"] = [{"type": "paragraph", "text": "x" * 32768}]
    assert "characters_limit" in codes(validate_spec(spec))


def test_calm_table_budget_is_warning(load_golden):
    spec = deepcopy(load_golden("ticket-table"))
    spec["selection"]["density"] = "calm"
    spec["blocks"][1]["rows"] = [[{"text": "A"}, {"text": "B"}, {"text": "C"}]]
    report = validate_spec(spec)
    assert report.valid
    assert "calm_table_columns" in codes(report)
