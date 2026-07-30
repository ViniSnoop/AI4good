# Workspace-OS Roadmap — the v1 push
> **Single entrypoint for all workspace-os (wos) build work.** Goal file
> [brain/goals/workspace-os.md](brain/goals/workspace-os.md) holds *why* (signals, dynamics, timing);
> this file holds *what*. [brain/TODO.md](brain/TODO.md) holds life tasks only;
> [core/ROADMAP.md](core/ROADMAP.md) holds agent-library internals only. An item lives in exactly one
> of the four — a copy is a bug. Reference evidence: [core/refs/REFS.md](core/refs/REFS.md).

## v1 definition of done

wos v1 is not "all items closed". It is these four, and nothing else gates it:

| # | Criterion | Owner |
|---|-----------|-------|
| 1 | **verify-fast green + Tier 0 live** — naming, placement, pointer integrity, size-as-signal all deterministic; entropy dashboard exists and reads clean | Frente 4 |
| 2 | **One ledger, no duplicates** — this file is the sole wos work ledger, verified by scan not eyeball | Frente 8 |
| 3 | **Everything pushed, gitflow-shaped** — every `code/` repo on `main`/`feature/*`, zero unpushed, no repo without a remote | Frente 11 |
| 4 | **Clonable by a student** — fresh clone gets every capability; deps declared, no undocumented hand-installs | Frente 10 |

Everything below either serves a criterion or is explicitly **parked** (last section). Post-v1
validation is `[mvp-validate]`: use the system daily for 30 days, then assess whether it reduced
mental load — that is the *real* test, and it can only run after v1.

## How to read this

Each frente (front) is a self-contained line of work with numbered steps. Every step carries:

- **model** — the tier that is *enough*: `haiku` (mechanical), `sonnet` (normal engineering /
  writing), `opus` (design, security, cross-cutting judgment). A floor, not a ceiling.
- **switch** — how to get that model onto that step (guide at the bottom).

