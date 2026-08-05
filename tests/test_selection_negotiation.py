from __future__ import annotations

import pytest

from telegram_rich_composer.negotiate import CapabilitySet, negotiate
from telegram_rich_composer.selector import select_composition


def test_short_chat_stays_plain():
    result = select_composition({"intent": "answer", "complexity": "low"})
    assert result.mode == "plain"
    assert result.density == "calm"


def test_structure_selects_rich():
    result = select_composition({"intent": "comparison", "needs_structure": True})
    assert result.mode == "rich"
    assert result.pattern == "comparison-matrix"


def test_group_reduces_density():
    result = select_composition({"intent": "report", "group_chat": True})
    assert result.mode == "rich"
    assert result.density == "calm"


def test_explicit_showcase_is_respected():
    result = select_composition({"intent": "showcase", "user_requested_rich": True})
    assert result.density == "showcase"
    assert result.showcase_requested


def test_negotiation_follows_declared_ladder(load_golden):
    spec = load_golden("ticket-table")
    caps = CapabilitySet(rich_html=True, legacy_html=True)
    plan = negotiate(spec, caps)
    assert plan.selected == "rich_html"
    assert plan.attempts[:2] == ("rich_html", "legacy_html")
    assert plan.as_dict()["reason"] == "highest_supported_route"


def test_capabilities_round_trip():
    caps = CapabilitySet.from_mapping({"rich_blocks": True, "legacy_html": False})
    assert caps.supports("rich_blocks")
    assert caps.as_dict()["legacy_html"] is False


def test_plain_selection_skips_rich_routes(load_golden):
    spec = load_golden("ticket-table")
    spec["selection"]["mode"] = "plain"
    plan = negotiate(spec, CapabilitySet(legacy_html=True))
    assert plan.selected == "legacy_html"
    assert plan.reason == "plain_selected"


def test_negotiation_fails_closed(load_golden):
    spec = load_golden("ticket-table")
    caps = CapabilitySet(
        legacy_html=False,
        legacy_markdown=False,
        plain_album=False,
    )
    with pytest.raises(ValueError, match="No supported"):
        negotiate(spec, caps)
