# Workspace-OS Roadmap — the v1 push

> **Single entrypoint for all workspace-os (wos) build work.** Goal file
> [brain/goals/workspace-os.md](brain/goals/workspace-os.md) holds *why*; this file holds *what*.
> [brain/TODO.md](brain/TODO.md) holds life tasks only; [core/ROADMAP.md](core/ROADMAP.md) holds
> agent-library internals only. An item lives in exactly one of the four — a copy is a bug.
> Evidence: [core/refs/REFS.md](core/refs/REFS.md).
>
> **Deletion policy: hard delete. Git is the history.** No strikethrough, no annotated corpses. A
> killed item gets one line under *Rejected* so it does not resurface looking new.

## v1 definition of done

Four criteria. Nothing else gates v1.

| # | Criterion | Owner | State |
|---|-----------|-------|-------|
| 1 | **verify-fast green + Tier 0 live** — naming, placement, pointer integrity, size-as-signal deterministic; entropy dashboard reads clean | Frente 4 | open |
| 2 | **One ledger, no duplicates** — this file is the sole wos ledger, verified by scan not eyeball | Frente 8 | open |
| 3 | **Everything pushed, gitflow-shaped** — every `code/` repo on `main`/`feature/*`, zero unpushed, no repo without a remote | Frente 11 | ✅ **MET 2026-07-29** |
| 4 | **Clonable by a student** — fresh clone gets every capability; deps declared, no undocumented hand-installs | Frente 10 | open |

Post-v1 validation is `[mvp-validate]`: use the system daily for 30 days, then assess whether it
reduced mental load. That is the real test and it can only run after v1.

## How to read this

Each step carries the model tier that is *enough* — `haiku` (mechanical), `sonnet` (normal
engineering), `opus` (design, security, cross-cutting judgment). A floor, not a ceiling.
🔴 needs Lucas's sign-off · 🟡 prove on one subtree first · 🟢 mechanical or additive.

**Only four open steps need Lucas's own judgment: 3.1, 8.1, 9.1, 10.3.** Everything else is
Sonnet or Haiku. Stating that number is part of the cure for feeling lost.

**Load-bearing principle: automatic + zero-token beats agent-checked, and free checks are never
coupled to paid ones.** Deterministic scripts run per-commit; human judgment runs on demand.

> **Evidence caveat, once for the whole doc.** Some steps lean on two strong but *unreviewed*
> preprints — progressive disclosure ([P] 2607.17598) and ACE ([P] 2510.04618). Preprint =
> provisional. We never turn a preprint into a hard gate.

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

---

## Frente 4 — workspace anti-entropy — **the keystone, v1 criterion 1**

> The real target: files grow, scatter, duplicate, and drift from naming/structure patterns.
> **Structure is a spec; drift is a test failure.** `code/` already has this (the `> spec:` gate);
> the agent library has [core/SCHEMA.md](core/SCHEMA.md). Nothing yet governs the shape of the
> workspace itself.

1. 🟢 **Tier 0 — per-commit, zero-token, deterministic.** No LLM. Scripts in the pre-commit/verify
   path:
   - **uppercase type allowlist** (decided 2026-07-30, Lucas). `UPPERCASE.md` = a **type**, meaning
     the same thing in every subtree; `lowercase.md` = an **instance**, named freely. Uppercase
     names are therefore a **closed set**, and inventing a new type must be a deliberate act (one
     line added to the allowlist), never an accident. Evidence: 25 distinct uppercase names existed,
     15 of them appearing exactly once. Allowlist: `AGENTS · CONTEXT · README · ROADMAP · SPECS ·
     BUGS · REFS · SKILL · GOALS · TODO · INBOX · USER · SCHEMA`. Anything else blocks with "add it
     to the allowlist if you mean it."
   - **naming** — kebab-case, full words not truncations (the `architect`>`arch` rule made
     machine-checkable); lowercase top-level dirs; no spaces or accents in filenames (live
     violation: `academy/administration/coordenacao-lc/novo-ppc-bcc/Restrições Curriculares
     Atualizado.md`).
   - **retired-token assertion** — after a rename lands, assert the retired token appears nowhere.
     This is what makes 4.2's class of bug catchable instead of re-discovered.
   - **no hand-maintained file inventory in CONTEXT.md** — the routing block is generated and owns
     inventory. Live violations: `code/voti/CONTEXT.md` (79 hand-written lines re-listing all 20
     components) and `code/isoroll-content/CONTEXT.md` (a `Repository Shape` ASCII tree *and* a
     File Map *and* the routing block). This is the answer to "can CONTEXT.md files be smaller" —
     the problem was never size, it was three overlapping inventories of the same files.
   - **placement** — a file's location matches its declared type; includes `core/tools/*` Python
     files carrying no `.py` suffix — decide accept-or-standardize.
   - **project ⟺ goal link** — every project `CONTEXT.md` declares its goal on line 3.
     **Backfill first, then enforce** (warn → block).
   - **pointer integrity** — DONE. Open sub-decision: is an unresolved `[[slug]]` a *planned* memory
     (allowed) or a typo (error)? Needed before the checker can gate it.
   - **size as a *signal*, never a cap** — warn-for-delta-review when a curated doc crosses a
     threshold; **never force-summarize** (ACE brevity-bias trap). Also list tracked files above
     `BLOCK_LINES` with the commit that introduced them, since `--no-verify` bypasses leave no trace.
   - **duplicate-slug scan** — assert each bracketed item slug appears in exactly one ledger. This
     is what keeps criterion 2 true without vigilance.
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
3. 🟢 **the unifying artifact — an entropy dashboard.** One generated report written by the Tier-0
   checks: naming violations, oversized curated docs, dead pointers, misplaced files. Agents and
   Lucas read the **dashboard** (pre-computed, cheap), never re-scan the tree.
   → **model: sonnet** · **switch: `/loops`.**

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
   `core/tools/video.SETUP.md`.
   → **model: sonnet**.
