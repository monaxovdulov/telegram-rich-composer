# Iva integration

Iva already detects tables, task lists, details, and block math before calling `channel.telegram.request("sendRichMessage", ...)`. Install this skill next to Iva's packaged skills and replace the heuristic-only decision with `select_composition`; keep Iva's outbound `scanOutbound` call before both rich and legacy delivery.

The supplied `routing.ts` shows the intended order:

1. scan generated content for outbound secrets;
2. build and validate a `CompositionSpec`;
3. render against current channel capabilities;
4. call `channel.telegram.request` for the active chat only;
5. fall back after a known permanent rejection;
6. stop after timeout, transport loss, or any unknown result.

Do not reuse the older standalone rich-post default chat when responding inside a conversation. The incoming channel context is authoritative. Preserve its thread and reply fields.
