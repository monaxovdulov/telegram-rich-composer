"""Command-line surface for skill and adapter harnesses."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .direct import TrustedConversationContext, build_request, send_request
from .negotiate import CapabilitySet, negotiate
from .render import render
from .selector import select_composition
from .validator import validate_spec


def _read_json(path: str) -> dict[str, Any]:
    if path == "-":
        return json.load(sys.stdin)
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _print(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True))


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="telegram-rich-composer")
    commands = parser.add_subparsers(dest="command", required=True)
    validate = commands.add_parser("validate", help="validate a CompositionSpec")
    validate.add_argument("spec")
    validate.add_argument("--media-root", action="append", default=[])
    validate.add_argument("--check-files", action="store_true")
    render_cmd = commands.add_parser("render", help="render a CompositionSpec")
    render_cmd.add_argument("spec")
    render_cmd.add_argument(
        "--target",
        default="rich_blocks",
        choices=[
            "rich_blocks",
            "rich_markdown",
            "rich_html",
            "legacy_html",
            "legacy_markdown",
            "plain_album",
        ],
    )
    plan = commands.add_parser("plan", help="negotiate a route")
    plan.add_argument("spec")
    plan.add_argument("--capability", action="append", default=[])
    select = commands.add_parser("select", help="select plain or rich composition")
    select.add_argument("context")
    request = commands.add_parser("request", help="build a Bot API request without sending")
    request.add_argument("spec")
    request.add_argument("--chat-id", required=True)
    request.add_argument("--thread-id", type=int)
    request.add_argument("--reply-to", type=int)
    request.add_argument("--media-root", action="append", default=[])
    send = commands.add_parser("send", help="send once using trusted CLI context")
    send.add_argument("spec")
    send.add_argument("--chat-id", required=True)
    send.add_argument("--thread-id", type=int)
    send.add_argument("--reply-to", type=int)
    send.add_argument("--media-root", action="append", default=[])
    send.add_argument("--yes", action="store_true", help="confirm network delivery")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "validate":
        report = validate_spec(
            _read_json(args.spec),
            allowed_media_roots=tuple(Path(p) for p in args.media_root),
            check_local_files=args.check_files,
        )
        _print(report.as_dict())
        return 0 if report.valid else 2
    if args.command == "render":
        _print(render(_read_json(args.spec), args.target).as_dict())
        return 0
    if args.command == "plan":
        values = {name: True for name in args.capability}
        _print(negotiate(_read_json(args.spec), CapabilitySet.from_mapping(values)).as_dict())
        return 0
    if args.command == "select":
        _print(select_composition(_read_json(args.context)).as_dict())
        return 0
    if args.command in {"request", "send"}:
        spec = _read_json(args.spec)
        context = TrustedConversationContext(
            args.chat_id, args.thread_id, reply_to_message_id=args.reply_to
        )
        roots = tuple(Path(p) for p in args.media_root)
        request = build_request(spec, context, allowed_media_roots=roots)
        if args.command == "request":
            _print(
                {
                    "method": request.method,
                    "parameters": request.parameters,
                    "files": {key: str(value) for key, value in request.files.items()},
                }
            )
            return 0
        if not args.yes:
            print("Refusing network delivery without --yes", file=sys.stderr)
            return 2
        _print(send_request(request))
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