2. 🟢 **safe — declare the ad-hoc venv deps.** Four known cases, each installed straight into `.venv`
   to unblock a tool, so a fresh clone silently loses the capability: `pypandoc-binary`
   (`core/tools/parse` on `.docx`), `secretstorage` (`core/tools/video` reading Brave cookies —
   without it yt-dlp fails with an AES-CBC decrypt error that reads like bad credentials; cost a
   session to diagnose), `gallery-dl` (`core/tools/video` carousel path), and **`flutter`** (found
   2026-07-29: `apptime`'s verify cannot run at all). Fix the **class**: a declared dep list the
   whole `core/tools/` surface is checked against.
   → **model: sonnet**.
3. 🔴 **decide-first — clonable for others (the students case).** Make the workspace genuinely
   plug-and-play for anyone who clones it: what is Lucas-specific, what is general, and how the two
   separate.
   → **model: opus**.

---

## Frente 11 — Git & sync integrity — **v1 criterion 3 — MET**

**Swept 2026-07-29.** 16/16 repos: zero unpushed, every branch `main` or `feature/*`, every repo has
a remote. 41 commits pushed across 8 repos; `cria` published (`lsfcin/cria`, public, secret-scanned
first); `loop/*` branches renamed to `feature/*` and 5 stale ones deleted (all ancestors of live
feature branches, zero unique commits). Dirty 215 → 93.

The "294 dirty files" figure was wrong twice over. Real count was 215, and **122 of those were
unstaged generated interface stubs, not Lucas's work**. The near-miss is worth recording: the first
read was that stubs are debris to gitignore. They are the opposite — `SETUP.md:41` stages them and
`SETUP.md:536` *hard-blocks reading a source file when its interface is current*, so ignoring them
breaks the read-gate on every fresh clone.

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
| `CONTEXT.md` | What is *this directory*, and where inside it do I go? | `TREE.md` |
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

1. [x] 🟢 **safe — apply the type system.** DONE 2026-07-30. Law written into
   [core/SCHEMA.md](core/SCHEMA.md) § The `.md` type system (13-name allowlist, the three boundary
   rules, No-archive-types, and the transient-initiative-doc exception). Deleted `brain/ARCHIVE.md`,
   `core/HISTORY.md`, `brain/.log/done.md`, `core/WATCHLIST.md`, `brain/FOUNDATIONS.md`. Folded
   WATCHLIST into `core/refs/REFS.md` as a `status: unjudged` section and FOUNDATIONS into
   `brain/SPECS.md` § Rationale. Renamed `brain/goals/ARCHETYPE.md` → `_template.md`.
   **Rewired the live wiring, which was the actual work:** `/roundup` Phase 2 no longer archives
   (it deletes, and writes one `## Rejected` line for a killed idea), `/compass` ditches to a
   `## Ditched` line in `brain/GOALS.md` instead of ARCHIVE, `.hooks/brain_stats.py` lost
   `append_done_log`, and `code/_templates/{ROADMAP,BUGS}.md` + `code/SPECS.md` + `core/ROADMAP.md`
   now state the delete policy. The `brain_stats` trailing-newline bug (ex-Batch B) was fixed in the
   same pass. Per-project `HISTORY.md` files remain in the nested repos — deleted per repo as each is
   next touched, since some carry a live parallel session.
2. 🟢 **safe — one or two refinement passes over the surviving docs.** Crop dead parts, collapse
   overlaps, compress the prose (caveman-compress the writing style, keep every technical fact).
   Requested by Lucas 2026-07-30, after the type system lands so the passes are not wasted on files
   about to be deleted.
   → **model: sonnet**.
3. 🟢 **safe — `KNOWN-BUGS.md` → `BUGS.md`.** DONE 2026-07-30. Six files renamed, gate hook renamed
   (`bugs-gate.py`) with its `.claude/settings.json` registration and the **functional
   spawn-by-filename reference** in `.opencode/plugins/workspace-policy.js`. Zero old strings remain.

> **A fourth type exists and must not be folded: the transient initiative doc.** `code/VERIFY.md`
> self-declares this lifecycle and names `REFACTOR.md` as its species; siblings are
> `code/SPEC-DRIVE.md`, `code/isoroll-module/REFACTOR.md`, `core/MIGRATION-STATUS.md`,
> `code/dobra/DECISIONS.md`. Folding `VERIFY.md` into a ROADMAP was **investigated 2026-07-30 and
> rejected as unsafe**: it has 24 inbound references, 7 of them in `.hooks/*` source comments citing
> stable anchor IDs (`VERIFY.md W1/W2/I2/G1/G3/G7/A1`). It is a cross-project rollout with cited
> anchors and a defined death date — genuinely not a per-project ROADMAP. Open question for Lucas:
> the type is legitimate, but does it need a **name convention** (all five are named differently) and
> a rule that it must be deleted when its rollout completes?

---

## Batch B — live bugs, ready to execute (Sonnet, `/loops`)

One test each. Nothing here needs a decision.

1. `.hooks/context_synchronizer.py`, three bugs: (a) hoisting a child CONTEXT.md's line-2 description
   copies relative links verbatim into the parent's routing row, where they resolve one level up —
   live in `branches/casinhas/CONTEXT.md` and `code/{apptime,dobra,isoroll-content}/CONTEXT.md`;
   (b) stale rows survive file deletion (block only updates on save) — live in
   `core/prompts/CONTEXT.md`; (c) it appends a **duplicate** routing block to a hand-curated
   CONTEXT.md that has a manual `## Routing` without sentinels.
2. `core/tools/video`: `--level full` crashes on image-only posts — `assemble()` always calls
   `media().transcribe(audio)` when the audio path is truthy, but an image post has no audio stream →
   `IndexError: tuple index out of range` inside `faster_whisper`/`av`. Workaround: `--level visual`.
3. `pre-edit.py` fails **silently** ("No stderr output") on `Write` of new files in some paths
   (scratchpad `.html`, a new `test/*.py` under `isoroll-content`) — blocks the write without saying
   why; workaround is a Bash heredoc. Probably an unhandled exception on an unexpected path.
4. **`stubgen` misses projects** — `.py`/`.ts` files created outside Edit/Write never get their stub
   staged. Blast radius measured 2026-07-29: **122 unstaged stubs across 7 repos**, and since the
   read-gate blocks reading source when the interface is current, a missing stub breaks a fresh
   clone. Needs a pre-commit sweep, not an edit-time hook.
5. `.hooks/brain_stats.py` `compress_done()` writes `new_inner` without a trailing newline, so the
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
- **`[mvp-validate]`** — 30 days of daily use, assessed. Post-v1 by definition.
- **Serious OCR** — real need (image-only PDFs in `branches/ecovila/burocracia/` where
  `core/tools/parse` returns empty; test Baidu "Unlimited OCR" first), but it belongs where the PDFs
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
- **`core/tools/papers --ss` live smoke** — it will smoke itself on the next real use.
- **Commit the `.claude/commands/{drive,calendar}.md` symlinks** — done inline rather than tracked.

## Sequencing

1. **Frente 12.1** — apply the type system + write it into `core/SCHEMA.md`. Do it before 4.1 so
   Tier 0 enforces a vocabulary that is already true, and before 12.2 so the refinement passes are
   not spent on files about to be deleted.
2. **Frente 4.1 + 4.3** — Tier 0 and the entropy dashboard. The keystone.
3. **Frente 4.2** — the `loops`→`flows` generator rename.
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
