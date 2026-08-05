#!/usr/bin/env python3
"""Small dependency-free JSON-RPC stdio bridge for MCP-capable harnesses.

It implements initialize, tools/list, and tools/call for validation, selection,
planning, and rendering. Network delivery intentionally remains adapter-owned.
"""

from __future__ import annotations

import json
import sys
from typing import Any

from telegram_rich_composer import negotiate, render, select_composition, validate_spec

TOOLS = [
    {
        "name": "telegram_rich_validate",
        "description": "Validate a CompositionSpec",
        "inputSchema": {
            "type": "object",
            "required": ["spec"],
            "properties": {"spec": {"type": "object"}},
        },
    },
    {
        "name": "telegram_rich_select",
        "description": "Choose plain or rich composition",
        "inputSchema": {
            "type": "object",
            "required": ["context"],
            "properties": {"context": {"type": "object"}},
        },
    },
    {
        "name": "telegram_rich_plan",
        "description": "Negotiate a supported delivery route",
        "inputSchema": {
            "type": "object",
            "required": ["spec"],
            "properties": {"spec": {"type": "object"}, "capabilities": {"type": "object"}},
        },
    },
    {
        "name": "telegram_rich_render",
        "description": "Render a CompositionSpec",
        "inputSchema": {
            "type": "object",
            "required": ["spec", "target"],
            "properties": {"spec": {"type": "object"}, "target": {"type": "string"}},
        },
    },
]


def _call(name: str, arguments: dict[str, Any]) -> Any:
    if name == "telegram_rich_validate":
        return validate_spec(arguments["spec"]).as_dict()
    if name == "telegram_rich_select":
        return select_composition(arguments["context"]).as_dict()
    if name == "telegram_rich_plan":
        return negotiate(arguments["spec"], arguments.get("capabilities")).as_dict()
    if name == "telegram_rich_render":
        return render(arguments["spec"], arguments["target"]).as_dict()
    raise ValueError(f"Unknown tool: {name}")


def main() -> None:
    for line in sys.stdin:
        request = json.loads(line)
        method = request.get("method")
        if method == "initialize":
            result = {
                "protocolVersion": "2025-06-18",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "telegram-rich-composer", "version": "0.1.0"},
            }
        elif method == "tools/list":
            result = {"tools": TOOLS}
        elif method == "tools/call":
            params = request.get("params", {})
            value = _call(params["name"], params.get("arguments", {}))
            result = {"content": [{"type": "text", "text": json.dumps(value, ensure_ascii=False)}]}
        elif method == "notifications/initialized":
            continue
        else:
            response = {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {"code": -32601, "message": "Method not found"},
            }
            print(json.dumps(response), flush=True)
            continue
        print(
            json.dumps(
                {"jsonrpc": "2.0", "id": request.get("id"), "result": result}, ensure_ascii=False
            ),
            flush=True,
        )


if __name__ == "__main__":
    main()
