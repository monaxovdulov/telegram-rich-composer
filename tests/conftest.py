from __future__ import annotations

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
GOLDEN = ROOT / "examples" / "golden"


@pytest.fixture
def load_golden():
    def load(name: str) -> dict:
        return json.loads((GOLDEN / f"{name}.json").read_text(encoding="utf-8"))

    return load
