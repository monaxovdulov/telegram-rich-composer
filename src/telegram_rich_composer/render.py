"""Render CompositionSpec to Telegram rich blocks or graceful text fallbacks."""

from __future__ import annotations

import html
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class RenderedComposition:
    target: str
    rich_message: dict[str, Any] | None
    text: str | None
    parse_mode: str | None
    media: tuple[dict[str, Any], ...]

    def as_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {"target": self.target}
        if self.rich_message is not None:
            result["rich_message"] = self.rich_message
        if self.text is not None:
            result["text"] = self.text
        if self.parse_mode is not None:
            result["parse_mode"] = self.parse_mode
        if self.media:
            result["media"] = list(self.media)
        return result


def _inline(value: Any) -> Any:
    if isinstance(value, str):
        return value
    result: list[Any] = []
    type_map = {"mark": "marked"}
    for node in value:
        kind = node["type"]
        if kind == "text":
            result.append(node["text"])
        elif kind in {
            "bold",
            "italic",
            "underline",
            "strikethrough",
            "spoiler",
            "mark",
            "code",
            "subscript",
            "superscript",
        }:
            result.append({"type": type_map.get(kind, kind), "text": _inline(node["content"])})
        elif kind == "link":
            result.append({"type": "url", "text": _inline(node["content"]), "url": node["href"]})
        elif kind == "anchor_link":
            result.append(
                {
                    "type": "anchor_link",
                    "text": _inline(node["content"]),
                    "anchor_name": node["target"],
                }
            )
        elif kind == "reference":
            result.append(
                {"type": "reference", "text": _inline(node["content"]), "name": node["name"]}
            )
        elif kind == "reference_link":
            result.append(
                {
                    "type": "reference_link",
                    "text": _inline(node["content"]),
                    "reference_name": node["target"],
                }
            )
        elif kind == "custom_emoji":
            result.append(
                {
                    "type": "custom_emoji",
                    "custom_emoji_id": node["custom_emoji_id"],
                    "alternative_text": node["alt"],
                }
            )
        elif kind == "formula":
            result.append({"type": "mathematical_expression", "expression": node["expression"]})
    return result


def _caption(value: Mapping[str, Any] | None) -> dict[str, Any] | None:
    if not value:
        return None
    output = {"text": _inline(value["text"])}
    if "credit" in value:
        output["credit"] = _inline(value["credit"])
    return output


def _input_media(media: Mapping[str, Any]) -> dict[str, Any]:
    source = media["source"]
    value = source.get("file_id") or source.get("url") or f"attach://{media['id']}"
    kind = media["kind"]
    result = {"type": kind, "media": value}
    if media.get("mime_type"):
        result["mime_type"] = media["mime_type"]
    return result


def _rich_message_media(media: Mapping[str, Any]) -> dict[str, Any]:
    return {"id": media["id"], "media": _input_media(media)}


