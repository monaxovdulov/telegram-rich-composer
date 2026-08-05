// Illustrative insertion point after Iva's scanOutbound and before Telegram send.
export type DeliveryFailure = {
  permanent: boolean;
  certainty: "rejected" | "unknown";
  message: string;
};

export function mayAdvanceFallback(failure: DeliveryFailure): boolean {
  return failure.permanent && failure.certainty === "rejected";
}

export function trustedTelegramParams(context: {
  chatId: string;
  threadId?: number;
  replyToMessageId?: number;
}) {
  return {
    chat_id: context.chatId,
    ...(context.threadId ? { message_thread_id: context.threadId } : {}),
    ...(context.replyToMessageId
      ? { reply_parameters: { message_id: context.replyToMessageId } }
      : {}),
  };
}
