from __future__ import annotations

import json
import urllib.error

import pytest

from telegram_rich_composer.cli import main
from telegram_rich_composer.direct import (
    BotApiRequest,
    DeliveryError,
    TrustedConversationContext,
    _multipart,
    build_request,
    send_request,
)


def test_adapter_binds_trusted_context(load_golden):
    spec = load_golden("ticket-table")
    request = build_request(spec, TrustedConversationContext(-1001, 17, reply_to_message_id=42))
    assert request.method == "sendRichMessage"
    assert request.parameters["chat_id"] == -1001
    assert request.parameters["message_thread_id"] == 17
    assert request.parameters["reply_parameters"] == {"message_id": 42}
    assert "chat_id" not in spec


def test_required_reply_fails_without_context(load_golden):
    spec = load_golden("ticket-table")
    spec["delivery"]["reply"] = "required"
    with pytest.raises(ValueError, match="requires a reply"):
        build_request(spec, TrustedConversationContext(1))


def test_cli_validate(capsys, load_golden, tmp_path):
    path = tmp_path / "spec.json"
    path.write_text(json.dumps(load_golden("ticket-table")), encoding="utf-8")
    assert main(["validate", str(path)]) == 0
    assert json.loads(capsys.readouterr().out)["valid"] is True


def test_cli_send_requires_confirmation(load_golden, tmp_path, capsys):
    path = tmp_path / "spec.json"
    path.write_text(json.dumps(load_golden("ticket-table")), encoding="utf-8")
    assert main(["send", str(path), "--chat-id", "1"]) == 2
    assert "without --yes" in capsys.readouterr().err


def test_cli_render_plan_select_and_request(load_golden, tmp_path, capsys):
    spec_path = tmp_path / "spec.json"
    spec_path.write_text(json.dumps(load_golden("ticket-table")), encoding="utf-8")
    assert main(["render", str(spec_path), "--target", "rich_blocks"]) == 0
    assert json.loads(capsys.readouterr().out)["target"] == "rich_blocks"
    assert main(["plan", str(spec_path), "--capability", "rich_blocks"]) == 0
    assert json.loads(capsys.readouterr().out)["selected"] == "rich_blocks"
    context_path = tmp_path / "context.json"
    context_path.write_text('{"intent":"answer"}', encoding="utf-8")
    assert main(["select", str(context_path)]) == 0
    assert json.loads(capsys.readouterr().out)["mode"] == "plain"
    assert main(["request", str(spec_path), "--chat-id", "9"]) == 0
    assert json.loads(capsys.readouterr().out)["method"] == "sendRichMessage"


def test_plain_album_request_is_valid_input_media(load_golden):
    spec = load_golden("museum-drawers")
    caps = {"plain_album": True}
    request = build_request(spec, TrustedConversationContext(1), caps)
    assert request.method == "sendMediaGroup"
    assert request.parameters["media"][0]["media"] == "telegram-hero"
    assert request.parameters["media"][0]["caption"]


def test_multipart_contains_fields_and_file(tmp_path):
    media = tmp_path / "image.png"
    media.write_bytes(b"PNG")
    body, content_type = _multipart({"chat_id": 1}, {"hero": media})
    assert b'name="chat_id"' in body
    assert b'name="hero"; filename="image.png"' in body
    assert content_type.startswith("multipart/form-data; boundary=")


class FakeResponse:
    def __enter__(self):
        return self

    def __exit__(self, *args):
        return None

    def read(self):
        return b'{"ok":true,"result":{"message_id":7}}'


def test_send_request_success(monkeypatch):
    monkeypatch.setattr("urllib.request.urlopen", lambda *args, **kwargs: FakeResponse())
    request = BotApiRequest("sendMessage", {"chat_id": 1, "text": "ok"}, {})
    assert send_request(request, "test-token")["result"]["message_id"] == 7


def test_send_request_requires_token(monkeypatch):
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    with pytest.raises(ValueError, match="TELEGRAM_BOT_TOKEN"):
        send_request(BotApiRequest("sendMessage", {}, {}))


def test_send_request_unknown_transport_stops(monkeypatch):
    def fail(*args, **kwargs):
        raise urllib.error.URLError("lost")

    monkeypatch.setattr("urllib.request.urlopen", fail)
    with pytest.raises(DeliveryError) as caught:
        send_request(BotApiRequest("sendMessage", {}, {}), "test-token")
    assert caught.value.certainty == "unknown"
    assert not caught.value.permanent


def test_delivery_error_attributes():
    error = DeliveryError("bad request", certainty="rejected", permanent=True)
    assert str(error) == "bad request"
    assert error.certainty == "rejected"
    assert error.permanent is True
