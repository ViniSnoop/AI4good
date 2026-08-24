# Workspace-OS Roadmap — the v1 push

> **Single entrypoint for all workspace-os (wos) build work, and an index rather than a document.**
> The work lives in the `ROADMAP-<slug>.md` shards below; what stays here is what decides which one
> to open, plus what is true of all of them ([core/SCHEMA.md](core/SCHEMA.md) § A type that outgrows
> the cap shards). **The whole family is ONE ledger** — sharding does not make the shards rivals,
> and `test_no_item_lives_in_two_ledgers` reads them as one namespace.
>
> Goal file [brain/goals/workspace-os.md](brain/goals/workspace-os.md) holds *why*; this family holds
> *what*. Personal life tasks live in the goal backlog they serve (`brain/goals/*.md`), not here;
> [core/ROADMAP.md](core/ROADMAP.md) holds agent-library internals only. An item lives in exactly one
> of the three — a copy is a bug.
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
| 1 | **verify-fast green + Tier 0 live** — naming, placement, pointer integrity, size-as-signal deterministic; **this repo** clean, every nested repo on a shrinking baseline | [`ROADMAP-entropy.md`](ROADMAP-entropy.md) | checks live · **read [`ISSUES.md`](ISSUES.md) § Entropy for the count, never a copy of it** |
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
`checks/citation-gate.py` ([`core/hooks/SPECS.md`](core/hooks/SPECS-gates.md) § Git pre-commit), which
matches `ROADMAP.md` and `ROADMAP-<slug>.md` and nothing else. Completion is deletion, so a cited
number is a pointer to nothing the day the item lands; point at the section that owns the rule
instead — or, across shards, at the shard's filename, which is what `blocked-by` carries.

Measurements never live here. The instrument is
[`core/tools/wos/session/context`](core/tools/wos/session/context); results live in
[`core/experiments/`](core/experiments/CONTEXT.md); drift counts live in [`ISSUES.md`](ISSUES.md) § Entropy.
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
`.tsv` ([`core/SCHEMA.md`](core/SCHEMA.md) § The `.md` type system).

**Nothing in this track waits on a word from Lucas any more, and this paragraph claimed two things
did for longer than either was true** — a specimen of the front directly below, found by one probe
on 2026-08-24. `CTX_LOUD` was ruled on 2026-08-17 (show both crossings, to both readers, at the end
of a response); the state-dir rename landed, so no run record carries the old name and the exemption
question had nothing left to be about. Frozen run records were ruled the same day: a finished chain's
trail is deleted like any other done work, and git is its history.

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
| [`ROADMAP-archive.md`](ROADMAP-archive.md) | What is NOT being worked on, and what would change that? Three kinds: blocked on a named trigger, parked as out of scope, killed outright — each keeping its reason so a dead idea cannot return looking new. Read it before proposing something that sounds obvious; nothing here counts toward the drain, so Open reads empty. | — | — | — | — | `gdrive-integration` `offline-resilience` `task-metric` |
| [`ROADMAP-cost.md`](ROADMAP-cost.md) | What does a session cost, and which of that is avoidable? Holds which tier runs what, what loads at session start, and what fills the context window. Open it for what we intend to change about spend; every measured number lives in `core/experiments/`, so re-run the instrument for what spend actually is. | important | 6 | 1 | — | — |
| [`ROADMAP-entropy.md`](ROADMAP-entropy.md) | Does the tree still have the shape we said it has, and does anything check? Holds the Tier 0 checks, the ratchet that makes their count shrink, and rules declared in a `SPECS.md` with no implementation. Open it for a check, a drifted name or an unenforced limit — never for what the drift *means*, which is legibility's. | essential | 8 | — | — | — |
| [`ROADMAP-ledger.md`](ROADMAP-ledger.md) | Where does a piece of writing belong, and is it written down twice? Holds the `.md` type system's unfinished migrations and the rule that an item lives in exactly one ledger. Open it when a file's NAME or PLACE is the question; the law itself is `core/SCHEMA.md` and the checks that catch a breach are entropy's. | essential | 2 | — | — | — |
| [`ROADMAP-legibility.md`](ROADMAP-legibility.md) | Can Lucas still read the thing he owns — its words, its decisions, its shape? A standing front that never closes: the jargon audit, the pictures that show the workspace at a glance, and the rule that a session may not decide quietly. Open it when something is UNREADABLE or was decided without him, not when it is broken. | essential | 6 | 1 | — | — |
| [`ROADMAP-measurement.md`](ROADMAP-measurement.md) | Does any of this scaffold actually help, and what catches the agent being confidently wrong? Two halves with one cause: the ablation that would measure whether a rule earns its keep, and the gates that would make a claim carry its evidence. Open it before trusting a number or a technical opinion; the experiment's design lives in its paper twin. | important | 3 | 2 | ROADMAP-portability.md | — |
| [`ROADMAP-portability.md`](ROADMAP-portability.md) | Would this workspace work on a machine that is not Lucas's? Every dependency is declared and `SETUP.md` is an executed procedure, so what is left is the public scaffold repo his students will clone and the one feature that cannot be switched off. Open it for anything crossing the line between what is general and what is his. | essential | 2 | 1 | — | — |
| [`ROADMAP-self-description.md`](ROADMAP-self-description.md) | Why does this workspace keep asserting things about its own code that one command would refute? Holds the discipline problem — a structural claim written into a durable file with no probe attached — and the routing descriptions a reader meets first. Open it when the workspace says something false ABOUT ITSELF; the outside world is measurement's. | important | 4 | 1 | — | — |

