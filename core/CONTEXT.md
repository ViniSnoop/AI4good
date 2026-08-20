# Core
> Agent library: skills, agents, prompts, flows, tools. Provider-agnostic.

**Runtime-agnostic** — no provider-specific code. Skills invoke via `/skill-name`. Tools call via bash. Flows orchestrate agents.

## Research Agent System

Ported from Feynman (https://github.com/companion-inc/feynman), adapted for provider-agnostic use.

1. **Lead agent** (`agents/lead.md`) — receives requests, plans, orchestrates workers, synthesizes results. Read before any research task.
2. **Worker agents** (`agents/`) — specialist subagents spawned by lead: `researcher`, `writer`, `verifier`, `reviewer`.
3. **Flows** (`flows/`) — step-by-step orchestration protocols. Each names agents and sequence.
4. **Tools** (`tools/`) — executable CLI scripts; call via bash. Auto-documented in `tools/CONTEXT.md`.

<!-- routing:start -->
## Routing

| Subdirectory | Description |
|--------------|-------------|
| [`agents/`](agents/CONTEXT.md) | Agent definitions; load as system prompt to spawn a specialist worker. |
| [`experiments/`](experiments/CONTEXT.md) | What we measured about this workspace, when, and what changed because of it. One file per question. |
| [`flows/`](flows/CONTEXT.md) | Workflow protocols; each names the agents and steps to execute. |
| [`hooks/`](hooks/CONTEXT.md) | The enforcement layer: git hooks, agent lifecycle hooks, and the Tier 0 checks they run. |
| [`norms/`](norms/CONTEXT.md) | Rules obeyed rather than enforced. One file each; `AGENTS.md`'s rule block is generated from them. |
| [`prompts/`](prompts/CONTEXT.md) | Prepared session prompts — copy-paste into parallel agent sessions. Each file notes target tier/effort and deliverable. |
| [`refs/`](refs/CONTEXT.md) | Captured references for the agent library / workspace-os scaffold — tier-1 links in [REFS.md](refs/REFS.md). |
| [`skills/`](skills/CONTEXT.md) | Agent skills — provider-agnostic workflows invoked as slash commands or by instruction. |
| [`tools/`](tools/CONTEXT.md) | CLI tools callable via bash, one directory per family; routing block auto-synced on save. |

| File | Description |
|------|-------------|
| [`ROADMAP.md`](ROADMAP.md) | Making the agent library sound: one enforced frontmatter contract per layer, symmetric within layer/type. Contract in [SCHEMA.md](SCHEMA.md). Completed work is deleted -- git is the history. **Scope: agent-library internals only** — skills, agents, flows, tools, and their schema. Workspace scaffold work (hooks, gitignore, anti-entropy, cost, portability)… |
| [`SCHEMA-layers.md`](SCHEMA-layers.md) | The frontmatter every skill, agent, norm and flow declares, and how they compose. |
| [`SCHEMA-outgrowing.md`](SCHEMA-outgrowing.md) | Where an unclassified name goes, and how a type that passed the cap splits. |
| [`SCHEMA-placement.md`](SCHEMA-placement.md) | Which directory a file belongs in, and how deep the routing may go. |
| [`SCHEMA-vocabulary.md`](SCHEMA-vocabulary.md) | One word per idea, one idea per word, and every token a rename retired. |
| [`SCHEMA.md`](SCHEMA.md) | The enforced frontmatter contract for skills, flows, and agents, plus the workspace-wide `.md` type system. Drift from this is a bug. |
| [`SPECS-discipline.md`](SPECS-discipline.md) | What an always-loaded rule must prove, when doubt costs, when to delegate. |
| [`SPECS-features.md`](SPECS-features.md) | What counts as a feature, what its columns mean, and what may not be undeclared. |
| [`SPECS-library.md`](SPECS-library.md) | How the agent library is arranged, and how a tool family and its auth attach. |
| [`SPECS-session.md`](SPECS-session.md) | How a session closes, and who carries context when work is handed off. |
| [`SPECS.md`](SPECS.md) | Architecture decisions and conventions for the Core agent library. |
| [`features.txt`](features.txt) | Every toggleable feature this workspace has, declared: what group it belongs to, how hard it enforces, whether it is general or Lucas-specific, and whether it can actually be switched off. Read by core/hooks/feature_law.py; the answers live in core/profile.txt. |
| [`profile.txt`](profile.txt) | Which features are switched on for THIS machine, and the settings that are not switches. The registry is core/features.txt; this file holds only the answers. Read by core/hooks/feature_law.py, edited through `core/tools/wos/features --on|--off <slug>`. |
<!-- routing:end -->
