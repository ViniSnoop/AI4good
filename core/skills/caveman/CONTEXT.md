# caveman
> Ultra-compressed communication mode — vendored suite: router skill, mode subfiles, hooks, scripts.

Upstream: **[JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman)** — the caveman modes,
the commit/review/compress skills, the cavecrew presets and the activate / mode-tracker / stats /
statusline hooks all originate there. Vendored here and adapted; the upstream project keeps the
credit for the idea and the original implementation.

A **folder-shaped** skill: `SKILL.md` is the router, everything beside it is a subfile of that
router. It registers globally rather than through `.claude/skills/`, which is what puts it in every
project instead of only this workspace.

Global registration, the `$HOME` symlinks and their sync command, and the local adaptations that a
re-sync has to reconcile: [`SPECS.md`](SPECS.md).

<!-- routing:start -->
## Routing

| Subdirectory | Description |
|--------------|-------------|
| [`hooks/`](hooks/CONTEXT.md) | Claude Code lifecycle hooks for the caveman suite — activation, mode tracking, s |
| [`scripts/`](scripts/CONTEXT.md) | Compression CLI behind `/caveman compress <file>` — detect file type, call the m |

| File | Description |
|------|-------------|
| [`SKILL.md`](SKILL.md) | Ultra-compressed communication mode — router. Cuts token usage ~75% by speaking like a smart caveman while keeping full technical accuracy. Intensity levels: lite, full (default), ultra, wenyan-lite, wenyan-full, wenyan-ultra. Sub-commands: /caveman commit, review, compress, stats, crew, help. Use when the user says "caveman mode", "talk like caveman", "less tokens", "be brief", or invokes /caveman. Also auto-triggers when token efficiency is requested. |
| [`SPECS.md`](SPECS.md) | caveman — Specs |
| [`cavecrew.md`](cavecrew.md) | Cavecrew — Delegating to Caveman Subagents |
| [`commit.md`](commit.md) | Caveman — Commit Messages |
| [`compress.md`](compress.md) | Caveman — Compress a Prose File |
| [`modes.md`](modes.md) | Caveman — intensity levels, worked |
| [`review.md`](review.md) | Caveman — Code Review Comments |
<!-- routing:end -->
