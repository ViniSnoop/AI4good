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
| [`hooks/`](hooks/CONTEXT.md) | Claude Code lifecycle hooks for the caveman suite — activation, mode tracking… |
| [`scripts/`](scripts/CONTEXT.md) | Compression CLI behind `/caveman compress <file>` — detect file type, call the… |

| File | Description |
|------|-------------|
| [`SKILL.md`](SKILL.md) | Ultra-compressed communication mode — router. Cuts token usage ~75% by speaking… |
| [`SPECS.md`](SPECS.md) | Global registration, the `$HOME` wiring, and the local adaptations that are the… |
| [`cavecrew.md`](cavecrew.md) | Subfile of the `caveman` skill. Reached via `/caveman crew` (legacy… |
| [`commit.md`](commit.md) | Subfile of the `caveman` skill. Reached via `/caveman commit` (legacy `/caveman… |
| [`compress.md`](compress.md) | Subfile of the `caveman` skill. Reached via `/caveman compress <file>` (legacy… |
| [`modes.md`](modes.md) | Caveman — intensity levels, worked |
| [`review.md`](review.md) | Subfile of the `caveman` skill. Reached via `/caveman review` (legacy… |
<!-- routing:end -->
