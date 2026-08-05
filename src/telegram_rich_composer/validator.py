"""JSON Schema, Telegram limit, editorial, and safety validation."""

from __future__ import annotations

import ipaddress
import json
import socket
from collections.abc import Iterable
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Literal
from urllib.parse import urlsplit

from jsonschema import Draft202012Validator

from .model import (
    MEDIA_BLOCK_TYPES,
    RICH_MESSAGE_BLOCK_LIMIT,
    RICH_MESSAGE_CHARACTER_LIMIT,
    RICH_MESSAGE_MEDIA_LIMIT,
    RICH_MESSAGE_NESTING_LIMIT,
    RICH_MESSAGE_TABLE_COLUMN_LIMIT,
    SCHEMA_PATH,
    iter_blocks,
)

Severity = Literal["error", "warning"]
FORBIDDEN_RECIPIENT_KEYS = {
    "chat_id",
    "recipient",
    "recipient_id",
    "target_chat",
    "target_chat_id",
    "bot_token",
}


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    severity: Severity
    code: str
    message: str
    path: str = "$"

    def as_dict(self) -> dict[str, str]:
        return {
            "severity": self.severity,
            "code": self.code,
            "message": self.message,
            "path": self.path,
        }


@dataclass(frozen=True, slots=True)
class ValidationReport:
    issues: tuple[ValidationIssue, ...]
    character_count: int
    block_count: int
    nesting_depth: int
    media_count: int

    @property
    def valid(self) -> bool:
        return not any(issue.severity == "error" for issue in self.issues)

    @property
    def errors(self) -> tuple[ValidationIssue, ...]:
        return tuple(issue for issue in self.issues if issue.severity == "error")

    @property
    def warnings(self) -> tuple[ValidationIssue, ...]:
        return tuple(issue for issue in self.issues if issue.severity == "warning")

    def as_dict(self) -> dict[str, Any]:
        return {
            "valid": self.valid,
            "issues": [issue.as_dict() for issue in self.issues],
            "metrics": {
                "characters": self.character_count,
                "blocks": self.block_count,
                "nesting_depth": self.nesting_depth,
                "media": self.media_count,
            },
        }


@lru_cache(maxsize=1)
def _schema_validator() -> Draft202012Validator:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def _json_path(parts: Iterable[Any]) -> str:
    path = "$"
    for part in parts:
        path += f"[{part}]" if isinstance(part, int) else f".{part}"
    return path


