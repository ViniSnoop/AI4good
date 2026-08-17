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
| 1 | **verify-fast green + Tier 0 live** — naming, placement, pointer integrity, size-as-signal deterministic; **this repo** clean, every nested repo on a shrinking baseline | Front 4 | checks live · **read [`entropy.md`](entropy.md) for the count, never a copy of it** |
| 2 | **One ledger, no duplicates** — this file is the sole wos ledger, verified by scan not eyeball | Front 8 | ✅ **MET 2026-07-30** — `test_no_item_lives_in_two_ledgers` |
| 3 | **Everything pushed, gitflow-shaped** — every `code/` repo on `main`/`feature/*`, zero unpushed, no repo without a remote | Front 11 | ✅ **MET 2026-08-14** — re-audited across every repo |
| 4 | **Clonable by a student** — fresh clone gets every capability; deps declared, no undocumented hand-installs | Front 10 | ✅ **MET 2026-08-16** — `SETUP.md` is an executed procedure, every dep declared in `core/tools/deps.txt`, both enforced by `verify-fast` |

Post-v1 validation is `[mvp-validate]`: use the system daily for 30 days, then assess whether it
reduced mental load. That is the real test and it can only run after v1.

## How to read this

Per-step `model` = the tier that is *enough* (a floor, not a ceiling).
🔴 needs Lucas · 🟡 pilot on one subtree first · 🟢 mechanical.

**Three open steps need Lucas's own judgment: 9.5, 11.3, 15.1** — the single list, quoted here and
nowhere else. Everything else is agent work.
Stating that number is part of the cure for feeling lost, so **keep it true** — it has been wrong
three times: once claiming one while five were live; once (2026-08-16) carrying four items marked 🔴
whose own `→ model:` line said sonnet; and once holding *two* lists of the same set, here and in
§ Sequencing, which named different threes and so were both wrong. **Derive it from the 🔴 marks.**
**This is the only list; § Sequencing points here rather than restating it.** Two lists of the same
set is the asymmetry, and the count is only ever its symptom, so the cure is one list rather than
two kept in sync. **🔴 means Lucas decides, not "this is hard"**; an item an opus-tier agent can
rule on alone is 🟡. Re-derive the count from the marks before quoting it.

The whole Front 10 chain came off this list on 2026-08-16 — six 🔴 items closed in one sitting,
because they were one decision wearing six numbers and none of them could be taken alone.

**Never cite an item number from code or from a test — now ENFORCED**, by
[`core/hooks/checks/citation-gate.py`](core/hooks/checks/citation-gate.py) on every commit. A closed
item is *deleted*, so every `Front N.M` in a comment becomes a dead pointer the day the work lands.
Point at the `SPECS.md` or `SCHEMA.md` section that owns the rule instead; those are durable, and
writing the rule there is what closing an item is *for*. Numbering is legal inside `ROADMAP.md` and
`ROADMAP-<slug>.md`, and in a commit message, which git keeps.

**What the sweep found, and it is the argument for gating rather than asking** (2026-08-16). This
rule was prose for a fortnight and the corpus reached **91 numbered citations across ~50 files** —
including pointers to *Fronts 2 and 6, which have never existed*, cited from the `.gitignore`
self-heal and the pointer-integrity test. Two of the checks whose job is catching dead pointers were
themselves carrying them. **A rule that only a careful reader applies is a rule the corpus grows
past.**

**Sequence a ban before a rename, never after.** Renaming `Frente`→`Front` looked like it shared a
sweep with this ban. It did not: 91 of the 160 mentions were citations the ban deletes outright, so
doing the ban first cut the rename from a 50-file sweep to three files. The reverse order would have
carefully moved 91 pointers and then deleted them.

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

## Front 3 — Memory and always-loaded context

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

## Front 4 — workspace anti-entropy — **the keystone, v1 criterion 1**

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
   → **model: sonnet** · **switch: `/craft`.**
