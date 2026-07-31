# Core Library Schema
> The enforced frontmatter contract for skills, flows, and agents, plus the workspace-wide `.md`
> type system. Drift from this is a bug.

## Vocabulary

Aliases that mean exactly one thing, so a reader never has to guess whether two spellings are two
concepts. This is **data, not a rule** — which is why it lives here and not in the always-loaded
`AGENTS.md` (moved 2026-07-30).

| Canonical | Also written |
|-----------|--------------|
| **workspace-os** | `wos` · `WOS` · `w-os` · `W-OS` |
| **craft flow** | the `/loops` skill, `core/flows/craft/` (retired spellings: § Retired tokens) |

### Retired tokens

**A rename is finished when its old token appears nowhere.** Until then the leaves drift back and the
drift is indistinguishable from entropy — the lesson of the `loops`→`flows` rename, which kept
resurfacing because nothing asserted its completion.

This table *is* the assertion. `core/hooks/entropy_ledger.py` fails if any token below survives in a
tracked file, this file excepted — the law has to be able to name what it retires. Add a row the
moment a rename lands, and delete the prose that would otherwise explain it: git holds the history,
this table holds the guard.

| Retired token | Replacement | Retired |
|---------------|-------------|---------|
| `loop-engineering` | `craft` | 2026-07-23 |
| `loop-router` | `route` | 2026-07-23 |
| `loop-architecture` | `architect` | 2026-07-23 |
| `LOOP-TREE` | `tree.md` | 2026-07-23 |
| `KNOWN-BUGS` | `BUGS.md` | 2026-07-30 |

Not yet listed because the rename has not landed: `SPEC.md`→`SPECS.md` (load-bearing in five
enforcement points; see [ROADMAP.md](../ROADMAP.md) Frente 12.1). A token joins this table only when
the sweep is complete — a row that fails on the day it is written trains people to ignore the check.

## The `.md` type system

> Decided 2026-07-30. Lucas: *"delimit precisely where one file ends and another begins, so there is
> no conceptual intersection."*

**`UPPERCASE.md` is a type. `lowercase.md` is an instance.** A type means the same thing in every
subtree; an instance is content, named freely. Uppercase names are therefore a **closed set** —
inventing a type must be a deliberate act (one line added below), never an accident. Before this
rule there were 25 distinct uppercase names, 15 appearing exactly once.

Each type answers exactly one question. If you cannot say which question a file answers, it does not
get a new type.

| Type | The one question it answers |
|------|------------------------------|
| `AGENTS.md` | What rules always apply, and where do I start? (root only) |
| `CONTEXT.md` | What is *this directory*, and where inside it do I go? |
| `ROADMAP.md` | What do we intend to do — and what did we reject, and why? |
| `SPECS.md` | What must be true of this thing, and *why*? (contract + rationale) |
| `BUGS.md` | What is currently **untrue** that we know about? |
| `README.md` | I just cloned this. What is it and how do I run it? (repo root only) |
| `REFS.md` | What external material exists, and what did we conclude about it? |
| `SKILL.md` | What procedure does the agent follow when invoked? |
| `GOALS.md` | Which goals have wind right now? (dashboard + router) |
| `TODO.md` | What must I do in life this week? |
| `INBOX.md` | Raw capture, zero taxonomy, drained to empty |
| `USER.md` | Who is Lucas, and how does he fail? |
| `SETUP.md` | How do I make this environment work? (toolchain install + config) |
| `SCHEMA.md` | This file: the law about types. |

Anything else is rejected: *"add it to the allowlist if you mean it."*

`SETUP.md` earns its row on the evidence (added 2026-07-30, 8 instances): `README.md` is **repo-root
only**, and 4 of the 8 sit in directories that are not repos — the workspace root, `academy/`,
`code/`, `code/_templates/`. "How do I make this work" is not "what is this and how do I run it".

### The four disposal routes

An off-allowlist `UPPERCASE.md` is not automatically wrong — it is *unclassified*. Route it, so a new
name resolves without a decision meeting (decided 2026-07-30):

| Route | When | Cases resolved 2026-07-30 |
|-------|------|---------------------------|
| lowercase instance | **generated** by a tool | the old `LABELS` name → `labels.md` (×6 papers; emitted by `core/hooks/tex-interface-gen.py`, header says "do not edit") |
| lowercase instance | hand-authored **content** | `DRAFT.md`→`draft.md` (×3 embryo papers), `TREE.md`→`tree.md` (the craft-tree map: curated rationale, not generated — the first read of it corrected the route) |
| → `SPECS.md` | hand-authored **constraint** | `BRIDGE.md`→`SPECS.md` § Twin (×3, the section carries the same name on both sides — "Paper Twin" reads wrong inside the paper): *"every measured number files a P-task"* is an invariant |
| new type | answers a question **no type answers** | `SETUP.md` only |

