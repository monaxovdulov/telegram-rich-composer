"""Capability negotiation and deterministic fallback planning."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class CapabilitySet:
    rich_blocks: bool = False
    rich_markdown: bool = False
    rich_html: bool = False
    legacy_html: bool = True
    legacy_markdown: bool = True
    plain_album: bool = True
    controlled_local_upload: bool = False
    details_nested_media: bool = False
    media_spoiler: bool = False
    rich_draft_streaming: bool = False
    reply_parameters: bool = True
    reply_markup: bool = True
    topics: bool = True
    direct_message_topics: bool = True

    @classmethod
    def from_mapping(cls, values: Mapping[str, bool] | None) -> CapabilitySet:
        values = values or {}
        fields = cls.__dataclass_fields__
        return cls(
            **{name: bool(values.get(name, field.default)) for name, field in fields.items()}
        )

    def supports(self, target: str) -> bool:
        return bool(getattr(self, target, False))

    def as_dict(self) -> dict[str, bool]:
        return {name: bool(getattr(self, name)) for name in self.__dataclass_fields__}


@dataclass(frozen=True, slots=True)
class DeliveryPlan:
    selected: str
    attempts: tuple[str, ...]
    feature_loss: bool
    reason: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "selected": self.selected,
            "attempts": list(self.attempts),
            "feature_loss": self.feature_loss,
            "reason": self.reason,
        }


def negotiate(
    spec: Mapping[str, Any], capabilities: CapabilitySet | Mapping[str, bool] | None = None
) -> DeliveryPlan:
    """Choose the first supported route from the declared ladder.

    The adapter owns the authoritative capability set. Surface capabilities in the
    spec are advisory and used only when an explicit set is not supplied.
    """
    if capabilities is None:
        capabilities = spec.get("surface", {}).get("capabilities", {})
    caps = (
        capabilities
        if isinstance(capabilities, CapabilitySet)
        else CapabilitySet.from_mapping(capabilities)
    )
    selection = spec.get("selection", {})
    if selection.get("mode") == "plain":
        plain_routes = ("legacy_html", "legacy_markdown", "plain_album")
        supported = tuple(route for route in plain_routes if caps.supports(route))
        chosen = supported[0] if supported else "plain_album"
        return DeliveryPlan(
            chosen, supported or (chosen,), chosen == "plain_album", "plain_selected"
        )

    ladder = tuple(
        spec.get("fallback", {}).get("ladder", ("rich_blocks", "legacy_html", "plain_album"))
    )
    supported = tuple(route for route in ladder if caps.supports(route))
    if not supported:
        raise ValueError("No supported delivery route in the fallback ladder")
    selected = supported[0]
    return DeliveryPlan(
        selected=selected,
        attempts=supported,
        feature_loss=selected not in {"rich_blocks", "rich_markdown", "rich_html"},
        reason="highest_supported_route",
    )
