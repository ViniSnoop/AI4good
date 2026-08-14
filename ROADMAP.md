# Workspace-OS Roadmap — the v1 push

> **Single entrypoint for all workspace-os (wos) build work.** Goal file
> [brain/goals/workspace-os.md](brain/goals/workspace-os.md) holds *why*; this file holds *what*.
> [brain/TODO.md](brain/TODO.md) holds life tasks only; [core/ROADMAP.md](core/ROADMAP.md) holds
> agent-library internals only. An item lives in exactly one of the four — a copy is a bug.
> Evidence: [core/refs/REFS.md](core/refs/REFS.md).
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

**One open step needs Lucas's own judgment: 10.3** — and even that is now mostly downstream of
10.4, because a feature-toggle registry *is* the Lucas-specific/general split made executable.
Everything else is Sonnet or Haiku. Stating that number is part of the cure for feeling lost, so
keep it true: the 2026-08-14 sprint took it from four to one by ruling 8.1, 11.1, 11.3, 12.3, the
transient-doc type, the `loops`→`craft` rename and the `core/tools` axis in a single sitting, and by
turning 3.1 from a decision into a measurement.

**Load-bearing principle: automatic + zero-token beats agent-checked, and free checks are never
coupled to paid ones.** Deterministic scripts per-commit; human judgment on demand.

> **Evidence caveat, once for the whole doc.** Some steps lean on two strong but *unreviewed*
> preprints — progressive disclosure ([P] 2607.17598) and ACE ([P] 2510.04618). Provisional; never a
> hard gate.

---

## Frente 3 — Memory and always-loaded context

1. 🟡 **measure-first — what is always-loaded about Lucas, and where does memory live?**
   `brain/USER.md` enters via the brain CONTEXT chain; `MEMORY.md` index enters every session.
   Lucas's suspicion: the auto-memory overlaps what `USER.md` + `goals/` + the CONTEXT chain +
   `refs/` already do. Decide the role of each (always-loaded vs durable vs on-demand) and whether
   the separate memory store justifies itself or should fold. **First act of this step is the
   measurement** — instrument what actually loads at session start and the real hop count to a leaf
   (this absorbs the old depth-audit step; it is one afternoon, not a project). Sub-question: do
   `context-gate.py` / `bash-context-gate.py` make a *subagent* reread the full CONTEXT.md chain on
   every subtree touch instead of once per session? If so a narrow subagent pays the full chain
   repeatedly.
   **Decided 2026-07-30:** `USER.md` survives as a type — it is the only file whose content is not
   derivable from anything else (goals say what Lucas wants, CONTEXT says what a subtree is,
   `USER.md` says *how he fails*), and it has global scope, so splitting it into CONTEXT.md files
   would duplicate it into every subtree. Trim its two non-profile intrusions: the dead pointer to
   `branches/writing/mantras.md` (does not exist) and the embedded wos TODO on line 40.

   **Confirmed 2026-08-14 (Lucas): measure before deciding — this is no longer a judgment call
   waiting on him, it is instrumentation waiting on someone.** The disposition of the memory store
   (fold it / keep it with a narrowed charter) is downstream of the measurement, and deciding it
   first would repeat exactly the mistake Frente 9 paid for: steering for weeks by a number nobody
   could re-run. Two things the instrument must report, because both are load-bearing and neither is
   currently observable: (a) what genuinely enters the context at session start, split by source, so
   the memory store's marginal cost is separable from the CONTEXT chain's; (b) whether a *subagent*
   re-pays the full chain on every subtree touch instead of once per session — if it does, narrow
   workers are quietly the most expensive thing we run.
   → **model: sonnet** to build the instrument, **opus** for the disposition it feeds.