2. 🟢 **finish the retired-word rename at the per-run state dir.** APPROVED 2026-07-29 (Lucas: *"we
   renamed loops to be flows but apparently this keeps coming back"*). It keeps coming back because
   it **was never a drift problem** — the rename stopped at the flow pool (`core/flows/`, flow
   renamed `craft`) while the generators still emit the retired word *legitimately*, so no naming
   check could ever flag it. The skill half is closed — the command is `/craft`, the file is
   `core/skills/craft.md`, and `core/SCHEMA.md` § Retired tokens guards the invocation shape.

   What is left is the state dir, and it is the larger half: `.loop/<slug>/` is hardcoded in
   `craft.md`, `architect.md`, `runtimes.md` and `routing.md`, with 14 live dirs across `aiwbot`,
   `isoroll-content` and `isoroll-module`; the cross-run pattern library is
   `core/flows/.loop-skills/`. Scope: `.loop/` → `.craft/`, `.loop-skills/` → `.craft-skills/`, and
   the live dirs migrate with it. Add that token to § Retired tokens the day it lands — **not
   before**, because a row that fails on the day it is written trains people to ignore the check.
   **Keep "Loop 0..6" as step names** — an iterative step really is a loop; that word is correct
   English, not the retired label.
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
   those repos, including the commits that would fix it. Live lists in [`entropy.md`](entropy.md);
   when they read Clean, add fanout to `core/hooks/checks/` beside the type gate and delete
   `BASELINE` from `test_entropy_fanout.py` in the same commit.

   **This repo, `code/aiwbot` and `code/flows` are drained.** What the draining taught is written
   into [`code/SPECS.md`](code/SPECS.md) § Splitting an over-full directory — five rules, each of
   which cost a session to find, and that is where a future repo will look for them rather than in
   a ledger item that closes.

   **Everything remaining lives in nested repos and is refiled there (2026-08-16)**, because a
   workspace commit cannot touch those files and a pointer to another ROADMAP is a duplicate by
   definition. `apptime` and `spacemantics` carry their own items now, on
   `feature/workspace-drift-refile`. The isoroll pair — `isoroll-content/src/pipeline` and its
   siblings, `isoroll-module/src/render` and its siblings, plus the one file over `BLOCK_LINES` —
   were **not** refiled: both checkouts are held by the parallel isoroll session and writing into
   them from here is the mid-flight collision Front 11 exists to prevent. **That session refiles
   them**, and until it does, this repo cannot flip the gate.
   → **model: sonnet**, one repo at a time.

6. 🟡 **close the first-line-comment hole, then sweep — in that order, because sweeping first
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
   2026-08-15 while draining the corpus. `ALL_EXTS` and `COMMENT_RE` in
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

8. 🟢 **`python_api` advertises nested closures as importable API.** Found 2026-08-15 by
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

## Front 8 — The ledger discipline — **v1 criterion 2**

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
      would regenerate it — that is the lesson job A of Front 12.1 already paid for.

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
   respectively — so the next session on this front starts by paying that down, before adding
   anything.
   **The parser is fixed and tested (`test_brain_attention.py`), so start from a quiet baseline.**
   It used to read the goal's body as repo paths and print nine warnings per commit. Worth
   remembering while doing the counting work: nothing was ever *miscounted* by it, which is why it
   survived — the output was wrong in a way that changed no number.

   → **model: sonnet**. The plan is the three findings above; it used to point at a file in
   `~/.claude/plans/`, which `AGENTS.md` forbids — a plan lives in the ROADMAP of the thing it
   changes, not in harness-owned state no clone of this workspace would ever get.

---

## Front 9 — Cost & model routing

> **The output-cost plan is [`ROADMAP-output-cost.md`](ROADMAP-output-cost.md)**; the measurement it
> may not contradict is [`core/experiments/output-cost.md`](core/experiments/output-cost.md).
> Output is **~13% of spend at sticker and ~25% once re-reads are counted** — a mean turn is ~12%
> self-authored, and one written token costs **1.9x** list. Only **35%** of billed output tokens are
> logged and re-read; the other 65% is thinking, paid once. `usage` prints all of it and `roundup`
> prints the per-session line plus compaction adoption, so these regenerate instead of being quoted.

**Why — re-measured 2026-08-16, and the old numbers were wrong twice over.** The first framing came
from a single 24 h window. The second came from `usage` itself, which summed transcript *records*
rather than API responses (1.97x) and charged thinking the re-read multiplier — so the numbers this
section carried until 2026-08-16 were inflated by the tool built to make them trustworthy. Re-run it
yourself: [`core/tools/wos/session/usage`](core/tools/wos/session/usage). Over
**141 sessions · 11,381 turns**:

> **Trust the ratios, not the dollar total.** Absolute spend is list price and has never been checked
> against a bill. Quote percentages and $/turn.

| Claim | Verdict |
|---|---|
| "59% of usage from subagent-heavy sessions" | **Unmeasured, and the retirement was wrong too.** The audit searched for `Task`; the tool is named **`Agent`**, and it ran **56 times across 12 sessions**. Subagent turns are also absent from the parent transcript by design — they live in `<session>/subagents/*.jsonl`, 48 files this audit never opened. Re-measure with `context` before any claim here. |
| "55% from >150k-context sessions" | **Understated.** **72%** of spend is paid above 150k of context; **41%** above 250k. |
| "25% from `/roundup`" (step 1 said ~7%) | **~7% was right; 25% was not.** 24 of 119 sessions invoked it; the tail after invocation is **~10%**. |

**The real driver is context size — and the curve is a staircase, not a ramp.** Cost of one turn by
the context it carried, and what each band adds over the one below it:

| band | $/turn | vs. band below | | band | $/turn | vs. band below |
|---|---|---|---|---|---|---|
| <50k | 0.077 | — | | 200-250k | 0.167 | +13% |
| 50-100k | 0.085 | +10% | | 250-300k | 0.195 | +17% |
| 100-150k | 0.116 | **+36%** ← bend | | 300-400k | 0.244 | +25% |
| 150-200k | 0.148 | +28% | | >400k | 0.326 | +34% |

Flat below 100k, then a climb that never stops — **4.2x from the cheapest band to the dearest**.
**88% of spend is paid above 100k, 56% above 200k.** The mechanism is that every turn re-reads the
whole thread: **2.2 Gtok** of cache reads. Long sessions therefore cost super-linearly in their own
length, and the **top decile of sessions is ~46% of total spend.**

The old reading of this table claimed a *plateau* at 200-300k (+5%, +8%) and set `CTX_LOUD` where the
climb was thought to finish. The plateau was an artifact of the record-duplication bug: bands whose
turns carry more content blocks were counted more times. The corrected curve has no plateau, which
strengthens the thresholds rather than moving them — 100k is still where the bend starts, and past
200k there is no point at which one more turn stops getting dearer.

Two facts that decide where a threshold can usefully sit. **Most sessions cross the bend** — median
peak context **136k**, p75 **248k** — so firing at 100k rather than 150k costs almost no extra noise
(52% of sessions against 48%). And **there is runway to act**: after crossing 100k the median session
still has **~85 turns** ahead, enough for a hand-off to repay its re-grounding cost. Warning early
does not cost precision work; that fear priced a session about to end, and at these thresholds the
session is not about to end.

Both halves of the session transition are live. The size signal is
[`core/hooks/session/context-meter.py`](core/hooks/session/context-meter.py) on `UserPromptSubmit`:
it reads the size the API already reported and announces `CTX_WARN` / `CTX_LOUD` once each, costing
zero tokens until crossed and never blocking. **The session cannot see its own size**, which is why
the hand-off decision is made late without it — a hook is the only thing that can see it *and* speak
at the moment it applies. The close itself is [`core/tools/wos/roundup`](core/tools/wos/roundup) plus
the two skills; every decision behind that split, and why no session spawns its own successor, is
[`core/SPECS.md`](core/SPECS.md) § AD-09.

**The lesson this front cost the most to learn, twice: a number nobody can re-run steers the work
anyway — and building the instrument is not the same as checking it.** The first framing came from a
single 24 h window wrong in every claim. The second came from a tool, was re-runnable, and was still
wrong by 2x for three weeks because nobody re-derived its output by hand. So: a number in this file
that [`core/tools/wos/session/usage`](core/tools/wos/session/usage) cannot reproduce should be
**deleted, not softened** — and a new instrument owes one hand-check before anything is quoted from it.

1. 🟢 **safe — cheaper models where the work is mechanical.** Measured split (2026-08-16):
   opus-5 56.5%, opus-4.8 27.5%, fable 8.3%, sonnet 7.7%, haiku ~0%. Worth doing, but note the
   ceiling — routing cannot beat a 4x context multiplier, and the transition above already took the
   larger win. → **model: sonnet**.
3. 🟡 **make delegation happen, instead of hoping for it.** Lucas, INBOX 2026-08-15: *"só tenho
   confiado no opus. mas gostaria que ele delegasse mais ao sonnet pra economizar quando fosse
   pertinente. não sei como fazer isso, seria ótimo se tivesse uma forma mais garantida de fazer
   isso acontecer."* Item 1 says routing is *worth doing* and measures the split at opus 84% /
   sonnet 7.7%; this item is why that split has not moved. **A per-item `→ model:` line in this
   file is advice an agent may skip, and mostly does** — same class of defect as Front 4.6's
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
   **Partly demonstrated 2026-08-16**: this session's own plan carried a `model:` per task, which is
   the mechanism in its cheapest form — the plan *is* the assignment record. What is unbuilt is
   anything that makes it non-optional.
   → **model: opus** for the mechanism, sonnet to wire it.
5. 🔴 **discuss — should this workspace have agents, or are skills enough?** Lucas, same capture,
   and flagged by him as a discussion rather than a task: *"um aluno comentou que existem formas
   diretas de o claudecode delegar pra subagentes, ele falou acho que com @. é fato que não temos
   agentes no workspace, me pergunto se deveríamos. temos skills e isso me parece suficiente, mas
   talvez não seja. esse é um ponto que merece discussão ao meu ver."*

   Two facts to put on the table before opinions. `core/agents/` **does** exist — lead, researcher,
   writer, verifier, reviewer, ported from Feynman — so the claim "não temos agentes" is about them
   being unused, not absent; find out which is true before designing anything. And the measured
   fact from this front: *zero* sidechain messages across 328 transcripts, which is why the
   "59% from subagent-heavy sessions" claim was retired. **Nothing has ever been delegated here**,
   so this is a question about a capability with no usage data at all, not a tuning question.
   Same treatment as Front 10.1: bring options and trade-offs, decide with Lucas, do not arrive
   with one answer.
   → **model: opus**, with Lucas in the loop — not a solo pass.
6. 🟢 **measure whether our own gates make a session re-read the same file.** Lucas, INBOX
   2026-08-15: *"does a session, due to our hooks/gates, re-read the same context file more than
   once? can we have a report at the end of each session (maybe on the /roundup) that automatically
   prints (zero-token) all the read and all the written files, and for each file how much of that
   file was read and how many times as well."*

   **This is the sharpest question anyone has asked about the enforcement layer, because it points
   at a cost we impose rather than one we inherit.** `context-gate.py` demands a whole `CONTEXT.md`
   chain before any file access in a subtree, and `pre-read.sh` redirects source reads to stubs —
   both are designed to *save* context, and neither has ever been measured doing it. A chain
   re-read once per subtree per session is the mechanism paying for itself; re-read per *file* is
   the mechanism billing for the same page repeatedly, and the front's own rule applies: a number
   nobody can re-run steers the work anyway.

   The transcript already holds every `Read` with its offset and limit, and
   [`core/tools/wos/session/usage`](core/tools/wos/session/usage) already replays transcripts — so
   this is a second lens on data we have, zero-token, no new capture. Report per file: bytes read,
   read count, and whether a stub or the source was served. Ships in the same roundup block as
   item 4, and **feeds Front 14** — read amplification is exactly the kind of cost an ablation
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
8. 🟡 **auto-continue when the session limit is hit.** Lucas, INBOX 2026-08-16: *"estudar uma forma
   de ativar um 'auto-continue' do claude code quando o limite das sessões é atingido."* Filed here
   rather than in `code/aiwbot` because the thing that must survive the interruption is this
   workspace's session ritual, not a bot's transport.
   **Study before building** — the honest first question is what the harness actually does at the
   limit and what state survives it, and the second is whether resuming is even right: a session
   that hit the limit is a session at maximum context, where `/roundup` plus a fresh start is
   cheaper per turn than continuing (see the band table above). The likely answer is *auto-close,
   not auto-continue*. → **model: sonnet** to study, Lucas to rule.

---

## Front 10 — Portability & clonability — **v1 criterion 4**

> **Ruled 2026-08-16 (Lucas). The whole decide-first chain is closed; what is left is build work.**
>
> **The harness is the installer.** *"the user opens up a harness and points it to the git repo. all
> the rest is done intermediated by the harness the user is using. so our job is not to provide an
> all-in-one installer but rather guidance (in the best way we can, with maybe tools to automate the
> installation of parts etc) for the harness that is being used."* This kills the 2026-07-30
> "executable installer" ruling and every idiom that was compared against it — `curl | sh` exists to
> deliver a binary you do not have, and whoever installs WOS has already cloned the repo. **The
> newcomer's own agent performs the install**, which is the only shape that is harness-agnostic by
> construction rather than by porting.
>
> **`SETUP.md` lives, and is the deliverable** (closes the 2026-07-30 contradiction with
> `core/SCHEMA.md`, which now records the ruling). It stops being prose an installer would replace
> and becomes prose an agent *executes*. `code/SETUP.md` and `academy/SETUP.md` answer a question no
> WOS installer covers, so the type keeps its row and nine files stay legal.
>
> **Features: one grouping, everything else a column.** Grouping is Lucas's own sketch — hooks ·
> the `AGENTS.md`/`CONTEXT.md` tree + routing · brain · per-area capabilities · skills — because it
> matches the tree, so a feature is findable. The other three candidate axes become **columns** on
> the row: installability, enforcement strength (blocks/warns/generates/advises), and scope
> (general vs Lucas-specific). *"levels of features"* described a column, not a set of boxes. The
> symmetry test passes: nothing is both a hook and a skill.
>
> **This repo is Lucas's and tracks its own profile.** *"our current repo is mine… I want to use it
> on more machines. so I envision both tracked in the repo. BUT the shareable version of WOS will be
> placed on a different repo, a public one… the profile part on that repo will be just a
> placeholder."* So the registry **and** the answers are versioned here, and step 5's sync replaces
> the profile with a placeholder on the way out. That also settles the old step 3: the
> general/Lucas-specific line is not a document, it is **what the sync script is allowed to copy**.

**The install itself is done (2026-08-16) and criterion 4 is met.** The feature slugs `SETUP.md`
declares per step are the registry's keys, already written — step 4 below supplies the answers, not
the vocabulary. One dependency is still genuinely missing on this machine and `core/tools/wos/deps`
says so on every run: **`flutter`**, without which `code/apptime`'s verify cannot run at all.

**The registry is live and the profile answers it.** `core/features.txt` declares 62 capabilities,
`core/profile.txt` holds this machine's answers, `core/hooks/feature_law.py` reads both, and
`core/tools/wos/features` is the CLI. The rule is [`core/SPECS.md`](core/SPECS.md) § AD-14; the
placement is [`core/SCHEMA.md`](core/SCHEMA.md) § The four disposal routes. Step 5 inherits one
file to replace with a placeholder, which is the sync's simplest possible case.

**Sixty of the 62 are not switchable, and that number is the work** — `features --findings` prints
it, so it is never copied here. Wiring one is mechanical: call `feature_law.is_enabled()` in the
file that enforces the rule, then name that file in the `wired` column. Two are wired as the
proof, one per seam — a shell gate and a node hook, both through the same `--enabled` arm.
**Front 14 cannot report on a feature whose row still reads `-`.**

5. 🟡 **the public scaffold repo and its one-way sync.** A **separate public repository**, not a
   branch — personal history never leaves this repo, where a branch would carry every commit that
   ever touched `brain/`. That is what makes the general/Lucas-specific line checkable on every run
   instead of documented.

   **Ruled 2026-08-16 (Lucas), both open questions closed:**
   - **`brain/` crosses as empty structure** — `CONTEXT.md`, an empty `INBOX.md` and `GOALS.md`, one
     example goal file. No real goals, no `USER.md`, no attachments. The brain system is half the
     value of WOS; shipping `core/` alone hands someone an enforcement layer with nothing to enforce
     on. An example rich enough to look like real personal data is the thing to avoid.
   - **Sync is one-way, contributions land as INBOX entries.** The script pushes private → public
     and nothing auto-flows back. A useful PR is read and re-implemented here by hand, captured
     through `brain/INBOX.md` like every other input. The private repo stays the single source of
     truth, and contribution stays honest rather than blocked.
   - **The public checkout lives at `code/wos/`**, as a nested repo like every other project. Lucas:
     *"maybe a good idea is for us to have it here as a code repo under `code/wos/` so it is easy to
     monitor it. this workspace repo is private, mine and only I use it amongst my machines (two
     laptops), and the public is for my students and anyone else."* Still its own repository with its
     own history — that is what keeps personal commits from crossing — this only fixes where the
     working copy sits. It pays twice: the sync becomes an ordinary write into a tree that can be
     `git diff`ed **before** anything is pushed, so **the allowlist is reviewable as a diff rather
     than trusted as a script**; and the public repo inherits the gates, since `core/hooks` is wired
     globally and fires in every nested repo. Mechanically free — `code/wos` joins the `code/*`
     ignore list like `aiwbot` and `apptime`, so no gitlink forms.

   The registry (step 4) ships as scaffold — it is the thing that makes a subset installable — with
   the profile replaced by a placeholder on the way out. **The sync's allowlist is the deliverable**,
   not the copy: a path that is not on it does not travel, so adding a new top-level directory fails
   closed.
   → **model: sonnet**.

---

## Front 11 — Git & sync integrity — **v1 criterion 3 — ✅ MET 2026-08-14**

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

**The lesson, and it is the same one Front 9 paid for: an audit's findings rot faster than the
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

3. 🔴 **is spec-driven development resumed, rescoped, or killed?** Lucas, 2026-08-15: *"sobre SDD
   (SPEC DRIVEN DEVELOPMENT), sinto que começamos isso mas esquecemos completamente."* The ledger
   is [`code/ROADMAP-spec-drive.md`](code/ROADMAP-spec-drive.md) and it is **readable now** — it was
   gitignored by the `code/*` rule, so every edit stayed on one machine, which is a sufficient
   explanation for the forgetting on its own.

   **The decision cannot be deferred cheaply, because the gates are live either way.** `pre-commit`
   §1d and `read/spec-read-gate.py` fire on every session regardless of whether anyone is still
   rolling this out, which makes an *abandoned* rollout more expensive than a dead one. Read the
   file's own Open items with fresh eyes and rule.

   **What tracking it immediately revealed, and it is the argument for the whole `.gitignore`
   allowlist discipline:** the moment the file entered the corpus it failed `verify-fast` on three
   retired tokens from the July `loops`→`flows` rename. Every other file was swept then. This one
   could not be seen, so for a month it kept pointing readers at a flow file that had been renamed,
   **An untracked file does not merely lack backup — it opts out of every
   check the workspace has**, and goes on giving instructions while it rots.

   **Read [`github/spec-kit`](https://github.com/github/spec-kit) before ruling** (ref in
   [`core/refs/REFS.md`](core/refs/REFS.md); Lucas, INBOX 2026-08-16: *"vale a pena pesquisar bem
   pra não pegar a primeira opção sem pensar"*). It is input to the decision, not a replacement for
   it — ours is already wired into five enforcement points, so the honest question is what spec-kit
   does that those do not, and whether adopting it would mean deleting our gates or feeding them.
   → **model: opus**, with Lucas.

---

## Front 12 — The `.md` type system (decided 2026-07-30)

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

1. 🟢 **the `SPEC.md` → `SPECS.md` migration — the one part of retyping that is still wos work.**
   `core/hooks/checks/type-gate.py` stops *new* off-allowlist names; the existing ones are
   enumerated live in [`entropy.md`](entropy.md) — read the report, never re-scan.

   **Three `SPEC.md` instances**: `spacemantics`, `aiwbot`, and `code/_templates/module.SPEC.md`.
   The template is the generator, so it moves first or the name grows straight back. This is
   **one reviewed change, never piecemeal**, because the singular spelling is load-bearing in five
   enforcement points — `core/hooks/pre-commit` §1d, `read/spec-read-gate.py`,
   `read/context-tracker.py`, `core/tools/wos/spec-scan`, `core/tools/wos/spec-contract-check` —
   and in the `> spec:` convention every `code/` CONTEXT.md declares. Only when it lands does
   `SPEC.md` earn its row in `core/SCHEMA.md` § Retired tokens; a row written before the sweep
   completes fails on day one and trains people to ignore the check.

   **The rest is refiled (2026-08-16).** spacemantics' eleven spec-shaped names are that repo's
   design question and now live in its ROADMAP; the twenty-name long tail across nine repos is
   each repo's own, as are the completed-milestone corpses still sitting in `flows` and `aiwbot`.
   [`entropy.md`](entropy.md) keeps counting all of it, so nothing goes dark.

   **The lesson that generalises, from draining the six `HISTORY.md`: delete the generator before
   the artefact, or the name grows back.** Four ROADMAP headers were *instructing every future
   session* to write one. And rejected-approach content is the single thing git cannot hold — save
   it to `ROADMAP.md § Rejected` before the file goes.
   → **model: sonnet**.
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
   move), and `code/isoroll-module/REFACTOR.md` → `ROADMAP-refactor.md`, which is that repo's own
   commit. `code/dobra/DECISIONS.md` is not a roadmap at all — decisions are *what must be true and
   why*, so it folds into that project's `SPECS.md`, also in that repo.

   **Sweep the file's own content, not just the references to it.** A file that was gitignored has
   been exempt from every check the workspace runs, so a rename of one is a first import, not a
   move — expect it to arrive carrying tokens the rest of the corpus retired months ago.
   → **model: sonnet**, one file per commit.

---

## Front 14 — ablation: nothing in this workspace has ever been measured

> **The paper twin is [`academy/papers/wos-ablation/`](academy/papers/wos-ablation/CONTEXT.md)**
> (2026-08-16). Lucas: *"o WOS pode virar um artigo. o estudo de ablação, se bem feito, me parece
> bem publicável."* The ablation and the paper are one artifact, so the experimental design lives
> there and this front holds only the build work it depends on.

1. 🟡 **build the instrument, then run the ablation.** Lucas, INBOX 2026-08-15: *"um engenheiro
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
   Front 10.4 is not a sibling of this item, it is its instrument — *"it also would ease ablation
   tests so we can indeed see the impacts of each option"* (Lucas, 2026-08-14). Building the bench
   before the switch repeats the failure.

   **Named for measurement by Lucas (INBOX 2026-08-16), and the list is the scope:** *"incluir na
   nossa medição do estudo de ablação as funcionalidades da fachada, das interfaces, do limite de
   LOC, limite de arquivos, enfim, fazer o planejamento desse estudo com bastante calma."* Facade
   discipline, interface-first reads, the 150/200-line cap and the 7/10-file fanout cap — the four
   restraint gates nobody has ever measured, each of which shapes how every file in this workspace
   is written. *"com bastante calma"* is a constraint on the study, not a mood: these are the
   workspace's most load-bearing rules, so a weak design produces a number that gets quoted forever.

   Scope is the whole enforcement layer, not the `.md` corpus: hooks, skills, tools, `AGENTS.md`
   itself. The corpus drain is downstream — its verdicts are judgement calls today precisely because this
   instrument does not exist, and it says so rather than implying they are measured.
   → **model: opus** for the design, sonnet to run it.

---

## Front 15 — the agent is confidently wrong, and nothing catches it

Lucas, INBOX 2026-08-16: *"vi um comentário sobre o OPUS ter MUITA SEGURANÇA sobre pontos que na
verdade ele estava errado… eu gostaria que todas as opiniões técnicas da IA fossem tomadas com base
em pesquisas."* His two proposals: a **knowledge base** — a curated store, cheap to look up, refreshed
when a stored fact is old enough to have moved — and an **instruction**: *"YOU DON'T KNOW THINGS,
don't feel too certain, search before giving precise technical opinions."*

**This workspace has the case study, and it is not hypothetical.** Front 9 was steered for three
weeks by a confident, re-runnable, wrong number. The instrument agreed with the script it replaced,
which read as confirmation and was not, because both shared one misunderstanding. Before that, four
consecutive explanations of the rtk hook were asserted and retracted. In neither case was the agent
short of information; it was short of the habit of checking.

**What that case study says about the two proposals, and it cuts against the easy one.** The
instruction is the cheap half and is the half already tried: the workspace is thick with
*re-run it, never quote it* prose, and it did not prevent either failure. Prose asking for doubt is
INDUCED, and this repo's whole bet is that INDUCED loses to ENFORCED. So the front's real question
is **what a confidence check looks like as a gate**, not as a paragraph.

Three sub-questions, in the order they can be answered:

1. 🔴 **What is the store, and what earns a row?** The wikilinked memory store
   ([`brain/memory/`](brain/memory/CONTEXT.md)) and `core/refs/REFS.md` already exist and already
   hold curated facts — a third store is the failure
   this workspace names EDIT > CREATE. Establish first whether the graph Lucas wants is a **new
   structure** or a **query layer and a freshness field** over what is there. → **model: opus**,
   with Lucas.
2. 🟡 **What makes a stored fact go stale?** A hash-addressed store is only as good as its refresh
   rule; a confidently-served 2026-07 fact is the same failure with extra steps. Every fact needs a
   measured-on date and a claim about how fast its subject moves — harness behaviour ages in weeks,
   a published result in years. → **model: sonnet**.
3. 🟡 **Where can doubt be enforced rather than requested?** The one mechanism proven here is the
   experiments ledger: a number is not quotable until it has a runnable Method
   ([`core/experiments/SPECS.md`](core/experiments/SPECS.md)), and its new corollary — *a new
   instrument owes one hand-check against raw data before anything is quoted from it*. Extending
   that discipline beyond numbers to technical claims is the concrete, non-prose version of what
   Lucas asked for. → **model: opus**.

**Do not open this with a prompt rule.** That is the cheapest-looking move and the one the evidence
above already rejects.

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

## Front 16 — post-v1, and the ledger is open again on purpose

**Ruled 2026-08-16 (Lucas), after all four v1 criteria went green.** The governing constraint
(*"quero zerar o roadmap do WOS o quanto antes"*) was a filter for reaching v1, not a permanent ban:
asked where three real ideas should land, he chose to **reopen this ledger** rather than push them
into `core/ROADMAP.md` or leave them in the INBOX. So v1 is a milestone, not a stopping point —
**but the filter that got us here still applies to what enters**: an item another repo owns is
refiled there, and a finding worth keeping goes into the `SPECS.md` section that owns the rule.

1. 🟡 **adversarial review as a standard, possibly enforced.** Lucas, INBOX 2026-08-16: *"have
   adversarials as our standards, maybe enforced… e.g., a plan that doesn't have any adversarial
   steps is rejected"*. The natural home is the craft flow's plan step
   ([`core/flows/craft/`](core/flows/craft/CONTEXT.md)), which already has a plan-review stage — so
   the question is whether that stage becomes a *requirement with a shape a check can see*, the way
   the citation gate matches `Frente <n>` rather than a word.

   **Design against the failure the source itself names**: the practitioner who proposed this says
   the technique *"can be a death loop"*. A gate that demands an adversarial step, on a plan whose
   adversary always finds something, is a loop with no exit. Whatever ships needs a termination
   rule before it needs a check. Refs and the two unread method docs: `core/refs/REFS.md`
   § Adversarial review as a standard.
   → **model: opus** for the shape, sonnet to wire it.
2. 🟡 **measure which `UPPERCASE.md` files are actually read, and what they cost.** Lucas, INBOX
   2026-08-16: *"sinto que arquivos de objetivos (goals) são pouco usados. roadmaps são muito
   usados. gostaria de primeiro ter esse monitoramento de forma automática (zero-token) de quais
   arquivos UPPERCASE.md são lidos e com que frequência (e se possível o custo em tokens de leitura
   deles). tudo isso monitorado no tempo."*

   **Ordering is explicit and it is the whole point: measure first, then act.** He suspects goal
   files are dead weight; this measures it instead of assuming it. The instrument is close to
   existing — [`core/tools/wos/session/context`](core/tools/wos/session/context) already attributes
   context growth per file from the transcripts, so this is mostly a longitudinal store plus a
   per-type rollup, not a new measurement. Results belong in
   [`core/experiments/`](core/experiments/CONTEXT.md), never in this file.
   → **model: sonnet**.
3. 🟡 **then reinforce the goal↔roadmap link, possibly enforced.** Same capture, and deliberately
   second: *"depois gostaria de reforçar a conexão entre os goals e os roadmaps, não sei se tem
   como, talvez até algo ENFORCED"*. Every goal file already carries an `>**owns**` block and every
   plan is supposed to live in a `ROADMAP.md`; what is missing is anything asserting the two agree.
   **Do not design this before item 2 reports** — if goal files turn out to be read rarely, the fix
   is not a stronger link to them.
   → **model: sonnet**.
4. 🟡 **evaluate `obra/Superpowers` against our own craft flow.** Lucas, INBOX 2026-08-16: *"será
   que eu deveria usar o superpowers?"* It is the same shape as `/craft` — spec from an interview,
   plan written for a junior engineer, subagent-driven TDD — and it installs across 14 harnesses,
   so it is provider-agnostic the way we are. **The question is not whether it is good, it is
   whether it is better than the flow we already run**, and the answer has to name what it does
   that `core/flows/craft/` does not. A real outcome here is deleting our own flow.
   → **model: opus** — this is a judgement about our own work.
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

- **INBOX provenance probe** — Front 1 shipped; the probe measures a threat model already ruled inert.
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
- **`/caveman compress` on workspace docs** — piloted on the worst offender: 8571 → 8552 chars, **0.22%**, for one full quota call. The docs have no lexical fat, so placement beats phrasing and compression stays the last step on an already-reduced surface (core/SCHEMA.md § Placement).
- **A media-host allowlist for INBOX link extraction** — deciding which links the video tool runs from a list of known hosts (instagram/youtube/tiktok/…) is faster, and the list rots into exactly the silent skip the batch fix exists to kill. Every link is attempted; one with no media falls back to `core/tools/web/fetch`.
- **The ~8% unexplained spend gap between `usage` and the one-off script** — the premise is void. Both summed transcript records instead of API responses, so they agreed on shares while being 1.97x wrong together, and the agreement is what stopped anyone looking. Absolute spend is list price and has never been checked against a bill; that is the only caveat left.

## Sequencing

**All four v1 criteria are met as of 2026-08-16.** What remains in Front 10 is past v1, and the
governing constraint in [`brain/goals/workspace-os.md`](brain/goals/workspace-os.md) applies at full
force to it: an item that does not earn its keep is a candidate for *Rejected*, not the backlog.

**14.1 is no longer waiting on an instrument — it waits on a backlog.** The registry exists; what
it reports is that 60 of 62 capabilities still cannot be switched off, and that list is what an
ablation has to eat through. Read it from `core/tools/wos/features --findings`, never from here.

1. **wire the registry's findings** — the mechanical follow-on, one feature per commit: call
   `feature_law.is_enabled()` where the rule is enforced, then name that file in the `wired`
   column. **Front 14 cannot report on a feature whose row still reads `-`**, so this is the
   ablation's real precondition and the count lives in the tool, never copied here.

   **Wire the four features 14.1 names before anything cheaper** (ruled 2026-08-17, Lucas). Facade
   discipline, interface-first reads, the LOC cap and the fanout cap are the ablation's declared
   scope, so wiring them is what makes a first run produce signal at all. Ordering the backlog by
   *files touched per feature* instead maximises rows closed per hour and leaves the study with
   nothing to measure — it had put two of the four last and one nowhere. **Cheapest-first is the
   right order only among features the study does not name.**
2. **10.5** — the public scaffold repo at `code/wos/` and its one-way sync. The allowlist is the
   deliverable, and `core/profile.txt` is the one file it replaces with a placeholder.
3. **14.1** — the ablation, against whatever is switchable by then.

Alongside, in any order, all mechanical:

- **11.2** the branch-drift warning and **11.1** the unmerged-branch signal — both cheap, both
  measure something currently invisible.
- **4.2** the `.loop/` → `.craft/` state-dir rename, all that survives of the July `loops`→`flows`
  sweep now that the skill half has landed; its token joins `core/SCHEMA.md` § Retired tokens the
  day it does, not before.
- **a registry slug and the file it governs carry the same name** (Lucas, 2026-08-17) — the rule
  now holds for every skill row, and `core/SCHEMA.md` § Retired tokens carries the guard.
- **12.1** the `SPEC.md`→`SPECS.md` migration — one reviewed change across five enforcement points.
- **4.6** the first-line-comment gate, **4.8** the `python_api` walk, **8.2**, **8.3**, **9.6**.

**Needing Lucas: the list is in § How to read this and only there.** It used to be restated here,
and the two copies named different threes — each missing a different item, both claiming three.
**Two lists of the same set is the asymmetry; the count is the symptom**, so the cure is one list,
not two careful ones. 14.1 was the item they disagreed about and it is now 🟡: Lucas ruled
2026-08-16 that it needs no ruling, only its precondition.

## Model-switching guide

The canonical guide lives in the flow that produced this plan:
**[`core/flows/research/scout.md`](core/flows/research/scout.md) → "Canonical model-switching guide"**
(same-session `/model` · `/craft` autorouting · Agent-tool `model:` override · `/handoff`).
Mapping: 🔴 → **Opus, same session**; 🟢/🟡 → **Sonnet via `/craft`** (mechanical parts drop to haiku).
