# Source register

Reviewed on 2026-08-05. Use primary sources for behavior that can change.

| Source | Baseline | Decision supported |
|---|---|---|
| [Telegram Bot API Rich Messages](https://core.telegram.org/bots/api#rich-messages) | Bot API 10.2 page | InputRichMessage alternatives, explicit blocks, media bindings, limits, draft streaming, reply and topic fields. |
| [Agent Skills specification](https://agentskills.io/specification) | Page read 2026-08-05 | Skill name, description, frontmatter, and progressive disclosure. |
| [ASD-STE100](https://www.asd-ste100.org/) | Issue 9 public page | Issue date, ownership, trademark, and careful claim wording. |
| [Eve](https://github.com/vercel/eve) | `e5c91918ed898f72047d2a1e33902cbb9db3e452` | Packaged skills, typed tools, runtime context, Telegram channel limitations. |
| [Eve site](https://eve.dev/) | Page read 2026-08-05 | Public project layout and tool model. |
| [Iva](https://github.com/smixs/iva) | `b3544a2c19341a2231353b2942905748bf391751` | Rich routing, outbound redaction, current conversation binding, and HTML fallback. |
| [Iva rich-post](https://github.com/smixs/iva/tree/main/agent/skills/rich-post) | Same commit | Prior standalone rich skill and its recipient guard. |
| [Hermes skills](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/skills.md) | `6564f319a647b47de391cab2f608660323804a2b` | Skill installation, GitHub-path packages, security scanning, and progressive loading. |
| [Hermes Telegram](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/messaging/telegram.md) | Same commit | Gateway, group, topic, and media behavior. |
| [Hermes plugins](https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins) | Same commit | Plugin tool registration and opt-in execution. |
| [humanizer-ru](https://github.com/smixs/humanizer-ru) | `91f70df11f7fb30722e6fcf18803d402e2d86a53` | Russian editorial audit and deterministic lint. |

## Copyright notes

- ASD-STE100 is copyrighted and trademarked by ASD. This repository does not include the standard or its protected dictionary.
- English documentation uses selected public ASD-STE100 principles. The project does not claim certification or strict conformance.
- Eve, Iva, Hermes Agent, and humanizer-ru are used as documented integration references. Their source is not vendored here.
