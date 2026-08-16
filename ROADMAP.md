# Workspace-OS Roadmap — the v1 push

> **Single entrypoint for all workspace-os (wos) build work.** Goal file
> [brain/goals/workspace-os.md](brain/goals/workspace-os.md) holds *why*; this file holds *what*.
> [brain/TODO.md](brain/TODO.md) holds life tasks only; [core/ROADMAP.md](core/ROADMAP.md) holds
> agent-library internals only. An item lives in exactly one of the four — a copy is a bug.
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
| 1 | **verify-fast green + Tier 0 live** — naming, placement, pointer integrity, size-as-signal deterministic; **this repo** clean, every nested repo on a shrinking baseline | Frente 4 | checks live · **read [`entropy.md`](entropy.md) for the count, never a copy of it** |
| 2 | **One ledger, no duplicates** — this file is the sole wos ledger, verified by scan not eyeball | Frente 8 | ✅ **MET 2026-07-30** — `test_no_item_lives_in_two_ledgers` |
| 3 | **Everything pushed, gitflow-shaped** — every `code/` repo on `main`/`feature/*`, zero unpushed, no repo without a remote | Frente 11 | ✅ **MET 2026-08-14** — re-audited across every repo |
| 4 | **Clonable by a student** — fresh clone gets every capability; deps declared, no undocumented hand-installs | Frente 10 | open |

Post-v1 validation is `[mvp-validate]`: use the system daily for 30 days, then assess whether it
reduced mental load. That is the real test and it can only run after v1.

## How to read this

Per-step `model` = the tier that is *enough* (a floor, not a ceiling).
🔴 needs Lucas · 🟡 pilot on one subtree first · 🟢 mechanical.

**Six open steps need Lucas's own judgment: 10.1, 10.1b, 10.3, 10.5, 13.1, 14.1.** Everything else
is Sonnet or Haiku. Stating that number is part of the cure for feeling lost, so **keep it true** —
it was wrong for a fortnight, claiming one while five were live. Four of the six are one decision
wearing four numbers: the feature-toggle registry (10.4) is what makes the Lucas-specific/general
split executable, what an installer writes a profile into, what a public scaffold repo is allowed to
copy, and the switch Frente 14 needs before it can measure anything.

**Never cite an item number from code or from a test.** A closed item is *deleted* — that is the
workspace rule — so every `Frente N.M` in a comment becomes a dead pointer the day the work lands.
Cutting 4.7 broke six of them at once (2026-08-15). Point at the `SPECS.md` or `SCHEMA.md` section
that owns the rule instead; those are durable, and writing the rule there is what closing an item
is *for*. Citing a number is fine **inside this file**, and in a commit message, which git keeps.

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

## Frente 3 — Memory and always-loaded context

0. 🟢 **measure `.claude/commands/`, then decide — the only unmeasured thing left at session start.**
   `mirror.sh` copies all 13 skills a *second* time as slash commands (52 KB on disk). That copy is
   folded into the system prompt, so it lands inside the **77% residual** that
   [`session/context`](core/tools/wos/session/context) cannot decompose — it is invisible to every
   number we have. It may be a real chunk of the residual or nothing at all, and the honest order is
   measure first: the cheapest probe is a session with the directory emptied, comparing turn-1
   context. **Do not cut it on suspicion** — that is the mistake the 1.6-3.5x inflation already
   taught. Record the result in [`core/experiments/context-window.md`](core/experiments/context-window.md).
   → **model: sonnet**.

