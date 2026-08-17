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
| **craft flow** | the `/craft` skill, `core/flows/craft/` (retired spellings: § Retired tokens) |
| **Front** | a top-level workstream in `ROADMAP.md` (retired spelling: `Frente`) |

**Why `Front` and not `Workstream`** — ruled 2026-08-16 (Lucas). *"progress on several fronts"* is
ordinary English for parallel areas of effort, which is exactly what these are, so the word carries
the meaning without the military or meteorological reading a bare *front* invites. It also keeps the
initial, so every existing habit of reference survives the rename. A roadmap heading is a
**contract**, and this workspace writes contracts in English even where its rationale is Portuguese.

**A Front number is not a citable identifier.** Closed items are deleted, so `Front 4.1` becomes a
dead pointer the day the work lands — cite the `SPECS.md` or `SCHEMA.md` section that owns the rule
instead. Numbering is legal only inside `ROADMAP.md` / `ROADMAP-<slug>.md`, and in commit messages,
which git keeps.

### Retired tokens

**A rename is finished when its old token appears nowhere.** Until then the leaves drift back and the
drift is indistinguishable from entropy — the lesson of the `loops`→`flows` rename, which kept
resurfacing because nothing asserted its completion.

This table *is* the assertion. `core/hooks/entropy/entropy_ledger.py` fails if any token below survives in a
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
| `/loops` | `/craft` | 2026-08-17 |

**The skill rename is a shape, not a word, for the same reason `Frente` is.** `loops` is ordinary
English — the corpus holds a thousand honest uses, from "file-relayed loops" to "execution loops"
to "Loop 0..6" as step names — so a bare `loops` row would fail on correct prose the day it was
written. What is retired is the **command**, so the row is the invocation shape `/loops`. The
per-run state dir `.loop/<slug>/` is a *different* token on the same rename and is deliberately
absent: it is still live in fourteen directories across three repos, and a row that fails today
teaches people to ignore the check. It joins this table when that sweep lands.

**`Frente`→`Front` (2026-08-16) is deliberately *not* a row here, and the reason is a limit of
this table.** Every token above is a coined string that can only mean the thing it names, so a
bare-word match is safe. `frente` is an ordinary Portuguese noun — `branches/casinhas/CONTEXT.md`
uses it in a table header to mean a work front on a building site — and a row would have failed
on honest prose the day it was written, which is precisely what the paragraph above says trains
people to ignore a check. `core/hooks/checks/citation-gate.py` owns that rename instead, by
matching the **citation shape** `Frente <n>` rather than the word. The word stays legal; the
pointer does not. **A rename whose old spelling is also a real word needs a shape, not a token.**

Not yet listed because the rename has not landed: `SPEC.md`→`SPECS.md` (load-bearing in five
enforcement points; see [ROADMAP.md](../ROADMAP.md)). A token joins this table only when
the sweep is complete — a row that fails on the day it is written trains people to ignore the check.

## The `.md` type system

> Decided 2026-07-30. Lucas: *"delimit precisely where one file ends and another begins, so there is
> no conceptual intersection."*

**`UPPERCASE.md` is a type. `lowercase.md` is an instance.** A type means the same thing in every
subtree; an instance is content, named freely. Uppercase names are therefore a **closed set** —
inventing a type must be a deliberate act (one line added below), never an accident.

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
| `MEMORY.md` | Which memories exist, and what is each about? (index + router, `brain/memory/` only) |
| `SETUP.md` | How do I make this environment work? (toolchain install + config) |
| `SCHEMA.md` | This file: the law about types. |

Anything else is rejected: *"add it to the allowlist if you mean it."*

`MEMORY.md` earns its row on symmetry: `~/.claude/projects/<slug>/memory` is a symlink to
`brain/memory/`, so it stands to [`brain/memory/`](../brain/memory/CONTEXT.md) exactly as `GOALS.md`
stands to `brain/goals/` — an index and router over a directory of instances, one line each, loaded
every session. The instances themselves are lowercase and need no type. **It is the one type written
by the agent rather than authored**, which is why its content is checked like any other file.

