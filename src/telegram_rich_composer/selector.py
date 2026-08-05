"""Situational plain-versus-rich response selection."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

RICH_PATTERNS = {
    "comparison": "comparison-matrix",
    "tutorial": "step-by-step-tutorial",
    "incident": "incident-status",
    "report": "executive-brief",
    "gallery": "visual-gallery",
    "map": "location-brief",
    "decision": "decision-record",
    "release": "release-notes",
    "faq": "layered-faq",
    "dashboard": "compact-dashboard",
    "catalog": "curated-catalog",
    "showcase": "rich-showcase",
}


@dataclass(frozen=True, slots=True)
class Selection:
    mode: str
    pattern: str
    density: str
    reason_codes: tuple[str, ...]
    showcase_requested: bool = False

    def as_dict(self) -> dict[str, Any]:
        return {
            "mode": self.mode,
            "pattern": self.pattern,
            "density": self.density,
            "reason_codes": list(self.reason_codes),
            "showcase_requested": self.showcase_requested,
        }


def select_composition(context: Mapping[str, Any]) -> Selection:
    """Return a conservative, explainable composition choice.

    Expected hints are semantic rather than harness-specific: ``intent``,
    ``complexity`` (low/medium/high), ``has_media``, ``needs_structure``,
    ``user_requested_rich`` and ``group_chat``.
    """
    intent = str(context.get("intent", "answer")).lower()
    complexity = str(context.get("complexity", "low")).lower()
    requested = bool(context.get("user_requested_rich") or intent == "showcase")
    structured = bool(context.get("needs_structure"))
    media = bool(context.get("has_media"))
    reasons: list[str] = []
    if requested:
        reasons.append("user_requested_rich")
    if structured:
        reasons.append("structure_improves_scan")
    if media:
        reasons.append("media_is_semantic")
    if complexity == "high":
        reasons.append("high_information_density")

    rich = requested or structured or media or complexity == "high" or intent in RICH_PATTERNS
    if not rich:
        return Selection("plain", "conversational-answer", "calm", ("plain_is_clearer",))

    pattern = RICH_PATTERNS.get(intent, "structured-answer")
    density = "showcase" if requested else "standard"
    if context.get("group_chat") and not requested:
        density = "calm"
        reasons.append("group_noise_budget")
    return Selection("rich", pattern, density, tuple(dict.fromkeys(reasons)), requested)
