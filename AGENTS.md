# Workspace Root
> Canonical workspace entrypoint. Read before any task.

<!-- norms:start -->
- FILESYSTEM = source of truth. No memory, no assumptions.
- **PROVIDER-AGNOSTIC STORAGE: the workspace owns its state, never a harness.** Agnostic to provider, company and harness — so nothing that matters is written to a vendor's private directory. If a harness insists on its own path, symlink that path into the repo. Live case: `~/.claude/projects/<slug>/memory` → `brain/memory/`, so what the agent writes lands in git.
- IMPROVE WORKSPACE at any opportunity. WRITE ISSUES DOWN at the end of INBOX.md
- DON'T ASSUME, interview user if in doubt about his idea or intent.
- EXPAND ACRONYMS on first use. Aliases: [`core/SCHEMA.md`](core/SCHEMA.md) § Vocabulary.
- EDIT > CREATE: refine / improve / reduce **wins over** creating new, except for prototyping. Avoid scattering.
- SYMMETRY IS A CORE VALUE, semantic and structural. When you find an asymmetry, write it down.
- **DONE WORK IS DELETED. GIT IS THE HISTORY.** No strikethrough, no annotated corpses.
- USE OUR TOOLS / FLOWS: we want those to be useful and perfected.
- **AGENT-FACING TEXT NAMES ONE ACTION.** A hook message, nudge or skill instruction is read mid-thread, not studied. Name the one flow to run — never its internals, never two commands, never "do the thing" in the abstract. Every extra noun is a decision the agent may improvise against.
<!-- norms:end -->

Git Flow, the branch gate's scope, the `--no-verify` protocol, and the push policy:
[`code/SPECS.md`](code/SPECS.md) § Git Branching. *Gated by `core/hooks/git/gitflow-gate.sh`.*
What the hooks block, and the contract a new agent's shim must satisfy:
[`core/hooks/SPECS.md`](core/hooks/SPECS.md). Installing the toolchain they need — stubgen, tsc,
caveman, rtk: [SETUP.md](SETUP.md).

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