`SPEC.md` is **not** a type: it collapses into `SPECS.md` (decided 2026-07-30, Lucas). The
singular/plural pair was the sharpest asymmetry in the corpus — two spellings, one meaning — and it
had leaked into enforcement, so the `> spec:` convention, `core/hooks/pre-commit` §1d,
`core/hooks/spec-read-gate.py`, `core/hooks/context-tracker.py`, `core/tools/spec-scan` and
`core/tools/spec-contract-check` all move with it.

### Boundaries where types nearly touch

The three real conflicts, with the resolving rule:

| Conflict | Rule |
|----------|------|
| `CONTEXT.md` vs its own routing block | CONTEXT **never hand-lists files**; the generated routing block owns inventory. A hand-written File Map is a bug. |
| `CONTEXT.md` vs `SPECS.md` | Rules that *constrain code* → SPECS. What the directory *is* → CONTEXT. |
| `ROADMAP.md` vs `BUGS.md` | BUGS owns the bug text; ROADMAP references it by id and never restates it. Intent vs. state: a roadmap item leaves the list when deprioritised, a bug does not stop being true. |

### No archive types

`ARCHIVE.md`, `HISTORY.md` and `.log/done.md` are **deleted, not renamed**. A file that is "never
auto-loaded, ask explicitly" is doing git's job. **Done work is deleted; git is the history.**

