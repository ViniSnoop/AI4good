# Workspace-OS Roadmap — the v1 push

> **Single entrypoint for all workspace-os (wos) build work, and an index rather than a document.**
> The work lives in the `ROADMAP-<slug>.md` shards below; what stays here is what decides which one
> to open, plus what is true of all of them ([core/SCHEMA.md](core/SCHEMA.md) § A type that outgrows
> the cap shards). **The whole family is ONE ledger** — sharding does not make the shards rivals,
> and `test_no_item_lives_in_two_ledgers` reads them as one namespace.
>
> Goal file [brain/goals/workspace-os.md](brain/goals/workspace-os.md) holds *why*; this family holds
> *what*. [brain/TODO.md](brain/TODO.md) holds life tasks only; [core/ROADMAP.md](core/ROADMAP.md)
> holds agent-library internals only. An item lives in exactly one of the four — a copy is a bug.
> Evidence: [core/refs/REFS.md](core/refs/REFS.md) for external material,
> [core/experiments/](core/experiments/CONTEXT.md) for what we measured about ourselves — an
> intent item belongs here, a measurement over time belongs there, and neither restates the other.
>
> **Deletion policy: hard delete. Git is the history.** No strikethrough, no annotated corpses. A
> killed item gets one line under *Rejected* so it does not resurface looking new.
>
> **Completion is deletion, not `[x]`** (Lucas, 2026-07-30). Once a task's verification passes, cut
> the item out — do not tick it and leave it sitting there. A roadmap holds only what is still open,
> so its length is a real measure of remaining work. What was built is recorded by the code, its
> tests, and git. Keep a line only when the *next* session needs it to extend the work instead of
> recreating it, and write that line as present-tense state, never as a report of what was done.

## v1 definition of done

Four criteria. Nothing else gates v1.

| # | Criterion | Owner | State |
|---|-----------|-------|-------|
| 1 | **verify-fast green + Tier 0 live** — naming, placement, pointer integrity, size-as-signal deterministic; **this repo** clean, every nested repo on a shrinking baseline | [`ROADMAP-entropy.md`](ROADMAP-entropy.md) | checks live · **read [`entropy.md`](entropy.md) for the count, never a copy of it** |
| 2 | **One ledger, no duplicates** — this family is the sole wos ledger, verified by scan not eyeball | [`ROADMAP-ledger.md`](ROADMAP-ledger.md) | ✅ **MET 2026-07-30** — `test_no_item_lives_in_two_ledgers` |
| 3 | **Everything pushed, gitflow-shaped** — every `code/` repo on `main`/`feature/*`, zero unpushed, no repo without a remote | — | ✅ **MET 2026-08-14** — re-run, never trusted: one loop over `find . -name .git` asserting a remote and a legal branch per repo |
| 4 | **Clonable by a student** — fresh clone gets every feature; deps declared, no undocumented hand-installs | [`ROADMAP-portability.md`](ROADMAP-portability.md) | ✅ **MET 2026-08-16** — `SETUP.md` is an executed procedure, every dep declared in `core/tools/deps.txt`, both enforced by `verify-fast` |

Post-v1 validation is `[mvp-validate]`: use the system daily for 30 days, then assess whether it
reduced mental load. That is the real test and it can only run after v1.

## How to read this

Per-step `tier` = the tier that is *enough* (a floor, not a ceiling). **Which concrete model
fills a tier is data and lives in [`core/flows/craft/routing.md`](core/flows/craft/routing.md),
never here** — a ledger that names a vendor's model goes stale the day that model does.
🔴 needs Lucas · 🟡 pilot on one subtree first · 🟢 mechanical.

**How many steps need Lucas is in the § Routing table below, per shard, counted from the marks.**
Nobody keeps that number: a hand-kept one was wrong four times, twice while the paragraph asking to
keep it true sat directly above it, and once as *two lists of the same set* — here and in
§ Sequencing — naming different threes and both claiming three. The generator counts marks in item
position, which is also what the phrase means: **🔴 is "Lucas decides", never "this is hard"**; an
item a high-tier agent can rule on alone is 🟡. Every one of them is a research-and-discussion item
rather than a question with options attached, which is what he has asked for in every case.

**Never cite an item number outside the roadmap family** — enforced on every commit by
`checks/citation-gate.py` ([`core/hooks/SPECS.md`](core/hooks/SPECS.md) § Git pre-commit), which
matches `ROADMAP.md` and `ROADMAP-<slug>.md` and nothing else. Completion is deletion, so a cited
number is a pointer to nothing the day the item lands; point at the section that owns the rule
instead — or, across shards, at the shard's filename, which is what `blocked-by` carries.

Measurements never live here. The instrument is
[`core/tools/wos/session/context`](core/tools/wos/session/context); results live in
[`core/experiments/`](core/experiments/CONTEXT.md); drift counts live in [`entropy.md`](entropy.md).
Re-run them rather than quoting a number from this file.

