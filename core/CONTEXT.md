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
| [`experiments/`](experiments/CONTEXT.md) | What we measured about this workspace, when, and what changed because of it. One… |
| [`flows/`](flows/CONTEXT.md) | Workflow protocols; each names the agents and steps to execute. |
| [`hooks/`](hooks/CONTEXT.md) | The enforcement layer: git hooks, agent lifecycle hooks, and the Tier 0 checks… |
| [`prompts/`](prompts/CONTEXT.md) | Prepared session prompts — copy-paste into parallel agent sessions. Each file… |
| [`refs/`](refs/CONTEXT.md) | Captured references for the agent library / workspace-os scaffold — tier-1 links… |
| [`skills/`](skills/CONTEXT.md) | Agent skills — provider-agnostic workflows invoked as slash commands or by… |
| [`tools/`](tools/CONTEXT.md) | CLI tools callable via bash, one directory per family; routing block auto-synced… |

| File | Description |
|------|-------------|
| [`ROADMAP.md`](ROADMAP.md) | Making the agent library sound: one enforced frontmatter contract per layer… |
| [`SCHEMA.md`](SCHEMA.md) | The enforced frontmatter contract for skills, flows, and agents, plus the… |
| [`SPECS.md`](SPECS.md) | Architecture decisions and conventions for the Core agent library. |
| [`features.txt`](features.txt) | Every toggleable capability this workspace has, declared: what group it belongs to, how hard it |
| [`profile.txt`](profile.txt) | Which capabilities are switched on for THIS machine, and the settings that are not switches. |
<!-- routing:end -->
