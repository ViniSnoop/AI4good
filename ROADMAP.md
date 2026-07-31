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
| 1 | **verify-fast green + Tier 0 live** — naming, placement, pointer integrity, size-as-signal deterministic; entropy dashboard reads clean | Frente 4 | checks live · **read [`entropy.md`](entropy.md) for the count, never a copy of it** |
| 2 | **One ledger, no duplicates** — this file is the sole wos ledger, verified by scan not eyeball | Frente 8 | ✅ **MET 2026-07-30** — `test_no_item_lives_in_two_ledgers` |
| 3 | **Everything pushed, gitflow-shaped** — every `code/` repo on `main`/`feature/*`, zero unpushed, no repo without a remote | Frente 11 | 🟡 **one repo short** — audited 2026-07-31, see below |
| 4 | **Clonable by a student** — fresh clone gets every capability; deps declared, no undocumented hand-installs | Frente 10 | open |

Post-v1 validation is `[mvp-validate]`: use the system daily for 30 days, then assess whether it
reduced mental load. That is the real test and it can only run after v1.

## How to read this

Per-step `model` = the tier that is *enough* (a floor, not a ceiling).
🔴 needs Lucas · 🟡 pilot on one subtree first · 🟢 mechanical.

**Only four open steps need Lucas's own judgment: 3.1, 8.1, 9.1, 10.3.** Everything else is Sonnet
or Haiku. Stating that number is part of the cure for feeling lost.

**Load-bearing principle: automatic + zero-token beats agent-checked, and free checks are never
coupled to paid ones.** Deterministic scripts per-commit; human judgment on demand.

> **Evidence caveat, once for the whole doc.** Some steps lean on two strong but *unreviewed*
> preprints — progressive disclosure ([P] 2607.17598) and ACE ([P] 2510.04618). Provisional; never a
> hard gate.

---

## Frente 3 — Memory and always-loaded context

1. 🔴 **decide-first — what is always-loaded about Lucas, and where does memory live?**
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
   → **model: opus**.
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
   grandfathering). The flip is coherent only at zero — switching it on today fails every commit in
   eight repos, including the commits that would fix it. Live lists in `entropy.md`; when both read
   Clean, add fanout to `core/hooks/gates/` beside the type gate and delete `BASELINE` from
   `test_entropy_fanout.py` in the same commit.
   - **files over `BLOCK_LINES`** — `post-edit.sh` (208) and `s3_batch.sh` (209) are one small split
     each; the rest are `code/flows/engine/ui/src/*.jsx`, which is a React refactor, not a sweep.
   - **directories over `BLOCK_FILES`** — worst first: `isoroll-content/src/pipeline` (55),
     `aiwbot/tests` (51 — natural split `bugs/ features/ unit/`), `core/hooks` (49, halved by its
     own split already), `aiwbot/frontend` (38), `core/tools` (37).
   → **model: sonnet**, one repo at a time.

---

## Frente 8 — The ledger discipline — **v1 criterion 2**

Collapsed 2026-07-29 (four ledgers → one) and cut 2026-07-30 (52 open steps → 17). The collapse made
the ledger honest but not smaller — items went 158 → 123 while mass stayed flat, and Lucas reported
feeling lost twice. **Mass is the disease and only deletion cures it.**

1. 🔴 **decide-first — TODO layer redesign.** Reported twice, unprompted: *"sinto que o TODO.md
   simplesmente não tá sendo usado"*, and the evidence is that Lucas writes tasks into the INBOX
   instead. Two questions, one design: (a) **what would make it actually get checked daily** —
   accountability without the anxious tone the workspace exists to avoid (see
   [brain/SPECS.md](brain/SPECS.md) § Rationale); (b) **TODO × goals boundary**. Wanted: mutable,
   self-archiving, per-task recommended tier + creation date so stalled tasks flag themselves.
   → **model: opus** (design) · then sonnet to build.
2. 🟢 **safe — `/inbox` refreshes the goals dashboard.** Run `brain_stats.py` as `/inbox`'s last
   step, not only on commit, so the dashboard never goes stale between commits.
   → **model: haiku**.

---

## Frente 9 — Cost & model routing

**Why.** Measured over 24 h: 59% of usage from subagent-heavy sessions, 55% from >150k-context
sessions, 25% from `/roundup`. Context management is currently Lucas's job, which it should not be.

1. 🔴 **decide-first — `/roundup` redesign + automatic session transition.** `/roundup` costs ~7% of
   usage. With it: induce session switching by context size (frequent checkpoints, effective
   transition points), and investigate whether an agent can open a new session itself. Includes the
   session-size monitor (warn at ~40%/50% to evaluate handoff — 80% is too late and risks discarding
   work) and **context-drift detection** (plant a verifiable fact early, re-check periodically).
   Note the weak version: the "canary call-me-Lucas" trick is a confounded proxy (caveman suppresses
   it, self-reported) — keep it as a free passive tell, build no infrastructure on it.
   → **model: opus** (design) · sonnet to build.
2. 🟢 **safe — cheaper models where the work is mechanical.** Set model frontmatter on `/roundup` and
   craft-flow subagents for mechanical steps; re-measure after.
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

---

## Frente 11 — Git & sync integrity — **v1 criterion 3 — one repo short**