Impact flags mark steps that change shared behavior and need discussion before shipping:
🔴 **decide-first** (workspace-wide policy or security — needs Lucas's sign-off) ·
🟡 **pilot-first** (prove on one subtree, measure, then generalize) ·
🟢 **safe** (mechanical or additive, low blast radius).

> **Evidence caveat, stated once for the whole doc.** Several frentes lean on the two strongest but
> *unreviewed* preprints in our refs — progressive disclosure ([P] 2607.17598) and ACE
> ([P] 2510.04618). Preprint = provisional (see [core/refs/CONTEXT.md](core/refs/CONTEXT.md)). Where a
> step's justification is preprint-only, it says so and stays 🔴/🟡 until a published source or our
> own measurement confirms it. We do not turn a preprint into a hard gate.

**Principle, load-bearing across every frente: automatic + zero-token beats agent-checked, and
free checks are never coupled to paid ones.** Deterministic scripts run per-commit; token-costing
detectors run periodically and opt-in; human judgment runs on demand.

**Second principle: the entry point must not require memory.** The workspace must ease
communication and discovery — Lucas should never have to remember what exists. Discoverability via
skills, nudges, and routing is a feature, not polish (`[entry-point]`).

---

## Frente 1 — INBOX provenance (security) — ESSENTIALLY DONE

**Why.** INBOX ingests telegram, gmail, and the output of `core/tools/{video,fetch,search}`, then
`/inbox` routes those lines into goals and ROADMAPs — trusted context. This is the memory-poisoning
*write* channel, which standard prompt-injection defenses do not cover ([P] 2606.04329; fix shape
from [P] 2606.24322 origin-bound authority; design ref CaMeL, Google DeepMind).

> **Trust model (decided 2026-07-24, Lucas).** **INBOX is always inert as instruction — nothing in it
> is ever obeyed as a command.** Authorship does not decide obey-vs-ignore (always ignore); it decides
> **what may be promoted into trusted files** during triage. A `lucas`-authored line may be routed into
> goals/ROADMAPs; a line whose true origin is a link/fetch/other-sender is **quoted data** — filed,
> never obeyed, never promoted raw. `/inbox` is the act to protect; every other INBOX reader inherits
> the rule.

Shipped 2026-07-25: capture-time `[src: …]` tagging (`core/tools/gmail_triage.py`,
`code/aiwbot/frontend/inbox.py` `build_entry(forwarded=…)`, regression in `code/aiwbot/tests/test_inbox.py`)
and reader-side enforcement (`core/skills/inbox.md` § Provenance, `core/skills/roundup.md`).

1. 🟡 **pilot-first — measure.** Plant a benign "instruction" in a fetched page, run it through
   video→INBOX→`/inbox`, confirm it lands as data and is not acted on. Seed of the Tier-1 gold tasks.
   → **model: sonnet** to build the probe · **opus** to judge the result.

---

## Frente 3 — Routing depth vs. locality (the SLM question)

**Why.** Two axes, kept separate on purpose:

- **Locality** — small CONTEXT.md glued to the files it governs. Evidence ([P] 2607.17598,
  controlled, on haiku-4.5 + qwen3.6-27b): *"the weaker the agent's native navigation, the earlier the
  skill pack earns its keep"*; the flat pack hits ~2× accuracy at ½ the tokens vs. raw at corpus scale,
  and the always-loaded index is the most cache-friendly input. **For a workspace that must run on
  Sonnet and SLMs, scattered local CONTEXT.md is not overhead — it is what makes weak models work, and
  it is cheaper.** → keep it.
- **Depth** — hops to content. Same paper: a second routing level is *not* uniformly free; it hurt
  some tasks, helped open-QA. Cost is task- and scale-specific → measure, don't decree.

Policy written 2026-07-24 in [core/SCHEMA.md](core/SCHEMA.md) § *Routing depth and locality* and
induced into [AGENTS.md](AGENTS.md) (the always-read root) 2026-07-25. Not yet **enforced** —
enforcement is Frente 4 Tier 0.

1. 🟡 **pilot-first — measure our own depth.** Instrument what actually loads at session start
   (AGENTS.md chain + every CONTEXT.md on a typical path + memory) and the real hop count to a leaf.
   Decide per-path if any level is dead weight. Includes: consider trimming `MEMORY.md`, and inspect
   what is stored unannounced under `~/.claude/`.
   **Sub-question (Lucas, 2026-07-26):** do `context-gate.py` / `bash-context-gate.py` force a
   *subagent* to reread the full CONTEXT.md chain on every subtree touch rather than once per session?
   If so, a subagent spawned for a narrow task may pay the full-chain cost repeatedly. Intended, or an
   unwanted induction of this frente's own policy?
   → **model: sonnet** to instrument + tabulate · **opus** to read the tradeoff.
2. 🟡 **pilot-first — SLM confirmation run.** Before trusting the preprint on *our* content, run one
   real task on a small model (via `code/dobra` / opencode) against the flat vs. nested layout, our
   files, and compare. Ties to Frente 10 (`opencode-parity`).
   → **model: sonnet** to design + judge · execution is *by* the SLM under test.
3. 🔴 **decide-first — what is always-loaded about Lucas, and where does memory live?**
   `brain/USER.md` enters via the brain CONTEXT chain; `MEMORY.md` index enters every session.
   Lucas's suspicion: the auto-memory overlaps what `USER.md` + `goals/` + CONTEXT chain +
   `WATCHLIST` + `refs/` already do. Decide the role of each (always-loaded vs durable vs
   on-demand) and whether the separate memory store justifies itself or should fold.
   → **model: opus** · depends on step 1's measurement.

---

## Frente 4 — workspace anti-entropy — **the keystone, v1 criterion 1**

> Reframed by Lucas 2026-07-24 from "verify-agent gold tasks" to the real target: the recurring decay
> he has flagged repeatedly — **files grow, scatter, duplicate, and drift from naming/structure
> patterns.** verify-agent is now *one detector inside* a three-tier strategy.

**The frame: structure is a spec; drift is a test failure.** `code/` already has this (the `> spec:`
gate); the agent library has it ([core/SCHEMA.md](core/SCHEMA.md), frontmatter). Nothing governs the
**shape of the workspace itself** — naming, placement, size, pointers, redundancy. This frente
**subsumes** the old Frente 2 (pointer integrity — checker shipped 2026-07-25,
[core/tools/test/test_pointer_integrity.py](core/tools/test/test_pointer_integrity.py), runs in
`make verify-fast`), Frente 5 (size-as-signal), and four ex-`TODO.md` items (200-LOC-`.md`, `.md`
filename enforcement, "standardization as a recurring need → skill", capital-case dir names).

**Why.** The self-improvement survey ([P] 2607.13104) names evaluation as *the* open problem for
scaffolds; practitioner tools (claudemd-check, agenteval, instrlint) only lint text. Anti-entropy is
broader — detection + consolidation across the whole tree.

Cost-ordered by "automatic + zero-token beats agent-checked":

1. 🟢 **Tier 0 — per-commit, zero-token, deterministic.** No LLM. Scripts in the pre-commit/verify
   path:
   - **naming** — kebab-case, full words not truncations (the `architect`>`arch` rule made
     machine-checkable); lowercase top-level dirs (the `Models/`-recurrence class); the
     `UPPERCASE_IMPORTANT.md` type set is >10 types in Lucas's view — **reduce the type vocabulary
     first, then enforce it** (ex-`[md-type-uniformity]`).
   - **placement** — a file's location matches its declared type (extend `sync-skills`); includes
     `core/tools/*` Python files carrying no `.py` suffix — decide accept-or-standardize
     (ex-`[tools-py-suffix]`).
   - **project ⟺ goal link** — every project `CONTEXT.md` declares its goal on line 3,
     `> goal: [slug](../../brain/goals/<slug>.md)`. **Backfill the ~15 projects first, then enforce**
     via post-edit hook (warn → block). `dobra` has no goal yet: create one or declare `> goal: none`.
     A reverse `> project:` link in the goal file is optional.
   - **pointer integrity** — DONE. Open sub-decision: `[[slug]]` resolution policy — an unresolved
     `[[slug]]` is a *planned* memory (allowed) or a *typo* (error)? The memory spec allows dangling,
     and the corpus mixes kebab-case `name:` with underscore filenames, so there is no single rule
     yet. Needed before the checker can gate it (the checker's own header comment points here).
   - **size as a *signal*, never a cap** — warn-for-delta-review when a *curated* doc crosses a
     threshold; **never force-summarize** (ACE brevity-bias trap, [P] 2510.04618). Also flags the
     `--no-verify` debt class: bypasses leave no trace outside the commit message, so list tracked
     files above `BLOCK_LINES` with the commit that introduced them (ex-`[no-verify-ledger]`).
   - **self-healing `.gitignore` allowlist** — shipped 2026-07-25, corrected 2026-07-29 (see Frente 11.1).
   → **model: sonnet** · **switch: `/loops`.**
2. 🟡 **Tier 1 — periodic, cheap-agent, `/compass`-cadence.** Token-costing checks, **separated from
   Tier 0** (free checks must not be coupled to paid ones), run weekly / opt-in / on the `/loop`
   scheduler — nothing here is critical-often. On sonnet/haiku **through the aiwbot backend so it stays
   harness-portable** (the Agent-tool runner would Claude-Code-lock it). Detectors: **behavioral gold
   tasks** (routing correctness — cold subagent, substring-assert grading, start with **3** tasks not
   5, seed = the Frente 1.1 provenance probe); **semantic scatter/redundancy** (schedule the existing
   `/dedup`, never per-commit); **misplacement audit** (does each doc still match its folder's
   `CONTEXT.md` charter?).
   → **model: sonnet** runner + judge · graded subagents run at the tier under test.
3. 🟡 **Tier 2 — on-demand, human-triggered: a `/tidy` skill.** Reads the cached Tier-0/1 findings and
   does the *consolidation* — merge / move / rename / delete — as **curated delta, not monolithic
   rewrite** (ACE context-collapse). This is the ex-`[padronização como skill]` item given a precise
   job. Runs only when Lucas chooses.
   → **model: opus** · **switch: same session or `/loops` high tier.**
4. 🟢 **The unifying artifact — an entropy dashboard.** One generated report written by the automatic
   Tier-0/1 checks: naming violations, oversized curated docs, dead pointers, dup candidates,
   misplaced files. Agents and Lucas read the **dashboard** (pre-computed, cheap), never re-scan the
   tree. Detection automatic and cached; only the Tier-2 *decision* costs tokens.
   → **model: sonnet** · **switch: `/loops`.**
5. 🟡 **pilot-first — high-coupling / import-graph detection.** Pilot on `isoroll-module`, then decide
   a workspace-wide policy. Discuss before generalizing.
   → **model: sonnet** · ex-`TODO.md`.

6. 🟢 **finish the `loops` → `flows` rename at the generator.** APPROVED 2026-07-29 (Lucas: *"we
   renamed loops to be flows but apparently this keeps coming back"*). It keeps coming back because it
   **was never a drift problem** — the rename stopped at the flow pool (`core/flows/`, flow renamed
   `craft`) while three generators still emit the retired word *legitimately*, so no Tier-0 naming check
   could ever flag it: (a) the skill/command is still `core/skills/loops.md` = `/loops`; (b)
   `.loop/<slug>/` is the hardcoded per-run state dir in `craft.md`, `architect.md`, `runtimes.md`,
   `routing.md` — 14 live dirs across `aiwbot`, `isoroll-content`, `isoroll-module`; (c) the cross-run
   pattern library is `core/flows/.loop-skills/`. Retired `loop/*` git branches were the visible
   symptom and are already gone (Frente 11.2). Scope: `/loops` → `/craft`, `.loop/` → `.craft/`,
   `.loop-skills/` → `.craft-skills/`, sweep the 74 doc mentions. **Keep "Loop 0..6" as step names** —
   an iterative step really is a loop; that word is correct English, not the retired label.
   **The general lesson, which is the reusable part: an incomplete rename is indistinguishable from
   entropy at the leaves, and only fixable at the generator.** Tier 0 should assert the retired token
   appears nowhere *after* the rename lands, so a regression is caught instead of re-discovered.
   → **model: sonnet** · **switch: `/loops`** (last time under that name).

**Research lead (offered, not run — budget).** Two on-point links in `core/refs/REFS.md`
(`awesome-harness-engineering`, `best-of-Agent-Harnesses`) plus the core/ROADMAP "survey outside
skills" item. Mine them for prior-art anti-entropy tooling on a **Sonnet** subagent before building
Tier 0.

---

## Frente 5 — Anti-collapse: size policy (decided, folded)

**Why.** ACE ([P] 2510.04618) measures **brevity bias** (a summary drops the domain heuristic that
mattered) and **context collapse** (monolithic rewrite erodes a doc until performance falls off a
cliff). Decision 2026-07-24: split-by-navigation (many small linked files) = **yes**; hard line-cap
that forces a curated ROADMAP/CONTEXT to be summarized = **no**. Enforcement home is Frente 4 Tier 0
(size = delta-review signal).

1. 🟡 **pilot-first — anti-collapse gate (optional).** A hook flagging an edit that shrinks a curated
   `.md` above X% without an explicit `consolidate:` intent, making append-delta the default. Needs
   Frente 3.1 first, to know which files are "curated". Touches the edit path.
   → **model: sonnet** to build · **opus** to set threshold + exemptions.
2. 🟢 **safe — split the known oversized docs by navigation.** `SETUP.md` (41 KB) is the flagged
   example; `SPECS.md` / `KNOWN-BUGS.md` / `ROADMAP.md` become file-trees rather than single files
   where size warrants. Split by *access pattern* (always-loaded vs on-demand), the technique proven
   in the `craft.md` decomposition — not arbitrary fragmentation.
   → **model: sonnet** · pairs with Frente 10.1 (SETUP audit) — do them together, same file.

---

## Frente 6 — Hygiene

1. 🟢 **safe — clean the workspace floor.** `tmp/` is 297 MB and holds the ablation-bench pilot;
   `outputs/` (384 KB) and assorted misplaced/obsolete files. **Move `tmp/ablation-bench/REPORT.md`
   somewhere durable first** (see core/ROADMAP § ablation-bench) — `tmp/` will be cleaned. Also: 6
   orphan `*.original.md`, duplicate `Modelo de Projeto (1)(2)(3)` in `Downloads`.
   → **model: haiku** for the sweep · **sonnet** to judge what is obsolete.
2. 🟢 **safe — Downloads unification.** Some programs still bypass the workspace path and write to
   `~/Downloads` (partial fix 2026-07-21: `ementas/port.py` + `filler.py` hardcodes; other scripts not
   swept). Then set up a shared Downloads across smartphone + both computers, unified on
   `/mnt/workspace/Downloads/`.
   → **model: sonnet** (grep for hardcoded paths) · the cross-device part is config, not code.
3. 🟢 **safe — dated re-check: `GOALS.md` attention dashboard.** Re-check **after 2026-08-05**. Lucas
   reported 2026-07-23 that it "isn't monitoring correctly" — nearly every goal showed exactly 7
   touches. Verified *not* a live bug: the `f372446` fix (2026-07-22) stopped the hook from
   `git add`-ing all 54 goals per commit, and today's commits touch 0-1 goal files. The 14-day window
   washes the old history out by ~2026-08-05. If the numbers are still flat on 2026-08-06, **then** it
   is a real bug.
   → **model: haiku** (read the table, compare).

---

## Frente 7 — Scaffold update log (optional; paper thread)

**Why.** The survey ([P] 2607.13104) frames the workspace as a *scaffold* and Lucas as the *update
operator*. Git records *what* changed, not *what signal motivated it* or *whether it worked*. A
`core/SCAFFOLD-LOG.md` (one line per scaffold change: trigger → change → outcome) closes that. No
published longitudinal study of one real user evolving an agent scaffold exists — this is
paper-shaped, and Lucas runs a Hybrid Intelligence lab.

1. 🟡 **pilot-first — decide if it earns its keep.** A log only helps if it is actually written.
   Trial: one line per scaffold change for two weeks, then judge. Defer until v1 lands.
   → **model: sonnet** · **switch: same session.**

---

## Frente 8 — The ledger discipline — **v1 criterion 2**

**Why.** `[roadmap-entrypoint]`, `[todo-redesign]`, `[md-growth]` and `[task-metric]` were four names
for one disease: ledgers grow, nothing is deleted, so no ledger is trusted. Measured 2026-07-29:
~94 wos items across four files, with four *already-false* entries (two shipped frente steps still
unchecked, a doc count off by 119, a "remove `Models/`" task for a directory that no longer exists).

Collapsed 2026-07-29: this file is the single wos ledger; the goal file, `brain/TODO.md`, and
`core/ROADMAP.md` were scoped to why / life / library respectively. **Deletion policy: hard delete.
Git is the history** — no HISTORY append, no strikethrough, no annotated corpses.

1. 🟢 **safe — duplicate scan in Tier 0.** Assert each bracketed item slug appears in exactly one
   ledger. Cheap, deterministic, and it is what keeps criterion 2 true after today.
   → **model: sonnet** · folds into Frente 4 Tier 0.
2. 🟢 **safe — the `[task-metric]` instrument.** Count items closed vs. items created per week across
   the four ledgers (git log over the ledger files gives it for free). This is the direct diagnostic
   for `[md-growth]`, and the **post-v1 exit signal**: closed > created, sustained two weeks.
   Baseline: 789 lines across the four ledgers on 2026-07-29, pre-collapse.
   → **model: sonnet** · **switch: `/loops`.**
3. 🔴 **decide-first — TODO layer redesign.** Reported twice, unprompted: *"sinto que o TODO.md
   simplesmente não tá sendo usado"* (2026-07-27), and the evidence is that Lucas writes tasks into
   the INBOX instead. Two questions, one design: (a) **what would make it actually get checked
   daily** — accountability without the anxious tone the workspace exists to avoid (see
   [brain/FOUNDATIONS.md](brain/FOUNDATIONS.md)); (b) **TODO × goals boundary** — what belongs in
   which. Wanted: mutable, self-archiving, per-task recommended model/tier + creation date so stalled
   tasks flag themselves.
   → **model: opus** (design) · then sonnet to build.
4. 🟢 **safe — `/inbox` refreshes the goals dashboard.** Run `brain_stats.py` as `/inbox`'s last step,
   not only on commit, so the dashboard never goes stale between commits.
   → **model: haiku**.
5. 🟡 **pilot-first — `/inbox` offers `/compass` on a trigger only.** Fire when an anchor crossed
   <3 weeks or a goal flipped to stalled — never automatically on every call. Cheap capture stays
   cheap.
   → **model: sonnet**.
6. 🟢 **safe — retroactive ref→task pairing.** The policy (a captured link must spawn a paired
   assessment task, never land ref-only) was coded into `core/skills/inbox.md` 2026-07-25. Apply it
   **retroactively** to the refs already captured ref-only, and refine the wording.
   → **model: sonnet**.
7. 🔴 **decide-first — the ditch pass. DECIDED 2026-07-29, not yet run.** The collapse made the ledger
   honest but not smaller: items 158 → 123, mass flat (789 → 780 lines). Lucas, same day: *"this wos is
   already too big and I confess I am a bit lost"* — the second such report (the first was
   `brain/TODO.md`, 2026-07-27), so it is a live problem, not a mood. **Mass is the disease and only
   deletion cures it.** Procedure: Opus reads all ~45 frente steps and proposes a **kill list**, target
   **≤20 steps**; Lucas approves or vetoes each; killed items get one line of rejection note and are
   deleted (per `[[feedback_delete_weak_features]]`), not demoted. Accepted price: some killed ideas
   will resurface in months looking new. That is cheaper than a list nobody reads.
   **Orientation that should survive the pass:** of the open steps, only **five** need Lucas's own
   judgment — 3.3 (memory design), 8.3 (TODO redesign), 9.2 (`/roundup` redesign), 10.3 (clonable for
   students), 11.2 (dirty-tree calls). Everything else is Sonnet/Haiku mechanical or parked. Stating
   that number is itself part of the cure.
   → **model: opus** · **switch: same session**, right after the push sweep.
8. 🟢 **safe — populate `>**routing**` tier·effort on goal files** (spec in `brain/SPECS.md`, vocab
   shared with `core/skills/prepare.md`) and wire the router/`prepare` to read it.
   → **model: sonnet**.

---

## Frente 9 — Cost & model routing

**Why.** Measured (24 h, this machine): 59% of usage from subagent-heavy sessions, 55% from
>150k-context sessions, 25% from `/roundup`, 22% from `/loops` subagents. Context management is
currently *Lucas's* job, which it should not be.

1. 🟢 **safe — cheaper models where the work is mechanical.** Set model frontmatter on `/roundup` and
   `/loops` (craft-flow) subagents for mechanical steps; re-measure after.
   → **model: sonnet**.
2. 🔴 **decide-first — `/roundup` redesign + automatic session transition.** `/roundup` costs ~7% of
   usage. Together with it: induce session switching by context size (frequent checkpoints /
   effective transition points), and investigate whether an agent can open a new session by itself.
   Includes the session-size monitor (a hook warning at ~40%/50% to evaluate handoff — 80% is too
   late, likely to discard work) and **context-drift detection** (an objective recall probe: plant a
   verifiable fact early, re-check periodically, tied to the %-monitor). Note the weak version:
   the "canary call-me-Lucas" trick is a confounded proxy (caveman suppresses it, self-reported) —
   keep it as a free passive tell, build no infrastructure on it.
   → **model: opus** (design) · sonnet to build.
3. 🟡 **pilot-first — model-routing strategy.** (a) Prepare the ground for Sonnet: triage what it can
   do without philosophy/discussion, to save tokens. (b) In plan mode, offer to *raise* the model for
   planning and *lower* it for execution, per step. Ties to Frente 8.7 and the
   `prompt-opt-automation` goal; feeds step 4.
   → **model: opus** to design the routing rules.
4. 🟡 **pilot-first — benchmark `/loops` (craft) on result *and* cost**, and compare our skills/flows
   against SOTA industry repos — with the caveat that industry cares less about tokens (a US/EU dev
   spends ~$100/mo, Lucas ~$20). Pairs with core/ROADMAP § survey-outside-skills.
   → **model: sonnet** to run · **opus** to read.
5. 🟡 **pilot-first — triggers after a limit window renews.** Always-on use of the daily/weekly
   limits. `ScheduleWakeup` (dynamic `/loop`) covers this *inside a live session*; the missing case is
   "session died, limit renewed, nobody wakes the agent".
   → **model: sonnet**.

---

## Frente 10 — Portability & clonability — **v1 criterion 4**

1. 🟢 **safe — SETUP.md audit.** Still needed? Are all additions represented? Anything discarded but
   still documented? Two axes: **coverage** (features / skills / hooks / flows / brain all present)
   and **accuracy** (a newcomer gets plug-and-play on every capability). Do it together with Frente
   5.2 (the split) — same file, one pass.
   → **model: sonnet**.
2. 🟢 **safe — declare the ad-hoc venv deps.** Three known cases, each `pip install`ed straight into
   `.venv` to unblock a tool, so a fresh clone silently loses the capability: `pypandoc-binary`
   (`core/tools/parse` on `.docx`), `secretstorage` (`core/tools/video` reading Brave cookies —
   without it, yt-dlp fails with an AES-CBC decrypt error that reads like bad credentials; cost a
   session to diagnose), `gallery-dl` (`core/tools/video` carousel path). Fix the **class**: a declared
   dep list or a SETUP step the whole `core/tools/` surface is checked against.
   → **model: sonnet** · was core/ROADMAP, moved here as a v1 gate item.
3. 🔴 **decide-first — clonable for others (the students case).** Make the workspace genuinely
   adaptable/plug-and-play for anyone who clones the repo. Distinct from Frente 12's content import:
   this is the robustness of the *scaffold* for third parties — what is Lucas-specific, what is
   general, and how the two separate.
   → **model: opus**.
4. 🟡 **pilot-first — opencode + copilot parity.** Confirm everything working on Claude Code also
   works on opencode **and** copilot: test every hook on opencode, and pick one concrete pilot project
   to be executed by opencode end-to-end. Includes provider switching via workspace config
   (openrouter → NVIDIA key when credits run out) so instability in one provider is survivable.
   → **model: sonnet** · ties Frente 3.2.

---

## Frente 11 — Git & sync integrity — **v1 criterion 3**

**Why.** Two machines share this workspace; unpushed work is invisible work, and `main` is the sync
point, not a release tag. Measured 2026-07-29 — the nested `code/` repos are **out of policy**:

**Swept 2026-07-29 — criterion 3 MET.** 16/16 repos: zero unpushed, every branch `main` or
`feature/*`, every repo has a remote. 41 commits pushed across 8 repos; `cria` published
(`lsfcin/cria`, public, Lucas's call — 5 `.md` files, secret-scanned first); `loop/arm-a-homography`
→ `feature/arm-a-homography` and `loop/painter-mvp-1` → `feature/painter-mvp-1`; 5 stale `loop/*`
refs deleted (all ancestors of the live feature branches, zero unique commits). Dirty 215 → 93.

The "294 dirty files" was wrong twice over. Real count was 215 (11.1's `.gitignore` fix had already
cleared ~79), and **122 of those were unstaged generated interface stubs, not Lucas's work** —
`.pyi`/`.d.ts`/`.dart.api` that the edit-time hook stages on Edit/Write but which files created by
other means never got. That is Batch B item 5 with a measured blast radius, and the near-miss is
worth recording: the first read of the evidence was that stubs are debris to gitignore. They are the
opposite — SETUP.md:41 stages them and SETUP.md:536 *hard-blocks reading a source file when its
interface is current*, so ignoring them breaks the read-gate on every fresh clone (criterion 4).
Backfilled on `feature/stub-backfill` in 7 repos, stubs only, WIP untouched.

1. [x] 🟢 **safe — `.gitignore` / self-heal correction.** DONE 2026-07-29. The self-heal hook
   (Frente 6, 2026-07-25) added a `!code/<n>/` + `code/<n>/*` + `!code/<n>/CONTEXT.md` triplet for
   each own-repo project, intending to track its routing stub. **That pattern cannot work**: git
   cannot track files inside a nested repo without submodules, which the 2026-07-22
   `[nested-gitlink-gate]` decision deliberately killed. Net effect was 13 permanent `?? code/*`
   entries in every `git status`. Fix: plain re-ignore lines (matching the pre-existing
   `code/{cria,gira,laplata}` precedent), and `.hooks/gitignore-self-heal.sh` now **skips**
   `.git`-bearing dirs instead of emitting the triplet. Discoverability was never affected —
   [code/CONTEXT.md](code/CONTEXT.md)'s routing table hoists each project's description already.
2. [x] 🔴 **decide-first — the push sweep.** DONE 2026-07-29 (see above).
3. 🔴 **decide-first — what the sweep exposed that Lucas must rule on.** Four findings, none of them
   guesses:
   - **`Makefile` is untracked in 7 repos** (`apptime`, `shortvid`, `ppc`, `corpora`, `futebots`,
     `isometric-perspective`, `flows`). The **verify entrypoint itself is not in the repo**, so a fresh
     clone has no `make verify-fast` at all — a direct criterion-4 hole. Lucas declined committing them
     in the sweep; the decision is still open.
   - **`shortvid/shortvid/`** holds a *duplicated source tree* — `_crop_overlay.py`, `_effects.py`,
     `_eraser.py`, `CONTEXT.md`, a whole second copy of the package one level deep, alongside the same
     filenames untracked at `shortvid/ui/`. Not stub debris; either a wrongly-rooted tool write or the
     live version of an in-progress UI split. Untouched by the sweep on purpose.
   - **`prog1` and `programacao1` have no repo of their own** — they are tracked *inside* the workspace
     structural repo, inverting the AGENTS.md rule that internal projects use own repos. No work is at
     risk (they push with the workspace); the shape is wrong. Give them repos or declare them teaching
     material that belongs in the workspace tree.
   - **Two repos verify RED on already-committed code**: `flows` (3 failures in
     `engine/tests/unit/test_ui_m10_client.py::TestHandleClient`) and `voti` (8
     `react/no-unescaped-entities` errors — its `CONTEXT.md` §Working Rules already documents a
     deliberate warn-level backlog, but these are `error`). Pushed anyway on Lucas's call: the red
     predates the unpushed commits, and invisible work is the worse risk.
   - Also: `apptime`'s verify **cannot run** — `flutter: not found`. An undeclared toolchain dep,
     i.e. Frente 10.2's class with a fourth member.
   → **Lucas decides** each · sonnet to execute.
4. 🟢 **safe — nested-repo git graph in VSCode.** The git graph does not show subrepository history;
   find the extension or config that fixes it.
   → **model: haiku** (search + config).

---

## Frente 12 — Content & integrations (mostly parked, listed for completeness)

1. 🔴 **decide-first — Google Drive strategy** (`[gdrive-integration]`): link, sync, or selective
   copy. The per-folder migration checklist lives in `brain/TODO.md` § drive migration — that is
   *content work*, tracked as life tasks, not scaffold work.
2. 🟢 **safe — Google Slides API** enable on GCP project 1048141740528 (same project as
   drive/calendar), then the base slide templates (aula, talk acadêmico, projeto).
3. 🟢 **safe — commit the `.claude/commands/{drive,calendar}.md` symlinks** — still pending.
4. 🟢 **safe — serious OCR.** Sweep our already-annotated `refs/`/`WATCHLIST` (e.g.
   `opendataloader-pdf` = parse, not OCR) plus a web+github search for the best PDF/scan OCR — **bad
   OCR is actively harmful**. Precondition for reading the image-only PDFs in
   `branches/ecovila/burocracia/`, where `core/tools/parse` returns empty. **Test first: Baidu
   "Unlimited OCR"** — 100 pages in one pass, preserves layout/tables, runs local, MIT (ref in
   `core/refs/REFS.md`, INBOX 2026-07-28).
   → **model: sonnet**.
5. 🟢 **safe — mobile INBOX access (Android).** Recover the 2 app options from the prior conversation,
   pick one for the Xiaomi Redmi Note 10 Pro.
6. 🟡 **pilot-first — brain coverage.** Every `GOALS.md` stub has a real goal file
   (`[brain-full-files]`); `branches/` covers all active life domains (`[branches-coverage]`).
7. 🟡 **pilot-first — English-learning mode.** Re-enable: log Lucas's English errors during use into
   one doc with example + explanation + correction.
8. 🟢 **safe — aiwbot is the away-from-PC front door.** Plan and status live in
   [code/aiwbot/ROADMAP.md](code/aiwbot/ROADMAP.md) (own repo — do not duplicate it here). Open on the
   wos side: Lucas live-tests `/new`, reply-to-continue on both backends, and plain-text capture via
   @lsfaiwbot. The old `telegram_daemon.py` and its 12-step conversational-UX plan are **deleted**,
   superseded by this rebuild (per `[[feedback_delete_weak_features]]`).
9. 🟢 **safe — extract the "10 GitHub repos that replace paid tools" list.** The names are in the
   carousel images, not the caption: run `core/tools/video_images.py` on the post, then compare the
   list against what the wos already has. Ref in `core/refs/REFS.md`.
   → **model: haiku** to extract · **sonnet** to compare.
10. 🟡 **pilot-first — evaluate Surfsense** (self-hosted research assistant, NotebookLM-shaped). The
   question is not whether it is good standalone but whether it beats the pieces we already have:
   `core/tools/{search,papers,fetch,parse}` plus the research flow (ref in `core/refs/REFS.md`,
   INBOX 2026-07-29). Judge against our stack, not in isolation.
   → **model: sonnet**.
11. 🟢 **safe — research-flow hallucination audit.** Check `research`/`scout`/`sota` for points where
   the model can invent without a source; require provenance/verification where it is missing.
   → **model: opus** to judge, sonnet to patch.

---

## Batch B — small fixes, ready to execute (Sonnet, `/loops`)

One test each. Nothing here needs a decision.

1. `.hooks/context_synchronizer.py`, two bugs: (a) hoisting a child CONTEXT.md's line-2 description
   copies relative links verbatim into the parent's routing row, where they resolve one level up —
   live in `branches/casinhas/CONTEXT.md` and `code/{apptime,dobra,isoroll-content}/CONTEXT.md`;
   (b) stale rows survive file deletion (block only updates on save) — live in `core/prompts/CONTEXT.md`
   and `academy/papers/2027-CHI-cria/outputs/CONTEXT.md`. Third, related: it appends a **duplicate**
   routing block to a hand-curated CONTEXT.md that has a manual `## Routing` without sentinels.
2. `core/tools/video`: `--level full` crashes on image-only posts — `assemble()` always calls
   `media().transcribe(audio)` when the audio path is truthy, but an image post has no audio stream →
   `IndexError: tuple index out of range` inside `faster_whisper`/`av`. Workaround is `--level visual`.
   *Related but already closed:* the "OCR/video extraction doesn't always run during triage" report
   (Lucas, 2026-07-29) was a **skill** gap, not a code one — `core/skills/inbox.md` now states the
   extraction step is neither optional nor a judgement call (commit `17664e6`). This item is only the
   crash.
3. `pre-edit.py` vs `check-line-counts.sh` disagree on scope: the edit-time gate enforces the 200-line
   block on `.hooks/*`, the commit-time gate **exempts** it. Pick one policy. (This is the real content
   of the ex-`[stats-split-or-exempt]` item — the split itself already happened.)
4. `pre-edit.py` fails **silently** ("No stderr output") on `Write` of new files in some paths
   (scratchpad `.html`, a new `test/*.py` under `isoroll-content`) — blocks the write without saying
   why; workaround is a Bash heredoc. Probably an unhandled exception on an unexpected path.
5. `stubgen` misses projects: `.py` files created outside Edit/Write never get a `.pyi`. Consider a
   pre-commit sweep.
6. `.hooks/brain_stats.py` `compress_done()` writes `new_inner` without a trailing newline, so the
   surviving last entry ends up glued to the `<!-- done:end -->` marker (seen live in
   `brain/goals/workspace-os.md`, 2026-07-29). Cosmetic, one-line fix, no test needed beyond a
   round-trip assertion. Same function also leaves `brain/.log/done.md` unstaged after appending —
   the archive lands but the commit that caused it does not carry it.
7. Live-smoke `core/tools/papers --ss --reviewed --min-cit`. Validated offline only 2026-07-23
   (Semantic Scholar returned HTTP 429 all day); the parser is correct on 4 synthetic cases, but it
   has never run against the live API.

## Batch C — core library symmetry

All decided, all build work — tracked in [core/ROADMAP.md](core/ROADMAP.md), not here. Listed as a
pointer only: craft-agent tier source + generator, skill `flow:` field, `engineering` in the flow
type enum, `loops`-vs-`craft` naming, Google-auth CLI convergence.

## Parked — explicitly out of v1

- **`[gdrive-integration]` / `[courses-import]`** — content migration, large; Frente 12.1 holds the
  strategy decision, the per-folder work lives in `brain/TODO.md`.
- **`[offline-resilience]`** — a workspace surviving a world without internet: the filesystem is
  already the source of truth, so the gaps are (a) network — [Reticulum](https://github.com/markqvist/Reticulum),
  E2E without infrastructure, and (b) an offline corpus — **Kiwix** (all of Wikipedia offline; this is
  almost certainly the "NOMAD project" Lucas half-remembered). Ties to `[courses-import]`: local class
  material is half of it. Refs in `core/WATCHLIST.md`.
- **Frente 7** (scaffold log) — the paper thread; revisit after v1.
- **`[mvp-validate]`** — 30 days of daily use, assessed. By definition post-v1.

---

## Sequencing

1. **Frente 11.2** — the push sweep. Highest risk of *losing* work, and it is a v1 criterion.
   **Confirmed by Lucas 2026-07-29 as the next session's opening item.**
2. **Frente 8.7** — the ditch pass, immediately after the sweep, same session if budget allows.
   Decided 2026-07-29; every later item is cheaper against a shorter list.
3. **Frente 4 Tier 0** + the entropy dashboard (4.1, 4.4) — the keystone; subsumes old Frentes 2 and 5
   and four ex-TODO items. Build after the ledger collapse so the dashboard does not inherit lies.
4. **Batch B** — small fixes, parallel-safe, cheap.
4. **Frente 10** (1, 2) — SETUP audit + declared deps, with Frente 5.2's split in the same pass.
5. **Frente 8** (1, 2) — duplicate scan + `[task-metric]`, so criterion 2 stays true without vigilance.
6. **Frente 4 Tier 1/2** — gold tasks, `/dedup`, `/tidy`.
7. **Frente 3.1** — the depth audit; then 3.3 (memory design) which depends on it.
8. **Frente 9** — cost and routing, once there is a stable baseline to measure against.

Opus is needed for exactly five things: Frente 3.3, 8.3, 9.2, 10.3, 11.2's dirty-tree calls. Everything
else is Sonnet or Haiku.

## Model-switching guide

The per-step `model` + `switch` tags use the workspace's canonical model-switching guide, which lives
in the reusable flow that produced this plan:
**[`core/flows/research/scout.md`](core/flows/research/scout.md) → "Canonical model-switching guide"**
(same-session `/model` · `/loops` autorouting · Agent-tool `model:` override · `/handoff`). It is
methodology, not specific to this plan, so it is not re-tabulated here.

**Mapping:** 🔴 decide-first → **Opus, same session**. 🟢/🟡 build steps → **Sonnet via `/loops`**
(mechanical parts drop to haiku automatically). Run **haiku deliberately** only inside the Tier-1 gold
tasks, where the weak model is the subject under test.
