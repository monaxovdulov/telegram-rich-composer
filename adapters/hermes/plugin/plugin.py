"""Hermes policy helpers; no recipient or network authority."""

from __future__ import annotations

from typing import Any

from telegram_rich_composer import select_composition


def should_attempt_rich(context: dict[str, Any]) -> bool:
    """Use the shared situational selector instead of an eager format heuristic."""
    return select_composition(context).mode == "rich"


def may_fallback(*, permanent: bool, certainty: str) -> bool:
    """Unknown delivery can duplicate a Telegram message, so it must stop."""
    return permanent and certainty == "rejected"
