# experiments
> What we measured about this workspace, when, and what changed because of it. One file per question.

**Why this exists.** *"No feature in this workspace has ever been measured"*
([/ROADMAP.md](../../ROADMAP.md) Frente 10.4). Every instrument we own —
[`session/context`](../tools/wos/session/context), [`session/usage`](../tools/wos/session/usage),
[`entropy.md`](../../entropy.md) — prints the present and forgets; git holds the past but not a
readable trend. This directory is the readable half, and differs on purpose from
`core/SCAFFOLD-LOG.md` ([/ROADMAP.md](../../ROADMAP.md) § Rejected): that logged narrated
**changes**, redundant with git; this records **measurements over time**, which git cannot give you.

Per-file format, the rule that keeps a stored number honest, and the reporting discipline:
[`SPECS.md`](SPECS.md).

<!-- routing:start -->
## Routing

| File | Description |
|------|-------------|
| [`SPECS.md`](SPECS.md) | The format every file in this directory follows, and the discipline that keeps a… |
| [`caveman-cost.md`](caveman-cost.md) | What does keeping caveman mode on cost per session, and does the compression it… |
| [`context-window.md`](context-window.md) | What fills a session's context window, split by source, and how much of it the… |
| [`subagent-context-chain.md`](subagent-context-chain.md) | Does forcing an agent to read a subtree's CONTEXT.md chain change what it does … |
<!-- routing:end -->