`SETUP.md` earns its row on the evidence: `README.md` is **repo-root only**, and several instances
sit in directories that are not repos — the workspace root, `academy/`, `code/`, `code/_templates/`.
"How do I make this work" is not "what is this and how do I run it". **The type survives — ruled
2026-08-16 (Lucas), and the question is closed.** The install path does not stop being prose, it
becomes *executable* prose: the harness the newcomer already opened is what performs the install,
reading this file as a procedure. That makes `SETUP.md` the deliverable rather than the thing an
installer replaces. The per-directory instances answer a question no installer covers — `code/`
holds per-language setup, `academy/` the LaTeX toolchain — so they are not install steps that a
root-level script absorbs.

### The four disposal routes

An off-allowlist `UPPERCASE.md` is not automatically wrong — it is *unclassified*. Route it, so a new
name resolves without a decision meeting (decided 2026-07-30):

| Route | When |
|-------|------|
| lowercase instance | **generated** by a tool |
| lowercase instance | hand-authored **content** |
| → `SPECS.md` | hand-authored **constraint** |
| new type | answers a question **no type answers** — `SETUP.md` is the only one that ever qualified |

**A generated file that is also a ratchet is tracked, at the root** (ruled 2026-08-17). `entropy.md`
takes the first route and the case half of the question was never open: it is written by
[`core/hooks/entropy/entropy-dashboard.py`](hooks/entropy/entropy-dashboard.py) and committed by
[`core/tools/wos/roundup`](tools/wos/roundup), never authored, so it is lowercase like any other
generated instance. What looked like an oversight is its **placement** — every other generated
artifact lives beside its generator or under `outputs/`, and this one sits at the workspace root.
It sits there because `outputs/` is gitignored and **a ratchet that is not tracked cannot ratchet**:
the whole use of the number is being diffable commit over commit, which is what makes "the count
must shrink" a check rather than a feeling. So the untracked route is not available to it, and of
the tracked ones the root is right for the same reason `core/SCHEMA.md` sits at `core/` root rather
than inside `core/hooks/` — it measures the whole workspace, and a file that measures everything
does not live inside one of the things it measures.

**A declaration table is a fifth thing, and it takes none of these routes** (ruled 2026-08-16).
`core/features.txt` and `core/profile.txt` join `core/hooks/limits.env`, `core/tools/deps.txt`,
`core/hooks/vendored.txt` and `core/hooks/extensionless.txt`: tab-separated or `key=value` data,
authored by hand, read by exactly one law module, and **never prose**. It is not an
`UPPERCASE.md` awaiting classification — the type allowlist stays closed and untouched, which is
the whole reason the shape is worth naming. The two at `core/` root rather than beside their
reader are there for the same reason `core/SCHEMA.md` is: they are read by `core/hooks/`, but they
govern the whole workspace, and a file that governs everything does not live inside one of the
things it governs.

**The extension names the shape** (ruled 2026-08-17, Lucas: *"`.txt` seems too naive"*). The class
is one idea but not one format, and `.txt` was carrying three jobs while saying "unstructured text"
about a file with a closed seven-column header:

| shape | extension | files |
|---|---|---|
| tab-separated table with a header row | `.tsv` | `core/features.tsv`, `core/profile.tsv`, `core/tools/deps.tsv` |
| one value per line, no columns | `.txt` | `core/hooks/vendored.txt`, `extensionless.txt`, `gitignore-exceptions.txt` |
| `key=value` | `.env` | `core/hooks/limits.env` |

`.tsv` is a registered media type (`text/tab-separated-values`), so this buys editor and diff
support as well as honesty. The rule is what makes the two that did **not** move right *by the
rule* rather than by accident, which is the half worth keeping: a one-value list genuinely is plain
text, and only the tables were mislabelled.

`SPEC.md` is **not** a type: it collapses into `SPECS.md` (decided 2026-07-30, Lucas). The
singular/plural pair was the sharpest asymmetry in the corpus — two spellings, one meaning — and it
had leaked into enforcement, so the `> spec:` convention, `core/hooks/pre-commit` §1d,
`core/hooks/read/spec-read-gate.py`, `core/hooks/read/context-tracker.py`, `core/tools/wos/spec-scan` and
`core/tools/wos/spec-contract-check` all move with it.

### Boundaries where types nearly touch

The three real conflicts, with the resolving rule:

