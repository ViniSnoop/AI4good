# Core Library Schema
> The enforced frontmatter contract for skills, flows, and agents, plus the workspace-wide `.md`
> type system. Drift from this is a bug.

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
| `ISSUES.md` | What is currently **untrue** that we know about? (hand-written issues + generated measurements) |
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

### Boundaries where types nearly touch

The three real conflicts, with the resolving rule:

| Conflict | Rule |
|----------|------|
| `CONTEXT.md` vs its own routing block | CONTEXT **never hand-lists files**; the generated routing block owns inventory. A hand-written File Map is a bug — as a bullet list *or* a table, both counted by `entropy_context.check_inventory`. **But ask why it was written before deleting it**: `core/hooks/CONTEXT.md` hand-listed `limits.env` and three siblings because the generator could not *reach* them, and cutting the table would have cut three real pointers. Fix the generator first, then the list is redundant. |
| `CONTEXT.md` vs `SPECS.md` | Rules that *constrain code* → SPECS. What the directory *is* → CONTEXT. |
| `ROADMAP.md` vs `ISSUES.md` | ISSUES owns the issue text; ROADMAP references it by id and never restates it. Intent vs. state: a roadmap item leaves the list when deprioritised, an issue does not stop being true. |
| `ISSUES.md` hand-written vs generated | The hand-written issues come first; every generated measurement lives inside its own delimited block (`entropy:start`, `verify:start`) exactly as the routing block does inside `CONTEXT.md`. Never hand-edit inside a block, and never write a measured number outside one — a copied count is the drift these checks exist to catch. The FIXED gate governs the hand-written half only. |

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

<!-- routing:start -->
## Routing

| Shard | Description | Answers | Enforced by |
|-------|-------------|---------|-------------|
| [`SCHEMA-layers.md`](SCHEMA-layers.md) | The frontmatter every skill, agent, norm and flow declares, and how they… | what fields each layer requires, which layer may point at which | core/tools/wos/skills/validate.sh |
| [`SCHEMA-outgrowing.md`](SCHEMA-outgrowing.md) | Where an unclassified name goes, and how a type that passed the cap splits. | what to do with an off-allowlist name, how a type shards, what an index keeps | core/hooks/checks/type-gate.py, core/hooks/checks/pre-edit.py |
| [`SCHEMA-placement.md`](SCHEMA-placement.md) | Which directory a file belongs in, and how deep the routing may go. | where a file lives, how many hops to content, when a directory splits | core/hooks/entropy/entropy_naming.py, core/hooks/entropy/entropy_fanout.py |
| [`SCHEMA-vocabulary.md`](SCHEMA-vocabulary.md) | One word per idea, one idea per word, and every token a rename retired. | which spelling is canonical, what a term means, what may no longer be written | core/hooks/entropy/entropy_ledger.py, core/hooks/checks/citation-gate.py |
<!-- routing:end -->