1. 🟡 **test the six "inverted practices" against our own instructions.** Claim, from a practitioner post
   (`[C]`, ref in [core/refs/REFS.md](core/refs/REFS.md), captured INBOX 2026-07-31, Lucas: *"ver se é
   verdade e se for estudar como aproveitar no wos"*): Anthropic cut **>80%** of Claude Code's system
   prompt for its newest models and replaced hardcoded rules with judgement over rules, interfaces over
   examples, disclosure over dumping — `TodoWrite` reportedly going from ~9.1k chars of worked examples to
   an enum-typed interface, verification and code review moving out of the prompt into on-demand skills,
   and tool definitions deferred behind `ToolSearch` until needed.
   **The 80% number is self-reported with no published benchmark and is not independently verifiable — do
   not cite it.** The *framework* is testable here, which is the whole value: our own hooks already prove
   the mechanism half of it (a hook's error message is a zero-token instruction that arrives exactly when
   it applies), and the MOVE OUT bucket in 3.2 is the same move by another name.
   Concrete probe, cheapest first: take the two or three most rule-shaped surfaces we own — `AGENTS.md`,
   the fattest `CONTEXT.md` heads, and the skills flagged in `core/ROADMAP.md` — and ask per rule whether
   it could be a **tool parameter, an enum, or a hook message** instead of prose. Whatever survives that
   question is prose that earns its place. Feeds directly into 3.2's MOVE OUT and the skills audit.
   → **model: opus** for the judgement pass, sonnet for the rewrites.

---

## Frente 4 — workspace anti-entropy — **the keystone, v1 criterion 1**

> The real target: files grow, scatter, duplicate, and drift from naming/structure patterns.
> **Structure is a spec; drift is a test failure.** `code/` already has this (the `> spec:` gate);
> the agent library has [core/SCHEMA.md](core/SCHEMA.md). Nothing yet governs the shape of the
> workspace itself.

1. 🟢 **Tier 0 — per-commit, zero-token, deterministic.** Live: `core/hooks/checks/type-gate.py` (ratchet, only
   what a commit *adds*) + `schema_law.py` · `entropy_naming.py` · `entropy_ledger.py`, asserted by
   35 tests in `verify-fast`. Every rule is **parsed from `core/SCHEMA.md`**, never restated in a
   checker. Covered: type allowlist, hand-inventory, filename shape, directory case, type placement,
   retired tokens, duplicate slugs, size-as-signal.
   The **project ⟺ goal link** check went straight to blocking, no warn phase: the backfill turned
   out to be already done, all 14 projects declaring line 3. Six declare `goal: none` — and two of
   those, `gira` and `laplata`, **have** goal files (`startapps-gira`, `startapps-laplata`). A
   content question for Lucas, not a check failure.
   **Wiki-link resolution — decided 2026-07-30 (Lucas), and shipped.** A double-bracketed slug may
   name a goal file *or* a bracketed item inside one: both are real pointers
   (`spec-driven-development` is the file, `prompt-dsl` is an item in `craft-flows.md`) and both
   resolve by scan. Vocabulary is 333 names. One dead link found and fixed — `dobra` is a project,
   not a goal; its goal is `local-ai`. That closes pointer integrity, and Tier 0 with it.

   Conventions the checks had to be taught, each because it is a law that outranks ours: snake_case
   Python modules and `__init__`, PascalCase/camelCase in JS/TS, uppercase venue acronyms in
   `academy/papers/<year>-<VENUE>-<slug>`, `_`-prefixed scaffolding, and **received documents keep
   their names** — the 91 tracked paths with spaces and accents are all `.docx`/`.pdf` from the PPC
   process, where the filename *is* the provenance. Decided the same way: `core/tools/*` CLI
   entrypoints stay extensionless, which is the convention for anything meant to be run by name.
   → **model: sonnet** · **switch: `/loops`.**
2. 🟢 **finish the `loops` → `flows` rename at the generator.** APPROVED 2026-07-29 (Lucas: *"we
   renamed loops to be flows but apparently this keeps coming back"*). It keeps coming back because
   it **was never a drift problem** — the rename stopped at the flow pool (`core/flows/`, flow
   renamed `craft`) while three generators still emit the retired word *legitimately*, so no naming
   check could ever flag it: (a) the skill is still `core/skills/loops.md` = `/loops`; (b)
   `.loop/<slug>/` is the hardcoded per-run state dir in `craft.md`, `architect.md`, `runtimes.md`,
   `routing.md` — 14 live dirs across `aiwbot`, `isoroll-content`, `isoroll-module`; (c) the
   cross-run pattern library is `core/flows/.loop-skills/`. Retired `loop/*` git branches were the
   visible symptom, already gone (11.2). Scope: `/loops` → `/craft`, `.loop/` → `.craft/`,
   `.loop-skills/` → `.craft-skills/`, sweep the 74 doc mentions. **Keep "Loop 0..6" as step
   names** — an iterative step really is a loop; that word is correct English, not the retired label.
   **The reusable lesson: an incomplete rename is indistinguishable from entropy at the leaves, and
   is only fixable at the generator.**
   → **model: sonnet**.
3. 🟢 **drain the entropy dashboard.** `make entropy` → [`entropy.md`](entropy.md), the whole
   workspace and its nested repos in seconds. Read the report; never re-scan the tree. **Never copy
   its counts into this file** — a copied number is the drift these checks exist to catch, and the
   summary table at the top of the report is the interface. Criterion 1 wants it reading clean.

   The dashboard scans nested repos, the **tests do not** — an assertion in this repo about
   another repo's content fails for reasons this repo cannot fix, and each nested repo runs its
   own verify. Where a check is green workspace-wide it is asserted at zero in `verify-fast`
   (retired tokens, duplicate slugs); where it is not, `test_entropy_naming.py` holds a named
   **baseline** so a new violation fails the build and a fixed one must leave the list.

5. 🟡 **drain to zero, then flip fanout to a hard block** (Lucas 2026-07-31: hard block, no
   grandfathering). The flip is coherent only at zero — the pre-commit hook is global
   (`core.hooksPath`), so switching it on while nested repos are over the cap fails every commit in
   those repos, including the commits that would fix it. Live lists in `entropy.md`; when both read
   Clean, add fanout to `core/hooks/checks/` beside the type gate and delete `BASELINE` from
   `test_entropy_fanout.py` in the same commit.

   **This repo is done (2026-07-31).** `core/hooks` 50 → a root of 6 and 13 responsibilities;
   `core/tools` 37 → 8 families, every CLI path changed (Lucas's call over a named exception);
   `core/tools/test` 12 → `law/ workspace/ video/`. No directory in the wos repo is over
   `BLOCK_FILES`; the five that remain are 8-10 files, which `limits.env` calls a warning on
   purpose. The `BASELINE` in `test_entropy_fanout.py` is down to three entries, none in `core/`
   except the two caveman directories.

   **The lesson worth keeping.** Moving files satisfies the fanout count without helping the
   reader: the routing generator folds any directory under `WARN_FILES` back into its parent, so a
   split only pays off once each new directory declares itself with a `CONTEXT.md`. Both splits
   here did that — `core/hooks/CONTEXT.md` went 50 rows → 19, `core/tools/CONTEXT.md` 37 → 12.
   A split that leaves the parent table the same size is the check being gamed, not answered.

   **`code/aiwbot` is done (2026-08-01)**, on `feature/fanout-drain`: `tests` 51 → nine subjects,
   `frontend` 38 → a root of 5 and seven surfaces, `backend` 12 → a provider-agnostic root and
   `providers/`. Nothing in the repo is over `BLOCK_FILES` now; two directories sit at 8. Tests
   and source carry the same directory names, so a surface and its coverage are one word apart.

   **Two hazards that only show up in a package, both worth expecting in the next repo.** A
   directory turns a flat import into a boundary, so the facade gate starts firing on imports
   that were legal the day before — five of them here, fixed by re-exporting from the new
   package `__init__.py` rather than by importing past it. And `spec-read-gate.py` stops at the
   *nearest* ancestor declaring `> spec:`, so a new subdirectory written with `spec: none`
   silently unlocks a spec-locked module; every subdirectory of a locked module must re-declare
   `> spec: ../SPEC.md`.

   **`code/flows` is done (2026-08-02).** `engine/ui` 20 → 6 by **deleting** the pre-React
   Cytoscape canvas rather than splitting it; `libraries/tools` 24 → five families; `engine/tests/
   unit` 23 → seven subjects plus two shared kits; `components` 19 → four groups; `App.jsx`
   844 → 187 and the two node cards 515/428 → 126/63. The bundle came out **smaller than before
   the work started** (74.05 → 70.51 kB) because the node cards were near-copies of each other.

   **The lesson from flows: check whether the directory is a split or a delete.** The biggest
   one was neither tangled nor needed — 14 dead modules whose own headers still said
   "Cytoscape". **A file nothing imports is the first thing to look for in an over-full
   directory.**

   **But "nothing imports it" is not proof it is dead, and I got this wrong once today.** Five
   orphan React components read as debris on imports plus `git log`; the repo's own `ROADMAP.md`
   said otherwise — one milestone had *deliberately unwired* two of them, and the next milestone
   planned to reuse them. They were drafts for open work. Deleting them stayed right (drafts,
   over the line cap, git holds them) but only once each milestone was made to name the commit
   they live at. **Grep the repo's ROADMAP for the filename before calling it dead**; that is
   the step the import graph cannot give you.

   Two more hazards, on top of the two above: barrel `index.js` facades **defeat tree-shaking**
   (the dead components started being bundled the moment a facade re-exported them), and a
   `parts/` directory may not import its own parent's constants — that needs a third leaf
   (`nodes/shared/`) or the facade gate and a module cycle fight each other.

   **What is left, all of it in nested repos:**
   - **files over `BLOCK_LINES`** — one: `isoroll-content/src/pipeline/s3_batch.sh` (209),
     owned by the parallel isoroll session.
   - **directories over `BLOCK_FILES`** — the isoroll set, owned by that session:
     `isoroll-content/src/pipeline` (58), `/test` (31), `/src/cli` (18);
     `isoroll-module/src/render` (31), `/transform` (20), `/walls` (16), `test/unit` (21).
     Free to take: `apptime/lib/screens/analytics` (18), `/screens` (15), `/data` (14);
     `spacemantics/checker` (15).
   → **model: sonnet**, one repo at a time. `apptime` is Dart/Flutter — the routing generator
   and the facade gate both know `index.dart`, but no gate has been exercised on that repo yet.

6. 🔴 **close the first-line-comment hole, then sweep — in that order, because sweeping first
   just refills.** Each marker is a routing-table row that describes nothing, in the workspace's
   only enforced-read type.

   **Re-counted 2026-08-15 after the item-7 generator fixes: 150 markers in 54 `CONTEXT.md`,
   down from 204 in 77.** Not one was answered by hand — the drain is entirely files the
   generator could already describe and was not reading (`.sh`, `.env`/`.txt`, multi-line
   docstrings) plus the six hand-written inventories item 7 removed. **Three of the four
   markers left in the wos repo are in nested-repo-shaped directories or genuinely
   undocumented files; the queue that remains is nested-repo work.** Size any sweep against
   150, and re-run the generator before measuring again — that is the cheap half, and it is
   now spent.

   **The frequency is the finding, and Lucas named it as such** (2026-08-15: *"this is an issue
   that should not be so frequent so it is a warning for us that we may find out a more
   enforced/guaranteed solution"*). A gate for this already exists and is why the number should
   have been near zero: [`pre-edit.py`](core/hooks/checks/pre-edit.py) checks the first line
   against a per-type pattern — **but only under `if not os.path.exists(file_path)`, so it fires
   on creation through `Edit`/`Write` and never again.** Everything else is uncovered: files that
   predate the gate, files written by a generator, by a shell heredoc, by `git checkout`, or by
   any agent not running our hooks. `core/hooks/checks/check-line-counts.sh` carries a marker
   **inside the enforcement directory itself**, which is the tell that the hole is structural and
   not a lapse of discipline.

   The guaranteed shape is the one the rest of Tier 0 already uses: a **commit-time check over
   staged files**, where a generator's output and a stranger's file both have to pass, rather than
   an edit-time check that only the harness path reaches. Ratchet it like the type gate — only
   what a commit *adds* — so the 204 do not have to be paid before it turns on.

   **Re-scope before building: a slice of this queue was never a discipline problem.** Found
   2026-08-15 while draining 13.1. `ALL_EXTS` and `COMMENT_RE` in
   [`core/hooks/routing/workspace_meta.py`](core/hooks/routing/workspace_meta.py) are two lists that
   have to agree, and nothing checked that they did: `.sh` (30 files) and `.jsx` (29) were scanned
   with no comment pattern, so `file_description()` returned `''` and the generator wrote the
   marker **no matter how well the file was commented**. `core/hooks/post-edit.sh` carrying one
   *inside the enforcement directory* was read above as proof the hole is structural — it is, but
   the structure was a missing dict key, not a lapse of discipline. Fixed, guarded by
   `test_every_scanned_extension_can_be_described`.

   The re-sync that this note called for is **done** (2026-08-15), and it is what the recount
   above measures. What it settles: **a marker is not evidence of a discipline problem until
   the generator has been asked whether it can answer it.** Four times out of four, it could.
   That does not remove the need for the gate — a commit-time check over staged files is still
   the only thing that covers a stranger's file — but it does mean the gate should be built
   against a queue of 150, not 204, and that **the next new marker deserves a look at
   `COMMENT_RE` before it deserves a sweep**.
   → **model: opus** for the gate, **sonnet** for the sweep behind it.

8. 🔴 **`python_api` advertises nested closures as importable API.** Found 2026-08-15 by
   reading the diff of the item above: `hoist.py`'s row listed `fix`, a closure inside
   `rebase_links`, beside four real exports. `python_api` walks the whole AST, so any nested
   `def` with a bare name is API; it has been masked until now by the `[:5]` cap, which means
   the corpus is quietly showing this wherever a module exports fewer than five names. Worked
   around at the call site by underscoring the closure — the convention already excludes `_`
   names — but the generator is still wrong. The fix is to walk module top level plus class
   bodies rather than `ast.walk`, and it will move API columns across the corpus, so measure
   the churn before taking it.
   → **model: sonnet**.

---

## Frente 8 — The ledger discipline — **v1 criterion 2**

Collapsed 2026-07-29 (four ledgers → one) and cut 2026-07-30 (52 open steps → 17). The collapse made
the ledger honest but not smaller — items went 158 → 123 while mass stayed flat, and Lucas reported
feeling lost twice. **Mass is the disease and only deletion cures it.**

1. 🟢 **`TODO.md` dies as a type — fold its content into goals, then delete the file.** Ruled
   2026-08-14. Lucas reported twice, unprompted, *"sinto que o TODO.md simplesmente não tá sendo
   usado"*, and the evidence was always that he writes tasks into the INBOX instead. He chose
   **both** the delete and the fold, and they are not alternatives — they are the two halves of one
   move, in order:

   1. **Fold** — every live line in `brain/TODO.md` becomes a backlog item in the goal it actually
      serves (`[short-id] description`, per [brain/SPECS.md](brain/SPECS.md) § Backlog Ordering).
      A task with no goal is the interesting case and there are only two honest outcomes: it belongs
      to a goal that does not exist yet (write the seed — a goal file's minimum is two lines), or it
      is capture, not commitment, and belongs in the INBOX.
   2. **Delete** — remove the file, then the type: the row in `core/SCHEMA.md`'s type table, the
      mention in [brain/CONTEXT.md](brain/CONTEXT.md), and the "four ledgers" phrasing in this
      file's own header, which becomes three. Deleting the file while leaving the type declared
      would regenerate it — that is the lesson job A of Frente 12.1 already paid for.

   **Why this beats redesigning it.** The redesign question was *"what would make it get checked
   daily"*, and the honest answer is nothing: `/compass` is already the review ritual and it reads
   goals, so a second surface competes with a ritual that works. Capture goes to INBOX, commitment
   goes to a goal backlog — no third place, no boundary to police. This is the *delete weak features*
   rule applied to our own scaffold instead of to code.
   → **model: sonnet**. The fold needs a judgment call per line, so read them, do not batch.
2. 🟢 **safe — `/inbox` refreshes the goals dashboard.** Run `brain_stats.py` as `/inbox`'s last
   step, not only on commit, so the dashboard never goes stale between commits.
   → **model: haiku**.
3. 🟡 **the attention dashboard measures the wrong thing** (Lucas, INBOX 2026-08-13). It counts
   edits to the goal's **own `.md` file**, not work **on** the goal — so the 2026-08-13 compass
   rendered `workspace-os ░░░░░░░░░░ 1 touch` in the same fortnight that **29 of 29** workspace
   commits were wos (hooks, tools, verify, session, entropy). Any goal whose work lands in `code/`
   or `core/` reads as dead, and the compass's Pareto has to be hand-corrected every cycle — the
   exact manual correction the workspace exists to kill. Each goal declares the paths it **owns**
   in a `>**owns**` block, and the counter counts commits touching those paths.

   **Scoped 2026-08-13, and the scoping moved it off `brain_dashboard.py` alone — three findings
   the one-line framing above missed:**
   - **The work is in other repos.** `code/*`, `academy/papers/*` and `branches/*` are gitignored
     by the workspace repo and are **24 independent git repos**, so `git log -- code/spacemantics`
     from root returns nothing, forever. Ownership buys nothing without resolving each path to its
     governing repo (walk up to nearest `.git`) and running git *there*. This is the load-bearing
     half of the fix.
   - **The instrument measures its own observer.** `/compass` writes back to every goal file it
     reviews; next cycle those goals read as active *because they were reviewed*. Drop commits whose
     changed paths lie **entirely** within `brain/goals/*.md` + `brain/GOALS.md` — a rule that reads
     what changed, not how it was described, so commit style cannot game it.
   - **Area bars must union, not sum.** `area_touches[area] += c` double-counts the moment one
     commit advances two goals (workspace-os owns `core/`, craft-flows owns `core/flows/craft/`).
     Count distinct `(repo, sha)` pairs. Overlap *between goals* stays intentional — that commit
     really did advance both.

   Measured set is `declared owns ∪ {the goal file}`, so a goal with no block behaves exactly as
   today: **life goals (dance, sleep, yoga) have no repo and their file genuinely is the artifact.**
   An empty `>**owns**` is not a gap to fill. Harvest one `git log --name-only` per *declared repo*
   (~12), not one per goal (~52 subprocesses today). New module
   `core/hooks/brain/brain_attention.py` owns the counting —
   [`brain_dashboard.py`](core/hooks/brain/brain_dashboard.py) is at **194 lines against
   `BLOCK_LINES=200`** and must shrink by handing counting away, not grow.

   **Committed 2026-08-14 as work in progress, and the shrink did not happen.** The session doing
   this was halted mid-flight; its tree was coherent (module imports, `brain_stats.py` consumes it,
   dashboard runs, `verify-fast` green) so it was committed rather than lost. But
   `brain_dashboard.py` went **194 → 196** and `brain_stats.py` is at **177**: counting moved out
   and something else moved in. Both are warns now, four and twenty-three lines from a hard block
   respectively — so the next session on this frente starts by paying that down, before adding
   anything.
   → **model: sonnet**. The plan is the three findings above; it used to point at a file in
   `~/.claude/plans/`, which `AGENTS.md` forbids — a plan lives in the ROADMAP of the thing it
   changes, not in harness-owned state no clone of this workspace would ever get.

---

## Frente 9 — Cost & model routing

> **The output-cost plan is [`ROADMAP-output-cost.md`](ROADMAP-output-cost.md)** (2026-08-15): output is
> ~15% of spend at sticker but **~86% once re-reads are counted** — a mean turn is ~75% self-authored.
> Its instruments exist: `usage` prints the billed-component split and the multiplier, `roundup`
> prints per-session cost and compaction adoption. Both re-runnable in one command, so those numbers
> regenerate instead of being quoted. What remains there measures Frente 4.6's shell-heredoc hole.

**Why — re-measured 2026-08-13, and the old numbers were wrong.** The previous framing came from a
single 24 h window. Re-run it yourself — that is the point of
[`core/tools/wos/session/usage`](core/tools/wos/session/usage), built this session so no claim here rests on a
number nobody can reproduce. Over **118 sessions · 18,122 turns · 2026-07-25 → 08-13**:

> **Trust the ratios, not the dollar total.** A one-off script and the tool agreed on every share
> and per-turn cost but differed ~8% on absolute spend (mostly the `fable` line), and that is not
> yet explained. Quote percentages and $/turn from the tool; treat any absolute total as ±10%.

| Claim | Verdict |
|---|---|
| "59% of usage from subagent-heavy sessions" | **Unmeasured, and the retirement was wrong too.** The audit searched for `Task`; the tool is named **`Agent`**, and it ran **56 times across 12 sessions**. Subagent turns are also absent from the parent transcript by design — they live in `<session>/subagents/*.jsonl`, 48 files this audit never opened. Re-measure with `context` before any claim here. |
| "55% from >150k-context sessions" | **Understated.** **72%** of spend is paid above 150k of context; **41%** above 250k. |
| "25% from `/roundup`" (step 1 said ~7%) | **~7% was right; 25% was not.** 24 of 119 sessions invoked it; the tail after invocation is **~10%**. |

**The real driver is context size — and the curve is a staircase, not a ramp.** Cost of one turn by
the context it carried, and what each band adds over the one below it:

| band | $/turn | vs. band below | | band | $/turn | vs. band below |
|---|---|---|---|---|---|---|
| <50k | 0.087 | — | | 200-250k | 0.202 | **+5%** ← plateau |
| 50-100k | 0.102 | +17% | | 250-300k | 0.218 | +8% |
| 100-150k | 0.147 | **+45%** ← bend | | 300-400k | 0.269 | +24% |
| 150-200k | 0.193 | +31% | | >400k | 0.373 | +39% |

Flat below 100k, a hard climb to 200k, then a **plateau at ~2x the cheap rate that never comes back
down**, and a second climb past 300k. **86% of spend is paid above 100k, 55% above 200k.** The
mechanism is that every turn re-reads the whole thread: **3.4 Gtok** of cache reads over the window.
Long sessions therefore cost super-linearly in their own length, and the **top decile of sessions is
~44% of total spend.**

Two facts that decide where a threshold can usefully sit. **Sessions are bimodal** — median peak
context **59k**, p75 **271k**, almost nothing between — so firing earlier costs far less noise than
it looks (100k fires in 48% of sessions, 150k in 44%). And **there is runway to act**: at 100k the
median session still has **~211 turns** ahead, so a hand-off has time to repay its re-grounding
cost. Warning early does not cost precision work; that fear priced a session about to end, and at
these thresholds the session is not about to end.

Both halves of the session transition are live. The size signal is
[`core/hooks/session/context-meter.py`](core/hooks/session/context-meter.py) on `UserPromptSubmit`:
it reads the size the API already reported and announces `CTX_WARN` / `CTX_LOUD` once each, costing
zero tokens until crossed and never blocking. **The session cannot see its own size**, which is why
the hand-off decision is made late without it — a hook is the only thing that can see it *and* speak
at the moment it applies. The close itself is [`core/tools/wos/roundup`](core/tools/wos/roundup) plus
the two skills; every decision behind that split, and why no session spawns its own successor, is
[`core/SPECS.md`](core/SPECS.md) § AD-09.

**The lesson this frente cost the most to learn: a number nobody can re-run steers the work anyway.**
It was aimed for weeks by a single 24 h window that turned out wrong in every claim — "59% from
subagent-heavy sessions" was retired outright (zero sidechain messages across 328 transcripts), and
the thresholds first shipped at 150k/250k, which fired *halfway up* the climb and *after* the
plateau began. So: a number in this file that
[`core/tools/wos/session/usage`](core/tools/wos/session/usage) cannot reproduce should be **deleted, not softened**.

1. 🟢 **safe — cheaper models where the work is mechanical.** Measured split: opus 68%, fable 24%,
   sonnet 7.8%, haiku ~0%. Worth doing, but note the ceiling — routing cannot beat a 3x context
   multiplier, and the transition above already took the larger win.
   → **model: sonnet**.
2. 🟡 **the ~8% spend gap is still unexplained**, four sessions running. A one-off script and
   [`core/tools/wos/session/usage`](core/tools/wos/session/usage) agree on every share and per-turn cost but differ
   on absolute total, almost all of it in the `claude-fable-5` line. Quote percentages and $/turn;
   treat any absolute total as ±10% until this closes. By the rule above, if it cannot be resolved
   the absolute numbers should be dropped from the tool's output rather than footnoted.
   → **model: sonnet**.
3. 🔴 **make delegation happen, instead of hoping for it.** Lucas, INBOX 2026-08-15: *"só tenho
   confiado no opus. mas gostaria que ele delegasse mais ao sonnet pra economizar quando fosse
   pertinente. não sei como fazer isso, seria ótimo se tivesse uma forma mais garantida de fazer
   isso acontecer."* Item 1 says routing is *worth doing* and measures the split at opus 68% /
   sonnet 7.8%; this item is why that split has not moved. **A per-item `→ model:` line in this
   file is advice an agent may skip, and mostly does** — same class of defect as Frente 4.6's
   first-line comment, where a rule existed and the number still grew.

   His proposed trigger is the concrete part: *"talvez se toda vez que o modo plan fosse utilizado
   ou toda vez que o prompt pedisse para montar um plano para cada tarefa do plano o modelo
   definisse qual modelo/agente deveria executar aquela tarefa… seria bom ter a delegação como
   parte de uma política natural mas o plano poderia ser um gatilho mais evidente."* Planning is
   already the moment the work is cut into tasks, so it is the one point where per-task routing is
   free to decide and cheap to record. Make the plan *carry* the assignment rather than leaving it
   to recall at execution time.

   **Its feedback loop is already wired**: [`core/tools/wos/roundup`](core/tools/wos/roundup) prints
   the per-session model split at every close, so whether this item moves the opus/sonnet ratio is
   readable without new instrumentation. A delegation policy nobody measures per session would be
   unenforced advice one more time.
   → **model: opus** for the mechanism, sonnet to wire it.
   → **model: sonnet**.
5. 🔴 **discuss — should this workspace have agents, or are skills enough?** Lucas, same capture,
   and flagged by him as a discussion rather than a task: *"um aluno comentou que existem formas
   diretas de o claudecode delegar pra subagentes, ele falou acho que com @. é fato que não temos
   agentes no workspace, me pergunto se deveríamos. temos skills e isso me parece suficiente, mas
   talvez não seja. esse é um ponto que merece discussão ao meu ver."*

   Two facts to put on the table before opinions. `core/agents/` **does** exist — lead, researcher,
   writer, verifier, reviewer, ported from Feynman — so the claim "não temos agentes" is about them
   being unused, not absent; find out which is true before designing anything. And the measured
   fact from this frente: *zero* sidechain messages across 328 transcripts, which is why the
   "59% from subagent-heavy sessions" claim was retired. **Nothing has ever been delegated here**,
   so this is a question about a capability with no usage data at all, not a tuning question.
   Same treatment as Frente 10.1: bring options and trade-offs, decide with Lucas, do not arrive
   with one answer.
   → **model: opus**, with Lucas in the loop — not a solo pass.
6. 🔴 **measure whether our own gates make a session re-read the same file.** Lucas, INBOX
   2026-08-15: *"does a session, due to our hooks/gates, re-read the same context file more than
   once? can we have a report at the end of each session (maybe on the /roundup) that automatically
   prints (zero-token) all the read and all the written files, and for each file how much of that
   file was read and how many times as well."*

   **This is the sharpest question anyone has asked about the enforcement layer, because it points
   at a cost we impose rather than one we inherit.** `context-gate.py` demands a whole `CONTEXT.md`
   chain before any file access in a subtree, and `pre-read.sh` redirects source reads to stubs —
   both are designed to *save* context, and neither has ever been measured doing it. A chain
   re-read once per subtree per session is the mechanism paying for itself; re-read per *file* is
   the mechanism billing for the same page repeatedly, and the frente's own rule applies: a number
   nobody can re-run steers the work anyway.

   The transcript already holds every `Read` with its offset and limit, and
   [`core/tools/wos/session/usage`](core/tools/wos/session/usage) already replays transcripts — so
   this is a second lens on data we have, zero-token, no new capture. Report per file: bytes read,
   read count, and whether a stub or the source was served. Ships in the same roundup block as
   item 4, and **feeds Frente 14** — read amplification is exactly the kind of cost an ablation
   needs an instrument for.
   → **model: sonnet**.
7. 🟡 **show context growth continuously, not just at two thresholds.** Lucas, same capture:
   *"gostaria de ver o crescimento da janela de contexto em tempo real, o claude code no vs code
   não mostra. tem alguma forma barata de me mostrar isso?"*
   [`core/hooks/session/context-meter.py`](core/hooks/session/context-meter.py) already reads the
   size the API reports and speaks at `CTX_WARN` / `CTX_LOUD` — the ask is the *trend* between
   them, and the cheapest honest answer is probably a statusline rather than more hook output,
   since the hook's whole design point is costing zero tokens until crossed. **Do not make it
   chatty every turn**; that trades the thing being measured for the measurement.
   → **model: sonnet**.

---

## Frente 10 — Portability & clonability — **v1 criterion 4**

1. 🔴 **decide-first — what shape does the install path take?** The root `SETUP.md` split landed
   2026-08-15 and needed no judgement: `core/SCHEMA.md` § The `.md` type system already assigns one
   question per type, so each section had exactly one destination. 643 lines → `core/hooks/SPECS.md`
   (the enforcement contract, new), `README.md` (what the workspace is and what each capability buys
   you — the sentences Frente 10.4 requires), and ~250 lines of install steps left in `SETUP.md`.
   Three sections were deleted rather than moved: a build log of shipped tasks, a hand-listed file
   tree that § Boundaries calls a bug and that had been stale since the 2026-07-31 hooks split, and
   a line-limit policy `code/SPECS.md` already owned. **Section numbers are gone** — `§6`/`§11`
   pointers had already gone stale twice, so sections are named.

   **What is still open is the part that was decided too early.** The 2026-07-30 ruling said install
   steps "should be an *executable installer*". Lucas, 2026-08-15: not certain. Before inventing a
   shape, follow an established one — **rtk** is the pattern this workspace already consumes
   (`curl -fsSL … | sh` for the binary, `rtk init --global --auto-patch` to wire one agent
   additively with a `.bak`, `--uninstall` to reverse it, `rtk init --show` to verify); also worth
   reading are caveman's node installer, opencode's project-level plugin auto-load, mise/asdf, and
   devcontainer. The question is not "script or prose" but **which install idiom an agent-workspace
   should present to a stranger**. Gates steps 2 and 4.

   **Lucas's precondition, INBOX 2026-08-15:** *"BEFORE creating an installer for the workspace…
   systematically list what the workspace is, what are the features. we have different levels of
   features, I would like to see this organized first."* First pass the same day put
   `README.md` § What the enforcement layer buys you on **navigation / restraint / drift control /
   cost**, one sentence of value each.

   **Clarified 2026-08-15, and explicitly NOT decided — this is a discussion, not a ruling.** Lucas:
   *"what I was thinking is that we have some 'types' of features. we have hooks, and each hook may
   be toggled, LOC limit, file fan-out limit, gitflow, etc. we have the agents.md|context.md tree +
   the automated routing. we have the whole brain thing, inbox + goals. we have capabilities per
   area, slides, email, papers/latex, skills for research and other tasks… I meant we may organize
   the whole thing somehow so our features fit a simple organization that is semantically correct
   and symmetric."* Asked whether that settles it, he was explicit: *"I am not decided on that, this
   is a discussion point."*

   So what is fixed is the **test**, not the taxonomy: whatever organization we land on must be
   *semantically correct and symmetric* — every feature lands in exactly one group, no group
   overlaps another, and the groups are peers. What is open is **which axis to cut on**, and the
   session that takes this **opens with the options and their trade-offs, and decides with Lucas.**
   Do not arrive with one table and call it done.

   The candidate axes, each with what it costs:

   | Axis | Groups it produces | Buys | Costs |
   |---|---|---|---|
   | **by kind of thing** (Lucas's sketch above) | hooks · the `AGENTS.md`/`CONTEXT.md` tree + routing · brain · per-area capabilities · skills | matches how the tree is already laid out, so a feature's group is findable | says nothing about whether a feature is optional, which is what an installer must ask |
   | **by what it buys the reader** (`README.md` today) | navigation · restraint · drift control · cost | sells the workspace to a stranger | one feature serves two values, so the groups are not disjoint — fails the symmetry test |
   | **by installability** | free vs needs a binary · scaffold vs Lucas-specific · toggleable vs structural | exactly what steps 2, 3 and 4 need | a pure install view; useless as a way to explain the workspace |
   | **by enforcement strength** | blocks · warns · generates · advises only | honest about what actually holds, and the ablation instrument (Frente 14) wants it | cuts across every other axis, so it reads as an attribute more than a grouping |

   The real question is likely **whether one axis has to carry all of it**, or whether one is the
   grouping and the rest are columns on its rows — worth putting on the table, since "levels of
   features" may describe a *column* (how optional is it) rather than a set of boxes. Whatever
   lands, step 2's install idiom and step 4's toggle registry both index into it, which is why this
   gates them.
   → **model: opus**, with Lucas in the loop — not a solo pass.

1b. 🔴 **decide-first — does `SETUP.md` die as a type?** The ledger and the law contradict each
   other and **both are dated 2026-07-30**: this frente said "`SETUP.md` dies as a type", while
   [`core/SCHEMA.md`](core/SCHEMA.md) § The `.md` type system keeps it on the allowlist with a
   justification paragraph ("earns its row on the evidence, 8 instances"). There are now **9**
   instances and ~50 inbound references, and `core/hooks/checks/type-gate.py` enforces the
   allowlist — so striking the row makes nine files illegal in one commit. Downstream of step 1: the
   type only dies if the install path stops being prose. `core/tools/video/SETUP.md`, the third
   naming shape, is retired by *this* decision and not before it.
   → **model: opus**.
2. 🟢 **safe — declare the ad-hoc venv deps.** Four known cases, each installed straight into `.venv`
   to unblock a tool, so a fresh clone silently loses the capability: `pypandoc-binary`
   (`core/tools/paper/parse` on `.docx`), `secretstorage` (`core/tools/video/video` reading Brave cookies —
   without it yt-dlp fails with an AES-CBC decrypt error that reads like bad credentials; cost a
   session to diagnose), `gallery-dl` (`core/tools/video/video` carousel path), and **`flutter`** (found
   2026-07-29: `apptime`'s verify cannot run at all). Fix the **class**: a declared dep list the
   whole `core/tools/` surface is checked against.
   → **model: sonnet**.
3. 🔴 **decide-first — clonable for others (the students case).** Make the workspace genuinely
   plug-and-play for anyone who clones it: what is Lucas-specific, what is general, and how the two
   separate.
   → **model: opus**.
4. 🟡 **the WOS installer — an interview, not a README.** Lucas (INBOX 2026-08-13): *"preparar um
   'INSTALL' do WOS pra quem quiser"* — the person answers a few questions (which harnesses, which
   tools, gdrive? gmail?, which hooks) and the workspace installs itself for them. **This is what
   step 1 already decided SETUP.md must become**, now with the shape named: not a script that
   installs everything, but one that asks and installs a subset. Two consequences that make it work
   as a v1 exit test rather than a nice-to-have: it can only ask about capabilities that step 2's
   declared dep list makes checkable, and it forces step 3's Lucas-specific/general split to be
   *executable* instead of documented. **Requirement Lucas stated explicitly: each hook is offered
   with what it is for and what it buys you** — nobody accepts an enforcement layer they cannot see
   the value of, and writing that sentence per hook is itself an audit of whether the hook earns its
   place. Sequence it after 1 and 2; running it on a clean machine is the honest test of criterion 4.

   **The mechanism, named by Lucas 2026-08-14 (INBOX):** *"the ability to toggle on and off the WOS
   features — LOC limit, file-per-folder limit, caveman, even context-tree, … also gdrive, latex,
   gmail, which skills and tools"*. An installer that asks questions needs something to *do* with the
   answers, and that something is a **feature registry with an on/off switch per capability** — the
   installer then writes a profile, not a patch. Two payoffs, and the second is the larger one:
   - **install** — a stranger enables the subset they want, which is the whole of step 3's
     Lucas-specific/general split made executable rather than documented.
   - **ablation** — Lucas: *"it also would ease ablation tests so we can indeed see the impacts of
     each option."* This is the missing half of the pilot in
     [`core/ROADMAP.md`](core/ROADMAP.md) § ablation-bench, whose first run produced no signal
     precisely because there was no clean way to turn one feature off. **No feature in this workspace
     has ever been measured**; a toggle is the cheapest instrument that would let one be.

   Design constraint that falls out of it: a toggle must reach the *enforcement* layer, not just the
   docs. The numbers already centralise (`core/hooks/limits.env`), the types already centralise
   (`core/SCHEMA.md`) — so the registry's job is mostly to name which hooks/skills/tools are wired,
   not to re-implement their rules. **Anything that cannot be switched off is a finding**: it means
   the capability is entangled with the scaffold rather than sitting on it.

   **One more question in the set, named by Lucas 2026-08-14 (INBOX):** *"deveríamos oferecer a
   opção de idioma principal para a interação com o usuário"* — thinking of third parties. It is a
   profile field like any other, but it lands somewhere the others do not: **agent-facing text**,
   not source docs. This workspace's own prose is deliberately mixed (rationale in Portuguese,
   contracts in English) and stays that way; what the setting governs is the language the agent
   *answers* in. Cheapest shape that does not fork the corpus.
   → **model: sonnet** to build, **opus** for the question set and the registry shape.

5. 🔴 **decide-first — a public scaffold repo, synced from here.** Lucas (INBOX 2026-08-14):
   *"poderíamos ter uma branch separada no git/github"*, resolved the same day to a **separate
   public repository holding only the scaffold** (`core/` + hooks + templates), synced from `main`
   by a script — not a branch. A branch was the first shape considered and lost on one property:
   personal history never leaves this repo, where a branch carries every commit that ever touched
   `brain/`. That makes it strictly stronger than step 3's split — the general/Lucas-specific line
   stops being documentation and becomes *what the sync script is allowed to copy*, checkable on
   every run. Open questions before building: what the sync does about a stranger's PR coming back,
   and whether the toggle registry in step 4 ships as scaffold (it should — it is the thing that
   makes a subset installable).
   → **model: opus** for the boundary and the sync direction, **sonnet** to build the script.

---

## Frente 11 — Git & sync integrity — **v1 criterion 3 — ✅ MET 2026-08-14**

**The criterion holds as of 2026-08-14**, re-audited across every repo in the tree: each has a
remote, each sits on `main`/`master`/`feature/*`, and the only unpushed commits are one apiece in
`isoroll-content` and `isoroll-module` — the parallel isoroll session's in-flight work, which
`core/hooks/post-commit` pushes on its own. Re-run the audit rather than trusting this line; it is
one loop over `find . -name .git` and it is how the two stale claims below were caught.

**What closed it: `branches/casinhas`.** `modelo/sketchup-referencia/volume-lucas-v04.skp` was
208 MB, over GitHub's hard 100 MB object limit, and was the single reason the repo had no remote.
Lucas ruled the study obsolete (2026-08-14), so it was dropped from history with `filter-branch`
rather than moved to LFS — `.git` went **193 M → 128 K** and the repo pushed clean. `*.skp` now sits
in that repo's `.gitignore` beside the other heavy binaries, so the next SketchUp export cannot
recreate the block.

**The lesson, and it is the same one Frente 9 paid for: an audit's findings rot faster than the
ledger holding them.** Every item of the old step 1 was re-checked on 2026-08-14 and **three of
four had resolved themselves** in a fortnight — the `Makefile` was untracked in **zero** repos (the
three named repos that still showed it had been moved to `.Trash-1000`), `shortvid`'s duplicated
source tree went with them, and of the two repos said to verify RED, `flows` now passes **225
tests** and `voti` was archived to a spec with its implementation deleted. The fourth,
`programacao1`, Lucas deleted during the same session. **A finding older than a week is a
hypothesis; re-run it before spending a decision on it.**

1. 🟢 **promotion is a decision the session must actually take, not one it may skip.** Lucas,
   2026-08-13: *"this 'merging up to main' maneuver should be a decision taken by agents as part of
   the roundup/handoff so we minimize the number of repos on open feature branches."* The skill
   already has the mechanism — `/roundup` Phase 5 merges `feature/*` → `develop` → `main` — but it
   fires only when the milestone "shipped this session", so the default outcome is a branch left
   open, and open branches accumulate silently across repos. Two parts:
   - **the ruling** (done, in `core/skills/roundup.md` Phase 5): promote whenever the work is green
     and coherent, and when *not* promoting, say which of the three reasons applies. Silence is no
     longer an option, because silence is what let branches idle.
   - **the measurement** (open): the entropy dashboard counts files, lines and directories but has
     no signal for *repos sitting on an unmerged feature branch* — so nobody can see the number
     this task exists to reduce. Add it beside the other Tier 0 checks, warn-only, one line per
     repo whose branch is ahead of `main`.

   **State after the 2026-08-13 sweep: exactly two repos carry unmerged work**, `isoroll-content`
   and `isoroll-module` (5 commits ahead each, both dirty). They belong to the parallel isoroll
   session, so they are *reason 3*: do not promote them from another session. Every other nested
   repo sits on its base branch — 11 fully-merged `feature/*` labels were deleted locally after
   checking, per repo, that the branch was ahead of base by **zero** commits and that local `main`
   was fully pushed. `branches/instituto` is on `master`, not `main`, which is why it reads `?`.

   **The same 11 branches still exist on `origin`** — deleting a remote branch is an outward-facing
   act and was left for Lucas: `git -C <repo> push origin --delete <branch>`, safe because every
   commit on them is already in `origin/main`.

   **The lesson: ahead-by-zero is the whole test, and it is cheap.** `git branch -d` refuses an
   unmerged branch, so the sweep cannot silently drop work — which is what makes it safe to run
   from a session that does not own those repos, as long as it skips the ones another session is
   holding.
   → **model: sonnet**.
2. 🟢 **HEAD is shared mutable state, and nothing warns — decided 2026-08-14, build it.** Observed 2026-08-14: a
   session began on `feature/wos-typeset`, a parallel session switched the shared checkout to
   `feature/brain-attention` mid-flight, and the first session's commit landed on *their* branch and
   was auto-pushed there by [`core/hooks/post-commit`](core/hooks/post-commit). It was caught only
   because that hook happens to print the branch it pushed. **The branch read correct at session
   start** — which is exactly why a start-of-session check cannot catch this.

   Recovery is non-destructive and worth keeping: `git merge-base --is-ancestor <your-branch> <sha>`
   to confirm a fast-forward, then `git branch -f <your-branch> <sha>` and push **yours**. Never
   reset or force-push theirs, and never `git checkout` your branch back — that just yanks HEAD out
   from under them, which is the same defect pointed the other way.

   **Ruled 2026-08-14 (Lucas): the pre-commit warning, not worktrees.** Record the branch at session
   start; `pre-commit` warns when HEAD no longer matches it. It is ~30 lines, costs nothing to adopt,
   and fires at the exact moment damage would land. One worktree per session removes the shared HEAD
   entirely and is the better end state, but every session has to adopt it before it protects
   anything, and a checked-out worktree makes `git branch -d` refuse — which fights the branch sweep
   in step 1. Keep worktrees as a later opt-in, piloted on one parallel pair, not as the fix for this.

   Build notes: the start-of-session branch needs somewhere to live — `core/hooks/session/` already
   owns session lifecycle state and is where a `SessionStart` hook can write it. Warn, never block: a
   deliberate mid-session branch switch is legitimate and common. `core/tools/wos/roundup
   --leave-dirty` already refuses to move HEAD for a diverged promotion, so the promotion path is
   covered; **ordinary commits are the gap.**
   → **model: sonnet**.

3. 🟡 **`code/SPEC-DRIVE.md` is gitignored, and the discipline it tracks was forgotten.** Two
   captures from 2026-08-15 that are the same finding from both ends. The mechanical half: the
   `code/*` rule at `.gitignore:37` excludes it while its first-level siblings `code/VERIFY.md` and
   `code/SPECS.md` are tracked, so every edit to it has stayed on one machine — found while
   repointing `SETUP.md` references, when a two-line fix showed up in neither `git status` nor
   `git diff`. The human half, Lucas: *"sobre SDD (SPEC DRIVEN DEVELOPMENT), sinto que começamos
   isso mas esquecemos completamente."*

   **Treat them as one.** A rollout ledger that cannot be pushed cannot be picked up by the next
   session, on this machine or any other — invisibility is a sufficient explanation for being
   forgotten, and it is the half that is cheap to fix. Do that first, then read the file's own Open
   items with fresh eyes and decide whether SDD is resumed, rescoped, or killed outright (its gates
   are live either way: `pre-commit` §1d and `read/spec-read-gate.py` are still firing on every
   session, which makes an abandoned rollout more expensive than a dead one). Frente 12 already
   queues its rename to `ROADMAP-spec-drive.md` — land tracking and that rename in the same commit,
   since both are about the file being a real ledger.
   → **model: opus** for the resume/kill call, sonnet for the `.gitignore` fix.

---

## Frente 12 — The `.md` type system (decided 2026-07-30)

**Why.** Lucas: *"all I want is to delimit precisely where one file ends and another begins, so there
is no conceptual intersection."* Each type answers exactly one question.

| Type | The one question it answers | Absorbs |
|---|---|---|
| `AGENTS.md` | What rules always apply, and where do I start? | — |
| `CONTEXT.md` | What is *this directory*, and where inside it do I go? | `tree.md` |
| `ROADMAP.md` | What do we intend to do — and what did we reject and why? | `ARCHIVE`, `HISTORY` |
| `SPECS.md` | What must be true of this thing, and *why*? | `FOUNDATIONS` |
| `BUGS.md` | What is currently **untrue** that we know about? | — |
| `README.md` | I just cloned this. What is it and how do I run it? | `SETUP` prose |
| `REFS.md` | What external material exists and what did we conclude? | `WATCHLIST` |
| `SKILL.md` | What procedure does the agent follow when invoked? | — |
| `GOALS.md` / `goals/<slug>.md` | Which goals have wind / why does this one matter? | — |
| `TODO.md` · `INBOX.md` · `USER.md` | Life tasks · raw capture · who Lucas is and how he fails | — |

**Three residual conflicts, with the resolving rule:**

| Conflict | Rule |
|---|---|
| CONTEXT vs its own routing block | CONTEXT never hand-lists files; the generator owns inventory |
| CONTEXT vs SPECS | rules that *constrain code* → SPECS; what the dir *is* → CONTEXT |
| ROADMAP vs BUGS | BUGS owns the text; ROADMAP references by id and never restates it |

1. 🟢 **retype what the gate now blocks but cannot fix.** `core/hooks/checks/type-gate.py` stops *new*
   off-allowlist names; **40 existing ones remain, enumerated live in
   [`entropy.md`](entropy.md)** — read the report, do not re-scan. They group into four jobs, in
   order of how much judgment each needs:

   | Job | Names | Route | Needs |
   |---|---|---|---|
   | **B. the SPEC migration** | `SPEC.md` ×2 (`spacemantics`, `aiwbot`) + `code/_templates/module.SPEC.md` | → `SPECS.md` | blocked: load-bearing in five enforcement points (`core/hooks/pre-commit` §1d, `spec-read-gate.py`, `context-tracker.py:36`, `spec-scan`, `spec-contract-check`). **One reviewed change**, never piecemeal. |
   | **C. spacemantics' own vocabulary** | 11 more in that one repo: `TAXONOMY` · `TAXONOMY-FAMILIES` · `TYPES` · `LEXICON` · `GRAMMAR-JSON` · `CONFORMANCE` · `CHECKABILITY` · `EXAMPLES` · `CONFLICTS` · `INVENTORY` · `INVENTORY-ADVISORY` | mostly → `SPECS.md` or lowercase instance | **its own session.** A DSL project legitimately has many spec-shaped documents; deciding which are one `SPECS.md` and which are content is a design question about spacemantics, not a naming sweep. |
   | **D. the long tail** | 20 across 9 repos: `isoroll-content` ×7, `flows` ×4, `casinhas` ×3, `instituto` ×3, `dobra` ×2, `2027-CHI-cria`, `2027-ICLR-dobra` | one of the four disposal routes each | a peek at each file. Sonnet, one repo at a time. |

   **Job A is drained** (2026-07-30): the six `HISTORY.md` are gone, one commit per repo. It was
   *not* zero judgment — 25 referrers had to be scrubbed, and the ROADMAP headers in `flows`,
   `isoroll-module`, `gira` and `laplata` were **instructing every future session to write a
   HISTORY.md**, which is what kept regenerating the type. **The lesson for B/C/D: delete the
   generator before the artefact, or the name grows back.** Rejected-approach content is the one
   thing git cannot hold — `aiwbot` (5 items) and `flows` (1) needed it salvaged to
   `ROADMAP.md § Rejected` before the file could go.

   Still on the floor from A: `flows` M12/M13 and `aiwbot`'s finish-line diagram are completed
   milestones kept as `Status: complete` bodies and struck-through text — annotated corpses that
   the same rule says to cut, and that `entropy.md` § Prose describing finished work now lists by
   file and line. Left for job D's pass over those repos, not smuggled into A.
2. 🟡 **does `entropy.md` sit in the right place, and should its name be uppercase?** Lucas, INBOX
   2026-08-15. It is the one always-present report at the workspace root that is not on the type
   allowlist, so the question is real rather than cosmetic. The evidence points at *lowercase, stays
   put*: § The four disposal routes sends a **generated** file to a lowercase instance name (the
   `LABELS` → `labels.md` precedent), and this file is written by
   `core/hooks/entropy/entropy-dashboard.py` and committed by `core/tools/wos/roundup`, never
   authored. What is genuinely open is whether the root is its place — every other generated
   artifact lives beside its generator or under `outputs/`, and `outputs/` is untracked while this
   one must be tracked to serve as the criterion-1 ratchet. Decide once and write the answer into
   `core/SCHEMA.md` so it stops looking like an oversight.
   → **model: opus** — one ruling, then at most a `git mv`.
2b. 🟡 **"Frente" is Portuguese in an English contract vocabulary — decide, then sweep or keep.**
   Lucas, INBOX 2026-08-15: *"por que chamamos de FRENTE as etapas do roadmap? … FRENTE até onde sei
   é só em português. em inglês seria FRONT não é n?"* He is right on the facts. The literal English
   is *front*, but an English roadmap would idiomatically say **workstream** or **track** — *front*
   reads as military or meteorological, so a straight translation is the worst of the three.

   Why it is a real item and not pedantry: this workspace's prose is deliberately mixed — rationale
   in Portuguese, **contracts in English** — and a roadmap heading is a contract, cited by
   **29 occurrences in this file and 27 other files**, including source comments in
   `core/hooks/entropy/*.py` and test docstrings. Those citations are anchor ids in practice, which
   is exactly the cost that priced the `VERIFY.md` rename in item 3.

   If it moves, it is a **retired token**: add it to `core/SCHEMA.md` § Retired tokens in the same
   commit, so the check proves the sweep complete instead of a grep claiming it. Keeping it is also
   a legitimate answer — but then say so in § Vocabulary, so the next reader stops wondering.
   → **model: opus** for the ruling, sonnet for the sweep.

3. 🟢 **the transient initiative doc is `ROADMAP-<slug>.md` — ruled 2026-08-14, three renames left.**
   The "fourth type" turned out not to be a type. Lucas's ruling was to unify by semantic symmetry
   with zero conceptual intersection, and *"make sure as well that we do not create a new .md file
   for each specific minor thing"* — and once asked that way the answer falls out of the type table:
   a rollout is *intent, plan, and what we rejected*, scoped to one initiative, which is the ROADMAP
   question exactly. It never needed a name, it needed a **scope suffix**, and `AGENTS.md` already
   sanctions `ROADMAP-<slug>.md`. **Five differently-named files were the symptom of a missing
   suffix, not of a missing type.** The law is rewritten in
   [`core/SCHEMA.md`](core/SCHEMA.md) § *The one exception*, membership is closed at four, and
   `test_type_gate.py` now asserts the exempt set by equality so a fifth name cannot appear quietly.

   **Done:** the skill-suite migration report under `core/` is deleted — it opened with *"What was
   done (2026-07-05)"*, an annotated corpse of a finished migration. Lucas called it *"very shady…
   do we really need that one?"* and he was right. Its one durable paragraph (the convention for
   skill `refs/` folders, plus the suite-folder rule) moved to `core/SCHEMA.md` § Layer: skill.

   **Left, one reviewed commit each:** `code/VERIFY.md` → `ROADMAP-verify.md` (24 inbound refs, 7 in
   `core/hooks/*` comments — but they cite **anchor ids**, which a rename preserves; only paths
   move), `code/SPEC-DRIVE.md` → `ROADMAP-spec-drive.md`, `code/isoroll-module/REFACTOR.md` →
   `ROADMAP-refactor.md`. And `code/dobra/DECISIONS.md` is not a roadmap at all — decisions are
   *what must be true and why*, so it folds into that project's `SPECS.md`.
   → **model: sonnet**, one file per commit.

---

## Frente 13 — the `.md` corpus audit: ASSESS, CUT, REDIRECT, then compress

**The four verbs, and the order** (Lucas, 2026-08-15). CUT alone was the wrong single verb, because
content in the wrong *place* is a different defect from content that is wrong, and some content is
*under*-placed rather than over-placed. ASSESS whether a section is still true and who needs it;
CUT what nothing changes without; REDIRECT what is true and needed but sitting where it is not
read, or read by everyone; COMPRESS only what survives. The law is
[`core/SCHEMA.md`](core/SCHEMA.md) § Placement — tier (ESSENTIAL / IMPORTANT / DESIRABLE) crossed
with read-frequency, giving KEEP / PROMOTE / REDIRECT / CUT.

**The mechanical halves are checked, so do not hand-count anything.** [`entropy.md`](entropy.md)
§ Prose describing finished work and § Constraints trapped in a CONTEXT.md head are this frente's
live queues; each ratchets in `core/tools/test/workspace/test_corpus_ratchet.py` and its ceiling
must be lowered as the drain proceeds. What the checks cannot answer — *does anyone need this* —
stays judgement, and stays unmeasured until Frente 14 gives it an instrument.

**One ratchet per named defect, never a shared one.** Until 2026-08-15 the corpse check also
matched the routing generator's unfilled-description marker, so 70 markers sat inside a queue of
105 wearing the wrong label and carrying a remedy — *cut it* — that made the generator rewrite them
on the next save. The marker is § Unanswered scaffold placeholders now, and draining it is **Frente
4 item 6**, not this frente. The lesson generalises: a queue that counts two defects can have one
of them grow while its number falls.

1. 🟡 **drain the nested repos — the whole of what is left.** Two thirds of the corpus (~187 of 261
   `CONTEXT.md`) lives in nested `code/` and `academy/papers/` repos with their own branches and
   gates, so it cannot ride a wos commit. Same classification as the `.d.ts` stub gap: counted in
   [`entropy.md`](entropy.md), drained where the files are. Live: **19 corpses, 17 trapped heads.**
   The wos half is done; `FINISHED_CEILING` and `MISPLACED_CEILING` in
   `core/tools/test/workspace/test_corpus_ratchet.py` hold that ground, and the nested repos cannot
   move them — each runs its own verify.

   **The REDIRECT recipe, in order, and it survives contact:** (1) delete what a hook enforces — it
   names the fix when it fires, except numbers that change how you write *before* the hook can
   speak, so the 150/200 line caps stay; (2) move constraints to a sibling `SPECS.md`, creating it
   if absent; (3) move data out (alias lists, schemas); (4) delete stale claims; (5) keep identity
   and navigation only.

   **Delete-first is what makes it cheap: six new `SPECS.md`, not eleven.** Running step 1 before
   step 2 found that most of what looked movable was already written better somewhere else —
   caveman's path table duplicated its own generated routing block, its `hooks/` layering table
   duplicated the child `CONTEXT.md`, and craft's vocabulary section restated `core/SCHEMA.md`
   verbatim. **Open the child `CONTEXT.md` and the file's own routing block before relocating
   anything.** Heads: `core/skills/caveman` 1332 → 211, `core/experiments` 708 → 212,
   `core/skills` 656 → 108, `core/flows/craft` 620 → 91, `academy/papers` 462 → 186,
   `core/refs` 441 → 120.

   **The check needs an over-size head *and* a modal, so a thin pointer line is the whole trick** —
   `Gate behavior and the agent-shim contract: SPECS.md`, never "you must read SPECS.md". Two heads
   (`core/tools/notes` 444, `core/tools/verify` 448) sit above the token warn with zero modals and
   are correct as they are; the warn is a signal, not a cap.

   `.opencode/CONTEXT.md` is the biggest head of all and is a **generated mirror** — fix it at the
   generator or leave it.

   **The prediction that every pass surfaces a defect held, and both were in generators, not prose:**
   `.sh`/`.jsx` missing from `COMMENT_RE` (see 4.6) and `is_skill()` in
   `core/tools/wos/skills/mirror.sh` excluding only `CONTEXT`, so the first `SPECS.md` written
   inside `core/skills/` read as a skill with no frontmatter and failed the commit for *every*
   staged `core/skills/*.md`. Both fixed with tests. **A doc pass is a cheap fuzzer for the
   generators that read those docs** — it writes file shapes nobody had written before.

   `brain/goals/workspace-os.md` and `test_gitignore_self_heal.py` both cite a **Frente 6** that no
   longer exists — retired ledger numbering still has live references.
   → **model: sonnet**, one repo at a time.

## Frente 14 — ablation: nothing in this workspace has ever been measured

1. 🔴 **build the instrument, then run the ablation.** Lucas, INBOX 2026-08-15: *"um engenheiro
   líder da Anthropic sugeriu de tempos em tempos a gente 'deletar' o CLAUDE.md e ver como modelos
   top (como o Opus) performam, dizendo que poderíamos nos surpreender. ou seja, diminuir a carga de
   instruções. esta recomendação é bem forte pro nosso caso. tudo que o WOS faz (ou pelo menos boa
   parte) é contornar ingenuidades do modelo. realmente precisamos fazer um benchmark com estudos de
   ablação em breve."*

   **The premise is falsifiable and nobody has tried to falsify it.** This workspace exists to
   compensate for model failures; a stronger model may not need the compensation, and every rule
   that outlives its failure is pure cost. The claim cuts at the whole scaffold, not just the docs.

   **Precondition, and it is the reason the last attempt produced nothing.**
   [`core/ROADMAP.md`](core/ROADMAP.md) § ablation-bench ran once and yielded no signal for exactly
   one reason: there was no clean way to turn a single feature off. So the toggle registry in
   Frente 10.4 is not a sibling of this item, it is its instrument — *"it also would ease ablation
   tests so we can indeed see the impacts of each option"* (Lucas, 2026-08-14). Building the bench
   before the switch repeats the failure.

   Scope is the whole enforcement layer, not the `.md` corpus: hooks, skills, tools, `AGENTS.md`
   itself. Frente 13 is downstream — its verdicts are judgement calls today precisely because this
   instrument does not exist, and it says so rather than implying they are measured.
   → **model: opus** for the design, sonnet to run it.

## Silent failure is the failure mode this workspace actually has

Batch B is drained (2026-08-14). The recap is git's; this is the part that changes how the next
bug hunt starts.

**All six were silent.** Not one failed loudly — they exited 0, blocked with no message, or wrote
a file nobody re-read. The JS declaration path had emitted nothing *for years*; `pre-edit.py`
refused edits without a reason attached; stubgen wrote into a mirror of its own path. A bug that
announces itself gets fixed the day it lands, so what survives here is selected for muteness, and
the only detector was Lucas's eye. Two of the six were already fixed and the ledger did not know.

So a check that a thing *happened* beats a check that it did not error, and three of the tests
added are cross-cutting rather than one-file: no generated stub inside a doubled path, no
blocking gate off stderr, no `jsconfig.json` carrying emit keys. **When hunting the next one,
prefer asking "what does this produce, and is it there?" over reading the code for a raised
exception.**

Open, and per-repo drain work rather than a wos item: the `.d.ts` half of the stub gap — 203
files, all in nested repos, now counted in [`entropy.md`](entropy.md) under the criterion-1
baseline rule.

## Parked — explicitly out of v1

- **`[gdrive-integration]` / `[courses-import]`** — content migration, large. Per-folder work lives in
  `brain/TODO.md`.
- **`[offline-resilience]`** — the gaps are (a) network: [Reticulum](https://github.com/markqvist/Reticulum),
  E2E without infrastructure, and (b) an offline corpus: **Kiwix** (all of Wikipedia offline — almost
  certainly the "NOMAD project" Lucas half-remembered). Refs in `core/refs/REFS.md`.
- **Serious OCR** — real need (image-only PDFs in `branches/ecovila/burocracia/` where
  `core/tools/paper/parse` returns empty; test Baidu "Unlimited OCR" first), but it belongs where the PDFs
  are, not in the wos ledger.

## Rejected — killed 2026-07-30, one line each

Kept only so a dead idea does not resurface looking new. Accepted price: some will resurface in
months anyway. Cheaper than a list nobody reads.

- **INBOX provenance probe** — Frente 1 shipped; the probe measures a threat model already ruled inert.
- **SLM confirmation run** — depends on `dobra` maturity that does not exist; the preprint stays provisional, which is fine.
- **Tier 1 periodic cheap-agent detectors** (gold tasks, scheduled `/dedup`, misplacement audit) — paid detection of what Tier 0 catches free.
- **Tier 2 `/tidy` skill** — a new skill to do what a human can do directly from the dashboard; scatter.
- **High-coupling / import-graph detection** — no evidence coupling is hurting anything.
- **Anti-entropy prior-art research lead** — a reading list, not work.
- **Anti-collapse edit gate** — self-declared optional, touches the edit path, guards a failure never observed here.
- **`/inbox` offers `/compass` on a trigger** — speculative UX on the one path whose whole virtue is being cheap.
- **`>routing` tier·effort metadata on goal files** — metadata for a router that reads fine without it.
- **Model-routing strategy doc** — the routing that pays is already in the per-step model tags and `/prepare`.
- **Benchmark craft flow vs SOTA repos** — expensive comparison against repos with different cost priorities.
- **Triggers after a limit window renews** — infrastructure to wake a dead session; `ScheduleWakeup` covers the live case.
- **`[task-metric]` closed-vs-created instrument** — measuring the ledger is more ledger; the honest signal is Lucas saying he feels lost, and he does say it.
- **Retroactive ref→task pairing** — the policy holds going forward; old unpaired refs can rot.
- **Scaffold update log** (`core/SCAFFOLD-LOG.md`) — the paper thread; git plus this file already carry trigger→change. Revisit only if a paper is actually written.
- **Downloads unification across devices** — cross-device config, life logistics, not scaffold.
- **Dated `GOALS.md` attention re-check** — a calendar reminder for 2026-08-06, not a ledger row. Verified *not* a live bug; the 14-day window washes the old history out on its own.
- **opencode + copilot parity** — aiwbot's own premise; lives in `code/aiwbot/ROADMAP.md`.
- **Nested-repo git graph in VSCode** — IDE trivia.
- **Google Slides API + slide templates** — content tooling.
- **Mobile INBOX Android app** — aiwbot is already the away-from-PC front door.
- **`brain` coverage sweep** (`[brain-full-files]`, `[branches-coverage]`) — content completeness, not scaffold.
- **English-learning mode** — was disabled once already; weak signal.
- **aiwbot as away-from-PC front door** — a pointer to another ROADMAP is a duplicate by definition.
- **Extract the "10 GitHub repos that replace paid tools" list** — a listicle.
- **Evaluate Surfsense** — our `core/tools/web/{search,fetch}` + `core/tools/paper/{papers,parse}` + research flow already cover it.
- **Research-flow hallucination audit** — real but unforced; no observed fabrication.
- **`pre-edit.py` vs `check-line-counts.sh` scope disagreement** — policy nit, no live symptom.
- **`core/tools/paper/papers --ss` live smoke** — it will smoke itself on the next real use.
- **Commit the `.claude/commands/{drive,calendar}.md` symlinks** — done inline rather than tracked.
- **`/caveman compress` on workspace docs** — piloted on the worst offender: 8571 → 8552 chars, **0.22%**, for one full quota call. The docs have no lexical fat, so placement beats phrasing and compression stays the last step on an already-reduced surface (Frente 13).

## Sequencing

1. **Frente 12.1** — apply the type system. Do it before 4.1 so Tier 0 enforces a vocabulary that is
   already true, and before 12.2 so refinement passes are not spent on files about to be deleted.
2. **Drain [`entropy.md`](entropy.md)** — the keystone is built; criterion 1 is a drain, not a
   design. Biggest families first; the report's summary table says which those are today.
3. **Frente 4.2** — the `loops`→`flows` generator rename. Its retired tokens are declared in
   `core/SCHEMA.md` § Retired tokens, so the sweep has an assertion waiting: add the old spellings
   to that table the moment the rename lands, and the check proves it complete.
4. **Frente 10** (1, 2) — the install idiom + declared deps.
5. **Frente 13.1** — the corpus drain, hot files first.
6. **Frente 11.1** — the four sweep rulings, whenever Lucas has direction.
7. **The judgment calls: 8.1, 9.1, then 10.1 → 10.3 → 10.4 → 14.1**, which is one chain rather than
   four independents — the toggle registry is the instrument the ablation needs.

## Model-switching guide

The canonical guide lives in the flow that produced this plan:
**[`core/flows/research/scout.md`](core/flows/research/scout.md) → "Canonical model-switching guide"**
(same-session `/model` · `/loops` autorouting · Agent-tool `model:` override · `/handoff`).
Mapping: 🔴 → **Opus, same session**; 🟢/🟡 → **Sonnet via `/loops`** (mechanical parts drop to haiku).
