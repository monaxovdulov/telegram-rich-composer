"""Semantic composition and safe delivery for Telegram Rich Messages."""

from .negotiate import CapabilitySet, DeliveryPlan, negotiate
from .render import render
from .selector import select_composition
from .validator import ValidationIssue, ValidationReport, validate_spec

__all__ = [
    "CapabilitySet",
    "DeliveryPlan",
    "ValidationIssue",
    "ValidationReport",
    "negotiate",
    "render",
    "select_composition",
    "validate_spec",
]

__version__ = "0.1.0"