def _block(block: Mapping[str, Any], media: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    kind = block["type"]
    if kind == "paragraph":
        return {"type": "paragraph", "text": _inline(block["text"])}
    if kind == "heading":
        return {"type": "heading", "text": _inline(block["text"]), "size": block["level"]}
    if kind == "divider":
        return {"type": "divider"}
    if kind in {"code", "preformatted"}:
        output = {"type": "pre", "text": block["text"]}
        if block.get("language"):
            output["language"] = block["language"]
        return output
    if kind == "formula":
        return {"type": "mathematical_expression", "expression": block["expression"]}
    if kind == "footer":
        return {"type": "footer", "text": _inline(block["text"])}
    if kind == "anchor":
        return {"type": "anchor", "name": block["name"]}
    if kind in {"list", "checklist"}:
        items = []
        for item in block["items"]:
            item_blocks = [{"type": "paragraph", "text": _inline(item["text"])}]
            item_blocks.extend(_block(child, media) for child in item.get("blocks", []))
            rendered = {"blocks": item_blocks}
            if kind == "checklist":
                rendered.update(has_checkbox=True, is_checked=bool(item.get("checked")))
            for source, target in (("value", "value"),):
                if source in item:
                    rendered[target] = item[source]
            if block.get("marker_type"):
                rendered["type"] = block["marker_type"]
            elif block.get("ordered"):
                rendered["type"] = "1"
            if block.get("ordered") and "value" not in rendered:
                offset = len(items)
                default_start = len(block["items"]) if block.get("reversed") else 1
                start = block.get("start", default_start)
                rendered["value"] = start - offset if block.get("reversed") else start + offset
            items.append(rendered)
        return {"type": "list", "items": items}
    if kind == "quote":
        output = {
            "type": "blockquote",
            "blocks": [_block(child, media) for child in block["blocks"]],
        }
        if "credit" in block:
            output["credit"] = _inline(block["credit"])
        return output
    if kind == "pull_quote":
        output = {"type": "pullquote", "text": _inline(block["text"])}
        if "credit" in block:
            output["credit"] = _inline(block["credit"])
        return output
    if kind == "table":
        cells = []
        for row in block["rows"]:
            rendered_row = []
            for cell in row:
                item = {"text": _inline(cell["text"])}
                mapping = {
                    "header": "is_header",
                    "colspan": "colspan",
                    "rowspan": "rowspan",
                    "align": "align",
                    "valign": "valign",
                }
                item.update(
                    {target: cell[source] for source, target in mapping.items() if source in cell}
                )
                rendered_row.append(item)
            cells.append(rendered_row)
        output = {"type": "table", "cells": cells}
        if block.get("bordered"):
            output["is_bordered"] = True
        if block.get("striped"):
            output["is_striped"] = True
        if "caption" in block:
            output["caption"] = _inline(block["caption"])
        return output
    if kind == "details":
        return {
            "type": "details",
            "summary": _inline(block["summary"]),
            "blocks": [_block(child, media) for child in block["blocks"]],
            "is_open": block["open"],
        }
    if kind == "map":
        output = {
            "type": "map",
            "location": {"latitude": block["latitude"], "longitude": block["longitude"]},
            "zoom": block["zoom"],
            "width": block["width"],
            "height": block["height"],
        }
        if "caption" in block:
            output["caption"] = _caption(block["caption"])
        return output
    if kind in {"collage", "slideshow"}:
        output = {"type": kind, "blocks": [_block(child, media) for child in block["blocks"]]}
        if "caption" in block:
            output["caption"] = _caption(block["caption"])
        return output
    if kind in {"photo", "video", "animation", "audio", "voice_note"}:
        field = kind
        output = {"type": kind, field: _input_media(media[block["media_id"]])}
        if "caption" in block:
            output["caption"] = _caption(block["caption"])
        if block.get("spoiler"):
            output[field]["has_spoiler"] = True
        return output
    if kind == "thinking":
        return {"type": "thinking", "text": _inline(block["text"])}
    raise ValueError(f"Unsupported block type: {kind}")


def _plain_inline(value: Any) -> str:
    if isinstance(value, str):
        return value
    chunks = []
    for node in value:
        if "content" in node:
            chunks.append(_plain_inline(node["content"]))
        elif node["type"] == "text":
            chunks.append(node["text"])
        elif node["type"] == "custom_emoji":
            chunks.append(node["alt"])
        elif node["type"] == "formula":
            chunks.append(node["expression"])
    return "".join(chunks)


def _plain_blocks(blocks: list[Mapping[str, Any]], depth: int = 0) -> list[str]:
    lines: list[str] = []
    for block in blocks:
        kind = block["type"]
        if kind in {"paragraph", "heading", "footer", "thinking", "pull_quote"}:
            lines.append(_plain_inline(block["text"]))
        elif kind == "divider":
            lines.append("—")
        elif kind in {"code", "preformatted"}:
            lines.append(block["text"])
        elif kind == "formula":
            lines.append(block["expression"])
        elif kind in {"list", "checklist"}:
            for index, item in enumerate(block["items"], 1):
                if kind == "checklist":
                    marker = "☑" if item.get("checked") else "☐"
                elif block.get("ordered"):
                    marker = f"{index}."
                else:
                    marker = "•"
                lines.append(f"{'  ' * depth}{marker} {_plain_inline(item['text'])}")
                lines.extend(_plain_blocks(item.get("blocks", []), depth + 1))
        elif kind in {"quote", "details"}:
            if kind == "details":
                lines.append(_plain_inline(block["summary"]))
            lines.extend(_plain_blocks(block["blocks"], depth + 1))
        elif kind == "table":
            for row in block["rows"]:
                lines.append(" | ".join(_plain_inline(cell["text"]) for cell in row))
        elif kind == "map":
            lines.append(f"Map: {block['latitude']}, {block['longitude']}")
        elif kind in {"collage", "slideshow"}:
            lines.extend(_plain_blocks(block["blocks"], depth + 1))
        elif kind in {"photo", "video", "animation", "audio", "voice_note"}:
            caption = block.get("caption")
            lines.append(_plain_inline(caption["text"]) if caption else f"[{kind}]")
    return lines


def render(spec: Mapping[str, Any], target: str = "rich_blocks") -> RenderedComposition:
    """Render a validated spec to one negotiated target."""
    media_index = {item["id"]: item for item in spec.get("media", [])}
    if target == "rich_blocks":
        rich = {"blocks": [_block(block, media_index) for block in spec["blocks"]]}
        if spec["delivery"]["entity_detection"] == "explicit_only":
            rich["skip_entity_detection"] = True
        return RenderedComposition(target, rich, None, None, ())

    plain = (
        "\n\n".join(line for line in _plain_blocks(spec["blocks"]) if line).strip()
        or spec["summary"]
    )
    media = tuple(_rich_message_media(item) for item in spec.get("media", []))
    if target == "rich_markdown":
        media_lines = []
        for item in spec.get("media", []):
            scheme = "audio" if item["kind"] in {"audio", "voice_note"} else item["kind"]
            media_lines.append(f"[Media](tg://{scheme}?id={item['id']})")
        if media_lines:
            plain = plain + "\n\n" + "\n".join(media_lines)
        rich = {"markdown": plain}
        if spec["delivery"]["entity_detection"] == "explicit_only":
            rich["skip_entity_detection"] = True
        if media:
            rich["media"] = list(media)
        return RenderedComposition(
            target,
            rich,
            None,
            None,
            media,
        )
    if target == "rich_html":
        value = "<p>" + html.escape(plain).replace("\n\n", "</p><p>").replace("\n", "<br>") + "</p>"
        tags = []
        for item in spec.get("media", []):
            scheme = "audio" if item["kind"] in {"audio", "voice_note"} else item["kind"]
            tag = "img" if item["kind"] == "photo" else scheme
            tags.append(f'<{tag} src="tg://{scheme}?id={item["id"]}"></{tag}>')
        if tags:
            value += "".join(tags)
        rich = {"html": value}
        if spec["delivery"]["entity_detection"] == "explicit_only":
            rich["skip_entity_detection"] = True
        if media:
            rich["media"] = list(media)
        return RenderedComposition(
            target,
            rich,
            None,
            None,
            media,
        )
    if target == "legacy_html":
        return RenderedComposition(target, None, html.escape(plain), "HTML", media)
    if target == "legacy_markdown":
        return RenderedComposition(target, None, plain, "MarkdownV2", media)
    if target == "plain_album":
        return RenderedComposition(target, None, plain, None, media)
    raise ValueError(f"Unknown render target: {target}")
