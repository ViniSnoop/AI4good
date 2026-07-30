# Workspace Root
> Canonical workspace entrypoint. Read before any task.

- FILESYSTEM = source of truth. No memory, no assumptions.
- IMPROVE WORKSPACE at any opportunity. WRITE ISSUES DOWN at the end of INBOX.md
- DON'T ASSUME, interview user if in doubt about his idea or intent.
- EXPAND ACRONYMS on first use. Aliases: [`core/SCHEMA.md`](core/SCHEMA.md) § Vocabulary.
- WOS = workspace os.
- EDIT > CREATE: refine / improve / reduce **wins over** creating new, except for prototyping. Avoid scattering.
- SYMMETRY IS A CORE VALUE, semantic and structural. When you find an asymmetry, write it down.
- **`UPPERCASE.md` = a type, `lowercase.md` = an instance.** Types are a closed allowlist.
- **DONE WORK IS DELETED. GIT IS THE HISTORY.** No strikethrough, no annotated corpses.
- USE OUR TOOLS / FLOWS: we want those to be useful and perfected.
- PLANS LIVE IN ROADMAPS: any plan must be persisted in the target project's `ROADMAP.md` — inline or as a `ROADMAP-<slug>.md` referenced from it.

Git Flow, the branch gate's scope, the `--no-verify` protocol, and the push policy:
[`code/SPECS.md`](code/SPECS.md) § Git Branching. *Gated by `.hooks/gitflow-gate.sh`.*
Hooks, stubgen, tsc, caveman, toolchain: [SETUP.md](SETUP.md).

<!-- routing:start -->
## Routing

| Subdirectory | Description |
|--------------|-------------|
| [`academy/`](academy/CONTEXT.md) | Research, teaching, academic work |
| [`brain/`](brain/CONTEXT.md) | Personal OS: goals, attention, ideas, life. Agent collaborates here. |
| [`branches/`](branches/CONTEXT.md) | Personal life management — health, finances, and home construction |
| [`code/`](code/CONTEXT.md) | Software projects developed under this workspace |
| [`core/`](core/CONTEXT.md) | Agent library: skills, agents, prompts, flows, tools. Provider-agnostic. |
| [`models/`](models/CONTEXT.md) | Local model checkpoints and weights used across research and code projects |
<!-- routing:end -->
