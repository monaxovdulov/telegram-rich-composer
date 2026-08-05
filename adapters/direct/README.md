# Direct Bot API and CLI

The direct adapter is implemented in `telegram_rich_composer.direct`. It separates semantic content from `TrustedConversationContext`; the latter is the only accepted source of `chat_id`, topic, and reply IDs.

```python
import json
from pathlib import Path

from telegram_rich_composer.direct import TrustedConversationContext, build_request, send_request

spec = json.loads(Path("composition.json").read_text())
context = TrustedConversationContext(
    chat_id=trusted_chat_id, reply_to_message_id=trusted_message_id
)
request = build_request(spec, context, allowed_media_roots=(Path("/srv/bot-media"),))
result = send_request(request)  # reads TELEGRAM_BOT_TOKEN
```

`send_request` performs one network attempt. A `DeliveryError` with `certainty="unknown"` must stop the fallback sequence until the caller reconciles Telegram state. A permanently rejected request may be rebuilt against the next negotiated capability only if the declared ladder allows feature loss.

The CLI has the same boundary. `trc request` is a dry request builder. `trc send` additionally requires `--yes` and a token from the process environment.
