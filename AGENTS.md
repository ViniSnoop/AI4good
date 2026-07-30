# Workspace Root
> Canonical workspace entrypoint. Read before any task.

- FILESYSTEM = source of truth. No memory, no assumptions.
- IMPROVE WORKSPACE at any opportunity. Findings can be 'existing bad' or 'new good' flows, instructions, skills, etc. Fix it or at least WRITE IT DOWN at the end of INBOX.md
- DON'T ASSUME, interview user if in doubt about his idea or intent.
- EXPAND ACRONYMS on first use — write the term out in full the first time it appears. For a very specific concept, add a short footnote. Never assume a term is shared vocabulary. (**workspace-os** = **wos** / **WOS** / **w-os** / **W-OS**, all the same thing.)
- PREFER EDIT OVER CREATE: edit / refine / improve / reduce **wins over** creating new, almost always — the exception is deliberate prototyping. Fix and reduce based on what works; avoid scattering.
- SYMMETRY IS A CORE VALUE, semantic and structural. Alike things look alike; a name means the same thing everywhere; no privileged special cases (a template is a template, not also an oracle). When you find an asymmetry, fix it or write it down.
- **`UPPERCASE.md` = a type, `lowercase.md` = an instance.** A type means the same thing in every subtree, so uppercase names are a **closed allowlist**: `AGENTS · CONTEXT · README · ROADMAP · SPECS · BUGS · REFS · SKILL · GOALS · TODO · INBOX · USER · SCHEMA`. Inventing a type is a deliberate act — add it to [`core/SCHEMA.md`](core/SCHEMA.md) § The `.md` type system, which also states what single question each type answers and the rules for where two types nearly touch.
- **DONE WORK IS DELETED. GIT IS THE HISTORY.** No `ARCHIVE.md`, no `HISTORY.md`, no strikethrough, no annotated corpses. The one exception: an approach *tried and rejected* was never committed, so git cannot hold it — give it **one line** under `## Rejected` in the relevant `ROADMAP.md` (a ditched goal: `## Ditched` in `brain/GOALS.md`).
- STRUCTURE HAS A SHAPE, and it holds across every subtree. Keep `CONTEXT.md` **local and granular** — small files glued to what they govern are what let weak models navigate and are the most cache-friendly input; do not consolidate them to "reduce clutter". A `CONTEXT.md` never hand-lists files: the generated routing block owns inventory, and line 2 is hoisted into the parent's row, so it must be a real description. Cap routing **depth** (hops to content), not file count. Treat a curated doc's size as a **delta-review signal, never a hard cap** — forcing a ROADMAP/CONTEXT to be summarized erases the heuristic that mattered (brevity bias). Full policy: [`core/SCHEMA.md`](core/SCHEMA.md).
- Before declaring a capability missing or impossible, read [`core/tools/CONTEXT.md`](core/tools/CONTEXT.md) and [`core/flows/CONTEXT.md`](core/flows/CONTEXT.md) — a CLI tool or flow already exists for most research/web/file/Google/PDF/GitHub needs. Same for any task that "would be easier with a tool": check the catalog first, then act.
- If uncertain SEARCH web first: `core/tools/search "<query>"` (bash, any agent, no MCP). Backend and flags: [SETUP.md §12](SETUP.md#12-unified-web-search-cli-all-agents).
- Workspace repo commits structural files (`AGENTS.md`, `CONTEXT.md`, domain docs). Internal projects use their own git repos.
- GITFLOW. `main` = production, `develop` = integration. Cycle: `develop` → `feature/*` → `develop` → `main` → rest on `main`. **Never commit directly to `main` or `develop` — branch `feature/*` first.** Enforced by `.hooks/gitflow-gate.sh` for every `code/*` repo and the workspace repo itself; paper repos (`academy/papers/*`) and other nested repos are exempt. Emergency bypass: `git commit --no-verify` — it leaves no trace outside the commit message, so state the reason there and file a TODO to pay it back.
- PUSH POLICY — two machines share this workspace, so unpushed work is invisible work and `main` is the sync point, not a release tag. `feature/*` auto-pushes via `.hooks/post-commit`; promotion to `develop`/`main` happens in `/roundup` Phase 5 behind a green verification run; `/handoff` only *reports* divergence, never merges.
- PLANS LIVE IN ROADMAPS: any plan (plan mode or otherwise) must be persisted in the target project's `ROADMAP.md` — inline or as a `ROADMAP-<slug>.md` referenced from it. `~/.claude/plans/*` is a scratch copy, never the canonical home.

See [SETUP.md](SETUP.md) for hooks, stubgen, tsc, caveman, and toolchain setup.

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