### What is open, per shard

*Generated from each shard's item headlines — open a shard only when one of these is the thing you came for.*

**[`ROADMAP-cost.md`](ROADMAP-cost.md)**

- 🟢 safe — cheaper models where the work is mechanical.
- 🟢 assess whether an ensemble router beats single-model routing on our own work.
- 🔴 give flows and agents a deliberate trial, then judge them.
- 🟡 show context growth continuously, not just at two thresholds.
- 🟡 auto-continue when the session limit is hit.
- 🟡 the lever nobody has looked at: thinking is 65% of billed output and no instrument here can see it.

**[`ROADMAP-entropy.md`](ROADMAP-entropy.md)**

- 🟡 the count's biggest jump has never been separated into scope and rot.
- 🟢 drain the entropy dashboard.
- 🟢 sweep this repo's first-line-comment markers now that the gate is shut.
- 🟡 Five `.md` files are still over the 200-line cap, and the gate cannot go live until none are.
- 🟡 What the drain hit on the way, still true.
- 🟢 the corpus is half Portuguese and the rule is English.
- 🟢 roundup compares the declared model split against the actual one.
- 🟢 import the auto-trigger.

**[`ROADMAP-ledger.md`](ROADMAP-ledger.md)**

- 🟡 the attention dashboard measures the wrong thing
- 🟢 the `SPEC.md` → `SPECS.md` migration — the one part of retyping that is still wos work.

**[`ROADMAP-legibility.md`](ROADMAP-legibility.md)**

- 🔴 The deep sitting: research and brainstorm what this front actually is, then build.
- 🟡 Replace the words that need a glossary to be read.
- 🟡 Keep trying shapes for the *is* picture until Lucas can read it, then cut.
- 🟡 The other two pictures — *becoming* and *goal*.
- 🟡 give every code repo an `ARCHITECTURE.html`, on the same scope line as `ISSUES.md`.
- 🟡 A session must not decide things quietly, and the record of *why* must survive.

**[`ROADMAP-measurement.md`](ROADMAP-measurement.md)**

- 🟡 build the instrument, then run the ablation.
- 🔴 What is the store, and what earns a row? — POSTPONED 2026-08-17, and the postponement is the ruling.
- 🔴 The agent agrees with the frame it was handed, and nothing catches that either.

**[`ROADMAP-portability.md`](ROADMAP-portability.md)**

- 🟡 the public scaffold repo and its one-way sync.
- 🔴 `code/aiwbot` lives in its own repo and that is why one feature cannot be switched off.

**[`ROADMAP-self-description.md`](ROADMAP-self-description.md)**

- 🔴 Open with a research and design sitting, and build nothing before it.
- 🟡 measure which `UPPERCASE.md` files are actually read, and what they cost.
- 🟡 then reinforce the goal↔roadmap link, possibly enforced.
- 🟡 audit the goal file format against what actually drives follow-through.
<!-- routing:end -->