def _walk_values(value: Any, path: str = "$") -> Iterable[tuple[str, Any]]:
    yield path, value
    if isinstance(value, dict):
        for key, child in value.items():
            yield from _walk_values(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _walk_values(child, f"{path}[{index}]")


def _rich_text_strings(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
        return
    if not isinstance(value, list):
        return
    for node in value:
        if not isinstance(node, dict):
            continue
        if node.get("type") == "text":
            yield str(node.get("text", ""))
        if "content" in node:
            yield from _rich_text_strings(node["content"])
        if node.get("type") == "custom_emoji":
            yield str(node.get("alt", ""))
        if node.get("type") == "formula":
            yield str(node.get("expression", ""))


def _block_text_strings(block: dict[str, Any]) -> Iterable[str]:
    kind = block.get("type")
    for key in ("text", "summary", "credit"):
        if key in block:
            yield from _rich_text_strings(block[key])
    if kind == "formula":
        yield str(block.get("expression", ""))
    caption = block.get("caption")
    if isinstance(caption, dict):
        yield from _rich_text_strings(caption.get("text", ""))
        yield from _rich_text_strings(caption.get("credit", ""))
    elif caption is not None:
        yield from _rich_text_strings(caption)
    for item in block.get("items", []):
        if isinstance(item, dict):
            yield from _rich_text_strings(item.get("text", ""))
            for nested in item.get("blocks", []):
                yield from _block_text_strings(nested)
    for row in block.get("rows", []):
        for cell in row:
            if isinstance(cell, dict):
                yield from _rich_text_strings(cell.get("text", ""))
    for nested in block.get("blocks", []):
        yield from _block_text_strings(nested)


def _character_count(spec: dict[str, Any]) -> int:
    blocks = spec.get("blocks", [])
    parts = list(_rich_text_strings(spec.get("summary", "")))
    for block in blocks:
        if isinstance(block, dict):
            parts.extend(_block_text_strings(block))
    return sum(len(part) for part in parts)


def _block_count(blocks: list[dict[str, Any]]) -> int:
    count = 0
    for block in blocks:
        count += 1
        if block.get("type") in {"list", "checklist"}:
            count += len(block.get("items", []))
        if block.get("type") == "table":
            count += len(block.get("rows", []))
        count += _block_count(block.get("blocks", []))
        for item in block.get("items", []):
            count += _block_count(item.get("blocks", []))
    return count


def _inline_depth(value: Any, depth: int = 1) -> int:
    if not isinstance(value, list):
        return depth
    best = depth
    for node in value:
        if isinstance(node, dict) and "content" in node:
            best = max(best, _inline_depth(node["content"], depth + 1))
    return best


def _nesting_depth(blocks: list[dict[str, Any]], depth: int = 1) -> int:
    best = 0 if not blocks else depth
    for block in blocks:
        for key in ("text", "summary", "credit"):
            best = max(best, _inline_depth(block.get(key), depth))
        nested = block.get("blocks", [])
        if nested:
            best = max(best, _nesting_depth(nested, depth + 1))
        for item in block.get("items", []):
            best = max(best, _inline_depth(item.get("text"), depth + 1))
            if item.get("blocks"):
                best = max(best, _nesting_depth(item["blocks"], depth + 2))
        for row in block.get("rows", []):
            for cell in row:
                best = max(best, _inline_depth(cell.get("text"), depth + 1))
    return best


def _is_private_or_special_ip(host: str) -> bool:
    try:
        addresses = {ipaddress.ip_address(host)}
    except ValueError:
        try:
            addresses = {
                ipaddress.ip_address(item[4][0])
                for item in socket.getaddrinfo(host, None, type=socket.SOCK_STREAM)
            }
        except OSError:
            return True
    return any(
        address.is_private
        or address.is_loopback
        or address.is_link_local
        or address.is_multicast
        or address.is_reserved
        or address.is_unspecified
        for address in addresses
    )


def _path_is_within(path: Path, roots: tuple[Path, ...]) -> bool:
    resolved = path.resolve(strict=False)
    return any(resolved == root or root in resolved.parents for root in roots)


def _semantic_issues(
    spec: dict[str, Any],
    *,
    allowed_media_roots: tuple[Path, ...],
    check_local_files: bool,
    resolve_url_hosts: bool,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    blocks = spec.get("blocks", [])
    capabilities = spec.get("surface", {}).get("capabilities", {})

    for path, value in _walk_values(spec):
        if isinstance(value, dict):
            for key in FORBIDDEN_RECIPIENT_KEYS & value.keys():
                issues.append(
                    ValidationIssue(
                        "error",
                        "recipient_in_spec",
                        f"CompositionSpec must not contain {key}; bind recipients in the adapter.",
                        f"{path}.{key}",
                    )
                )
            if value.get("type") == "link":
                href = value.get("href", "")
                split = urlsplit(href)
                unsafe_link = (
                    split.scheme != "https"
                    or not split.hostname
                    or split.username
                    or split.password
                )
                if unsafe_link:
                    issues.append(
                        ValidationIssue(
                            "error",
                            "unsafe_inline_url",
                            "Inline links must use HTTPS, include a host, and omit credentials.",
                            f"{path}.href",
                        )
                    )
                elif resolve_url_hosts and _is_private_or_special_ip(split.hostname):
                    issues.append(
                        ValidationIssue(
                            "error",
                            "private_inline_url",
                            "Inline link resolves to a private or special address.",
                            f"{path}.href",
                        )
                    )

    if spec.get("selection", {}).get("mode") == "rich" and not blocks:
        issues.append(
            ValidationIssue(
                "error", "rich_without_blocks", "Rich mode requires blocks.", "$.blocks"
            )
        )
    if spec.get("selection", {}).get("mode") == "plain" and blocks:
        issues.append(
            ValidationIssue(
                "warning",
                "plain_ignores_rich_blocks",
                "Plain mode keeps the summary and may ignore rich-only blocks.",
                "$.blocks",
            )
        )

    if spec.get("selection", {}).get("density") == "showcase" and not spec.get("selection", {}).get(
        "showcase_requested", False
    ):
        issues.append(
            ValidationIssue(
                "error",
                "showcase_not_requested",
                "Showcase density requires an explicit demo or user request.",
                "$.selection.density",
            )
        )

    media_items = spec.get("media", [])
    media_by_id: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(media_items):
        media_id = item.get("id")
        if media_id in media_by_id:
            issues.append(
                ValidationIssue(
                    "error",
                    "duplicate_media_id",
                    f"Media id {media_id!r} is not unique.",
                    f"$.media[{index}].id",
                )
            )
        media_by_id[media_id] = item
        source = item.get("source", {})
        source_type = source.get("type")
        if source_type == "url":
            url = source.get("url", "")
            split = urlsplit(url)
            if split.scheme != "https":
                issues.append(
                    ValidationIssue(
                        "error",
                        "insecure_media_url",
                        "Media URLs must use HTTPS by default.",
                        f"$.media[{index}].source.url",
                    )
                )
            if split.username or split.password or not split.hostname:
                issues.append(
                    ValidationIssue(
                        "error",
                        "unsafe_media_url",
                        "Media URL must not contain credentials and must have a host.",
                        f"$.media[{index}].source.url",
                    )
                )
            elif resolve_url_hosts and _is_private_or_special_ip(split.hostname):
                issues.append(
                    ValidationIssue(
                        "error",
                        "private_media_url",
                        "Media URL resolves to a private or special address.",
                        f"$.media[{index}].source.url",
                    )
                )
        elif source_type == "local_path":
            path = Path(source.get("path", ""))
            if not capabilities.get("controlled_local_upload", False):
                issues.append(
                    ValidationIssue(
                        "error",
                        "local_upload_not_allowed",
                        "Local media needs controlled_local_upload capability.",
                        f"$.media[{index}].source.path",
                    )
                )
            if not allowed_media_roots:
                issues.append(
                    ValidationIssue(
                        "error",
                        "local_media_roots_missing",
                        "Local media needs at least one adapter-owned allowed root.",
                        f"$.media[{index}].source.path",
                    )
                )
            elif not _path_is_within(path, allowed_media_roots):
                issues.append(
                    ValidationIssue(
                        "error",
                        "local_media_outside_root",
                        "Local media is outside the adapter-owned allowed roots.",
                        f"$.media[{index}].source.path",
                    )
                )
            if check_local_files and (not path.exists() or not path.is_file()):
                issues.append(
                    ValidationIssue(
                        "error",
                        "local_media_not_file",
                        "Local media path must resolve to a regular file.",
                        f"$.media[{index}].source.path",
                    )
                )

    anchors: set[str] = set()
    anchor_links: list[tuple[str, str]] = []
    references: set[str] = set()
    reference_links: list[tuple[str, str]] = []
    flattened = list(iter_blocks(blocks))
    for index, block in enumerate(flattened):
        kind = block.get("type")
        if kind == "anchor":
            name = block.get("name", "")
            if name in anchors:
                issues.append(
                    ValidationIssue(
                        "error", "duplicate_anchor", f"Anchor {name!r} is not unique.", "$.blocks"
                    )
                )
            anchors.add(name)
            if index + 1 >= len(flattened) or flattened[index + 1].get("type") not in {
                "heading",
                "details",
            }:
                issues.append(
                    ValidationIssue(
                        "error",
                        "anchor_not_before_visible_row",
                        "An anchor must be directly before a visible heading or details row.",
                        "$.blocks",
                    )
                )
        if kind in MEDIA_BLOCK_TYPES:
            media_id = block.get("media_id")
            item = media_by_id.get(media_id)
            if item is None:
                issues.append(
                    ValidationIssue(
                        "error",
                        "unknown_media_id",
                        f"Block references missing media id {media_id!r}.",
                        "$.blocks",
                    )
                )
            elif item.get("kind") != kind:
                issues.append(
                    ValidationIssue(
                        "error",
                        "media_kind_mismatch",
                        f"Block type {kind!r} does not match media kind {item.get('kind')!r}.",
                        "$.blocks",
                    )
                )
            if block.get("spoiler") and not capabilities.get("media_spoiler", False):
                issues.append(
                    ValidationIssue(
                        "warning",
                        "media_spoiler_unsupported",
                        "The adapter must remove the media spoiler or use another representation.",
                        "$.blocks",
                    )
                )
        if kind == "thinking" and not spec.get("surface", {}).get("is_draft"):
            issues.append(
                ValidationIssue(
                    "error",
                    "thinking_in_final",
                    "Thinking blocks are valid only in temporary rich drafts.",
                    "$.blocks",
                )
            )
        if kind == "map":
            width = block.get("width", 0)
            height = block.get("height", 0)
            if width + height > 10_000:
                issues.append(
                    ValidationIssue(
                        "error",
                        "map_size_sum",
                        "Map width and height must not exceed 10000 in total.",
                        "$.blocks",
                    )
                )
            if min(width, height) and max(width, height) / min(width, height) > 20:
                issues.append(
                    ValidationIssue(
                        "error",
                        "map_aspect_ratio",
                        "Map width-to-height ratio must not exceed 20.",
                        "$.blocks",
                    )
                )
        if kind == "table":
            for row_index, row in enumerate(block.get("rows", [])):
                columns = sum(cell.get("colspan", 1) for cell in row)
                if columns > RICH_MESSAGE_TABLE_COLUMN_LIMIT:
                    issues.append(
                        ValidationIssue(
                            "error",
                            "table_columns_limit",
                            f"Table row has {columns} columns; Telegram allows 20.",
                            f"$.blocks.table.rows[{row_index}]",
                        )
                    )
        _collect_inline_links(
            block, anchor_links=anchor_links, references=references, reference_links=reference_links
        )

    for path, target in anchor_links:
        if target and target not in anchors:
            issues.append(
                ValidationIssue(
                    "error",
                    "unknown_anchor_target",
                    f"Anchor target {target!r} does not exist.",
                    path,
                )
            )
    for path, target in reference_links:
        if target not in references:
            issues.append(
                ValidationIssue(
                    "error",
                    "unknown_reference_target",
                    f"Reference target {target!r} does not exist.",
                    path,
                )
            )

    if _contains_media_inside_details(blocks) and not capabilities.get(
        "details_nested_media", False
    ):
        issues.append(
            ValidationIssue(
                "warning",
                "nested_media_unsupported",
                "Adapter must move media out of details or select another representation.",
                "$.blocks",
            )
        )

    issues.extend(_editorial_issues(spec, flattened))
    return issues


def _collect_inline_value(
    value: Any,
    *,
    path: str,
    anchor_links: list[tuple[str, str]],
    references: set[str],
    reference_links: list[tuple[str, str]],
) -> None:
    if not isinstance(value, list):
        return
    for index, node in enumerate(value):
        if not isinstance(node, dict):
            continue
        node_path = f"{path}[{index}]"
        kind = node.get("type")
        if kind == "anchor_link":
            anchor_links.append((node_path, node.get("target", "")))
        elif kind == "reference":
            references.add(node.get("name", ""))
        elif kind == "reference_link":
            reference_links.append((node_path, node.get("target", "")))
        _collect_inline_value(
            node.get("content"),
            path=f"{node_path}.content",
            anchor_links=anchor_links,
            references=references,
            reference_links=reference_links,
        )


def _collect_inline_links(
    block: dict[str, Any],
    *,
    anchor_links: list[tuple[str, str]],
    references: set[str],
    reference_links: list[tuple[str, str]],
) -> None:
    for key in ("text", "summary", "credit"):
        _collect_inline_value(
            block.get(key),
            path=f"$.blocks.{key}",
            anchor_links=anchor_links,
            references=references,
            reference_links=reference_links,
        )
    caption = block.get("caption")
    if isinstance(caption, dict):
        for key in ("text", "credit"):
            _collect_inline_value(
                caption.get(key),
                path=f"$.blocks.caption.{key}",
                anchor_links=anchor_links,
                references=references,
                reference_links=reference_links,
            )
    for item in block.get("items", []):
        _collect_inline_value(
            item.get("text"),
            path="$.blocks.items.text",
            anchor_links=anchor_links,
            references=references,
            reference_links=reference_links,
        )
    for row in block.get("rows", []):
        for cell in row:
            _collect_inline_value(
                cell.get("text"),
                path="$.blocks.rows.text",
                anchor_links=anchor_links,
                references=references,
                reference_links=reference_links,
            )


def _contains_media_inside_details(blocks: list[dict[str, Any]], in_details: bool = False) -> bool:
    for block in blocks:
        kind = block.get("type")
        now_in_details = in_details or kind == "details"
        if now_in_details and (kind in MEDIA_BLOCK_TYPES or kind in {"collage", "slideshow"}):
            return True
        if _contains_media_inside_details(block.get("blocks", []), now_in_details):
            return True
        for item in block.get("items", []):
            if _contains_media_inside_details(item.get("blocks", []), now_in_details):
                return True
    return False


def _editorial_issues(
    spec: dict[str, Any], flattened: list[dict[str, Any]]
) -> list[ValidationIssue]:
    if spec.get("selection", {}).get("density") != "calm":
        return []
    issues: list[ValidationIssue] = []
    counts: dict[str, int] = {}
    for block in flattened:
        kind = block.get("type", "")
        counts[kind] = counts.get(kind, 0) + 1
    h1 = sum(1 for block in flattened if block.get("type") == "heading" and block.get("level") == 1)
    if h1 > 1:
        issues.append(
            ValidationIssue("warning", "calm_h1_budget", "Calm density normally uses one H1.")
        )
    for kind, limit in {"divider": 3, "pull_quote": 1, "details": 5}.items():
        if counts.get(kind, 0) > limit:
            issues.append(
                ValidationIssue(
                    "warning",
                    f"calm_{kind}_budget",
                    f"Calm density normally uses no more than {limit} {kind} blocks.",
                )
            )
    table_blocks = [block for block in flattened if block.get("type") == "table"]
    if any(
        max((sum(cell.get("colspan", 1) for cell in row) for row in block["rows"]), default=0) > 2
        for block in table_blocks
    ):
        issues.append(
            ValidationIssue(
                "warning",
                "calm_table_columns",
                "Calm density prefers two table columns on a phone.",
            )
        )
    visible_media = sum(1 for block in flattened if block.get("type") in MEDIA_BLOCK_TYPES)
    if visible_media > 4:
        issues.append(
            ValidationIssue(
                "warning", "calm_visible_media", "Calm density normally shows two to four images."
            )
        )
    return issues


def validate_spec(
    spec: dict[str, Any],
    *,
    allowed_media_roots: Iterable[str | Path] = (),
    check_local_files: bool = False,
    resolve_url_hosts: bool = False,
) -> ValidationReport:
    """Validate a CompositionSpec without sending or uploading anything."""
    issues: list[ValidationIssue] = []
    for error in sorted(_schema_validator().iter_errors(spec), key=lambda item: list(item.path)):
        issues.append(
            ValidationIssue(
                "error",
                "schema",
                error.message,
                _json_path(error.absolute_path),
            )
        )

    blocks = spec.get("blocks", []) if isinstance(spec.get("blocks"), list) else []
    characters = _character_count(spec)
    block_count = _block_count(blocks)
    depth = _nesting_depth(blocks)
    media_count = len(spec.get("media", [])) if isinstance(spec.get("media"), list) else 0

    for value, limit, code, label, path in (
        (
            characters,
            RICH_MESSAGE_CHARACTER_LIMIT,
            "characters_limit",
            "characters",
            "$.blocks",
        ),
        (block_count, RICH_MESSAGE_BLOCK_LIMIT, "blocks_limit", "blocks", "$.blocks"),
        (depth, RICH_MESSAGE_NESTING_LIMIT, "nesting_limit", "nesting levels", "$.blocks"),
        (media_count, RICH_MESSAGE_MEDIA_LIMIT, "media_limit", "media attachments", "$.media"),
    ):
        if value > limit:
            issues.append(
                ValidationIssue(
                    "error",
                    code,
                    f"Composition has {value} {label}; Telegram allows {limit}.",
                    path,
                )
            )

    if not any(issue.code == "schema" for issue in issues):
        roots = tuple(Path(root).resolve(strict=False) for root in allowed_media_roots)
        issues.extend(
            _semantic_issues(
                spec,
                allowed_media_roots=roots,
                check_local_files=check_local_files,
                resolve_url_hosts=resolve_url_hosts,
            )
        )

    return ValidationReport(
        issues=tuple(issues),
        character_count=characters,
        block_count=block_count,
        nesting_depth=depth,
        media_count=media_count,
    )
