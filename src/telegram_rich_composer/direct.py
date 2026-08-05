"""Direct Bot API request construction with trusted recipient context."""

from __future__ import annotations

import json
import mimetypes
import os
import secrets
import urllib.error
import urllib.request
from collections.abc import Mapping
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .negotiate import CapabilitySet, negotiate
from .render import render
from .validator import validate_spec


@dataclass(frozen=True, slots=True)
class TrustedConversationContext:
    chat_id: int | str
    message_thread_id: int | None = None
    direct_messages_topic_id: int | None = None
    reply_to_message_id: int | None = None


@dataclass(frozen=True, slots=True)
class BotApiRequest:
    method: str
    parameters: dict[str, Any]
    files: dict[str, Path]


class DeliveryError(RuntimeError):
    def __init__(self, message: str, *, certainty: str, permanent: bool) -> None:
        super().__init__(message)
        self.certainty = certainty
        self.permanent = permanent


def _delivery_parameters(
    spec: Mapping[str, Any], context: TrustedConversationContext
) -> dict[str, Any]:
    params: dict[str, Any] = {"chat_id": context.chat_id}
    delivery = spec["delivery"]
    if delivery["thread"] == "inherit" and context.message_thread_id is not None:
        params["message_thread_id"] = context.message_thread_id
    if context.direct_messages_topic_id is not None:
        params["direct_messages_topic_id"] = context.direct_messages_topic_id
    if delivery["reply"] in {"inherit", "required"} and context.reply_to_message_id is not None:
        params["reply_parameters"] = {"message_id": context.reply_to_message_id}
    elif delivery["reply"] == "required":
        raise ValueError("The spec requires a reply but trusted context has no message id")
    if delivery["silent"]:
        params["disable_notification"] = True
    if delivery["protect_content"]:
        params["protect_content"] = True
    if delivery.get("reply_markup"):
        params["reply_markup"] = {"inline_keyboard": delivery["reply_markup"]["inline_keyboard"]}
    return params


def build_request(
    spec: Mapping[str, Any],
    context: TrustedConversationContext,
    capabilities: CapabilitySet | Mapping[str, bool] | None = None,
    *,
    allowed_media_roots: tuple[Path, ...] = (),
) -> BotApiRequest:
    """Validate, negotiate, and construct a recipient-bound Bot API request."""
    validation_spec = deepcopy(spec)
    if capabilities is not None:
        caps = (
            capabilities
            if isinstance(capabilities, CapabilitySet)
            else CapabilitySet.from_mapping(capabilities)
        )
        validation_spec["surface"]["capabilities"] = caps.as_dict()
    report = validate_spec(
        validation_spec,
        allowed_media_roots=allowed_media_roots,
        check_local_files=True,
    )
    if not report.valid:
        messages = "; ".join(f"{issue.path}: {issue.message}" for issue in report.errors)
        raise ValueError(f"Invalid CompositionSpec: {messages}")
    plan = negotiate(spec, capabilities)
    rendered = render(spec, plan.selected)
    params = _delivery_parameters(spec, context)
    files: dict[str, Path] = {}
    for item in spec.get("media", []):
        if item["source"]["type"] == "local_path":
            files[item["id"]] = Path(item["source"]["path"]).resolve()

    if plan.selected.startswith("rich_"):
        if rendered.media:
            rendered.rich_message["media"] = list(rendered.media)
        params["rich_message"] = rendered.rich_message
        return BotApiRequest("sendRichMessage", params, files)
    if rendered.media:
        album = [item["media"] for item in rendered.media]
        if rendered.text:
            album[0]["caption"] = rendered.text[:1024]
        params["media"] = album
        return BotApiRequest("sendMediaGroup", params, files)
    params["text"] = rendered.text
    if rendered.parse_mode:
        params["parse_mode"] = rendered.parse_mode
    return BotApiRequest("sendMessage", params, files)


def _multipart(parameters: Mapping[str, Any], files: Mapping[str, Path]) -> tuple[bytes, str]:
    boundary = f"trc-{secrets.token_hex(16)}"
    chunks: list[bytes] = []
    for name, value in parameters.items():
        chunks.extend(
            [
                f"--{boundary}\r\n".encode(),
                f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode(),
                (
                    value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
                ).encode(),
                b"\r\n",
            ]
        )
    for name, path in files.items():
        mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        chunks.extend(
            [
                f"--{boundary}\r\n".encode(),
                (
                    f'Content-Disposition: form-data; name="{name}"; filename="{path.name}"\r\n'
                ).encode(),
                f"Content-Type: {mime}\r\n\r\n".encode(),
                path.read_bytes(),
                b"\r\n",
            ]
        )
    chunks.append(f"--{boundary}--\r\n".encode())
    return b"".join(chunks), f"multipart/form-data; boundary={boundary}"


def send_request(
    request: BotApiRequest, token: str | None = None, *, timeout: float = 30
) -> dict[str, Any]:
    """Send one prepared request. Never retries an uncertain delivery."""
    token = token or os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("Pass a token or set TELEGRAM_BOT_TOKEN")
    url = f"https://api.telegram.org/bot{token}/{request.method}"
    if request.files:
        body, content_type = _multipart(request.parameters, request.files)
    else:
        body = json.dumps(request.parameters, ensure_ascii=False).encode()
        content_type = "application/json"
    prepared = urllib.request.Request(
        url, data=body, headers={"Content-Type": content_type}, method="POST"
    )
    try:
        with urllib.request.urlopen(prepared, timeout=timeout) as response:
            payload = json.loads(response.read())
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode(errors="replace")
        raise DeliveryError(detail, certainty="rejected", permanent=400 <= exc.code < 500) from exc
    except (urllib.error.URLError, TimeoutError) as exc:
        raise DeliveryError(str(exc), certainty="unknown", permanent=False) from exc
    if not payload.get("ok"):
        raise DeliveryError(
            payload.get("description", "Bot API rejected request"),
            certainty="rejected",
            permanent=True,
        )
    return payload