The same rule applies *inside* a file, not only to whole files (Lucas, 2026-07-30): **a completed
`ROADMAP.md` item is cut, not ticked.** `[x]` is an annotated corpse with a checkbox — it keeps
paying rent in every read of the file, and it makes the roadmap's length measure history instead of
remaining work. Trim on verified completion. Keep a line only when the next session needs it to
*extend* the work rather than recreate it, and write that line as present-tense state ("extend
`core/hooks/type-gate.py`"), never as a report ("✅ built the type gate").

One thing git cannot hold: an approach we *tried and rejected* was never committed. That content has
exactly one home — a one-line entry under `## Rejected` in the relevant `ROADMAP.md` (for a ditched
goal, under `## Ditched` in `brain/GOALS.md`). One line, with the reason, so a dead idea does not
resurface looking new.

### The one exception: transient initiative docs

A **cross-project rollout** with cited anchor ids and a defined death date is a real type and is not
a ROADMAP. Members: `code/VERIFY.md`, `code/SPEC-DRIVE.md`, `code/isoroll-module/REFACTOR.md`,
`core/MIGRATION-STATUS.md`, `code/dobra/DECISIONS.md`.

Folding `VERIFY.md` into a ROADMAP was investigated 2026-07-30 and **rejected as unsafe**: it has 24
inbound references, 7 of them in `core/hooks/*` source comments citing stable anchors (`VERIFY.md W1`,
`W2`, `I2`, `G1`, `G3`, `G7`, `A1`). Breaking those would silently orphan the reasoning behind live
gates.

These are exempt from the allowlist **and** carry an obligation: each must state its own death
condition on line 3, and be deleted when its rollout completes. They are the only `.md` type allowed
to be temporary, so a stale one is the most expensive kind of clutter.

---

## Frontmatter contract

Companion to the code-side spec-drive convention (the `> spec:` module gate in `core/hooks/pre-commit`,
tracked under the [[spec-driven-development]] goal): that governs `code/` modules, this governs the
`core/` agent library.

**No flow is privileged.** The exemplar is [`flows/_template.md`](flows/_template.md) — a template,
nothing more. There is no "reference implementation" whose behaviour defines correctness (that dual
role coupled one flow's evolution to the schema; retired 2026-07-23). Realism is guaranteed by
`validate_flows` running over *every* flow, including the template, not by anointing one.

## The one rule

**Execution metadata lives on the executor (agent), never on the skill.**
A skill is a trigger. A flow is a procedure. An agent is the thing that runs, so tier/tools/output
belong to it. Provider and model names (`opus`, `haiku`, `claude-*`) appear **only in generated
runtime mirrors** (`.claude/agents/*`), never in `core/` source — exactly the
`core/skills → .claude/skills` split, now extended to agents.

```
skill  (trigger)   →  flow  (procedure)   →  agent  (executor)   →  subagent
name,description       description,args,       name,description,
[flow]                 type,confirm,[agents]   tier,[tools],[output],[defaultProgress]
```

The graph is a **sparse typed DAG**, one direction. Skills do not point to skills.

## Layer: skill — `core/skills/<name>.md`

| field | req | value |
|-------|-----|-------|
| `name` | ✅ | kebab-case, matches filename |
| `description` | ✅ | actionable; drives the menu. End with "Invoke with /name [args]." |
| `flow` | — | slug of the flow this skill dispatches to (THIN skills only); routers list all dispatchable flows as a comma list, same shape as a flow's `agents:` |

No `model`, `tier`, `tools`, or `subagents` on a skill — those are execution detail, pushed down.
A skill is THIN (dispatches to a flow) or FAT (self-contained protocol); both are valid. Any
`core/skills/*.md` that is not a skill (status doc, ADR) does **not** belong here — the validator
rejects a file with no `name`/`description` frontmatter.

## Layer: agent — `core/agents/<name>.md`

| field | req | value |
|-------|-----|-------|
| `name` | ✅ | matches filename |
| `description` | ✅ | one line: what evidence/output this worker produces |
| `tier` | ✅ | `low` \| `medium` \| `high` \| `max` — the provider-agnostic effort ladder (same as the craft flow) |
| `tools` | ▲ | comma list; required for **worker** agents (locked-down allowlist) |
| `output` | ▲ | default artifact filename; required for workers |
| `defaultProgress` | — | `true` for long workers |

**Agent variants:**
- **worker** (researcher, verifier, writer, reviewer): all six fields; `tier` + `tools` + `output` mandatory.
- **orchestrator** (lead): `name` + `description` + `tier` only. `tools`/`output`/`defaultProgress`
  are N/A — the orchestrator inherits the full toolset and owns no single artifact.

`tier` is the source of truth. A runtime that needs a concrete model sets it by hand per mirror file
— e.g. Claude Code's `.claude/agents/craft-high.md` carries `model: opus` for `tier: high`. There is
no generator and no `tier-map.json`; that was the planned mechanism, never built. Until it exists,
keep each mirror's `model:` in sync with its source `tier:` by hand.
**No `thinking:` and no `model:` in `core/agents/` source** — that was the old two-convention drift.

## Layer: flow — `core/flows/[<skill>/]<name>.md`

**Location rule.** A flow owned by a dispatcher skill lives in `core/flows/<skill>/` and its
**filename equals the command tail** — `core/flows/research/scout.md` ⟺ `research scout`. Flows not
owned by any dispatcher skill stay flat at `core/flows/`. Validation is recursive (`sync-skills`
`validate_flows` walks subfolders); a `<skill>/CONTEXT.md` is exempt like the root one. The
engineering cluster owned by the `loops` skill lives in [`flows/craft/`](flows/craft/) —
`craft` · `route` · `architect` (+ the `tree.md` map) — and is exempt from the table below.

| field | req | value |
|-------|-----|-------|
| `description` | ✅ | one line: what the flow produces |
| `args` | ✅ | arg signature, e.g. `<topic>` |
| `type` | ✅ | `research-brief` \| `utility` \| `domain` |
| `confirm` | ✅ | `plan` (stop for explicit "yes" before work) \| `none` (summarize plan, continue) |
| `agents` | — | comma list of worker agents the flow may spawn |
| `uses` | — | comma list of other flows this flow invokes; empty/absent = leaf. The `uses:` graph must be a **DAG** (see *Composition and cycles*), enforced by `validate_flows` |

`confirm` exists to kill the old contradiction where some flows blocked for approval and others
didn't, with no way for a caller to know which. Now it is declared and readable.

### Disciplines by flow `type`

Legend: ✅ required · ~ recommended · — not required

| discipline | research-brief | utility | domain |
|------------|:--:|:--:|:--:|
| **tool-discipline** — literal tool names, "use only visible tools", map-or-block on `Tool not found` | ✅ | ✅ | ✅ |
| **required-artifacts** — explicit on-disk file list + "never end chat-only after work starts" | ✅ | ~ | ✅ |
| **provenance** — `<slug>.provenance.md` sidecar (or a declared running log) | ✅ | — | ~ |
| **scale-gate** — explicit direct vs decomposed rule ("narrow explainer → no subagents") | ✅ | ~ | ~ |
| **integrity** — read-before-summarize, honest status, no invented sources/results | ✅ | ✅ | ✅ |

The canonical wording for each discipline lives in [`flows/_template.md`](flows/_template.md), each
block annotated with the types that require it — **copy from there**. Symmetry is required **within
a type**, not flattened across all flows: a scheduler (`utility`) is not forced to emit a provenance
sidecar. Holding the wording is the template's only privilege; it is still just a template, not a
reference implementation.

Flow-type assignments:
- **research-brief:** sota, literature, review, recipe, compare, audit, replicate, draft (in `flows/research/`)
- **utility:** watch, explore, summarize (in `flows/research/`)
- **domain:** mechanism-search
- **engineering:** `craft` · `route` · `architect` (in `flows/craft/`) — its own protocol, declares
  tier routing directly; exempt from this table and from flow-layer validation. **Known asymmetry:**
  `engineering` is not in the `type` enum, so the cluster is exempted by path rather than typed. The
  symmetric fix (add `engineering` to the enum, give the three flows real frontmatter, delete the
  exemption) is a schema change and is queued in [ROADMAP.md](ROADMAP.md), not taken silently here.

## Composition and cycles

> Decided 2026-07-23. Vocabulary: **"flow" is the canonical term.** "Loop" is retired for the
> orchestration/connected-agents sense — a real, tight repeat may still be called a loop, but the
> thing that connects agents is a *flow*. "Flow" is also the more accurate word: a loop runs end→start
> with no branching and one exit; our procedures branch, escape, and compose.

**Flows compose.** A flow may invoke another flow, declared as `uses: <flow>, <flow>`. Composite
versus leaf is **not a type** — it is merely whether a flow happens to invoke others. There is no
separate "orchestrator" layer in the schema.

**Two kinds of cycle. They live in different places, and only one is legal.**

| | Definitional cycle | Execution cycle |
|---|---|---|
| What | flow A is *built from* B, B is *built from* A | one flow runs step 3, decides "not good enough", returns to step 2 |
| Graph | the `uses:` graph (definition time) | the runtime trace (execution time) |
| Verdict | **forbidden** | **allowed** |
| Why | never bottoms out — expanding it is infinite | it is *iteration*: state changes each pass, it makes progress |
| Guard | static check: walk `uses:` links, error if any path returns to its start (the `uses:` graph must be a **DAG** — directed acyclic graph: arrows only point at what a flow is built from, and no path leads back to where it began) | runtime **iteration cap** (max N retries) plus an explicit exit condition |

**Why a runtime trace may revisit a flow without breaking the DAG.** An orchestrator `A` that uses
`B` and `C` produces the trace `A → B → C → A → B → C → …`. That is legal: the `uses:` graph holds
only `A → B` and `A → C`. `B` and `C` never call `A` — the back-arrow in the trace is *`A`'s own
bounded execution loop* deciding to go around again. Composition points **downward** through layers;
only the top layer repeats, and it repeats under a cap. Structure is acyclic; the trace need not be.

This mirrors how effective agent loops (ReAct, Reflexion, Voyager) avoid running forever: an exit
condition, a hard iteration cap as backstop, and **state that changes each pass**. A cycle whose
state does not change is not iteration — it is a hang.

## Routing depth and locality (structural policy)

> Decided 2026-07-24 (workspace-os Frente 3). Governs how every subtree is structured, not just the
> library. Two axes, deliberately separate — conflating them produced the wrong "flatten everything"
> call in an earlier round.

**Locality — keep it.** Small `CONTEXT.md` glued to the files it governs is **not** overhead. On a
workspace that must also run on Sonnet and small local models, scattered local `CONTEXT.md` is what
*makes weak models navigate*, and the always-loaded index is the most cache-friendly input there is.
Do **not** consolidate local CONTEXT.md to "reduce clutter" — granularity is the feature.

**Depth — cap it.** What costs is *hops to content*: a second routing level is not uniformly free —
it helps some tasks, hurts others. So cap **chain depth**, not **file count**. When in doubt about
adding a routing level, **measure** (a real task on the tier you care about), do not decree.

**Fanout — signal it.** *Refines the line below, measured 2026-07-30 (Frente 3.2).* "File count is
not the metric" was written about **CONTEXT.md granularity** and still holds there. It was read for
two years as though it also licensed a directory holding 51 source files, which is a different
axis and one this workspace already legislated: `workspace_scanner.SPLIT_THRESHOLD` = 7 code files,
warned by `context_synchronizer.sync` since long before this note. That warning printed to stdout
during a sync nobody reads, so the tail grew unopposed to 35 directories.

The three axes, kept separate on purpose:

| Axis | Rule | Enforced by |
|---|---|---|
| **locality** | many small local `CONTEXT.md` = good, never consolidate | judgement |
| **depth** | cap hops to content; measure before adding a routing level | judgement |
| **fanout** | `WARN_FILES=7` asks for a look, `BLOCK_FILES=10` is the cap | `entropy_fanout.py`, dashboard |

**Where they meet:** splitting an over-full directory *adds a hop*, so fanout and depth trade against
each other directly. Pay the hop only when the split removes more table than it adds. Worked example:
`code/aiwbot/tests/` is 51 flat files costing 4954 tok of routing table in a 6068 tok chain; splitting
it three ways (`bugs/` `features/` `unit/`) takes depth 3 → 4 and the chain to ~3000. It pays. A
directory at 9 files usually does not — the hop costs more than the two rows it saves.

**Net rule:** many small local CONTEXT.md files = good; deep CONTEXT.md → CONTEXT.md → CONTEXT.md
chains = the thing to bound. For *routing levels*, hop count is the metric, not file count. For
*source files in one directory*, fanout is the signal — **two** numbers, symmetric with the file
pair, both in [`core/hooks/limits.env`](hooks/limits.env): warn at 7, block at 10. The gap between
them is deliberate and is where "a split that saves two rows does not pay for its hop" lives.

### What the routing table may spend tokens on

Measured 2026-07-30 across 159 `CONTEXT.md` / 1242 rows: the generated **File** table is 55k tok of
a 102k corpus — but no session reads the corpus. A real gate cascade is **2126 tok median, of which
457 (22%) is the File table**, about one `AGENTS.md`. The size is a tail, not a tax, and the tail is
row *count* (median 7 rows, worst 51), i.e. the fanout signal above. So the table stays; two rules
trim what it says:

1. **A generated column empty on every row is not emitted.** 773 of 1242 rows carried an em-dash
   `Interface`, paying width to say "nothing here". `File` and `Description` always survive.
2. **`test_*` symbols are not API** — the runner collects them, no module imports one. Keyed on the
   **symbol, never the path**: a `tests/`-directory exemption would be a door to walk production code
   through, dodging the facade and interface-stub gates. Guarded by
   `test_a_production_symbol_in_a_test_directory_still_appears`.

The `Description` column is **not** on the table for trimming: it is each file's own first-line
comment, written by hand at the source and only *surfaced* here. Measured noise is 6%. That is
curated content, which is the side of the evidence split that helps — see [refs/REFS.md](refs/REFS.md)
§ Context engineering.

**Evidence + caveat.** Controlled study on haiku-4.5 + qwen3.6-27b ([P] 2607.17598): the flat skill
pack reaches ~2× accuracy at ½ the tokens vs. raw at corpus scale, and *"the weaker the agent's
native navigation, the earlier the skill pack earns its keep."* **Preprint = provisional** (see
[refs/CONTEXT.md](refs/CONTEXT.md)); this policy is a default, not a hard gate, until our own
depth-audit (Frente 3.2) or a published source confirms it.

## Enforcement

`core/tools/sync-skills --check` parses frontmatter and fails on violations; it is wired into
`core/hooks/pre-commit`. All three layers are live:
- **skill:** frontmatter present, `name:` + `description:`, non-skills rejected.
- **flow:** `description:` + `args:` present, `type ∈ {research-brief, utility, domain}`,
  `confirm ∈ {plan, none}`. Exempt: `CONTEXT.md`, `tree.md`, `loop-*` (engineering cluster).
  Validation is **recursive** — it walks `flows/<skill>/` subfolders, not just the flat root.
- **composition:** every `uses:` target resolves to a real flow, and the `uses:` graph is a **DAG**
  (three-colour DFS; a path returning to its own start fails the check). The exemption list does
  *not* apply here — every flow file is a node, so an engineering flow cannot smuggle in a cycle.
  The **runtime iteration cap** is the other half of this guard and is *not* statically checkable:
  any flow with an execution loop must declare a numeric cap plus an exit condition in prose
  (wording in [`flows/_template.md`](flows/_template.md) § Execution Loops). Do not try to enforce
  it with the DAG check — that check forbids cycles; the cap is what *permits* them, bounded.
- **agent:** `name:` + `description:` present, `tier ∈ {low, medium, high, max}`, `model:`/`thinking:`
  forbidden in source, workers (everyone but `lead`) must carry `tools:` + `output:`.
