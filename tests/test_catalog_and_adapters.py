from __future__ import annotations

import json
import runpy
from pathlib import Path

from telegram_rich_composer.selector import select_composition

ROOT = Path(__file__).resolve().parents[1]


def test_selection_evals():
    path = ROOT / "examples" / "evals" / "selection.jsonl"
    for line in path.read_text(encoding="utf-8").splitlines():
        case = json.loads(line)
        actual = select_composition(case["context"]).as_dict()
        for key, value in case["expected"].items():
            assert actual[key] == value, case


def test_every_adapter_has_guidance_and_code():
    for name, code in (
        ("eve", "tool.ts"),
        ("iva", "routing.ts"),
        ("hermes", "plugin/plugin.py"),
        ("direct", None),
    ):
        adapter = ROOT / "adapters" / name
        assert (adapter / "README.md").is_file()
        if code:
            assert (adapter / code).is_file()


def test_hermes_unknown_delivery_policy():
    plugin = runpy.run_path(str(ROOT / "adapters" / "hermes" / "plugin" / "plugin.py"))
    assert plugin["may_fallback"](permanent=True, certainty="rejected")
    assert not plugin["may_fallback"](permanent=False, certainty="unknown")