2. 🟡 **the always-loaded corpus — measured 2026-07-30, disposition before compression.** Trigger
   was Lucas hitting Claude Code limits and suspecting `AGENTS.md`. The measurement says otherwise:
   `AGENTS.md` is 33 lines / **~1.3k tok**, while a *single* `context-gate` cascade in one session
   cost **~5k tok** (six CONTEXT.md to run two `head` commands). Cutting `AGENTS.md` optimises the
   wrong thing. Across all **171** `CONTEXT.md`:

   | Block | Total | Verdict |
   |---|---|---|
   | curated head (rules, cues) | 44.3k tok | the content — keep, but see MOVE OUT |
   | generated **Subdirectory** table (navigation) | **5.7k tok** (avg 34/file) | keep — cheap, and it *is* the useful routing |
   | generated **File** table (per-file symbol dump) | **55.8k tok** | ~~the whole problem~~ — see below |

   ✅ **SETTLED 2026-07-30 with Lucas. The corpus framing above was wrong and is retired.** 55.8k is
   a sum nobody pays: no session reads the corpus, it reads a *chain*. Measured over all 159 chains:
   **2126 tok median, of which the File table is 457 (22%)** — about one `AGENTS.md`, cached. Not a
   tax; a tail. Only 10 chains exceed 5k.

   And the tail is row **count**, not row width (median 7 rows, worst 51 — width is a flat 40 tok/row).
   Which makes it a *code organisation* problem wearing a context-cost disguise: `code/aiwbot/tests/`
   is 51 flat test files. **The rule already existed** — `workspace_scanner.SPLIT_THRESHOLD = 7`,
   warned by `context_synchronizer.sync` — but it printed to stdout during a sync nobody reads.

   Landed, in order of evidence: **(a)** the fanout signal promoted to Tier 0 (`entropy_fanout.py`,
   dashboard section, 8 tests incl. a ratchet) — surfaces **35 pre-existing** over-full directories,
   which is why the dashboard total rose to 108 rather than a regression; **(b)** a generated column
   empty on every row is no longer emitted (773 of 1242 rows carried an em-dash `Interface`);
   **(c)** `test_*` symbols dropped from the `API` column, keyed on the **symbol not the path** so
   there is no `tests/`-shaped door for production code to dodge the facade gate through — guarded by
   `test_a_production_symbol_in_a_test_directory_still_appears`. Rules + the depth/fanout
   reconciliation are in `core/SCHEMA.md` § Routing depth and locality; the research verdict table is
   in `core/refs/REFS.md` § What this evidence actually settles for us.

   **Read-gate change: dropped, correctly.** Lucas rejected stopping the gate at `| File |` and he was
   right — the table is cheap per chain and its `Description` column is curated at source (6% noise).
   New `[P]` evidence cuts both ways and is now filed: Gloaguen et al. (ETH) found repository overviews
   unhelpful and >20% costlier, but the harm concentrates in *LLM-generated* files while *curated* ones
   help. Nobody has A/B'd our tables on our tasks; probe-and-refine is the method if it ever matters.

   Still open from the original framing: `context-gate` forces the full CONTEXT.md chain before any
   file access while `SPECS.md` is on-demand, so **every constraint written into a CONTEXT.md head is
   paid by every session in that subtree** — that is the MOVE OUT bucket below, and it is about the
   41.9k tok *head*, which the evidence says is the half that actually earns its keep.

   Four buckets, in payoff order. **Compression is the LAST step** (Lucas, 2026-07-30) — assess
   what to remove, move, and transform first.
   - **REMOVE** — ~~stop the gate at `| File |`~~ **rejected, see above.** Still live here:
     **43** CONTEXT.md carry `← add` placeholders — Frente 12.2 matched only
     `← add description` and missed the `← add first-line comment` class entirely, so the real count
     was never 23. Also `code/CONTEXT.md:28` says *"See SPECS.md for the full table"* and inlines
     all of R1–R6 anyway.
   - **MOVE OUT** — constraints from CONTEXT.md → SPECS.md. **40** heads exceed 400 tok; **33 of
     those have no sibling SPECS.md.** Two done as the pilot, and they establish the recipe:
     `academy/papers` **1702→456 tok** (−73%, 1259 tok of constraint moved to a new `SPECS.md`) and
     `code` **658→482** (the R1–R6 table was inlined directly under a pointer that said "see
     SPECS.md for the full table"). **The recipe, in order:** (1) delete what a hook enforces — it
     names the fix when it fires, except numbers that change how you write *before* the hook can
     speak (the 150/200 line caps stay); (2) move constraints to `SPECS.md`, creating it if absent;
     (3) move data out (alias lists, schemas); (4) delete stale claims; (5) keep identity +
     navigation. Every pass so far has also surfaced a dead pointer or a false claim in the file it
     touched, so budget for that. Next by size: `.opencode` (1650),
     `code/apptime` (1635, and 4 placeholders), `code/isoroll-module/src/transform` (1353, 5
     placeholders), `core/skills/caveman` (1328), `code/flows/libraries/tools` (1184).
   - **TRANSFORM** — the 14 retypings under Frente 12 (four disposal routes), plus the **15**
     CONTEXT.md whose *head* hand-lists files (`TREE`/`PATHS`/`TBL` signals), duplicating the
     generated block they sit above: `code/isoroll-content` (ASCII tree *and* File Map),
     `academy/papers` (`## Project Layout` tree), `brain/CONTEXT.md:9-14`.
   - **KEEP** — curated cues and the Subdirectory table. Untouched.

   Rejected here, with evidence: **`/caveman compress` on workspace docs.** Piloted on the worst
   offender — 8571→8552 chars = **19 chars, 0.22%**, in 43s and one model call (no
   `ANTHROPIC_API_KEY`, so it falls back to `claude --print` and spends *the same quota*). Six
   trivial word swaps. Extrapolated: ~2h and 171 quota calls for ~0.3%. The docs are already
   caveman-dense; there is no lexical fat. Reverted.
   → **model: sonnet** for the sweeps.

3. ✅ **CLOSED 2026-07-31 — the trim shipped and the nested repos are resynced.** All 24 nested
   repos regenerated and pushed to their default branch. The corpus barely moved (54.9k → 53.9k)
   because this same session *added* 7 CONTEXT.md by splitting `pre-commit` and `sync-skills` — but
   the tail, which was the actual problem, collapsed: `code/aiwbot/tests` **4604 → 2048 tok
   (−56%)**, `code/isoroll-content/test` **2507 → 1189 (−53%)**, `code/spacemantics/tests`
   829 → 498. Median chain 2126 → 2075 tok, File-table share still 22%.

   **What this cost, recorded because the estimate was wrong.** The plan called it a mechanical
   resync. It surfaced the root defect below (Frente 4.4) and three live bugs: the gitignore
   allowlist silently dropped new files in a moved directory, `pre-edit.py` counted lines one
   higher than every other counter, and `entropy_corpus.ENFORCEMENT` spelled out a sibling path
   that stopped exempting the retired-token checker the moment the hooks moved.
4. 🟡 **test the six "inverted practices" against our own instructions.** Claim, from a practitioner post
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
0. ✅ **criterion 1 rescoped 2026-08-14 (Lucas) — the DoD now says what the tests always said.**
   Measured: of the **90** distinct paths the dashboard reports, **81 live in nested repos and 9 in
   this one** — and those 9 carry **zero** BLOCK-level violations (5 are doc size *signals*:
   `ROADMAP.md` 735, `SETUP.md` 624, `core/SCHEMA.md` 363, `core/flows/craft/craft.md` 382, a prog-1
   slide deck 635; 3 are fanout at exactly 10 files, which `limits.env` calls a warn on purpose;
   1 is `code/_templates/module.SPEC.md`, blocked behind job B's single reviewed SPEC migration).
   So "dashboard reads clean" held v1 hostage to 24 repos this one cannot fix — including
   `isoroll-*`, owned by a parallel session. **Criterion 1 is now: this repo clean, plus a
   per-repo baseline that may only shrink.** The ratchet already exists (`BASELINE` in
   `test_entropy_naming.py` and `test_entropy_fanout.py`); nothing new is built for this. The
   workspace-wide drain does not disappear — it becomes per-repo work, gating `[mvp-validate]`
   rather than v1. **The lesson: a criterion whose scope is wider than its test's scope is a
   criterion nobody can close.**
3. 🟢 **the entropy dashboard — live.** `make entropy` → [`entropy.md`](entropy.md), 1904 tracked
   files across the workspace **and its 24 nested repos**, ~1.3 s. Read the report; never re-scan
   the tree. **Never copy its counts into this file** — a copied number is the drift these checks
   exist to catch; the summary table at the top of the report is the interface. Criterion 1 wants
   it reading clean; the remaining work is draining it.

   The dashboard scans nested repos, the **tests do not** — an assertion in this repo about
   another repo's content fails for reasons this repo cannot fix, and each nested repo runs its
   own verify. Where a check is green workspace-wide it is asserted at zero in `verify-fast`
   (retired tokens, duplicate slugs); where it is not, `test_entropy_naming.py` holds a named
   **baseline** so a new violation fails the build and a fixed one must leave the list.

4. ✅ **the file law — one definition of "a code file", shipped 2026-07-31.** It was defined **five**
   times (`check-line-counts.sh`, `entropy-dashboard.py`, `workspace_meta.py`, `pre-edit.py`,
   `facade-gate.py`) and no two agreed. `.sh` and extensionless executables were invisible to the
   **blocking** gate, which is how `pre-commit` reached 385 lines and `sync-skills` 341 unopposed —
   *not* a `--no-verify` bypass, as this file previously claimed. Now
   [`core/hooks/file_law.py`](core/hooks/file_law.py), the numeric-law sibling of `schema_law.py`,
   with `limits.env` holding all four numbers and `vendored.txt` / `extensionless.txt` as named
   exception lists. Guarded by `test_no_checker_carries_its_own_extension_list`.

   Hooks moved `.hooks/` → [`core/hooks/`](core/hooks/CONTEXT.md) the same day: nothing about the
   location was Claude-specific, and hidden meant unmonitored by its own checks.

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
   → **model: sonnet**. Plan: `~/.claude/plans/plan-a-fix-on-scalable-star.md`.

---

## Frente 9 — Cost & model routing

**Why — re-measured 2026-08-13, and the old numbers were wrong.** The previous framing came from a
single 24 h window. Re-run it yourself — that is the point of
[`core/tools/wos/usage`](core/tools/wos/usage), built this session so no claim here rests on a
number nobody can reproduce. Over **118 sessions · 18,122 turns · 2026-07-25 → 08-13**:

> **Trust the ratios, not the dollar total.** A one-off script and the tool agreed on every share
> and per-turn cost but differed ~8% on absolute spend (mostly the `fable` line), and that is not
> yet explained. Quote percentages and $/turn from the tool; treat any absolute total as ±10%.

| Claim | Verdict |
|---|---|
| "59% of usage from subagent-heavy sessions" | **False, and retired.** **Zero** sidechain messages and **zero** `Task` calls across all **328** transcripts. No subagent has run in five weeks. |
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

**Shipped 2026-08-13/14 — both halves of the session transition.** The size signal is
[`core/hooks/session/context-meter.py`](core/hooks/session/context-meter.py) on `UserPromptSubmit`:
it reads the size the API already reported and announces `CTX_WARN` / `CTX_LOUD` once each, costing
zero tokens until crossed and never blocking. The session cannot see its own size, which is why the
hand-off decision was always made late — a hook is the only thing that can see it *and* speak at the
moment it applies. The close itself is [`core/tools/wos/roundup`](core/tools/wos/roundup) plus the
two skills; every decision behind that split, and why no session spawns its own successor, is
[`core/SPECS.md`](core/SPECS.md) § AD-09, guarded by 20 tests in
[`core/tools/test/wos/`](core/tools/test/wos/CONTEXT.md).

**The lesson this frente cost the most to learn: a number nobody can re-run steers the work anyway.**
It was aimed for weeks by a single 24 h window that turned out wrong in every claim — "59% from
subagent-heavy sessions" was retired outright (zero sidechain messages across 328 transcripts), and
the thresholds first shipped at 150k/250k, which fired *halfway up* the climb and *after* the
plateau began. So: a number in this file that
[`core/tools/wos/usage`](core/tools/wos/usage) cannot reproduce should be **deleted, not softened**.

1. 🟢 **safe — cheaper models where the work is mechanical.** Measured split: opus 68%, fable 24%,
   sonnet 7.8%, haiku ~0%. Worth doing, but note the ceiling — routing cannot beat a 3x context
   multiplier, and the transition above already took the larger win.
   → **model: sonnet**.
2. 🟡 **the ~8% spend gap is still unexplained**, four sessions running. A one-off script and
   [`core/tools/wos/usage`](core/tools/wos/usage) agree on every share and per-turn cost but differ
   on absolute total, almost all of it in the `claude-fable-5` line. Quote percentages and $/turn;
   treat any absolute total as ±10% until this closes. By the rule above, if it cannot be resolved
   the absolute numbers should be dropped from the tool's output rather than footnoted.
   → **model: sonnet**.

---

## Frente 10 — Portability & clonability — **v1 criterion 4**

1. 🟢 **safe — SETUP audit + split.** Two axes: **coverage** (features / skills / hooks / flows /
   brain all present) and **accuracy** (a newcomer gets plug-and-play on every capability).
   **Decided 2026-07-30: `SETUP.md` dies as a type.** It is two things wearing one name — install
   steps, which should be an *executable installer* (criterion 4 is clonability, and a script is
   testable where prose is not), and capability prose, which is `README.md`. Split by access
   pattern, the technique proven in the `craft.md` decomposition. Retires the third naming shape
   `core/tools/video/SETUP.md`.
   → **model: sonnet**.
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
   → **model: sonnet** to build, **opus** for the question set and the registry shape.

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
   milestones kept as `Status: complete` bodies and `~~strikethrough~~` — annotated corpses that
   the same rule says to cut. Left for job D's pass over those repos, not smuggled into A.
2. 🟢 **safe — one or two refinement passes over the surviving docs.** Crop dead parts, collapse
   overlaps, compress the prose (caveman-compress the writing style, keep every technical fact).
   Requested by Lucas 2026-07-30, after the type system lands so the passes are not wasted on files
   about to be deleted.
   → **model: sonnet**.
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

## Batch B — live bugs, ready to execute (Sonnet, `/loops`)

One test each. Nothing here needs a decision.

1. `core/hooks/routing/context_synchronizer.py`, three bugs: (a) hoisting a child CONTEXT.md's line-2 description
   copies relative links verbatim into the parent's routing row, where they resolve one level up —
   live in `branches/casinhas/CONTEXT.md` and `code/{apptime,dobra,isoroll-content}/CONTEXT.md`;
   (b) stale rows survive file deletion (block only updates on save) — live in
   `core/prompts/CONTEXT.md`; (c) it appends a **duplicate** routing block to a hand-curated
   CONTEXT.md that has a manual `## Routing` without sentinels; (d) a description **prefix accumulates**
   across regenerations instead of replacing — live in `core/skills/caveman/scripts/CONTEXT.md:27`, where
   `__init__.py`'s description reads `**facade** — ` repeated **22 times** before the placeholder.
2. `core/tools/video/video`: `--level full` crashes on image-only posts — `assemble()` always calls
   `media().transcribe(audio)` when the audio path is truthy, but an image post has no audio stream →
   `IndexError: tuple index out of range` inside `faster_whisper`/`av`. Workaround: `--level visual`.
   ⚠ **May already be fixed** — `--level full` on an image-only carousel (`instagram.com/p/DbBJSzvnP3J`)
   ran clean through OCR + VLM captions on 2026-08-13. Reproduce before spending a loop on it.
3. `pre-edit.py` fails **silently** ("No stderr output") on some paths — blocks the edit without naming
   the fix, costing a round of investigation each time. Two shapes seen: `Write` of new files (scratchpad
   `.html`, a new `test/*.py` under `isoroll-content`), and **`Edit` of an existing file**
   (`code/isoroll-content/src/pipeline/kit_modules.py`, 2026-08-01). Running the hook by hand with a
   payload that busts the size gate prints the right message, so at least one rejection path exits
   non-zero mute. Workaround is a Bash heredoc. Probably an unhandled exception on an unexpected path.
4. **`stubgen` misses projects** — `.py`/`.ts` files created outside Edit/Write never get their stub
   staged. Blast radius measured 2026-07-29: **122 unstaged stubs across 7 repos**, and since the
   read-gate blocks reading source when the interface is current, a missing stub breaks a fresh
   clone. Needs a pre-commit sweep, not an edit-time hook.
5. `core/hooks/brain/brain_stats.py` `compress_done()` writes `new_inner` without a trailing newline, so the
   surviving last entry is glued to the `<!-- done:end -->` marker. Same function leaves
   `brain/.log/done.md` unstaged after appending — the archive lands but the commit does not carry it.
6. `.opencode/plugins/jsconfig.json` is self-defeating: `include: ["*.js"]` with
   `exclude: ["/mnt/workspace/.opencode/plugins"]` excludes its own directory, so every commit prints
   `error TS18003: No inputs were found` and no `.d.ts` is generated. Found 2026-07-30.

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
- **Evaluate Surfsense** — our `core/tools/{search,papers,fetch,parse}` + research flow already cover it.
- **Research-flow hallucination audit** — real but unforced; no observed fabrication.
- **`pre-edit.py` vs `check-line-counts.sh` scope disagreement** — policy nit, no live symptom.
- **`core/tools/paper/papers --ss` live smoke** — it will smoke itself on the next real use.
- **Commit the `.claude/commands/{drive,calendar}.md` symlinks** — done inline rather than tracked.

## Sequencing

1. **Frente 12.1** — apply the type system + write it into `core/SCHEMA.md`. Do it before 4.1 so
   Tier 0 enforces a vocabulary that is already true, and before 12.2 so the refinement passes are
   not spent on files about to be deleted.
2. **Drain `entropy.md`** — the keystone is built; criterion 1 is now a drain, not a design. Biggest
   families first: 41 off-allowlist types (this *is* Frente 12.1) and 29 size signals.
3. **Frente 4.2** — the `loops`→`flows` generator rename. Its retired tokens are now declared in
   `core/SCHEMA.md` § Retired tokens, so the sweep has an assertion waiting for it: add
   `.loop`/`loops` to that table the moment the rename lands and the check proves it complete.
4. **Frente 10** (1, 2) — SETUP split + declared deps.
5. **Batch B** — parallel-safe, cheap.
6. **Frente 12.2** — the refinement/compression passes.
7. **Frente 11.1** — the four sweep rulings, whenever Lucas has direction.
8. **Frente 3.1, 8.1, 9.1, 10.3** — the four judgment calls, in whatever order has wind.

## Model-switching guide

The canonical guide lives in the flow that produced this plan:
**[`core/flows/research/scout.md`](core/flows/research/scout.md) → "Canonical model-switching guide"**
(same-session `/model` · `/loops` autorouting · Agent-tool `model:` override · `/handoff`).
Mapping: 🔴 → **Opus, same session**; 🟢/🟡 → **Sonnet via `/loops`** (mechanical parts drop to haiku).