**Re-audited 2026-07-31 across all 25 repos** (the 2026-07-29 sweep covered 16 and the count has
grown). Result: zero unpushed anywhere, every branch `main`/`master`/`feature/*` — but **three repos
had no remote at all**, which the criterion forbids and the earlier sweep did not catch.

Two are now private GitHub remotes (`instituto`, `mechanism-search`), matching the convention
already used by the non-Overleaf papers. **`branches/casinhas` cannot be pushed as-is:**
`modelo/sketchup-referencia/volume-lucas-v04.skp` is **199 MB**, over GitHub's hard 100 MB limit, so
the push is rejected by a pre-receive hook. Three ways out, all Lucas's call because two rewrite
history: (a) **Git LFS** for `*.skp` — keeps the file, needs `git lfs migrate import`, still a
rewrite; (b) drop the binary from history and keep it local-only via `.gitignore`; (c) leave the
repo local and carve the criterion to exclude it deliberately. Until one is chosen, criterion 3 is
**not** met — recorded here rather than left as a green tick that is false.

*Original sweep, 2026-07-29:* 16/16 repos: zero unpushed, every branch `main`/`feature/*`, every
repo had a remote. 41 commits pushed across 8 repos; `cria` published (public, secret-scanned first); `loop/*`
renamed to `feature/*`, 5 stale ones deleted (ancestors of live branches, zero unique commits).
Dirty 215 → 93.

The "294 dirty files" was wrong twice: 215 real, and **122 of those were unstaged generated stubs,
not Lucas's work**. Near-miss worth keeping: the first read was that stubs are gitignorable debris.
Opposite — `SETUP.md:41` stages them and `SETUP.md:536` hard-blocks reading source while its
interface is current, so ignoring them breaks the read-gate on every fresh clone.

1. 🔴 **decide-first — four findings the sweep exposed.** Explanations pending Lucas's direction:
   - **`Makefile` untracked in 7 repos** (`apptime`, `shortvid`, `ppc`, `corpora`, `futebots`,
     `isometric-perspective`, `flows`). The verify entrypoint itself is not in the repo, so a fresh
     clone has no `make verify-fast` — a direct criterion-4 hole.
   - **`shortvid/shortvid/`** holds a *duplicated source tree* (`_crop_overlay.py`, `_effects.py`,
     `CONTEXT.md` — a whole second copy of the package one level deep) alongside the same filenames
     untracked at `shortvid/ui/`. Not stub debris. Untouched on purpose.
   - **`programacao1` has no repo of its own** — tracked inside the workspace structural repo,
     inverting the rule that internal projects use own repos. `brain/TODO.md:18-19` already holds the
     task to fix it. (`prog1`, its class-based predecessor, was deleted 2026-07-30.)
   - **Two repos verify RED on already-committed code**: `flows` (3 failures in
     `engine/tests/unit/test_ui_m10_client.py::TestHandleClient`) and `voti` (8
     `react/no-unescaped-entities` errors). Pushed anyway: the red predates the unpushed commits.
   → **Lucas decides** each · sonnet to execute.

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
> **A fourth type exists and must not be folded: the transient initiative doc.** `code/VERIFY.md`
> self-declares this lifecycle and names `REFACTOR.md` as its species; siblings are
> `code/SPEC-DRIVE.md`, `code/isoroll-module/REFACTOR.md`, `core/MIGRATION-STATUS.md`,
> `code/dobra/DECISIONS.md`. Folding `VERIFY.md` into a ROADMAP was **investigated 2026-07-30 and
> rejected as unsafe**: it has 24 inbound references, 7 of them in `core/hooks/*` source comments citing
> stable anchor IDs (`VERIFY.md W1/W2/I2/G1/G3/G7/A1`). It is a cross-project rollout with cited
> anchors and a defined death date — genuinely not a per-project ROADMAP. Open question for Lucas:
> the type is legitimate, but does it need a **name convention** (all five are named differently) and
> a rule that it must be deleted when its rollout completes?

---

## Batch B — live bugs, ready to execute (Sonnet, `/loops`)

One test each. Nothing here needs a decision.

1. `core/hooks/routing/context_synchronizer.py`, three bugs: (a) hoisting a child CONTEXT.md's line-2 description
   copies relative links verbatim into the parent's routing row, where they resolve one level up —
   live in `branches/casinhas/CONTEXT.md` and `code/{apptime,dobra,isoroll-content}/CONTEXT.md`;
   (b) stale rows survive file deletion (block only updates on save) — live in
   `core/prompts/CONTEXT.md`; (c) it appends a **duplicate** routing block to a hand-curated
   CONTEXT.md that has a manual `## Routing` without sentinels.
2. `core/tools/video/video`: `--level full` crashes on image-only posts — `assemble()` always calls
   `media().transcribe(audio)` when the audio path is truthy, but an image post has no audio stream →
   `IndexError: tuple index out of range` inside `faster_whisper`/`av`. Workaround: `--level visual`.
3. `pre-edit.py` fails **silently** ("No stderr output") on `Write` of new files in some paths
   (scratchpad `.html`, a new `test/*.py` under `isoroll-content`) — blocks the write without saying
   why; workaround is a Bash heredoc. Probably an unhandled exception on an unexpected path.
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