| Conflict | Rule |
|----------|------|
| `CONTEXT.md` vs its own routing block | CONTEXT **never hand-lists files**; the generated routing block owns inventory. A hand-written File Map is a bug — as a bullet list *or* a table, both counted by `entropy_context.check_inventory`. **But ask why it was written before deleting it**: `core/hooks/CONTEXT.md` hand-listed `limits.env` and three siblings because the generator could not *reach* them, and cutting the table would have cut three real pointers. Fix the generator first, then the list is redundant. |
| `CONTEXT.md` vs `SPECS.md` | Rules that *constrain code* → SPECS. What the directory *is* → CONTEXT. |
| `ROADMAP.md` vs `BUGS.md` | BUGS owns the bug text; ROADMAP references it by id and never restates it. Intent vs. state: a roadmap item leaves the list when deprioritised, a bug does not stop being true. |

### Placement: tier × read-frequency

§ Boundaries answers *which of two types*. This answers the prior question: **does this content earn
its place, and where does it belong?** Deleting is one of four outcomes, not the default one.

**Tier — ask what happens to an agent that never reads this.** Applied per *section*, never per file:

| Tier | Test | What it costs to carry |
|------|------|------------------------|
| **ESSENTIAL** | work comes out **wrong** — a rule broken, the wrong file edited, work lost | must be paid; put it where it is read without asking |
| **IMPORTANT** | work comes out **slower** — re-derived, re-asked, rediscovered | one hop away, never preloaded |
| **DESIRABLE** | **nothing changes** — rationale, provenance, the story of a change | git already holds it |

That question runs second. The first is **is it still true?** — checked against code, tests and
`git log`, not memory. An untrue ESSENTIAL is the most expensive object in the workspace.

**Read-frequency is a property of the enforcement layer, not a guess.**

| | Types | Why |
|---|---|---|
| **HOT** | `CONTEXT.md` | the only **enforced-read** type: `hooks/read/context-gate.py` demands the whole chain before any file access in a subtree |
| | `AGENTS.md`, `MEMORY.md` | folded into the system prompt every session |
| | `GOALS.md`, `ROADMAP.md` | induced-hot — the root `README.md` sends every reader to them first |
| **COLD** | `SPECS.md`, `REFS.md`, `BUGS.md`, `SETUP.md`, `USER.md`, `TODO.md` | on demand only |
| **MACHINE-READ** | `SCHEMA.md` | cold to humans, parsed on every check — so its *tables* are load-bearing where its prose is not |

**Where the two axes meet:**

| | HOT | COLD |
|---|---|---|
| **ESSENTIAL** | **KEEP** | **PROMOTE** — it is arriving too late to prevent the error |
| **IMPORTANT** | **REDIRECT** down, leave one pointer line | **KEEP** |
| **DESIRABLE** | **CUT** | cut on sight; cheap either way |

**A provider's own directory is not a placement, it is an escape.** `AGENTS.md` § provider-agnostic
storage: state written to a harness's private path is outside the type system entirely — no type
owns it, no check reads it, and it does not survive a change of harness. Symlink the path the
harness insists on into the tree and the file becomes an ordinary instance again, checked like any
other. `brain/memory/` is the live case.

REDIRECT needs no new mechanism: `CONTEXT.md` (hot) already pairs with a sibling `SPECS.md` (cold),
which is the thin-front/leaf-detail split, and `ROADMAP.md` pairs with `ROADMAP-<slug>.md`. **A
constraint sitting in a `CONTEXT.md` head is the standard defect** — it is a SPECS answer trapped in
the one file the gate forces everyone to read. Measurement and its dashboard section:
[`entropy.md`](../entropy.md).

Compression is the **last** step and only on what survives, because it is measured to be nearly
worthless on this corpus — a pilot moved the worst offender 0.22% for a full model call. Placement
beats phrasing.

**The REDIRECT recipe, in order.** It survived contact with the whole `core/` corpus, and the order
is the part that pays:

1. **Delete what a hook already enforces.** A gate names its own fix when it fires, so restating it
   is pure cost. The exception is a number that changes how you write *before* the hook can speak —
   the 150/200 line caps stay.
2. **Move constraints to a sibling `SPECS.md`**, creating it if absent.
3. **Move data out** — alias lists, schemas, key tables.
4. **Delete stale claims.**
5. **Keep identity and navigation only.**

**Running step 1 first is what makes it cheap: six new `SPECS.md` instead of eleven.** Most of what
looked movable was already written better somewhere else — a path table duplicating the file's own
generated routing block, a layering table duplicating the child `CONTEXT.md`, a vocabulary section
restating this file verbatim. **Open the child `CONTEXT.md` and the file's own routing block before
relocating anything.**

