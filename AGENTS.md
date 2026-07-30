# Workspace Root
> Canonical workspace entrypoint. Read before any task.

**Only rules no hook can check live here.** A gate's message arrives *at* the violation and costs
nothing until it fires; always-loaded prose costs every session and gets skimmed. Make a rule
checkable → delete it from here.

- FILESYSTEM = source of truth. No memory, no assumptions.
- IMPROVE WORKSPACE at any opportunity. Findings can be 'existing bad' or 'new good' flows, instructions, skills, etc. Fix it or at least WRITE IT DOWN at the end of INBOX.md
- DON'T ASSUME, interview user if in doubt about his idea or intent.
- EXPAND ACRONYMS on first use — write the term out in full the first time it appears. For a very specific concept, add a short footnote. Never assume a term is shared vocabulary. Aliases: [`core/SCHEMA.md`](core/SCHEMA.md) § Vocabulary.
- PREFER EDIT OVER CREATE: edit / refine / improve / reduce **wins over** creating new, almost always — the exception is deliberate prototyping. Fix and reduce based on what works; avoid scattering.
- SYMMETRY IS A CORE VALUE, semantic and structural. Alike things look alike; a name means the same thing everywhere; no privileged special cases (a template is a template, not also an oracle). When you find an asymmetry, fix it or write it down.
- **`UPPERCASE.md` = a type, `lowercase.md` = an instance.** Types are a closed allowlist; inventing one is a deliberate act. Law, the allowlist itself, and where to route a name that is not on it: [`core/SCHEMA.md`](core/SCHEMA.md) § The `.md` type system. *Gated by `.hooks/type-gate.py`.*
- **DONE WORK IS DELETED. GIT IS THE HISTORY.** No strikethrough, no annotated corpses. The one exception: an approach *tried and rejected* was never committed, so git cannot hold it — give it **one line** under `## Rejected` in the relevant `ROADMAP.md` (a ditched goal: `## Ditched` in `brain/GOALS.md`).
- STRUCTURE HAS A SHAPE, and it holds across every subtree. Keep `CONTEXT.md` **local and granular** — small files glued to what they govern are what let weak models navigate and are the most cache-friendly input; do not consolidate them to "reduce clutter". Cap routing **depth** (hops to content), not file count. Treat a curated doc's size as a **delta-review signal, never a hard cap** — forcing a ROADMAP/CONTEXT to be summarized erases the heuristic that mattered (brevity bias). Full policy: [`core/SCHEMA.md`](core/SCHEMA.md).
- Before declaring a capability missing or impossible, read [`core/tools/CONTEXT.md`](core/tools/CONTEXT.md) and [`core/flows/CONTEXT.md`](core/flows/CONTEXT.md) — a tool or flow already exists for most research/web/file/Google/PDF/GitHub needs. If uncertain, SEARCH web first: `core/tools/search "<query>"` (bash, any agent, no MCP).
- PLANS LIVE IN ROADMAPS: any plan (plan mode or otherwise) must be persisted in the target project's `ROADMAP.md` — inline or as a `ROADMAP-<slug>.md` referenced from it. `~/.claude/plans/*` is a scratch copy, never the canonical home.

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
