// Illustrative Eve typed-tool boundary. Adapt imports to the active Eve checkout.
type ComposeInput = {
  spec: Record<string, unknown>;
  target: "rich_blocks" | "rich_markdown" | "rich_html" | "legacy_html" | "plain_album";
};

type ComposeOutput = {
  target: string;
  payload: Record<string, unknown>;
};

export async function composeTelegramRich(input: ComposeInput): Promise<ComposeOutput> {
  // Invoke `trc validate -` and `trc render - --target ...` through Eve's
  // constrained subprocess helper or call the stdio MCP bridge. This function
  // intentionally accepts neither chatId nor bot token.
  throw new Error("Wire to Eve's constrained CLI/MCP runner; delivery stays channel-owned");
}
