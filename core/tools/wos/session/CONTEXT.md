# session
> What a session costs and what fills it, read from the local transcripts. No network, no model.

Split out of [`../CONTEXT.md`](../CONTEXT.md) on 2026-08-15, when `context` landed and took the
parent to 8 code files. The boundary is not thematic: these three share
[`session_log.py`](session_log.py), and the other five tools in the parent act on the workspace
tree rather than on `~/.claude/projects/<slug>/*.jsonl`.

| Tool | The one question it answers |
|------|-----------------------------|
| [`usage`](usage) | Where did the spend go — by model, by context size, per turn? |
| [`context`](context) | What is in the window at turn 1, and what fills it after? |
| [`session_log.py`](session_log.py) | Replay one transcript and attribute each turn's growth. |

**Both tools exist because a number nobody can re-run steers the work anyway** — the lesson
Frente 9 paid for, when four claims from a single 24 h window turned out false. Quote neither of
these reports from memory; re-run the command.

## Two rules that make the attribution honest

1. **Per-turn context is exact; what *entered* is only known in characters.** So the
   chars-per-token ratio is measured per turn, never a global `/4`. `context` prints the measured
   ratio and what it implies: well under ~3.5 means tokens enter that the transcript never logs,
   and those are spread across the reported rows in proportion. **Read the shares as shares of
   logged material.**
2. **A blocking gate is a failed `tool_result`, not an attachment.** Scanning only attachments
   found 1 `CONTEXT GATE` firing where the transcripts hold 518. Guarded by
   `test_a_blocking_gate_is_counted_from_the_failed_tool_result`.

`CLAUDE.md`, `AGENTS.md` and `MEMORY.md` never appear in a transcript — the harness folds them
into the system prompt. `context` measures them on disk and subtracts them from the residual, so
the memory store's cost stays separable from everything else's.

**Open:** `usage` still carries its own transcript loop and should adopt `walk()`.

<!-- routing:start -->
## Routing

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`context`](context) | — | — | what fills the context window: what |
| [`session_log.py`](session_log.py) | [`session_log.pyi`](session_log.pyi) | `label`, `blocks`, `walk`, `attribute`, `median` | session_log.py — replay a Claude Code transcript and attribute each turn's context growth. |
| [`usage`](usage) | — | — | where session spend goes: by model, |
<!-- routing:end -->