**What replaces a moved section is one thin pointer line, never an instruction.** Write
`Gate behavior and the agent-shim contract: SPECS.md`; never "you must read SPECS.md". The check
fires on an over-size head *and* a modal, so the modal is the half that makes prose a trapped
constraint. A large head with no modals is identity and navigation, and is correct as it is — the
token warn is a signal, not a cap.

**A doc pass is a cheap fuzzer for the generators that read those docs.** Every pass over this
corpus has surfaced a generator bug rather than a prose problem, because relocating sections writes
file shapes nobody had written before — a `SPECS.md` inside `core/skills/` read as a skill and
failed the commit for every staged sibling; two extensions were scanned with no comment pattern and
so were reported as undescribed no matter how well they were commented. Expect one, and fix it at
the generator.

### No archive types

`ARCHIVE.md`, `HISTORY.md` and `.log/done.md` are **deleted, not renamed**. A file that is "never
auto-loaded, ask explicitly" is doing git's job. **Done work is deleted; git is the history.**

The same rule applies *inside* a file, not only to whole files (Lucas, 2026-07-30): **a completed
`ROADMAP.md` item is cut, not ticked.** `[x]` is an annotated corpse with a checkbox — it keeps
paying rent in every read of the file, and it makes the roadmap's length measure history instead of
remaining work. Trim on verified completion. Keep a line only when the next session needs it to
*extend* the work rather than recreate it, and write that line as present-tense state ("extend
`core/hooks/checks/type-gate.py`"), never as a report ("✅ built the type gate").

One thing git cannot hold: an approach we *tried and rejected* was never committed. That content has
exactly one home — a one-line entry under `## Rejected` in the relevant `ROADMAP.md` (for a ditched
goal, under `## Ditched` in `brain/GOALS.md`). One line, with the reason, so a dead idea does not
resurface looking new.

### The one exception: transient initiative docs

A **cross-project rollout** with cited anchor ids and a defined death date is a real thing, but
**it is not a new type** — ruled 2026-08-14 by Lucas: *"unify, use the semantic symmetry strategy,
guarantee coverage and precision with zero conceptual intersection between those files… and make
sure as well that we do not create a new .md file for each specific minor thing."*

The resolution follows from the type table itself. A rollout is *intent, plan, and what we rejected*,
scoped to one initiative — which is precisely the question ROADMAP answers. It never needed a name
of its own; it needed a **scope suffix**. So a structural plan lives inline in the target project's
roadmap **or as a referenced ROADMAP-\<slug\>.md** — that sanction is this table's, enforced by
`checks/type-gate.py` against the exempt set closed at four. The conceptual intersection with ROADMAP
disappears (there was one: both answer *what do we intend to do*), and the type count does not grow.
**Five differently-named files were the symptom of a missing suffix, not of a missing type.**

**A session plan is not a roadmap, and the type system does not reach it** (ruled 2026-08-17, Lucas:
*"session plans and roadmaps are two different things… I am not even sure we need to keep that
directive"*). They differ in kind, not in placement: a roadmap is **structural, mid- and long-term**
and is re-read every few sessions; a session plan is **ephemeral, short-term, detailed execution**,
alive for one sitting. So a harness that writes a session plan to its own scratch path creates no
conflict with anything here — there is nothing to track, and the roadmap is not forgotten because a
plan sat elsewhere for an afternoon. The workspace-root rules used to carry a `PLANS LIVE IN ROADMAPS`
directive that read as a conflict precisely because it conflated the two; it was **deleted** rather
than given an exception, since placement of the structural kind is already blocked by the gate above
and the ephemeral kind was never in scope.

Membership **only shrinks** and each survivor has a route.

| File | Route | Why |
|---|---|---|
| `code/ROADMAP-spec-drive.md` | → ROADMAP-spec-drive.md | same shape, no anchor citations |
| `code/isoroll-module/REFACTOR.md` | → ROADMAP-refactor.md | project-local, cheapest of the three |
| `code/dobra/DECISIONS.md` | → that project's SPECS.md | **not a roadmap at all** — decisions are *what must be true and why*, which is the SPECS question. It sat in this list by naming accident |

**A rename preserves every anchor id**, so a doc cited by anchor from source comments (`W1`, `G5`,
`I2`) costs only its paths. A row leaves this table the day its rename lands, because the suffix
shape is recognised on its own by [`entropy_naming.py`](hooks/entropy/entropy_naming.py) — the
exemption covers the *old* name and nothing else.

**Every backticked `.md` name in this section is parsed as an exemption**, so naming a retired file
here to explain its history puts it straight back on the list. Say the name without backticks, or
leave it to git.

Until each rename lands, these stay exempt from the allowlist **and** carry an obligation: each
must state its own death condition on line 3, and be deleted when its rollout completes. They are the
only `.md` files allowed to be temporary, so a stale one is the most expensive kind of clutter.

---

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

> Decided 2026-07-24. Governs how every subtree is structured, not just the
> library. Two axes, deliberately separate — conflating them produced the wrong "flatten everything"
> call in an earlier round.

**Locality — keep it.** Small `CONTEXT.md` glued to the files it governs is **not** overhead. On a
workspace that must also run on Sonnet and small local models, scattered local `CONTEXT.md` is what
*makes weak models navigate*, and the always-loaded index is the most cache-friendly input there is.
Do **not** consolidate local CONTEXT.md to "reduce clutter" — granularity is the feature.

**Depth — cap it.** What costs is *hops to content*: a second routing level is not uniformly free —
it helps some tasks, hurts others. So cap **chain depth**, not **file count**. When in doubt about
adding a routing level, **measure** (a real task on the tier you care about), do not decree.

**Fanout — signal it.** "File count is not the metric" governs **CONTEXT.md granularity** and nothing
else. Source files in one directory are a different axis: `workspace_scanner.SPLIT_THRESHOLD` reads
`WARN_FILES` from [`limits.env`](hooks/limits.env) — never its own copy of the number — and
`entropy_fanout.py` reports it to the dashboard rather than to a stdout nobody reads, which is what
let the tail grow unopposed before.

The three axes, kept separate on purpose:

| Axis | Rule | Enforced by |
|---|---|---|
| **locality** | many small local `CONTEXT.md` = good, never consolidate | judgement |
| **depth** | cap hops to content; measure before adding a routing level | judgement |
| **fanout** | `WARN_FILES=7` asks for a look, `BLOCK_FILES=10` is the cap | `entropy_fanout.py`, dashboard |

**Where they meet:** splitting an over-full directory *adds a hop*, so fanout and depth trade against
each other directly. Pay the hop only when the split removes more table than it adds. A directory in
the dozens pays — the routing table it sheds dwarfs the one hop it costs. A directory at 8-9 files
does not: the hop costs more than the two rows it saves, which is why `WARN_FILES` asks for a look
instead of blocking. Current offenders are listed in [`entropy.md`](../entropy.md) § Directories
holding too many files; read that rather than a worked example, which goes stale the moment the
split lands.

**Net rule:** many small local CONTEXT.md files = good; deep CONTEXT.md → CONTEXT.md → CONTEXT.md
chains = the thing to bound. For *routing levels*, hop count is the metric, not file count. For
*source files in one directory*, fanout is the signal — **two** numbers, symmetric with the file
pair, both in [`core/hooks/limits.env`](hooks/limits.env): warn at 7, block at 10. The gap between
them is deliberate and is where "a split that saves two rows does not pay for its hop" lives.

### What the routing table may spend tokens on

**No session reads the corpus; it reads a chain.** A corpus-wide sum is therefore the wrong number to
optimise, and the cost that is real is row *count* per chain — i.e. the fanout signal above, not the
table's existence. So the table stays; two rules trim what it says. Re-run
[`core/tools/wos/session/context`](tools/wos/session/CONTEXT.md) for the live figures rather than
quoting any printed here.

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
[refs/CONTEXT.md](refs/CONTEXT.md)); this policy is a default, not a hard gate. Nothing here has been
measured on our own corpus — [ROADMAP.md](../ROADMAP.md) § ablation is where that would happen.

## Enforcement

`core/tools/wos/sync-skills --check` parses frontmatter and fails on violations; it is wired into
`core/hooks/pre-commit`. All three layers are live:
- **skill:** frontmatter present, `name:` + `description:`, non-skills rejected.
- **flow:** `description:` + `args:` present, `type ∈ {research-brief, utility, domain}`,
  `confirm ∈ {plan, none}`. Exempt: `CONTEXT.md` and everything under `flows/craft/` — the
  engineering cluster is exempted **by path**, which is why `tree.md` needs no separate mention.
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
