# Adapter guide

[Русская версия](../ru/adapters.md)

## Contract

An adapter connects semantic content to one trusted Telegram conversation. It implements four operations.

```text
capabilities(context) -> CapabilitySet
prepare(spec, context, capabilities) -> DeliveryPlan
send(plan, context) -> DeliveryResult
reconcile(attempt_id, context) -> DeliveryResult
```

`prepare` is pure. `send` can change external state. `reconcile` checks an earlier attempt that has an unknown result.

## TrustedConversationContext

The harness creates this object. The model does not create it.

| Field | Meaning |
|---|---|
| `conversation_id` | Stable harness identifier for the active conversation. |
| `chat_id` | Telegram chat that produced the active turn. |
| `chat_type` | `private`, `group`, `supergroup`, or `channel`. |
| `message_id` | Incoming message that the answer can reply to. |
| `message_thread_id` | Current forum topic when present. |
| `direct_messages_topic_id` | Current direct-message topic when present. |
| `sender_id` | Authenticated sender when the harness provides it. |
| `authorized` | Result of the harness authorization check. |
| `explicit_target` | Optional target approved from an explicit user request. |
| `allowlist_evidence` | Optional evidence for an approved target outside the active chat. |

The adapter rejects delivery when `authorized` is false. It also rejects a target that differs from `chat_id` unless both `explicit_target` and `allowlist_evidence` are present.

## CapabilitySet

Capabilities are atomic booleans. Do not use one `rich_messages` flag for every feature.

Required keys:

- `rich_blocks`
- `rich_markdown`
- `rich_html`
- `rich_draft_streaming`
- `legacy_markdown`
- `legacy_html`
- `reply_parameters`
- `reply_markup`
- `topics`
- `direct_message_topics`
- `media_file_id`
- `media_url`
- `controlled_local_upload`
- `details_nested_blocks`
- `details_nested_media`
- `media_spoiler`
- `anchors`
- `references`
- `custom_emoji`
- `maps`
- `diagram_renderer`

An adapter can add namespaced keys. The core ignores unknown keys.

## Negotiation

The core uses this decision order.

1. Use explicit blocks when `rich_blocks` is true and every requested feature has support.
2. Use Rich Markdown or Rich HTML when that route preserves all required features.
3. Use legacy HTML or Markdown for text that still fits a normal Telegram message.
4. Use plain text and an ordinary media plan.

The renderer emits warnings for each lost feature. The visible summary must survive every step.

If `details_nested_media` is false, move media after the `details` block and add a visible label. If `anchors` is false, replace anchor links with a short contents list. If `references` is false, append numbered source lines. If `maps` is false, show coordinates and a safe explicit map link.

## Delivery options

`delivery.reply` has three modes: `inherit`, `none`, and `required`. `inherit` uses the current message when the harness normally replies. `required` fails when no trusted reply target is available.

`delivery.thread` has `inherit` and `none`. Version 1 does not let the model provide an arbitrary thread ID.

`silent`, `protect_content`, and `reply_markup` are forwarded only when the capability exists. Buttons must represent a real action or choice. Decorative buttons are invalid in the `calm` profile.

## Entity detection

Use `entity_detection: auto` for ordinary prose. The renderer omits `skip_entity_detection`, so Telegram can detect URLs, e-mail addresses, phone numbers, commands, hashtags, and mentions.

Use `entity_detection: explicit_only` when automatic blue entities would break the visual hierarchy. The renderer sets `skip_entity_detection: true`. Every required link must then be an explicit inline node.

Do not disable entity detection for all messages.

## Media policy

### Telegram file ID

Use `file_id` when the media already exists in Telegram. The renderer binds it through `InputRichMessage.media` or an explicit media block.

### URL

Allow HTTPS by default. An adapter can allow HTTP only for a controlled network and an explicit policy. Reject loopback, link-local, private-network, credential-bearing, and unsupported-scheme URLs unless the host has a separate trusted fetcher.

### Local path

Local media is disabled by default. To enable it, the harness must provide allowed roots and `controlled_local_upload`. Resolve symlinks before the root check. Check that the file is regular, has an allowed media type, and has safe size. Upload directly to Telegram with multipart data. Do not use an anonymous public host.

## Failure classes

| Class | Example | Action |
|---|---|---|
| `permanent_syntax` | Bot API rejects rich syntax with a clear 400 error. | Prepare a lower representation and send once. |
| `capability` | Method or rich feature is unsupported. | Latch that capability off and use the next representation. |
| `authorization` | Current sender or target is not allowed. | Stop. Do not fall back to another target. |
| `local_validation` | Schema, limit, URL, path, or media policy fails. | Stop before network access. |
| `transport_not_connected` | A connection was not established. | The host can retry under its normal policy. |
| `unknown_delivery` | Timeout or disconnect after the request could have reached Telegram. | Record `unknown`. Do not send another representation. Reconcile first. |

## Eve

Place the packaged skill under `agent/skills/telegram-rich-composer/`. Add a short rule to `agent/instructions.md` so Telegram sessions consider the plain-or-rich choice on every turn. Keep the full pattern catalog lazy-loaded.

The typed tool reads the specification and returns a delivery plan. A Telegram channel event handler owns the actual request and gets the trusted chat and thread from `channel.telegram`. The model cannot pass `chat_id` to the tool.

Eve commit `e5c91918...` has no stock rich transport. The example adapter therefore uses the raw request surface. Review it when Eve adds native rich delivery.

## Iva

Iva commit `b3544a2c...` already gets the current chat and thread from `channel.telegram`. It applies `scanOutbound` before `sendRichMessage` and before HTML fallback.

Keep those controls. Add the selector and validator before `needsRichMessage`. Pass raw Rich Markdown only after validation. Permanent rich errors can use the existing HTML fallback. Unknown transport results must not use that fallback because a second message can duplicate the first.

Do not use the old `rich-post` default digest recipient for conversational replies. Use the active channel context. Keep its allowlist rule only for explicit report delivery outside the active chat.

## Hermes Agent

Hermes commit `1be70d635...` already supports an opt-in rich fast path, rich drafts, rich final edits, topic routing, `reply_parameters`, and no-resend behavior for unknown rich results.

Install the skill under `~/.hermes/skills/telegram-rich-composer/`. The optional plugin registers a compile and validate tool. It does not replace the Telegram platform adapter. The native adapter owns `chat_id`, topics, reply anchors, and delivery.

Enable third-party plugin code explicitly in `plugins.enabled`. A skill-only install requires no plugin execution when native Rich Markdown is enough.

## Direct Bot API

The reference CLI receives trusted values from command-line arguments supplied by the host. It never accepts a token as a command-line argument. Read the token from `TELEGRAM_BOT_TOKEN`.

Dry-run is the default for examples. Network delivery requires an explicit `send` command and `--yes`. The host must derive `chat_id` from trusted context or enforce an allowlist before invocation. The reference adapter has no delivery ledger, so the caller must reconcile an unknown result through its own update store or audit log.
