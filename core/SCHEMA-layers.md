# The agent-library layers
> The frontmatter every skill, agent, norm and flow declares, and how they compose.
> answers: what fields each layer requires, which layer may point at which
> enforced-by: core/tools/wos/skills/validate.sh

## Frontmatter contract

Companion to the code-side spec-drive convention (the `> spec:` module gate in `core/hooks/pre-commit`,
tracked under the [[spec-driven-development]] goal): that governs `code/` modules, this governs the
`core/` agent library.

**No flow is privileged.** The exemplar is [`flows/_template.md`](flows/_template.md) — a template,
nothing more. There is no "reference implementation" whose behaviour defines correctness: that dual
role couples one flow's evolution to the schema. Realism is guaranteed by `validate_flows` running
over *every* flow, including the template, not by anointing one.

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

**A skill's `refs/` folder:**

1. The folder sits **beside the skill file**, at `core/skills/<name>/refs/`.
2. `.yaml` for structured references — papers, datasets, configs with a schema.
3. `.md` for reading notes and informal summaries.
4. `REFS.md` for one-line link captures, the shape `/inbox` writes.
5. **Never** create `refs/` under `.claude/` or `.opencode/` — those are generated mirrors, and
   `sync-skills` prunes anything it did not put there.

**Sub-skills group into a suite folder** when a parent routes to them: the parent stays at
`core/skills/<name>.md` and is the only file mirrored; sub-skills live at `core/skills/<name>/*.md`,
are read from source, and drop the parent's prefix from their filenames (`foundry-canvas.md` inside
`foundry/` is `canvas.md` — the folder already says `foundry`).

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
— e.g. Claude Code's `.claude/agents/craft-high.md` carries `model: opus` for `tier: high`. **There is
no generator**, so keep each mirror's `model:` in sync with its source `tier:` by hand.
**No `thinking:` and no `model:` in `core/agents/` source.**

## Layer: norm — `core/norms/<name>.md`

| field | req | value |
|-------|-----|-------|
| `name` | ✅ | kebab-case, matches filename |
| `description` | ✅ | one line: what obeying the rule buys. Feeds the routing table, never `AGENTS.md` |

**The body is the published rule, verbatim.** Everything after the frontmatter is written into
`AGENTS.md` as one bullet by [`hooks/routing/norms.py`](hooks/routing/norms.py) — no rendering, no
wrapping. `AGENTS.md` is always loaded, so a norm's body is its entire cost: a rule needing a
paragraph of rationale is a `SPECS.md` section plus a pointer, not a longer norm.

**Order comes from [`features.txt`](features.txt), not from the directory listing.** Order matters in
a prompt, and two ordered lists of one set is the asymmetry this workspace keeps paying for — so
moving a rule up the prompt means moving its registry row. That generator is also the group's single
feature switch, the same shape as the skills mirror: a norm switched off is never written, so the
ablation removes it from every session's prompt instead of marking it inactive.

A norm that acquires a checker **stops being a norm and becomes a hook** — move the file, move the
registry row's group, and let the guard live where the check runs.

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