**Load-bearing principle: automatic + zero-token beats agent-checked, and free checks are never
coupled to paid ones.** Deterministic scripts per-commit; human judgment on demand.

> **Evidence caveat, once for the whole doc.** Some steps lean on two strong but *unreviewed*
> preprints — progressive disclosure ([P] 2607.17598) and ACE ([P] 2510.04618). Provisional; never a
> hard gate.

---

## Sequencing

**All four v1 criteria are met.** Everything left is past v1, so the governing constraint in
[`brain/goals/workspace-os.md`](brain/goals/workspace-os.md) applies at full force: an item that does
not earn its keep is a candidate for *Rejected*, not the backlog.

**The plan is four tracks, named rather than numbered.** An item number is a moving target under a
delete-on-completion policy, and this section is where the two-lists asymmetry has bitten twice — so
it points at work by name and at people by mark, never by number.

**Track A — wire the registry to zero.** Drained 2026-08-18 down to one row, whose blocker is a
decision rather than work; what is left of the track is [`ROADMAP-portability.md`](ROADMAP-portability.md)
and needs no separate plan. The three layers with no rows at all — `agents`, `flows`, `norms` — are
named there too.

**Track B — the one hard chain, because each step is the next one's precondition.**
1. The **public scaffold repo** at `code/wos/` and its one-way sync. It stopped being a neighbour of
   the ablation on 2026-08-17 and became its **hard precondition**: the experiment runs on variants
   built from the public repo, so no public repo means no arms to compare. Students needing a
   research-branch workspace makes it demand as well as precondition.
2. The **ablation**, against whatever is switchable by then. Design is high tier and belongs to the
   paper twin; the run is medium.

**Track C — unordered and mechanical, all medium tier.** The open rows in
[`ROADMAP-entropy.md`](ROADMAP-entropy.md) — including its § Declared but unbuilt —
[`ROADMAP-ledger.md`](ROADMAP-ledger.md), [`ROADMAP-cost.md`](ROADMAP-cost.md) and the post-v1 half
of [`ROADMAP-self-description.md`](ROADMAP-self-description.md), plus the declaration-table rename to
`.tsv` ([`core/SCHEMA.md`](core/SCHEMA.md) § The `.md` type system). Two of these are waiting on one word
from Lucas rather than on work: whether `CTX_LOUD` should **offer** the session close, and whether
frozen run records are exempt from the state-dir rename.

**Track D — the sittings.** The 🔴 rows, plus the thinking-effort measurement, which additionally
needs Track A finished because it runs on the registry.

**Needing Lucas: the list is in § How to read this and only there.** It used to be restated here and
the two copies named different threes, each missing a different item, both claiming three. **Two
lists of the same set is the asymmetry; the count is only its symptom.**

## Model-switching guide

The canonical guide lives in the flow that produced this plan:
**[`core/flows/research/scout.md`](core/flows/research/scout.md) → "Canonical model-switching guide"**
(same-session `/model` · `/craft` autorouting · Agent-tool `model:` override · `/handoff`).
Mapping: 🔴 → **high tier, same session**; 🟢/🟡 → **medium via `/craft`** (mechanical parts drop to
low). Which model fills each tier is data in that file, never in this one.

<!-- routing:start -->
## Routing

| Shard | Description | Prio | Open | Needs Lucas | Blocked by | Items |
|-------|-------------|------|------|-------------|------------|-------|
| [`ROADMAP-archive.md`](ROADMAP-archive.md) | Blocked on a trigger, parked out of v1, or killed — with the reason kept. | — | — | — | — | `gdrive-integration` `offline-resilience` `task-metric` |
| [`ROADMAP-cost.md`](ROADMAP-cost.md) | Where session spend goes, which tier runs what, and what loads every session. | important | 6 | 1 | — | — |
| [`ROADMAP-entropy.md`](ROADMAP-entropy.md) | Tier 0 checks, the shrinking-baseline ratchet, and rules declared but unbuilt. | essential | 14 | 3 | — | — |
| [`ROADMAP-ledger.md`](ROADMAP-ledger.md) | One ledger with no duplicates, and what each `.md` type is allowed to be. | essential | 6 | 1 | — | — |
| [`ROADMAP-legibility.md`](ROADMAP-legibility.md) | Lucas can no longer read his own workspace, and that is the root cause. | essential | 8 | 2 | — | — |
| [`ROADMAP-measurement.md`](ROADMAP-measurement.md) | Nothing here has been measured, and confident wrong answers pass unchallenged. | important | 4 | 3 | ROADMAP-portability.md | — |
| [`ROADMAP-portability.md`](ROADMAP-portability.md) | A fresh clone gets every feature: declared deps, no undocumented hand-installs. | essential | 2 | 1 | — | — |
| [`ROADMAP-self-description.md`](ROADMAP-self-description.md) | The workspace describes itself wrongly, plus the work reopened after v1. | important | 4 | 1 | — | — |
<!-- routing:end -->
